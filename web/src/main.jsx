import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { refsOn } from './refs.js'

// Every API call carries the references switch, so the sentences come back
// plain (the default) or as written. One place, instead of every fetch.
const _fetch = window.fetch.bind(window)
window.fetch = (input, init) => {
  const url = typeof input === 'string' ? input : input?.url || ''
  if (/\/api\/(?!account)/.test(url)) {
    const headers = new Headers(init?.headers || (typeof input !== 'string' ? input.headers : undefined) || {})
    headers.set('X-Refs', refsOn() ? '1' : '0')
    return _fetch(input, { ...(init || {}), headers })
  }
  return _fetch(input, init)
}

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
