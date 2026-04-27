// Progressive image loading: swap small thumbnails for high-res versions.
// Images start at ~400px (artworks_small/) for fast load,
// then upgrade to ~2000px (artworks/) as they come into view.
(function () {
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                var hiSrc = img.src.replace('artworks_small/', 'artworks/');
                var hiRes = new Image();
                hiRes.onload = function () {
                    img.src = hiSrc;
                };
                hiRes.src = hiSrc;
                observer.unobserve(img);
            }
        });
    }, { rootMargin: '200px' });

    document.querySelectorAll('img[src*="artworks_small/"]').forEach(function (img) {
        observer.observe(img);
    });
})();
