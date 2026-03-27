import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';
import path from 'path';

// Plugin to copy data JSON files to the output directory root
function copyJsonFilesPlugin() {
  return {
    name: 'copy-json-files',
    closeBundle() {
      // Source directory for JSON files (now only using src/data)
      const sourceDir = path.resolve(__dirname, 'src/data');
      
      // Destination directory (the build output, matching fetch path data/)
      const destDir = path.resolve(__dirname, 'dist/data');
      
      // Ensure destination directory exists
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      
      // Copy JSON files from source directory
      if (fs.existsSync(sourceDir)) {
        const files = fs.readdirSync(sourceDir);
        for (const file of files) {
          if (file.endsWith('.json')) {
            const sourcePath = path.join(sourceDir, file);
            const destPath = path.join(destDir, file);
            
            console.log(`Copying ${sourcePath} to ${destPath}`);
            fs.copyFileSync(sourcePath, destPath);
          }
        }
      } else {
        console.warn(`Warning: Source directory ${sourceDir} does not exist.`);
      }
    }
  };
}

export default defineConfig({
  root: 'src',
  base: process.env.VITE_APP_BASE_URL || '/', // Default to '/' for local, use env var for GH Pages
  
  // Don't use publicDir to handle data files, we'll use a plugin instead
  publicDir: false,
  
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/index.html'),
      },
    },
  },
  
  server: {
    open: true,
  },
  
  plugins: [copyJsonFilesPlugin(), {
    // Optimize resource loading in production HTML:
    // 1. CSS: preload + async load (eliminates render-blocking)
    // 2. JSON: preload default dataset (starts fetch in parallel with JS)
    name: 'optimize-resource-loading',
    transformIndexHtml(html) {
      const base = process.env.VITE_APP_BASE_URL || '/';

      // CSS: convert blocking <link rel="stylesheet"> to async preload
      const cssMatch = html.match(/<link rel="stylesheet"[^>]+>/);
      if (cssMatch) {
        const cssTag = cssMatch[0];
        const href = cssTag.match(/href="([^"]+)"/)?.[1];
        if (href) {
          html = html.replace(cssTag, '');
          const preload = `<link rel="preload" href="${href}" as="style" onload="this.onload=null;this.rel='stylesheet'">\n  <noscript>${cssTag}</noscript>`;
          html = html.replace('</head>', `  ${preload}\n</head>`);
        }
      }

      // JSON: preload default product data (cuts dependency chain)
      const jsonPreload = `<link rel="preload" href="${base}data/iphone_data.json" as="fetch" crossorigin>`;
      html = html.replace('</head>', `  ${jsonPreload}\n</head>`);

      return html;
    }
  }, {
    // Copy sw.js to dist root (must not be bundled by Vite)
    name: 'copy-service-worker',
    closeBundle() {
      const src = path.resolve(__dirname, 'src/sw.js');
      const dest = path.resolve(__dirname, 'dist/sw.js');
      if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
      }
    }
  }]
});
