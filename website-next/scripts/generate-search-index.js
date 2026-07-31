const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, '../src/db/knowledge-base.json');
const outDir = path.join(__dirname, '../public');
const outPath = path.join(outDir, 'search-index.json');

const SITE_URL = 'https://versatilesparks.qzz.io';
const SUMMARY_MAX = 180;

function truncate(s) {
    if (!s) return '';
    return s.length > SUMMARY_MAX ? s.slice(0, SUMMARY_MAX - 1).trimEnd() + '\u2026' : s;
}

function build() {
    if (!fs.existsSync(dbPath)) {
        console.error('search-index: knowledge-base.json not found. Run `npm run compile` first.');
        process.exit(1);
    }

    const db = JSON.parse(fs.readFileSync(dbPath, 'utf-8'));
    const entries = [];

    db.concepts.forEach((c) => {
        entries.push({
            type: 'concept',
            id: c.id,
            slug: c.slug,
            title: c.title,
            summary: truncate(c.summary),
            difficulty: c.difficulty,
            url: `${SITE_URL}/concepts/${c.slug}`,
            tags: [
                ...(c.aliases || []),
                ...(c.tags || []),
                c.id,
            ],
        });
    });

    db.recipes.forEach((r) => {
        entries.push({
            type: 'recipe',
            id: r.id,
            slug: r.slug,
            title: r.title,
            summary: truncate(r.summary || ''),
            difficulty: r.difficulty,
            book: r.book,
            url: `${SITE_URL}/recipes/${r.slug}`,
            tags: [...(r.concepts || [])],
        });
    });

    db.books.forEach((b) => {
        entries.push({
            type: 'book',
            id: b.id,
            slug: b.slug,
            title: b.title,
            summary: truncate(b.subtitle || b.summary || ''),
            version: b.version,
            url: `${SITE_URL}/books/${b.slug}`,
            tags: [...(b.formats || [])],
        });
    });

    db.problems.forEach((p) => {
        entries.push({
            type: 'problem',
            id: p.id,
            slug: p.slug,
            title: p.title,
            summary: truncate(p.description || ''),
            difficulty: p.conceptObject?.difficulty || null,
            url: `${SITE_URL}/problems/${p.slug}`,
            tags: [...(p.error_patterns || []), p.concept || ''],
        });
    });

    if (!fs.existsSync(outDir)) {
        fs.mkdirSync(outDir, { recursive: true });
    }

    fs.writeFileSync(outPath, JSON.stringify(entries, null, 2), 'utf-8');
    console.log(`Search index: ${entries.length} entries -> public/search-index.json`);
}

build();
