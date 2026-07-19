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
      
      db[cat].push({
        ...metadata,
        body
      });
    });
  });

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  fs.writeFileSync(
    path.join(outputDir, 'knowledge-base.json'),
    JSON.stringify(db, null, 2),
    'utf-8'
  );
  
  console.log('Successfully compiled knowledge database to src/db/knowledge-base.json');
}

compile();
