// main.js - Global JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Main JS loaded.');
    
    // Example: Toggle a CSS class on the body for dark mode (if implemented)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
        });
    }
});
