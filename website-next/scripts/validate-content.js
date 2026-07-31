const fs = require("fs");
const path = require("path");

const contentDir = path.join(__dirname, "../content");

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
    const problems = loadCategory("problems");

    const conceptIds = new Set(concepts.map((c) => c.id));
    const bookIds = new Set(books.map((b) => b.id));
    const recipeIds = new Set(recipes.map((r) => r.id));
    const problemIds = new Set(problems.map((p) => p.id));

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
    problems.forEach((p) => assertId(p, "problem"));

    /* Check for ID collisions across types */
    const allIds = new Map();
    [...concepts, ...recipes, ...books, ...problems].forEach((e) => {
        if (allIds.has(e.id)) {
            errors.push(`[cross-type] id "${e.id}" collides between ${allIds.get(e.id)} and ${e._file}`);
        }
        allIds.set(e.id, e._file);
    });

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
        (c.next_steps || []).forEach((ns) => {
            if (!conceptIds.has(ns))
                errors.push(`[concept] ${c.id}: "next_steps" references missing concept "${ns}"`);
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

        (r.prerequisites || []).forEach((prereq) => {
            if (!recipeIds.has(prereq) && !conceptIds.has(prereq))
                errors.push(`[recipe] ${r.id}: "prerequisites" references missing entity "${prereq}"`);
        });
    });

    /* 6. Problem integrity */
    problems.forEach((p) => {
        if (!p.concept || !conceptIds.has((p.concept || '').toLowerCase())) {
            errors.push(`[problem] ${p.id}: "concept" references missing concept "${p.concept}"`);
        }
        if (!p.error_patterns || p.error_patterns.length === 0) {
            errors.push(`[problem] ${p.id}: has no "error_patterns"`);
        }
        if (!p.description) {
            errors.push(`[problem] ${p.id}: missing required field "description"`);
        }
    });

    /* 7. requires / used_by symmetry (warning only) */
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

    /* 8. Orphan concepts (warning) */
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
        console.warn("\n  \u26a0  Content warnings:");
        warnings.forEach((w) => console.warn("     " + w));
    }

    if (errors.length > 0) {
        console.error("\n  \u2716  Content validation failed:");
        errors.forEach((e) => console.error("     " + e));
        console.error(
            `\n  ${errors.length} error(s), ${warnings.length} warning(s). Build aborted.\n`
        );
        process.exit(1);
    }

    console.log(
        `  \u2713  Content valid: ${concepts.length} concepts, ${recipes.length} recipes, ${books.length} books, ${problems.length} problems${warnings.length ? ` (${warnings.length} warning(s))` : ""
        }`
    );
}

module.exports = { main, parseFrontmatter, loadCategory };

if (require.main === module) {
    main();
}
