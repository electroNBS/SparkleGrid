<template>
    <div class="sensor">
      <!-- New table for THD, Power Factor, and RMS readings -->
      <div class="sensor-table">
        <h1>Real-Time Readings of {{ sensorName }}</h1>
        <table>
          <thead>
            <tr>
              <th>THD (%)</th>
              <th>Power Factor</th>
              <th>RMS</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ thd }}</td>
              <td>{{ powerFactor }}</td>
              <td>{{ rms }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <h1>{{ sensorType }} Data</h1>
      <!-- Table for sensor data -->
      <div class="sensor-table">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Readings</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(data, index) in recentSensdataData" :key="index">
              <td>{{ data.time }}</td>
              <td>{{ data.sensdata }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Chart placeholder -->
      <div id="staticChart" style="height: 300px;"></div> <!-- Added inline style for height -->
      <!-- Pause/Resume button -->
      <button @click="toggleUpdate">{{ isUpdating ? 'Pause' : 'Resume' }}</button>
      <div v-if="fetchError" class="error-message">
        Error fetching sensor data. Please check backend connection.
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineComponent, ref, computed, onMounted, type Ref, onUnmounted } from 'vue'
  import axios from 'axios'
  import ApexCharts, { type ApexOptions } from 'apexcharts'
  import { useRoute } from 'vue-router'
  
  interface SensdataMeasurement {
    sensdata: [string, string][] // 2D array of sensdata and deltaT
    time: string // Start time
    thd: string
    rms: string
    pf: string
    sname: string
    stype: string
  }
  
  interface SensdataData {
    sensdata: string
    time: string
  }
  
  const route = useRoute()
  const sensorNumber = route.query.number
  const measurement: Ref<SensdataMeasurement | null> = ref(null)
  const staticChart: Ref<ApexCharts | null> = ref(null)
  const startTime: Ref<Date> = ref(new Date())
  const thd: Ref<string> = ref('0')
  const powerFactor: Ref<string> = ref('0')
  const rms: Ref<string> = ref('0')
  const sensorName: Ref<string> = ref('Sensor Data') // Default sensor name
  const sensorType: Ref<string> = ref('Unknown Sensor Type') // Default sensor type
  const isUpdating: Ref<boolean> = ref(true)
  const fetchError = ref(false) // Ref to track fetch errors
  let fetchInterval: number | null = null // Variable to hold interval ID
  
  const fetchSensorData = async () => {
    if (!isUpdating.value) return
  
    try {
      fetchError.value = false // Reset error state before fetch
      const currentTime = new Date()
      const currentHour = currentTime.getHours()
      const tableNumber = Math.floor(currentHour / 4) + 1 // Calculate table number based on time
      const url = `http://127.0.0.1:8000/measurements/6/${sensorNumber}/`
  
      const response = await axios.get(url)
      const data: SensdataMeasurement = response.data.measurements
      startTime.value = new Date(data.time)
      measurement.value = data
      thd.value = data.thd
      powerFactor.value = data.pf
      rms.value = data.rms
      sensorName.value = data.sname || 'Sensor Data' // Use fetched name or default
      sensorType.value = data.stype || 'Unknown Sensor Type' // Use fetched type or default
      updateStaticChart()
    } catch (error) {
      console.error('Error during Axios GET request:', error)
      fetchError.value = true // Set error state on fetch fail
    }
  }
  
  const recentSensdataData = computed((): SensdataData[] => {
    return (
      measurement.value?.sensdata.slice(0, 20).map((sensdataTuple) => {
        const sensdataValue = String(parseFloat(sensdataTuple[0]) - 1.514)
        const deltaTime = parseFloat(sensdataTuple[1])
        const measurementTime = new Date(startTime.value.getTime() + deltaTime).toISOString()
        return {
          sensdata: sensdataValue,
          time: measurementTime
        }
      }) || []
    )
  })
  
  const formatNumber = (value: number) => {
    return value.toPrecision(5).replace(/(\.\d*?[1-9])0+|\.0+$/, '$1').replace(/(\.\d{2})\d+$/, '$1')
  }
  
  const initStaticChart = () => {
    const options: ApexOptions = {
      chart: {
        type: 'line',
        height: '100%',
        width: '100%',
        zoom: {
          enabled: true,
          type: 'x',
          autoScaleYaxis: true
        },
        toolbar: {
          autoSelected: 'zoom'
        },
        foreColor: '#fff', // White text color for chart labels and titles
        background: 'transparent' // Transparent chart background
      },
      series: [
        {
          name: 'Sensdata',
          data: []
        }
      ],
      xaxis: {
        type: 'datetime',
        labels: {
          formatter: function (value) {
            return new Date(value).toISOString().slice(11, 23)
          },
          style: {
            colors: '#fff' // White color for x-axis labels
          }
        },
        title: {
          text: 'Time',
          style: {
            color: '#fff' // White color for x-axis title
          }
        }
      },
      yaxis: {
        labels: {
          formatter: function (value) {
            return formatNumber(value)
          },
          style: {
            colors: '#fff' // White color for y-axis labels
          }
        },
        title: {
          text: 'Sensor Readings',
          style: {
            color: '#fff' // White color for y-axis title
          }
        }
      },
      tooltip: {
        x: {
          formatter: function (value) {
            return new Date(value).toISOString().slice(11, 23)
          }
        },
        theme: 'dark' // Dark tooltip theme to match dark background
      },
      theme: {
        mode: 'dark', // Ensure dark mode for chart
        palette: 'palette7' // Optional: Choose a specific dark palette
      }
    }
  
    staticChart.value = new ApexCharts(document.querySelector('#staticChart'), options)
    staticChart.value.render()
  }
  
  const updateStaticChart = () => {
    if (staticChart.value && measurement.value) {
      const seriesData = measurement.value.sensdata.map((sensdataTuple) => {
        const sensdataValue = String(parseFloat(sensdataTuple[0]) - 1.514)
        const deltaTime = parseFloat(sensdataTuple[1])
        const timeValue = new Date(startTime.value.getTime() + deltaTime).toISOString()
        return {
          x: timeValue,
          y: parseFloat(sensdataValue)
        }
      })
  
      // Update the series data
      staticChart.value.updateSeries([
        {
          name: 'Sensdata',
          data: seriesData
        }
      ])
    }
  }
  
  const toggleUpdate = () => {
    isUpdating.value = !isUpdating.value
    if (isUpdating.value) {
      startFetchingData() // Restart fetching when resuming
    } else {
      stopFetchingData() // Stop fetching when pausing
    }
  }
  
  const startFetchingData = () => {
    if (!fetchInterval) {
      fetchSensorData()
      fetchInterval = setInterval(fetchSensorData, 1000)
    }
  }
  
  const stopFetchingData = () => {
    if (fetchInterval) {
      clearInterval(fetchInterval)
      fetchInterval = null
    }
  }
  
  
  onMounted(() => {
    initStaticChart()
    startFetchingData() // Start fetching data on mount
  })
  
  onUnmounted(() => {
    stopFetchingData() // Clear interval on unmount to prevent memory leaks
  })
  
  
  </script>
  
  <style scoped>
  .sensor {
    padding: 1rem;
    color: white;
  }
  
  h1 {
    color: white;
  }
  
  .sensor-table {
    margin-top: 2rem;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th,
  td {
    border: 1px solid var(--color-table-border); /* Using CSS variable for border color */
    padding: 8px;
    text-align: left;
    color: white;
  }
  
  th {
    background-color: var(--color-table-header); /* Using CSS variable for header background */
    color: white;
  }
  
  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: var(--color-button); /* Using CSS variable for button background */
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: var(--color-button-hover); /* Using CSS variable for button hover background */
  }
  
  .error-message {
    color: #ff4d4d; /* Error text color */
    margin-top: 1rem;
  }
  
  
  @media (max-width: 768px) {
    .sensor {
      padding: 0.5rem;
    }
  
    table {
      font-size: 0.8rem;
    }
  }
  </style>