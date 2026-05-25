const CACHE_NAME = 'henan-cattle-v2';

// 安装Service Worker
self.addEventListener('install', event => {
  self.skipWaiting();
});

// 监听网络请求 - 优先从网络获取最新内容
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 网络成功，返回并缓存一份
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // 网络失败，从缓存获取
        return caches.match(event.request);
      })
  );
});

// 激活Service Worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});
