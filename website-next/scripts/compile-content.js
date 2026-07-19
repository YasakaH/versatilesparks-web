const fs = require('fs');
const path = require('path');

const contentDir = path.join(__dirname, '../content');
const outputDir = path.join(__dirname, '../src/db');

function parseFrontmatter(fileContent) {
  const parts = fileContent.split('---');
  if (parts.length < 3) return { metadata: {}, body: fileContent };

  const yamlSection = parts[1];
  const body = parts.slice(2).join('---').trim();

  const metadata = {};
  yamlSection.split('\n').forEach(line => {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) return;

    const key = line.substring(0, colonIndex).trim();
    let valStr = line.substring(colonIndex + 1).trim();

    // Parse values (arrays, strings, numbers, booleans)
    if (valStr.startsWith('[') && valStr.endsWith(']')) {
      metadata[key] = valStr.substring(1, valStr.length - 1)
        .split(',')
        .map(x => x.trim().replace(/^["']|["']$/g, ''))
        .filter(x => x);
    } else {
      valStr = valStr.replace(/^["']|["']$/g, '');
      if (valStr === 'true') metadata[key] = true;
      else if (valStr === 'false') metadata[key] = false;
      else if (!isNaN(valStr) && valStr !== '') metadata[key] = Number(valStr);
      else metadata[key] = valStr;
    }
  });

  return { metadata, body };
}

/**
 * Auto-derive related concepts for a given concept when `related` is not
 * explicitly curated in frontmatter. Strategy:
 *   1. Sibling concepts (share a requires or used_by) — strongest signal.
 *   2. Concepts sharing a tag — weaker signal.
 *
 * Direct graph neighbours (requires + used_by) are excluded because they are
 * already shown in the dependency panel of the concept page.
 *
 * Returns a de-duplicated, ordered list of concept IDs (excluding self and
 * direct graph neighbours).
 */
function deriveRelated(concept, allConcepts) {
  const directNeighbours = new Set([
    ...(concept.requires || []),
    ...(concept.used_by || []),
  ]);

  const scored = new Map(); // id -> score

  // Sibling signal: concepts that share a requires or used_by entry
  (concept.requires || []).forEach(reqId => {
    allConcepts.forEach(other => {
      if (other.id === concept.id) return;
      if ((other.requires || []).includes(reqId)) {
        scored.set(other.id, (scored.get(other.id) || 0) + 1);
      }
    });
  });
  (concept.used_by || []).forEach(useId => {
    allConcepts.forEach(other => {
      if (other.id === concept.id) return;
      if ((other.used_by || []).includes(useId)) {
        scored.set(other.id, (scored.get(other.id) || 0) + 1);
      }
    });
  });

  // Tag overlap signal
  (concept.tags || []).forEach(tag => {
    allConcepts.forEach(other => {
      if (other.id === concept.id) return;
      if ((other.tags || []).includes(tag)) {
        scored.set(other.id, (scored.get(other.id) || 0) + 0.5);
      }
    });
  });

  // Filter out direct graph neighbours (they're already shown elsewhere),
  // sort by score desc then by id for stable ordering, take top 5.
  return Array.from(scored.entries())
    .filter(([id]) => !directNeighbours.has(id))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 5)
    .map(([id]) => id);
}

function compile() {
  const db = {
    concepts: [],
    recipes: [],
    books: []
  };

  const categories = ['concepts', 'recipes', 'books'];

  categories.forEach(cat => {
    const catDir = path.join(contentDir, cat);
    if (!fs.existsSync(catDir)) return;

    const files = fs.readdirSync(catDir).filter(f => f.endsWith('.mdx'));
    files.forEach(file => {
      const filePath = path.join(catDir, file);
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const { metadata, body } = parseFrontmatter(fileContent);

      // Derive a slug for routing if not explicitly provided.
      // Uses `id` for concepts and recipes, and the filename (without
      // extension) for books since book ids may contain version dots.
      const slug =
        metadata.slug ||
        (cat === 'books'
          ? file.replace(/\.mdx$/, '')
          : metadata.id);

      db[cat].push({
        ...metadata,
        slug,
        body
      });
    });
  });

  // ---- Enrichment pass: related concepts + per-concept recipe/book lists ----
  const conceptIndex = new Map(db.concepts.map(c => [c.id, c]));

  db.concepts.forEach(concept => {
    // Related: explicit frontmatter wins, otherwise auto-derive.
    if (!concept.related || concept.related.length === 0) {
      concept.related = deriveRelated(concept, db.concepts);
    }
  });

  // Attach recipe summaries + book associations to each concept.
  db.concepts.forEach(concept => {
    const linkedRecipes = db.recipes.filter(r =>
      (r.concepts || []).includes(concept.id)
    );
    concept.recipes = linkedRecipes.map(r => ({
      id: r.id,
      title: r.title,
      slug: r.slug,
      book: r.book,
      difficulty: r.difficulty,
      environment: r.environment,
    }));

    const linkedBookIds = new Set(linkedRecipes.map(r => r.book));
    concept.books = db.books
      .filter(b => linkedBookIds.has(b.id))
      .map(b => ({
        id: b.id,
        title: b.title,
        slug: b.slug,
        version: b.version,
      }));
  });

  // Attach concept summaries to each recipe for richer recipe pages.
  db.recipes.forEach(recipe => {
    recipe.conceptObjects = (recipe.concepts || [])
      .map(cid => conceptIndex.get(cid))
      .filter(Boolean)
      .map(c => ({
        id: c.id,
        title: c.title,
        slug: c.slug,
        summary: c.summary,
        difficulty: c.difficulty,
      }));
  });

  // Attach book object (not just id) to each recipe.
  db.recipes.forEach(recipe => {
    const book = db.books.find(b => b.id === recipe.book);
    recipe.bookObject = book
      ? { id: book.id, title: book.title, slug: book.slug, version: book.version }
      : null;
  });

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(
    path.join(outputDir, 'knowledge-base.json'),
    JSON.stringify(db, null, 2),
    'utf-8'
  );

  console.log(`Compiled knowledge database:
  ${db.concepts.length} concepts
  ${db.recipes.length} recipes
  ${db.books.length} books
  -> src/db/knowledge-base.json`);
}

compile();