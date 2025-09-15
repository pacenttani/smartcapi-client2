const CACHE_NAME = 'smartcapi-cache-v1';
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  // Tambahkan file statis lain jika perlu
];

// Install: cache file statis
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_FILES))
  );
});

// Activate: langsung ambil alih tab client
self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

// Fetch: cache-first untuk file statis, network-first untuk API
self.addEventListener('fetch', event => {
  const url = event.request.url;

  // Cache-first untuk file statis
  if (STATIC_FILES.some(file => url.endsWith(file))) {
    event.respondWith(
      caches.match(event.request).then(response => response || fetch(event.request))
    );
    return;
  }

  // Network-first untuk API (manual/AI)
  if (url.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  // Default: network
  event.respondWith(fetch(event.request));
});

// (Opsional) Background sync, push notification, dsb. bisa ditambahkan di bawah sini