<template>
    <aside>
      <nav>
        <ul>
          <li v-for="sensor in sensors" :key="sensor.name">
            <!-- Pass the sensor name as a route query parameter -->
            <router-link :to="{ path: sensor.path, query: { number: sensor.number } }">
              <component :is="sensor.icon" class="icon" />
              <span class="text">{{ sensor.name }}</span>
            </router-link>
          </li>
          <!-- Plus button to add a new sensor -->
          <li>
            <button @click="$emit('add-sensor')">
              <PlusIcon class="icon" />
              <span class="text">Add Sensor</span>
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  </template>
  
  <script setup lang="ts">
  import { defineProps, defineEmits } from 'vue';
  import { RouterLink } from 'vue-router';
  import { PlusIcon } from '@heroicons/vue/24/solid';
  
  const props = defineProps({
    sensors: {
      type: Array,
      required: true
    }
  });
  
  const emit = defineEmits(['add-sensor']);
  </script>
  
  <style scoped>
  /* Most of the sidebar styling is in src/style.css,
     this is for component-specific styling if needed */
  </style>