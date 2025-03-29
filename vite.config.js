import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';
import path from 'path';

// 自定義插件，用於將 JSON 文件從 data 目錄復製到构建輸出目錄
// 而不是放在 data 子目錄下
function copyDataFilesPlugin() {
  return {
    name: 'copy-data-files',
    generateBundle() {
      const dataDir = path.resolve(__dirname, 'data');
      if (fs.existsSync(dataDir)) {
        const files = fs.readdirSync(dataDir);
        for (const file of files) {
          if (file.endsWith('.json')) {
            const filePath = path.join(dataDir, file);
            const content = fs.readFileSync(filePath, 'utf-8');
            this.emitFile({
              type: 'asset',
              fileName: file, // 移走自定義路徑，將斈件放在根目錄
              source: content
            });
          }
        }
      }
    }
  };
}

export default defineConfig({
  root: 'src',
  base: '/apple-store-scrape/',  // 添加基本路徑，與倉庫名稱一致
  // 使用自定義處理來確保數據文件被正確地複製，而不是放在 /data/ 子目錄中
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
    open: true, // 自動開啟瀏覽器
  },
  plugins: [copyDataFilesPlugin()]
});
