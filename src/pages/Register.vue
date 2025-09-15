<template>
  <div class="container">
    <div class="form-title">Registrasi Akun</div>
    <form @submit.prevent="onRegister">
      <input v-model="full_name" placeholder="Nama Lengkap" required />
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="retype" type="password" placeholder="Retype Password" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="phone" placeholder="Nomor Telepon" required />
      <div class="form-footer">
        <button type="button" @click="router.back()">BACK</button>
        <button type="submit" :disabled="loading">{{ loading ? '...' : 'NEXT' }}</button>
      </div>
      <div v-if="error" style="color:#e11d48;">{{ error }}</div>
    </form>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const full_name = ref('')
const username = ref('')
const password = ref('')
const retype = ref('')
const email = ref('')
const phone = ref('')
const loading = ref(false)
const error = ref('')
const auth = useAuthStore()

async function onRegister() {
  error.value = ''
  if(password.value !== retype.value) {
    error.value = "Password tidak cocok"
    return
  }
  loading.value = true
  try {
    await auth.register({ full_name: full_name.value, username: username.value, password: password.value, email: email.value, phone: phone.value })
    router.push('/')
  } catch(e) {
    error.value = e.message || "Registrasi gagal"
  } finally {
    loading.value = false
  }
}
</script>