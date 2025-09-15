import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia'; // Tambahkan ini!
import Interview from './pages/Interview.vue';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import RegisterVoice from './pages/RegisterVoice.vue';
import Settings from './pages/Settings.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/interview', component: Interview },
  { path: '/settings', component: Settings },
  { path: '/register', component: Register },
  { path: '/register/voice', component: RegisterVoice }
];

const router = createRouter({ history: createWebHistory(), routes });

const app = createApp(App);
app.use(createPinia());   // Inisialisasi Pinia
app.use(router);          // Inisialisasi Router
app.mount('#app');