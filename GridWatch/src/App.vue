<template>
  <div id="app">
    <Header />
    <Sidebar :sensors="sensors" @add-sensor="addPlaceholderSensor" />
    <main>
      <router-view />
      <div v-if="backendStatus !== 'connected'" class="status-indicator" :class="backendStatus">
        <span v-if="backendStatus === 'loading'">Loading...</span>
        <span v-if="backendStatus === 'error'">Backend Error</span>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { BoltIcon, PlusIcon } from '@heroicons/vue/24/solid'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import axios from 'axios' // Import axios for status check

interface Sensor {
  number: number
  name: string
  path: string
  icon: any // Use appropriate type for your icon components
}

const sensors: Ref<Array<Sensor>> = ref([
  // Example sensors - you can populate this from backend later
  // { number: 1, name: 'Sensor 1', path: '/sensor', icon: BoltIcon },
  // { number: 2, name: 'Sensor 2', path: '/sensor', icon: BoltIcon }
])

// Function to add a new sensor
function addSensor(name: string) {
  const NewIcon = BoltIcon // Placeholder for new sensor icon
  const sensorNumber = sensors.value.length + 1
  sensors.value.push({ number: sensorNumber, name, path: '/sensor', icon: NewIcon })
}

// Function to remove a sensor by name (not used in template yet)
function removeSensor(name: string) {
  sensors.value = sensors.value.filter((sensor) => sensor.name !== name)
}

// Function to add a placeholder sensor when the plus button is clicked
function addPlaceholderSensor() {
  const newSensorName = `Sensor ${sensors.value.length + 1}`
  addSensor(newSensorName)
}

const route = useRoute()

// Backend Status Indicator Logic
const backendStatus = ref<'loading' | 'connected' | 'error'>('loading')

const checkBackendStatus = async () => {
  backendStatus.value = 'loading'
  try {
    // Replace with your actual backend health check endpoint
    await axios.get('http://localhost:8000/microgrid_back/health')
    backendStatus.value = 'connected'
  } catch (error) {
    console.error('Backend check failed', error)
    backendStatus.value = 'error'
  }
}

onMounted(() => {
  checkBackendStatus() // Initial check on app mount
  // Optionally, set up interval for periodic checks if needed
  // setInterval(checkBackendStatus, 30000); // Check every 30 seconds
})
</script>

<style>
/* Import frontend styles - you can adjust path if needed */
@import './style.css';

#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--color-text); /* Using CSS variable from style.css */
  background-color: var(--color-background); /* Using CSS variable from style.css */
  height: 100vh; /* Make sure app takes full viewport height */
  display: flex;
  flex-direction: column; /* Arrange header, sidebar, main vertically */
}

main {
  flex: 1; /* Main content takes remaining space */
  padding: 1rem;
  margin-left: 60px; /* Default sidebar width, adjust if needed */
  margin-top: 6vh; /* Header height, adjust if needed */
  transition: margin-left 0.3s ease;
  background-color: transparent;
  position: relative; /* For positioning status indicator */
}

aside:hover + main {
  margin-left: 200px; /* Expanded sidebar width, adjust if needed */
}

/* Status Indicator Styles */
.status-indicator {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: white;
}

.status-indicator.loading {
  background-color: rgba(255, 255, 0, 0.7); /* Yellow for loading */
  color: black;
}

.status-indicator.error {
  background-color: rgba(255, 0, 0, 0.8); /* Red for error */
}

.status-indicator.connected {
  display: none; /* Hide when connected, or style as success if you prefer */
  background-color: rgba(0, 200, 0, 0.7); /* Green for connected (optional) */
}
</style>