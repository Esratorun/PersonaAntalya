const CACHE_NAME = 'persona-antalya-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/css/personas.css',
  // İleride çevrimdışı (offline) çalışmasını istediğin sayfaları buraya ekleyebilirsin
];

// Yükleme Aşaması
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Önbellek (Cache) açıldı');
        return cache.addAll(urlsToCache);
      })
  );
});

// İstekleri Yakalama (Çevrimdışı destek için temel)
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Önbellekte varsa onu döndür, yoksa ağdan çek
        return response || fetch(event.request);
      })
  );
});