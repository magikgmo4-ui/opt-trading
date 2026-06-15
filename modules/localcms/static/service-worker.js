// LocalCMS Service Worker — PWA offline cache
// GO_LOCALCMS_GLOBAL_PWA_PRIVATE_ACCESS_01
// Caches app shell for fast loading, falls back gracefully

const CACHE_NAME = 'localcms-v1';
const CACHE_URLS = [
  '/',
  '/ui',
  '/voice',
  '/voice/analytics',
  '/access',
  '/static/manifest.webmanifest',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CACHE_URLS).catch(() => {});
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Only cache GET requests to same origin
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  // Network-first for data, cache fallback for UI
  if (url.pathname.startsWith('/voice/query') || url.pathname.startsWith('/desk/')) {
    // Network-first — always try live data
    return;
  }

  // Cache-first for static UI shells
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetchPromise = fetch(event.request).then((response) => {
        if (response && response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
