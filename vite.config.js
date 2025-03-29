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
      
      // Destination directory (the build output)
      const destDir = path.resolve(__dirname, 'dist');
      
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
  base: '/apple-store-scrape/', // GitHub Pages subdirectory
  
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
  
  plugins: [copyJsonFilesPlugin()]
});
