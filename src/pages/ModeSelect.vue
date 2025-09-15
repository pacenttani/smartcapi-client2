<template>
  <div class="select-mode">
    <h2>Pilih Mode Pendataan</h2>
    <div>
      <Button @click="choose('ai')">SmartCAPI dengan AI (Rekam Suara)</Button>
      <Button @click="choose('manual')">SmartCAPI Manual (Input Keyboard)</Button>
    </div>
  </div>
</template>
<script setup>
import Button from '../components/Button.vue'
import { useMode } from '../composables/useMode'
import { useRouter } from 'vue-router'

const { setMode } = useMode()
const router = useRouter()

function choose(mode) {
  setMode(mode)
  if (mode === 'ai') router.push('/interview-ai')
  else router.push('/interview-manual')
}
</script>
<style>
.select-mode { text-align: center; margin-top: 4em; }
</style>