import ApexCharts from 'apexcharts'

export const createChartConfig = (type = 'line') => {
    return {
        chart: {
            type,
            height: 350,
            background: 'transparent',
            foreColor: '#fff',
            animations: {
                enabled: true,
                easing: 'easeinout',
                dynamicAnimation: {
                    speed: 1000
                }
            }
        },
        theme: {
            mode: 'dark'
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        xaxis: {
            type: 'datetime',
            labels: {
                style: {
                    colors: '#fff'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#fff'
                }
            }
        },
        grid: {
            borderColor: '#545b5e'
        },
        tooltip: {
            theme: 'dark'
        }
    }
}

export const initializeChart = (elementId: string, options = {}) => {
    const baseConfig = createChartConfig()
    const chart = new ApexCharts(
        document.querySelector(elementId),
        { ...baseConfig, ...options }
    )
    return chart
}
