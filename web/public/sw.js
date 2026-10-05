/*
 * Devashaa service worker — installability + a resilient offline app shell.
 *
 * Strategy, deliberately conservative so a bad cache can never strand a build:
 *   - Navigations (HTML): network-first, fall back to the cached shell offline.
 *     Every deploy ships a fresh index.html referencing new hashed assets, so
 *     network-first guarantees updates propagate without bumping this file.
 *   - Same-origin static assets (JS/CSS/img/font): stale-while-revalidate. They
 *     are content-hashed, so a cache hit is always correct; we refresh in the bg.
 *   - Everything else (the cross-origin API on devashaa-api.onrender.com, POSTs,
 *     range requests): passed straight through, never cached.
 *   - THE SAME-ORIGIN API (/api/* — accounts, shares, Pūjā): never touched.
 *     It is same-origin, so without an explicit exclusion it fell into the
 *     static-asset branch below and was served stale-while-revalidate: an old
 *     answer first, the true one only on the next load — and, because a cache
 *     is keyed by URL and not by who is signed in, one person's answer could be
 *     handed to the next person on the same browser. v2 exists to purge any
 *     such responses the v1 cache had collected.
 */
const VERSION = 'devashaa-v2';
const SHELL = ['/', '/favicon.svg', '/manifest.webmanifest'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return; // API + any 3rd-party: leave alone
  if (url.pathname.startsWith('/api/')) return;    // our own API: always the network, never a cache
  // the dev server's modules (/src, /@vite, /node_modules) change on every edit: never cache them either
  if (/^\/(?:src|@[a-z]+|node_modules)\//.test(url.pathname)) return;

  // App shell / SPA routes: network-first, offline fallback to cached index.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(VERSION).then((c) => c.put('/', copy));
          return res;
        })
        .catch(() => caches.match(request).then((m) => m || caches.match('/'))),
    );
    return;
  }

  // Static assets: serve from cache, revalidate in the background.
  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request)
        .then((res) => {
          if (res && res.status === 200 && res.type === 'basic') {
            const copy = res.clone();
            caches.open(VERSION).then((c) => c.put(request, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    }),
  );
});
