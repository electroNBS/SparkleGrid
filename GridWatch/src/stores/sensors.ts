import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Sensor {
    id: string
    number: number
    name: string
    type: string
    data?: any[]
}

export const useSensorStore = defineStore('sensors', () => {
    const sensors = ref<Sensor[]>([])
    const searchQuery = ref('')

    const filteredSensors = computed(() => {
        if (!searchQuery.value) return sensors.value
        return sensors.value.filter(sensor =>
            sensor.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
    })

    function addSensor(sensor: Sensor) {
        sensors.value.push(sensor)
    }

    function removeSensor(id: string) {
        sensors.value = sensors.value.filter(s => s.id !== id)
    }

    function filterSensors(query: string) {
        searchQuery.value = query
    }

    return {
        sensors,
        filteredSensors,
        addSensor,
        removeSensor,
        filterSensors
    }
})
