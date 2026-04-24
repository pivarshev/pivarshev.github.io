// Progressive image loading: swap small thumbnails for high-res versions.
// Images start at ~400px (artworks_small/) for fast load,
// then upgrade to ~2000px (artworks/) in the background.
window.addEventListener('load', function () {
    var images = document.querySelectorAll('img[src*="artworks_small/"]');
    var delay = 50;

    images.forEach(function (img, i) {
        setTimeout(function () {
            var hiRes = new Image();
            var hiSrc = img.src.replace('artworks_small/', 'artworks/');
            hiRes.onload = function () {
                img.src = hiSrc;
            };
            hiRes.src = hiSrc;
        }, delay * i);
    });
});
