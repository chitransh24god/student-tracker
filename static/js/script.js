/**
 * Student Tracker - Main JavaScript File
 * Handles chart initialization, form validation, and UI interactions
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupFormValidation();
    setupEventListeners();
});

/**
 * Initialize all charts on the dashboard
 */
function initializeCharts() {
    // Fetch and render attendance by subject chart
    const attendanceChart = document.getElementById('attendanceChart');
    if (attendanceChart) {
        renderAttendanceBySubjectChart();
    }

    // Fetch and render monthly trend chart
    const trendChart = document.getElementById('trendChart');
    if (trendChart) {
        renderMonthlyTrendChart();
    }

    // Fetch and render engagement distribution chart
    const engagementChart = document.getElementById('engagementChart');
    if (engagementChart) {
        renderEngagementDistributionChart();
    }
}

/**
 * Render attendance percentage by subject
 */
function renderAttendanceBySubjectChart() {
    fetch('/api/attendance-by-subject')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch attendance data');
            }
            return response.json();
        })
        .then(data => {
            if (!data.labels || data.labels.length === 0) {
                document.getElementById('attendanceChart').parentElement.innerHTML =
                    '<p style="text-align: center; color: #999; padding: 40px;">No attendance data available</p>';
                return;
            }

            const ctx = document.getElementById('attendanceChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Attendance Percentage (%)',
                        data: data.percentages,
                        backgroundColor: [
                            '#4F46E5',
                            '#06B6D4',
                            '#10B981',
                            '#F59E0B',
                            '#EF4444',
                            '#8B5CF6'
                        ],
                        borderRadius: 8,
                        borderSkipped: false,
                        hoverBackgroundColor: [
                            '#4338CA',
                            '#0891B2',
                            '#059669',
                            '#D97706',
                            '#DC2626',
                            '#7C3AED'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    indexAxis: 'x',
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: '#333',
                            padding: 12,
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 },
                            borderColor: '#ddd',
                            borderWidth: 1,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return context.parsed.y.toFixed(1) + '%';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading attendance chart:', error);
        });
}

/**
 * Render monthly attendance trend
 */
function renderMonthlyTrendChart() {
    fetch('/api/monthly-trend')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch trend data');
            }
            return response.json();
        })
        .then(data => {
            if (!data.labels || data.labels.length === 0) {
                document.getElementById('trendChart').parentElement.innerHTML =
                    '<p style="text-align: center; color: #999; padding: 40px;">No trend data available</p>';
                return;
            }

            const ctx = document.getElementById('trendChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Attendance Percentage (%)',
                        data: data.percentages,
                        borderColor: '#4F46E5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 6,
                        pointBackgroundColor: '#4F46E5',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 8,
                        hoverBorderWidth: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                usePointStyle: true,
                                padding: 20
                            }
                        },
                        tooltip: {
                            backgroundColor: '#333',
                            padding: 12,
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 },
                            borderColor: '#ddd',
                            borderWidth: 1,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return context.parsed.y.toFixed(1) + '%';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading trend chart:', error);
        });
}

/**
 * Render engagement distribution pie chart
 */
function renderEngagementDistributionChart() {
    fetch('/api/engagement-distribution')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch engagement data');
            }
            return response.json();
        })
        .then(data => {
            if (!data.labels || data.labels.length === 0) {
                document.getElementById('engagementChart').parentElement.innerHTML =
                    '<p style="text-align: center; color: #999; padding: 40px;">No engagement data available</p>';
                return;
            }

            const ctx = document.getElementById('engagementChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.counts,
                        backgroundColor: [
                            '#4F46E5',
                            '#06B6D4',
                            '#10B981',
                            '#F59E0B',
                            '#EF4444',
                            '#8B5CF6',
                            '#EC4899'
                        ],
                        borderColor: '#fff',
                        borderWidth: 2,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            backgroundColor: '#333',
                            padding: 12,
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 },
                            borderColor: '#ddd',
                            borderWidth: 1,
                            displayColors: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading engagement chart:', error);
        });
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value || field.value.trim() === '') {
                    isValid = false;
                    field.classList.add('invalid');
                } else {
                    field.classList.remove('invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'warning');
            }
        });
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Date input - set today's date as default
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value) {
            const today = new Date();
            input.valueAsDate = today;
        }
    });

    // Tab switching
    setupTabSwitching();

    // Search functionality
    setupSearch();

    // Notification auto-close
    setupAutoCloseNotifications();
}

/**
 * Setup tab switching
 */
function setupTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
}

/**
 * Switch tab content
 */
function switchTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Add active class to clicked button
    event.target.classList.add('active');
}

/**
 * Setup search functionality
 */
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.data-table tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

/**
 * Setup auto-close notifications
 */
function setupAutoCloseNotifications() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const container = document.querySelector('.flash-container') || document.body;
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="close-btn" onclick="this.parentElement.remove();">&times;</button>
    `;
    container.insertBefore(alert, container.firstChild);

    // Auto-close after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) {
            alert.remove();
        }
    }, 5000);
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

/**
 * Format date
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

/**
 * Export data to CSV
 */
function exportToCSV(filename = 'export.csv') {
    const table = document.querySelector('.data-table');
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td, th');
        const rowData = Array.from(cells).map(cell => {
            let text = cell.textContent.trim();
            // Escape quotes and wrap in quotes if contains comma
            text = text.replace(/"/g, '""');
            if (text.includes(',')) {
                text = `"${text}"`;
            }
            return text;
        });
        csv.push(rowData.join(','));
    });

    // Create blob and download
    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

/**
 * Confirmation dialog
 */
function confirmAction(message = 'Are you sure?') {
    return confirm(message);
}

// Export functions for global use
window.switchTab = switchTab;
window.showNotification = showNotification;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.exportToCSV = exportToCSV;
window.confirmAction = confirmAction;
