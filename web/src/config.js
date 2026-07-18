// Backend base URL. In production set VITE_API_URL (Cloudflare Pages → Settings →
// Environment variables) to your Render backend, e.g. https://devashaa-api.onrender.com
// Locally it falls back to the dev server.
export const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5174'
