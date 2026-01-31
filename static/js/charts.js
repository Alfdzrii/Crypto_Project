/**
 * Chart.js Configuration for Traffic Distribution
 */

let trafficChart = null;

// Initialize chart when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeChart();
});

function initializeChart() {
    const ctx = document.getElementById('trafficChart');

    if (!ctx) {
        console.error('Chart canvas not found');
        return;
    }

    trafficChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Normal Traffic', 'Attack Traffic'],
            datasets: [{
                data: [0, 0],
                backgroundColor: [
                    'rgba(0, 255, 136, 0.8)',  // Green for normal
                    'rgba(255, 51, 102, 0.8)'   // Red for attack
                ],
                borderColor: [
                    'rgba(0, 255, 136, 1)',
                    'rgba(255, 51, 102, 1)'
                ],
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        font: {
                            family: 'Rajdhani',
                            size: 14,
                            weight: '600'
                        },
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 58, 0.95)',
                    titleColor: '#00ccff',
                    bodyColor: '#ffffff',
                    borderColor: 'rgba(0, 255, 255, 0.3)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function updateChart(distribution) {
    if (!trafficChart) {
        console.error('Chart not initialized');
        return;
    }

    const normalCount = distribution.normal || 0;
    const attackCount = distribution.attack || 0;

    // Update chart data
    trafficChart.data.datasets[0].data = [normalCount, attackCount];

    // Animate update
    trafficChart.update('active');
}

// Export functions
window.updateChart = updateChart;
