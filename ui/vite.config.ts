import { defineConfig } from 'vite';
import handlebars from 'vite-plugin-handlebars';
import Handlebars from 'handlebars';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

import handlebarsLayouts from 'handlebars-layouts';

handlebarsLayouts.register(Handlebars);

export default defineConfig({
  plugins: [
    tailwindcss(),
    handlebars({
      partialDirectory: [
        path.resolve(__dirname, 'src', 'components'),
        path.resolve(__dirname, 'src', 'templates'),
        path.resolve(__dirname, 'src', 'pages'),
        path.resolve(__dirname, 'component'),
      ],
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

Handlebars.registerHelper('times', function (n, block) {
  let accum = '';
  for (let i = 0; i < n; ++i) {
    accum += block.fn(i);
  }
  return accum;
});
