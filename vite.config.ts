import { defineConfig } from 'vite'

// Vite configuration with proxy to Python backend
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/predict': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})