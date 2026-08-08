import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Capture the install prompt as early as possible — the browser can fire
// `beforeinstallprompt` before React has mounted. Stash it and re-dispatch a
// custom event so InstallButton picks it up whenever it renders.
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault()
  window.__deferredInstallPrompt = e
  window.dispatchEvent(new CustomEvent('pwa-installable', { detail: e }))
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

// Register the service worker for offline support + installability.
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {})
  })
}
