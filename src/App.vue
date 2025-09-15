<template>
  <div>
    <Sidebar v-if="!isLoginPage" />
    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Sidebar from './components/Layout/Sidebar.vue'

const route = useRoute()
const isLoginPage = computed(() => route.name === 'Login')
</script>