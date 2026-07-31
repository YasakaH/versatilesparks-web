/**
 * release-audit.js
 *
 * Pre-deploy sanity check. Runs a battery of structural assertions over the
 * compiled knowledge base so a broken content edit fails the build before it
 * reaches production. Exits non-zero on any failure so it can be wired into
 * CI / prebuild.
 *
 * Checks:
 *   1. Every concept/recipe/book has id, slug, title.
 *   2. Slugs are unique within their category.
 *   3. Recipe.concepts and recipe.book resolve to known entries.
 *   4. Concept.requires / used_by / related resolve to known concepts.
 *   5. Book.gumroad_url is a non-empty gum.co / gumroad.com URL.
 *   6. No duplicate recipe ids across books.
 *   7. Search index exists and is non-empty (if generate-search-index ran).
 */

const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, '../src/db/knowledge-base.json');
const searchIndexPath = path.join(__dirname, '../public/search-index.json');

let failures = 0;

function fail(msg) {
    failures++;
    console.error(`  ✗ ${msg}`);
}

function must(condition, msg) {
    if (!condition) fail(msg);
}

function isNonEmptyString(v) {
    return typeof v === 'string' && v.trim().length > 0;
}

function audit() {
    if (!fs.existsSync(dbPath)) {
        console.error('release-audit: knowledge-base.json not found. Run `npm run compile` first.');
        process.exit(1);
    }

    const db = JSON.parse(fs.readFileSync(dbPath, 'utf-8'));
    const conceptIds = new Set(db.concepts.map((c) => c.id));
    const bookIds = new Set(db.books.map((b) => b.id));

    console.log('release-audit: checking knowledge base...');
    const problemsLen = db.problems ? db.problems.length : 0;
    console.log(`  concepts=${db.concepts.length} recipes=${db.recipes.length} books=${db.books.length} problems=${problemsLen}`);

    // 1. Required fields
    db.concepts.forEach((c) => {
        must(isNonEmptyString(c.id), `concept missing id: ${JSON.stringify(c).slice(0, 80)}`);
        must(isNonEmptyString(c.slug), `concept ${c.id} missing slug`);
        must(isNonEmptyString(c.title), `concept ${c.id} missing title`);
    });
    db.recipes.forEach((r) => {
        must(isNonEmptyString(r.id), 'recipe missing id');
        must(isNonEmptyString(r.slug), `recipe ${r.id} missing slug`);
        must(isNonEmptyString(r.title), `recipe ${r.id} missing title`);
    });
    db.books.forEach((b) => {
        must(isNonEmptyString(b.id), 'book missing id');
        must(isNonEmptyString(b.slug), `book ${b.id} missing slug`);
        must(isNonEmptyString(b.title), `book ${b.id} missing title`);
    });
    if (db.problems) {
        db.problems.forEach((p) => {
            must(isNonEmptyString(p.id), 'problem missing id');
            must(isNonEmptyString(p.slug), `problem ${p.id} missing slug`);
            must(isNonEmptyString(p.title), `problem ${p.id} missing title`);
        });
    }

    // 2. Unique slugs within category
    ['concepts', 'recipes', 'books', 'problems'].forEach((cat) => {
        const slugs = db[cat].map((x) => x.slug);
        const seen = new Set();
        slugs.forEach((s) => {
            if (seen.has(s)) fail(`duplicate ${cat} slug: ${s}`);
            seen.add(s);
        });
    });

    // 3. Recipe references resolve
    db.recipes.forEach((r) => {
        (r.concepts || []).forEach((cid) => {
            must(conceptIds.has(cid), `recipe ${r.id} references unknown concept ${cid}`);
        });
        if (r.book) {
            must(bookIds.has(r.book), `recipe ${r.id} references unknown book ${r.book}`);
        }
    });

    // 4. Concept graph references resolve
    db.concepts.forEach((c) => {
        ['requires', 'used_by', 'related'].forEach((key) => {
            (c[key] || []).forEach((id) => {
                must(conceptIds.has(id), `concept ${c.id}.${key} references unknown concept ${id}`);
            });
        });
    });

    // 5. Book gumroad_url is well-formed
    db.books.forEach((b) => {
        const url = b.gumroad_url || '';
        must(
            /^https:\/\/(gum\.co|gumroad\.com)\//.test(url),
            `book ${b.id} has invalid gumroad_url: ${url}`
        );
    });

    // 6. No duplicate recipe ids
    const seenRecipeIds = new Set();
    db.recipes.forEach((r) => {
        if (seenRecipeIds.has(r.id)) fail(`duplicate recipe id: ${r.id}`);
        seenRecipeIds.add(r.id);
    });

    // 7. Search index exists + non-empty
    if (fs.existsSync(searchIndexPath)) {
        const idx = JSON.parse(fs.readFileSync(searchIndexPath, 'utf-8'));
        must(Array.isArray(idx) && idx.length > 0, 'search index is empty or missing entries');
        const total = db.concepts.length + db.recipes.length + db.books.length + (db.problems ? db.problems.length : 0);
        must(idx.length === total, `search index count (${idx.length}) != db total (${total})`);
    } else {
        console.log('  (skip) search-index.json not present yet');
    }

    if (failures === 0) {
        console.log('release-audit: PASS ✓');
        process.exit(0);
    } else {
        console.error(`release-audit: FAIL with ${failures} error(s)`);
        process.exit(1);
    }
}

audit();