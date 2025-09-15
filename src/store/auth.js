import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || '',
    interviewMode: localStorage.getItem('interviewMode') || 'ai', // 'ai' or 'manual'
  }),
  actions: {
    async login(username, password, mode = 'ai') {
      // Ganti URL sesuai backend Anda
      const res = await axios.post('/api/auth/login', { username, password })
      this.token = res.data.token
      this.user = res.data.user
      this.interviewMode = mode

      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))
      localStorage.setItem('interviewMode', mode)
    },
    async register(payload) {
      // Payload: { full_name, username, password, email, phone }
      await axios.post('/api/auth/register', payload)
    },
    logout() {
      this.token = ''
      this.user = null
      this.interviewMode = 'ai'
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('interviewMode')
    },
    setInterviewMode(mode) {
      this.interviewMode = mode
      localStorage.setItem('interviewMode', mode)
    },
    setUser(userObj) {
      this.user = userObj
      localStorage.setItem('user', JSON.stringify(userObj))
    },
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  }
})