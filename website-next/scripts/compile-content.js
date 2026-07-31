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

function deriveRelated(concept, allConcepts) {
  const directNeighbours = new Set([
    ...(concept.requires || []),
    ...(concept.used_by || []),
  ]);

  const scored = new Map();

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

  (concept.tags || []).forEach(tag => {
    allConcepts.forEach(other => {
      if (other.id === concept.id) return;
      if ((other.tags || []).includes(tag)) {
        scored.set(other.id, (scored.get(other.id) || 0) + 0.5);
      }
    });
  });

  return Array.from(scored.entries())
    .filter(([id]) => !directNeighbours.has(id))
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 5)
    .map(([id]) => id);
}

function loadDir(cat) {
  const catDir = path.join(contentDir, cat);
  if (!fs.existsSync(catDir)) return [];
  return fs.readdirSync(catDir).filter(f => f.endsWith('.mdx')).map(file => {
    const filePath = path.join(catDir, file);
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const { metadata, body } = parseFrontmatter(fileContent);
    const slug = metadata.slug || (cat === 'books' ? file.replace(/\.mdx$/, '') : metadata.id);
    return { ...metadata, slug, body, _file: file };
  });
}

function compile() {
  const db = {
    concepts: [],
    recipes: [],
    books: [],
    problems: [],
    articles: []
  };

  const categories = ['concepts', 'recipes', 'books', 'problems', 'articles'];
  categories.forEach(cat => {
    db[cat] = loadDir(cat);
  });

  const conceptIndex = new Map(db.concepts.map(c => [c.id, c]));
  const problemIndex = new Map(db.problems.map(p => [p.id, p]));

  // Auto-derive related concepts
  db.concepts.forEach(concept => {
    if (!concept.related || concept.related.length === 0) {
      concept.related = deriveRelated(concept, db.concepts);
    }
    if (!concept.group) concept.group = "general";
    if (!concept.next_steps) concept.next_steps = [];
  });

  // Attach recipe summaries + book associations to each concept
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

    // Attach problems
    concept.problems = db.problems
      .filter(p => (p.concept || '').toLowerCase() === concept.id)
      .map(p => ({
        id: p.id,
        title: p.title,
        slug: p.slug,
        error_patterns: p.error_patterns || [],
        severity: p.severity || "common",
      }));

      // Attach articles (from articles/json/manifest.json if exists)
    const manifestPath = path.join(__dirname, '../../articles/json/manifest.json');
    if (fs.existsSync(manifestPath)) {
      const raw = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
      // Support both legacy (array) and generated ({_meta, articles}) formats
      const entries = Array.isArray(raw) ? raw : (raw.articles || []);
      concept.articles = entries
        .filter(function(a) { return (a.concepts || []).includes(concept.id); })
        .map(function(a) { return {
          slug: a.slug || '',
          title: a.title || '',
          description: a.description || '',
          tags: a.tags || [],
        }; });
    } else {
      concept.articles = [];
    }
  });

  // Attach concept summaries to each recipe
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

    const book = db.books.find(b => b.id === recipe.book);
    recipe.bookObject = book
      ? { id: book.id, title: book.title, slug: book.slug, version: book.version }
      : null;

    if (!recipe.prerequisites) recipe.prerequisites = [];
  });

  // Attach concept object to each problem
  db.problems.forEach(problem => {
    const concept = conceptIndex.get((problem.concept || '').toLowerCase());
    problem.conceptObject = concept
      ? { id: concept.id, title: concept.title, slug: concept.slug, summary: concept.summary, difficulty: concept.difficulty }
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
  ${db.problems.length} problems
  ${db.articles.length} articles
  -> src/db/knowledge-base.json`);
}

compile();
