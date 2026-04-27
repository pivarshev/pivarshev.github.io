// Dark mode toggle — persists across pages via localStorage
(function () {
    var saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }

    function updateIcons() {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var buttons = document.querySelectorAll('.theme-toggle');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].textContent = isDark ? 'light' : 'dark';
        }
    }

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
