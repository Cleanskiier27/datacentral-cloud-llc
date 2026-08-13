import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '');
    return {
      define: {
        'process.env.API_KEY' : JSON.stringify('api-key-this-is-not-used-can-be-ignored!'),
      },
      server: {
        proxy: {
          '/api': 'http://localhost:5000',
          '/api-proxy': 'http://localhost:5000',
          '/ws-proxy': {target: 'ws://localhost:5000', ws: true},
        },
      },
      plugins: [react()],
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      }
    };
});
