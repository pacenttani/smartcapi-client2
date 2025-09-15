<template>
  <div class="login-page">
    <div class="login-logo">
      <img src="@/assets/smartcapi-logo.png" alt="SmartCAPI Logo" class="logo-img" />
      <span class="logo-text">SmartCAPI</span>
    </div>
    <div class="login-card">
      <form @submit.prevent="onLogin">
        <input v-model="username" type="text" placeholder="Username" required />
<input v-model="password" type="password" placeholder="Password" required />
        <button type="submit" class="login-btn">Log in</button>
      </form>
      <div class="login-links">
        <span>Belum punya akun? Klik <a href="#" @click.prevent="goRegister">daftar</a></span>
        <span>Lupa password ? Klik <a href="#" @click.prevent="goForgot">sini</a></span>
      </div>
    </div>
    <div class="login-mode">
      <label>
        <input type="radio" value="manual" v-model="mode" />
        <span :class="{ selected: mode==='manual' }">Manual</span>
      </label>
      <label>
        <input type="radio" value="ai" v-model="mode" />
        <span :class="{ selected: mode==='ai' }">Asistensi AI</span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const username = ref('')
const password = ref('')
const mode = ref('manual')

function onLogin() {
  // login logic here
}

function goRegister() {
  // route to register page
}

function goForgot() {
  // route to forgot password page
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f6f8fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.login-input {
  width: 100%;
  box-sizing: border-box;
  padding: 0.7em 1em;
  font-size: 1rem;
  border: 1px solid #b7b7b7;
  border-radius: 5px;
  margin-bottom: 10px;
  background: #fff;
}

.login-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
}
.logo-img {
  width: 110px;
  margin-bottom: 8px;
}
.logo-text {
  font-size: 2.3rem;
  font-weight: bold;
  letter-spacing: 1px;
  color: #222;
  font-family: 'Montserrat', Arial, Helvetica, sans-serif;
}
.login-card {
  background: #ededed;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(48,52,54,0.04);
  padding: 2rem 2.3rem 1.3rem 2.3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 320px;
  margin-bottom: 18px;
}
.login-card form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 13px;
}
.login-card input[type="text"],
.login-card input[type="password"] {
  width: 100%;
  border: 1px solid #b7b7b7;
  border-radius: 5px;
  padding: 0.7em 1em;
  font-size: 1rem;
}
.login-btn {
  background: #2196f3;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.7em 0;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: filter 0.2s;
}
.login-btn:hover { filter: brightness(0.95); }
.login-links {
  margin-top: 8px;
  font-size: 0.98em;
  color: #222;
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: center;
}
.login-links a {
  color: #1565c0;
  text-decoration: underline;
  cursor: pointer;
  font-weight: bold;
}
.login-mode {
  display: flex;
  justify-content: center;
  gap: 2em;
  margin-top: 10px;
  font-size: 1.2em;
}
.login-mode label {
  display: flex;
  align-items: center;
  gap: 0.4em;
  cursor: pointer;
}
.login-mode input[type="radio"] {
  accent-color: #2196f3;
  width: 22px; height: 22px;
}
.login-mode .selected {
  font-weight: bold;
  color: #222;
}
@media (max-width: 450px) {
  .login-card { min-width: 90vw; padding: 1.1em 0.6em; }
  .logo-img { width: 70px; }
  .logo-text { font-size: 1.3rem; }
}
</style>