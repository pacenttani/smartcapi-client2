<template>
  <div>
    <div class="container interview-page" style="margin-top:16px">
      <div class="form-title">Interview Responden</div>
      <template v-if="mode==='ai'">
        <!-- QnA Chat style, AI mode -->
        <div v-for="(question, idx) in questions" :key="question.key">
          <ChatBubble :msg="{ type:'system', text: (idx+1)+'. '+question.label }" />
          <ChatBubble v-if="answers[question.key]" :msg="{ type:'ai', text: answers[question.key] }" />
          <!-- Recorder untuk pertanyaan aktif -->
          <Recorder
            v-if="currentIdx === idx"
            :disabled="store.wsStatus!=='connected'"
            @audioChunk="chunk => onAudioChunk(chunk, question.key)"
          />
          <div v-if="currentIdx === idx && store.wsStatus!=='connected'" style="color:#e11d48;">
            WebSocket {{ store.wsStatus }}
          </div>
          <div v-if="currentIdx === idx && listening" style="color:#2563eb;">
            Merekam jawaban...
          </div>
          <!-- Next button untuk manual lanjut jika sudah dapat jawaban -->
          <div v-if="answers[question.key] && currentIdx === idx" style="margin:10px 0;">
            <Button type="primary" @click="nextQuestion">Pertanyaan Berikutnya</Button>
          </div>
        </div>
        <div v-if="currentIdx >= questions.length">
          <div style="margin:20px 0;">
            <Button type="success" @click="downloadData">Download Semua Jawaban</Button>
          </div>
        </div>
      </template>
      <template v-else>
        <!-- Manual form mode -->
        <form @submit.prevent="handleSubmit" style="margin-top:12px;">
          <div v-for="q in questions" :key="q.key" class="question-block">
            <label :for="q.key">{{ q.label }}</label>
            <input :id="q.key" v-model="manualForm[q.key]" :placeholder="q.label" :type="q.type||'text'" required />
          </div>
          <div class="actions">
            <Button type="primary" style="margin-top:18px;">SIMPAN JAWABAN</Button>
          </div>
        </form>
        <div class="mic-action-bar">
          <Button type="danger" class="action-btn" @click="handleClear">HAPUS DATA</Button>
          <img src="/icons/mic.svg" alt="Mic Icon" class="mic-icon" />
          <Button type="success" class="action-btn" @click="handleSave">SIMPAN DATA</Button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ChatBubble from '../components/Interview/ChatBubble.vue'
import Recorder from '../components/Interview/Recorder.vue'
import Button from '../components/ui/Button.vue'
import { useInterviewStore } from '../store/interview'
import { useAuthStore } from '../store/auth'

// Daftar pertanyaan sesuai kuesioner
const questions = [
  { key: 'nama', label: 'Nama Lengkap' },
  { key: 'alamat', label: 'Alamat' },
  { key: 'tempat_lahir', label: 'Tempat Lahir' },
  { key: 'tanggal_lahir', label: 'Tanggal Lahir', type: 'date' },
  { key: 'usia', label: 'Usia', type: 'number' },
  { key: 'pendidikan', label: 'Pendidikan' },
  { key: 'pekerjaan', label: 'Pekerjaan' },
  { key: 'hobi', label: 'Hobi' },
  { key: 'nomor_telepon', label: 'Nomor Telepon' },
  { key: 'alamat_email', label: 'Alamat Email', type: 'email' },
]

const store = useInterviewStore()
const auth = useAuthStore()
const mode = computed(() => auth.interviewMode)

// --- AI (asistensi) mode state ---
const currentIdx = ref(0) // index pertanyaan sekarang
const listening = ref(false)
const answers = ref({})

// --- Manual mode state ---
const manualForm = ref(Object.fromEntries(questions.map(q=>[q.key, ""])))

onMounted(() => {
  if (mode.value === 'ai') {
    store.connectWebSocket()
    // Mulai dari pertanyaan pertama
    askCurrentQuestion()
  }
})

// AI mode: mulai rekaman untuk pertanyaan aktif
function askCurrentQuestion() {
  listening.value = true
  // Recorder akan memicu @audioChunk dan diteruskan ke backend via store
}

// Saat audio dikirim untuk pertanyaan tertentu
function onAudioChunk(chunk, qKey) {
  listening.value = false
  // Kirim audio ke backend untuk STT+LLM
  store.sendAudio(chunk, qKey)
  // Tunggu hasil balik, lalu simpan ke answers
  store.onAnswer = (key, val) => {
    answers.value[key] = val
    listening.value = false
  }
}

// Fungsi lanjut ke pertanyaan berikutnya
function nextQuestion() {
  if (currentIdx.value < questions.length - 1) {
    currentIdx.value++
    askCurrentQuestion()
  } else {
    currentIdx.value++
  }
}

// Download jawaban (AI mode)
function downloadData() {
  const blob = new Blob([JSON.stringify(answers.value, null, 2)], {type:"application/json"})
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = "jawaban_responden.json"
  a.click()
  URL.revokeObjectURL(url)
}

// --- Manual mode: handler ---
function handleSubmit() {
  alert('Jawaban berhasil disimpan!')
  // Kirim manualForm.value ke backend/local sesuai kebutuhan
}
function handleSave() {
  alert('Data berhasil disimpan!')
}
function handleClear() {
  if (confirm('Yakin ingin menghapus semua data?')) {
    for (const key in manualForm.value) manualForm.value[key] = ""
  }
}
</script>

<style scoped>
.interview-page {
  max-width: 420px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  position: relative;
  min-height: 100vh;
  box-sizing: border-box;
}

.form-title, h2 {
  text-align: center;
  color: #1155cc;
  margin-bottom: 22px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

label {
  font-weight: bold;
  margin-bottom: 2px;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #eee;
  background: #f5f5f5;
}

.actions {
  text-align: center;
}

/* Mic & Action Bar */
.mic-action-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 32px;
  background: #fff;
  padding: 16px 0 24px 0;
  box-shadow: 0 -2px 8px #0002;
  z-index: 10;
}

.mic-icon {
  width: 54px;
  height: 54px;
  display: block;
  margin: 0 18px;
}

.action-btn {
  min-width: 120px;
}

@media (max-width: 600px) {
  .interview-page {
    max-width: 100vw;
    padding: 12px;
  }
  .mic-action-bar {
    gap: 16px;
    padding: 10px 0 16px 0;
  }
  .mic-icon {
    width: 42px;
    height: 42px;
    margin: 0 8px;
  }
  .action-btn {
    min-width: 90px;
    font-size: 0.95em;
  }
}
</style>