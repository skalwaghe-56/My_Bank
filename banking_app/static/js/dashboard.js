// dashboard.js - Scripts for dashboard interactions
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JS loaded.');
    
    // Example: Initialize a chart (if using Chart.js)
    const ctx = document.getElementById('balanceChart');
    if (ctx) {
        const balanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                datasets: [{
                    label: 'Balance',
                    data: [1200, 1500, 1700, 1600, 1800],
                    backgroundColor: 'rgba(0,123,255,0.2)',
                    borderColor: 'rgba(0,123,255,1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});
