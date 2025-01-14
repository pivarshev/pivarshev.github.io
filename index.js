window.onload = function() {
    // Add 'loaded' class after everything is loaded (including images)
    document.body.classList.add('loaded');

    // Optionally, you can set a delay here for smooth transitions
    setTimeout(function() {
        document.body.style.transition = "opacity 2s";
        document.body.style.opacity = 1;
    }, 100); // Slight delay to ensure transition starts after everything is ready
};


// Add fade-in when the page is fully loaded
window.addEventListener("load", function() {
    document.body.classList.add("fade-in");
});

// Ensure that the page is properly initialized when going back using the browser (pageshow event)
window.addEventListener("pageshow", function() {
    document.body.classList.remove("fade-out");  // Remove any fade-out effect in case it was left over
    document.body.classList.add("fade-in");      // Add fade-in effect again
});

// When navigating away, apply the fade-out effect (for all navigation links)
let isTransitioning = false;

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', event => {
        if (isTransitioning) return; // Avoid multiple transitions

        event.preventDefault(); // Prevent the default link action to trigger fade-out first

        isTransitioning = true; // Set the transition flag

        // Fade-out effect before navigating
        document.body.classList.remove('fade-in');
        document.body.classList.add('fade-out');

        // Get the target URL from the link
        const targetUrl = link.getAttribute('href');

        // Wait for the fade-out to finish, then navigate
        setTimeout(() => {
            window.location.href = targetUrl;  // Now it will navigate after the fade-out
        }, 500); // Match the fade-out duration
    });
});
