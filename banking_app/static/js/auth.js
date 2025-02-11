// auth.js - Scripts for authentication pages
document.addEventListener('DOMContentLoaded', function() {
    console.log('Auth JS loaded.');
    
    // Example: Validate registration form inputs (client-side)
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            if (password !== confirmPassword) {
                event.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }
});
