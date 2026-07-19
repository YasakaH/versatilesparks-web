/**
 * validate-content.js
 *
 * Content-layer validation for the Browser Engineering Knowledge System.
 * Runs before compile-content.js during `npm run build` (via the `prebuild` hook)
 * and fails the build on structural content errors so bad content never ships.
 *
 * Validation rules:
 *  1. Required fields present (id, title, body) on every entity.
 *  2. No duplicate IDs within or across entity types.
 *  3. Every concept `requires` / `used_by` / `related` reference resolves to an existing concept.
 *  4. Every recipe `concepts` reference resolves; every recipe `book` resolves to an existing book.
 *  5. No recipe without at least one concept association.
 *  6. `requires` / `used_by` symmetry (warning, not fatal) — if A requires B, B's used_by should include A.
 *  7. Orphan concepts (no graph edges and no recipes) — warning.
 *
 * Exit codes: 0 = valid, 1 = fatal errors found.
 */

const fs = require("fs");
const path = require("path");

const contentDir = path.join(__dirname, "../content");

/* ------------------------------------------------------------------ *
 * Minimal frontmatter parser (mirrors compile-content.js so validation
 * does not depend on the compiler being correct).
 * ------------------------------------------------------------------ */
function parseFrontmatter(fileContent) {
    const parts = fileContent.split("---");
    if (parts.length < 3) return { metadata: {}, body: fileContent };

    const yamlSection = parts[1];
    const body = parts.slice(2).join("---").trim();

    const metadata = {};
    yamlSection.split("\n").forEach((line) => {
        const colonIndex = line.indexOf(":");
        if (colonIndex === -1) return;

        const key = line.substring(0, colonIndex).trim();
        let valStr = line.substring(colonIndex + 1).trim();

        if (valStr.startsWith("[") && valStr.endsWith("]")) {
            metadata[key] = valStr
                .substring(1, valStr.length - 1)
                .split(",")
                .map((x) => x.trim().replace(/^["']|["']$/g, ""))
                .filter((x) => x);
        } else {
            valStr = valStr.replace(/^["']|["']$/g, "");
            if (valStr === "true") metadata[key] = true;
            else if (valStr === "false") metadata[key] = false;
            else if (!isNaN(valStr) && valStr !== "") metadata[key] = Number(valStr);
            else metadata[key] = valStr;
        }
    });

    return { metadata, body };
}

function loadCategory(cat) {
    const dir = path.join(contentDir, cat);
    if (!fs.existsSync(dir)) return [];
    return fs
        .readdirSync(dir)
        .filter((f) => f.endsWith(".mdx"))
        .map((file) => {
            const raw = fs.readFileSync(path.join(dir, file), "utf-8");
            const { metadata, body } = parseFrontmatter(raw);
            return { ...metadata, body, _file: file };
        });
}

function main() {
    const errors = [];
    const warnings = [];

    const concepts = loadCategory("concepts");
    const recipes = loadCategory("recipes");
    const books = loadCategory("books");

    const conceptIds = new Set(concepts.map((c) => c.id));
    const bookIds = new Set(books.map((b) => b.id));

    /* 1 & 2. Required fields + duplicate IDs */
    const seenIds = new Set();
    const assertId = (entity, type) => {
        if (!entity.id) {
            errors.push(`[${type}] ${entity._file}: missing required field "id"`);
            return;
        }
        if (!entity.title) errors.push(`[${type}] ${entity._file}: missing required field "title"`);
        if (!entity.body || entity.body.trim() === "")
            errors.push(`[${type}] ${entity._file}: empty body`);
        if (seenIds.has(entity.id)) {
            errors.push(`[${type}] ${entity._file}: duplicate id "${entity.id}"`);
        }
        seenIds.add(entity.id);
    };

    concepts.forEach((c) => assertId(c, "concept"));
    recipes.forEach((r) => assertId(r, "recipe"));
    books.forEach((b) => assertId(b, "book"));

    /* 3. Concept relationship integrity */
    concepts.forEach((c) => {
        (c.requires || []).forEach((rid) => {
            if (!conceptIds.has(rid))
                errors.push(`[concept] ${c.id}: "requires" references missing concept "${rid}"`);
        });
        (c.used_by || []).forEach((uid) => {
            if (!conceptIds.has(uid))
                errors.push(`[concept] ${c.id}: "used_by" references missing concept "${uid}"`);
        });
        (c.related || []).forEach((rid) => {
            if (!conceptIds.has(rid))
                errors.push(`[concept] ${c.id}: "related" references missing concept "${rid}"`);
        });
    });

    /* 4 & 5. Recipe integrity */
    recipes.forEach((r) => {
        if (!r.concepts || r.concepts.length === 0) {
            errors.push(`[recipe] ${r.id}: has no concept association`);
        } else {
            r.concepts.forEach((cid) => {
                if (!conceptIds.has(cid))
                    errors.push(`[recipe] ${r.id}: references missing concept "${cid}"`);
            });
        }
        if (!r.book || !bookIds.has(r.book))
            errors.push(`[recipe] ${r.id}: references missing book "${r.book}"`);
    });

    /* 6. requires / used_by symmetry (warning only) */
    concepts.forEach((a) => {
        (a.requires || []).forEach((bid) => {
            const b = concepts.find((c) => c.id === bid);
            if (b && !(b.used_by || []).includes(a.id)) {
                warnings.push(
                    `[symmetry] concept "${a.id}" requires "${bid}" but "${bid}".used_by does not list "${a.id}"`
                );
            }
        });
    });

    /* 7. Orphan concepts (warning) */
    const recipeConceptRefs = new Set();
    recipes.forEach((r) => (r.concepts || []).forEach((cid) => recipeConceptRefs.add(cid)));

    concepts.forEach((c) => {
        const hasEdges =
            (c.requires && c.requires.length > 0) || (c.used_by && c.used_by.length > 0);
        const hasRecipes = recipeConceptRefs.has(c.id);
        if (!hasEdges && !hasRecipes) {
            warnings.push(`[orphan] concept "${c.id}" has no graph edges and no recipes`);
        }
    });

    /* Report */
    if (warnings.length > 0) {
        console.warn("\n  ⚠  Content warnings:");
        warnings.forEach((w) => console.warn("     " + w));
    }

    if (errors.length > 0) {
        console.error("\n  ✖  Content validation failed:");
        errors.forEach((e) => console.error("     " + e));
        console.error(
            `\n  ${errors.length} error(s), ${warnings.length} warning(s). Build aborted.\n`
        );
        process.exit(1);
    }

    console.log(
        `  ✓  Content valid: ${concepts.length} concepts, ${recipes.length} recipes, ${books.length} books${warnings.length ? ` (${warnings.length} warning(s))` : ""
        }`
    );
}

module.exports = { main, parseFrontmatter, loadCategory };

if (require.main === module) {
    main();
}