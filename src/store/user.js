import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  function login(u) { user.value = u }
  function logout() { user.value = null }
  return { user, login, logout }
})