
        function taylorLn1PlusX(x, n) {
            let sum = 0;
            for (let i = 1; i <= n; i++) {
                const term = Math.pow(-1, i+1) * Math.pow(x, i) / i;
                sum += term;
            }
            return sum;
        }

        const dataPoints = 100;
        const xMin = -0.9;
        const xMax = 1.5;
        const step = (xMax - xMin) / dataPoints;

        const xValues = [];
        const taylorValues = [];
        const mathValues = [];

        const n = 10;

        for (let i = 0; i <= dataPoints; i++) {
            const x = xMin + i * step;
            xValues.push(x);

            if (x > -1) {
                taylorValues.push(taylorLn1PlusX(x, n));
                mathValues.push(Math.log1p(x));
            } else {
                taylorValues.push(null);
                mathValues.push(null);
            }
        }

        const ctx = document.getElementById('myChart').getContext('2d');

        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: xValues,
                datasets: [
                    {
                        label: 'Разложение в ряд Тейлора',
                        data: taylorValues,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        borderWidth: 2,
                        tension: 0.1,
                        pointRadius: 0
                    },
                    {
                        label: 'Math.log1p(x)',
                        data: mathValues,
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        borderWidth: 2,
                        tension: 0.1,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Сравнение разложения ln(1+x) в ряд Тейлора и вычисления через Math.log1p(x)',
                        font: {
                            size: 16
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line',
                                yMin: 0,
                                yMax: 0,
                                borderColor: 'rgb(0, 0, 0)',
                                borderWidth: 1,
                                label: {
                                    display: true,
                                    content: 'Ось X',
                                    position: 'end'
                                }
                            },
                            line2: {
                                type: 'line',
                                xMin: 0,
                                xMax: 0,
                                borderColor: 'rgb(0, 0, 0)',
                                borderWidth: 1,
                                label: {
                                    display: true,
                                    content: 'Ось Y',
                                    position: 'end'
                                }
                            },
                            point1: {
                                type: 'point',
                                xValue: 0,
                                yValue: 0,
                                backgroundColor: 'rgba(255, 0, 0, 0.5)',
                                radius: 5,
                                label: {
                                    display: true,
                                    content: '(0, 0)',
                                    position: 'top'
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'x',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'F(x)',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        });

        document.getElementById('saveBtn').addEventListener('click', function() {
            const link = document.createElement('a');
            link.download = 'ln1plusx-graph.png';
            link.href = myChart.toBase64Image();
            link.click();
        });