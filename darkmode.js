// Dark mode toggle — persists across pages via localStorage
(function () {
    var saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    function updateIcons() {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var buttons = document.querySelectorAll('.theme-toggle');
        buttons.forEach(function (btn) {
            btn.textContent = isDark ? '\u2600' : '\u263E';
        });
    }

    // Update icons once DOM is ready
    document.addEventListener('DOMContentLoaded', updateIcons);

    window.toggleDarkMode = function () {
        var current = document.documentElement.getAttribute('data-theme');
        if (current === 'dark') {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        }
        updateIcons();
    };
})();
