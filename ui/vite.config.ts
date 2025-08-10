import { defineConfig } from 'vite';
import handlebars from 'vite-plugin-handlebars';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';
export default defineConfig({
  plugins: [
    tailwindcss(),
    handlebars({
      partialDirectory: path.resolve(__dirname, 'component'),
    }),
  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        index: path.resolve(__dirname, 'index.html'),
        recommender: path.resolve(__dirname, 'recommender.html'),
        place: path.resolve(__dirname, 'place.html'),
      },
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'https://jsonplaceholder.typicode.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
