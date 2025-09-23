  const statuses = JSON.parse(document.getElementById('statuses-data').textContent);
    const counts = JSON.parse(document.getElementById('counts-data').textContent);
    const months = JSON.parse(document.getElementById('months-data').textContent);
    const monthCounts = JSON.parse(document.getElementById('months-counts-data').textContent);
    const interviewMonths = JSON.parse(document.getElementById('interview-months-data').textContent);
    const interviewData = JSON.parse(document.getElementById('interview-data').textContent);

    // --- Chart Initialization ---
    document.addEventListener('DOMContentLoaded', function () {
        // --- Status Pie Chart ---
        const statusCtx = document.getElementById('statusChart');
        if (statusCtx) {
            new Chart(statusCtx, {
                type: 'pie',
                data: {
                    labels: statuses,
                    datasets: [{
                        data: counts,
                        backgroundColor: [
                            getComputedStyle(document.documentElement).getPropertyValue('--bs-primary'),
                            getComputedStyle(document.documentElement).getPropertyValue('--bs-warning'),
                            getComputedStyle(document.documentElement).getPropertyValue('--bs-success'),
                            getComputedStyle(document.documentElement).getPropertyValue('--bs-danger')
                        ],
                        borderColor: '#fff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#fff'
                            }
                        }
                    },
                    scales: {
                        // Ensure the pie chart doesn't have a border
                    }
                }
            });
        }

        // --- Applications Over Time Line Chart ---
        const appsCtx = document.getElementById('applicationsChart');
        if (appsCtx) {
            new Chart(appsCtx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Applications',
                        data: monthCounts,
                        borderColor: getComputedStyle(document.documentElement).getPropertyValue('--bs-primary'),
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                color: '#fff'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#fff'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#fff'
                            }
                        }
                    }
                }
            });
        }

        // --- Interviews Over Time Bar Chart ---
        const interviewsCtx = document.getElementById('interviewsChart');
        if (interviewsCtx) {
            new Chart(interviewsCtx, {
                type: 'bar',
                data: {
                    labels: interviewMonths,
                    datasets: [{
                        label: 'Interviews',
                        data: interviewData,
                        backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--bs-success')
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                color: '#fff'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#fff'
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#fff'
                            }
                        }
                    }
                }
            });
        }

        // --- Counter Animation ---
        document.querySelectorAll('.counter').forEach(counter => {
            const targetRaw = counter.getAttribute('data-target') ?? '0';
            const target = Number(targetRaw);
            if (!Number.isFinite(target) || target <= 0) {
                counter.textContent = String(Math.max(0, Math.floor(target)));
                counter.classList.remove('fade-in');
                counter.style.opacity = '1';
                return;
            }
            const duration = 1000;
            const start = performance.now();
            const animate = (now) => {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const current = Math.round(progress * target);
                counter.textContent = current.toLocaleString();
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            };
            requestAnimationFrame(animate);
        });
    });




      document.addEventListener('DOMContentLoaded', function () {
        const scoreElement = document.getElementById('scoreData');
        if (scoreElement) {
            const score = JSON.parse(scoreElement.textContent);
            const ctx = document.getElementById('matchChart');

            if (ctx) {
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Match', 'Gap'],
                        datasets: [{
                            data: [score, 100 - score],
                            backgroundColor: [
                                getComputedStyle(document.documentElement).getPropertyValue('--bs-success'), // Match
                                getComputedStyle(document.documentElement).getPropertyValue('--bs-danger')   // Gap
                            ],
                            borderColor: '#fff',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false, // Important with fixed container height
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    color: getComputedStyle(document.documentElement).getPropertyValue('--bs-body-color') // Legend text color
                                }
                            }
                        }
                    }
                });
            }
        }
    });


    
    document.addEventListener('DOMContentLoaded', function () {
        const scoreElement = document.getElementById('scoreData');
        if (scoreElement) {
            const score = JSON.parse(scoreElement.textContent);
            const ctx = document.getElementById('matchChart');

            if (ctx) {
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Match', 'Gap'],
                        datasets: [{
                            data: [score, 100 - score],
                            backgroundColor: [
                                getComputedStyle(document.documentElement).getPropertyValue('--bs-success'), // Match
                                getComputedStyle(document.documentElement).getPropertyValue('--bs-danger')   // Gap
                            ],
                            borderColor: '#fff',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false, // Important with fixed container height
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    color: getComputedStyle(document.documentElement).getPropertyValue('--bs-body-color') // Legend text color
                                }
                            }
                        }
                    }
                });
            }
        }
    });
