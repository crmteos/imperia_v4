// build_catalog.js - Imperia v4 Project Directory Indexer
// Scans C:\imperia_v4 and generates PROJECT_STRUCTURE.md and project_catalog.json
// Ignores node_modules and .git directories

const fs = require('fs');
const path = require('path');
const os = require('os');

const ROOT_DIR = 'c:/imperia_v4';
const IGNORE_DIRS = ['node_modules', '.git'];
const IGNORE_EXTS = ['.mjs', '.cjs', '.lock'];

// Track visited paths to avoid duplicates
const visited = new Set();

// Recursive directory scanner
function scanDirectory(dirPath) {
  const results = [];
  let fullPath;
  
  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    
    for (const entry of entries) {
      // Skip ignored directories
      if (entry.isDirectory() && IGNORE_DIRS.includes(entry.name)) {
        continue;
      }
      
      fullPath = path.join(dirPath, entry.name);
      
      // Skip already visited paths
      if (visited.has(fullPath)) {
        continue;
      }
      visited.add(fullPath);
      
      if (entry.isDirectory()) {
        const dirResult = {
          type: 'directory',
          name: entry.name,
          path: fullPath,
          relativePath: path.relative(ROOT_DIR, fullPath),
          size: 0,
          modified: fs.statSync(fullPath).mtimeMs,
          children: scanDirectory(fullPath)
        };
        results.push(dirResult);
      } else if (entry.isFile()) {
        // Skip ignored extensions
        if (IGNORE_EXTS.some(ext => entry.name.endsWith(ext))) {
          continue;
        }
        
        const fileStat = fs.statSync(fullPath);
        results.push({
          type: 'file',
          name: entry.name,
          path: fullPath,
          relativePath: path.relative(ROOT_DIR, fullPath),
          size: fileStat.size,
          modified: fileStat.mtimeMs,
          description: getFileDescription(entry.name)
        });
      }
    }
  } catch (err) {
    console.error(`Error scanning ${dirPath}:`, err.message);
  }
  
  return results;
}

function getFileDescription(filename) {
  const descMap = {
    'index.html': 'Main application entry point',
    'package.json': 'Project dependencies and scripts',
    'README.md': 'Project documentation',
    'tsconfig.json': 'TypeScript configuration',
    'tslint.json': 'TypeScript linting configuration',
    '.gitignore': 'Git ignore patterns'
  };
  return descMap[filename] || 'Project file';
}

// Generate human-readable size
function formatSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// Main execution
const catalog = scanDirectory(ROOT_DIR);

// Generate PROJECT_STRUCTURE.md
function generateMarkdown(catalog, rootDir) {
  function buildTree(nodes, indent = 0) {
    let output = '';
    const prefix = '  '.repeat(indent);
    
    nodes.forEach(node => {
      if (node.type === 'directory') {
        output += `${prefix}- **${node.name}/**\n`;
        output += buildTree(node.children, indent + 1);
      } else {
        output += `${prefix}- ${node.name} (${formatSize(node.size)}) — ${node.description}\n`;
      }
    });
    
    return output;
  }
  
  const md = `# Imperia v4 Project Structure\n\nGenerated: ${new Date().toISOString()}\n\n## Directory Tree\n\n\`\`\`markdown\n${buildTree(catalog)}\n\`\`\`\n\n## Quick Stats\n\n- **Total files**: ${catalog.filter(n => n.type === 'file').length}\n- **Total directories**: ${catalog.filter(n => n.type === 'directory').length}\n- **Root directory**: ${rootDir}\n- **Ignored**: node_modules, .git\n- **Largest files**: [to be populated based on needs]`;
  
  return md;
}

// Generate JSON catalog
function generateJSON(catalog) {
  function convertNode(node) {
    if (node.type === 'directory') {
      return {
        type: 'directory',
        name: node.name,
        path: node.path,
        relativePath: node.relativePath,
        size: node.size,
        modified: node.modified,
        children: node.children.map(convertNode)
      };
    } else {
      return {
        type: 'file',
        name: node.name,
        path: node.path,
        relativePath: node.relativePath,
        size: node.size,
        modified: node.modified,
        description: node.description
      };
    }
  }
  
  return {
    generatedAt: new Date().toISOString(),
    rootDirectory: ROOT_DIR,
    totalFiles: catalog.filter(n => n.type === 'file').length,
    totalDirectories: catalog.filter(n => n.type === 'directory').length,
    items: catalog.map(convertNode)
  };
}

// Write output files
try {
  const mkdContent = generateMarkdown(catalog, ROOT_DIR);
  const jsonContent = JSON.stringify(generateJSON(catalog), null, 2);
  
  // Ensure docs directory exists
  const docsDir = path.join(ROOT_DIR, 'docs');
  if (!fs.existsSync(docsDir)) {
    fs.mkdirSync(docsDir, { recursive: true });
  }
  
  // Write files
  fs.writeFileSync(path.join(docsDir, 'PROJECT_STRUCTURE.md'), mkdContent, 'utf-8');
  fs.writeFileSync(path.join(docsDir, 'project_catalog.json'), jsonContent, 'utf-8');
  
  console.log('✅ Catalog generated successfully!');
  console.log(`   - docs/PROJECT_STRUCTURE.md (${mkdContent.length} bytes)`);
  console.log(`   - docs/project_catalog.json (${jsonContent.length} bytes)`);
  
} catch (err) {
  console.error('❌ Failed to generate catalog:', err.message);
  process.exit(1);
}