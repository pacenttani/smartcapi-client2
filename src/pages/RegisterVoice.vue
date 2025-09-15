<template>
  <div class="container" style="margin-top:16px;">
    <div class="form-title" style="font-size:1.7rem;">Perekaman Suara</div>
    <div style="text-align:center; color:#2563eb; font-weight:600; margin-bottom:10px;">
      Klik Tombol Rekam, lalu bacalah tulisan<br>di bawah ini dengan suara yang jelas
    </div>
    <div style="margin-bottom:10px; font-weight:600;">[Ucapan Salam]</div>
    <div class="voice-text">
      <p>
        Nama saya <b>{{ biodata.nama || '[Nama Anda]' }}</b>. Saya berasal dari <b>{{ biodata.kota_asal || '[kota asal]' }}</b>
        dan saat ini berusia <b>{{ biodata.usia || '[usia Anda]' }}</b> tahun.
        Saya adalah seorang <b>{{ biodata.jenis_kelamin || '[jenis kelamin Anda]' }}</b>, dan saya tinggal di
        <b>{{ biodata.alamat || '[alamat lengkap Anda]' }}</b>.
      </p>
      <p>
        Saya menyelesaikan pendidikan terakhir saya di <b>{{ biodata.institusi_pendidikan || '[nama institusi pendidikan]' }}</b>,
        dengan gelar <b>{{ biodata.gelar_akademik || '[gelar akademik]' }}</b>. Pendidikan ini telah memberikan saya pengetahuan dan keterampilan
        yang sangat berguna dalam berbagai aspek kehidupan.
      </p>
      <p>
        Saat ini, saya bekerja sebagai <b>{{ biodata.posisi_pekerjaan || '[posisi pekerjaan Anda]' }}</b> di
        <b>{{ biodata.perusahaan || '[nama perusahaan/organisasi tempat Anda bekerja]' }}</b>.
        Dalam pekerjaan saya, saya bertanggung jawab atas <b>{{ biodata.deskripsi_tugas || '[deskripsi tugas utama Anda]' }}</b>.
        Pengalaman kerja ini telah mengajarkan saya banyak hal tentang profesionalisme, kerjasama tim, dan tanggung jawab.
      </p>
      <p>
        Saya sudah menikah dan memiliki <b>{{ biodata.status_keluarga || '[sebutkan jika memiliki anak atau tidak, dan berapa jumlahnya jika ada]' }}</b>.
        Keluarga saya sangat mendukung segala aktivitas dan aspirasi saya, termasuk keinginan saya untuk menjadi petugas pendata di BPS.
      </p>
      <p>
        Alasan utama saya ingin menjadi petugas pendata BPS adalah karena saya percaya bahwa data yang akurat dan terpercaya
        sangat penting untuk pembangunan negara. Sebagai petugas pendata, saya akan memiliki kesempatan untuk berkontribusi
        langsung dalam pengumpulan data yang nantinya akan digunakan untuk merumuskan kebijakan-kebijakan penting.
      </p>
      <p>
        Saya juga ingin terlibat lebih dalam dengan masyarakat dan membantu memastikan bahwa suara mereka terwakili
        dalam data yang dikumpulkan. Dengan bekerja sebagai petugas pendata, saya berharap bisa membangun hubungan positif
        dengan komunitas saya dan bisa menjadi inspirasi di sekitar saya.
      </p>
      <p>
        Terima kasih atas kesempatan untuk memperkenalkan diri. Saya sangat berharap dapat berkontribusi sebagai petugas
        pendata BPS dan bekerja sama dengan tim yang berdedikasi untuk menciptakan data yang akurat dan bermanfaat.
      </p>
      <p>
        Salam hormat,<br>
        <b>{{ biodata.nama || '[Nama Anda]' }}</b>
      </p>
    </div>
    <!-- Recorder Section -->
    <div class="voice-recorder-wrap">
      <Recorder :disabled="recording" :recording="recording" @start="startRecording" @stop="stopRecording" @audioChunk="handleAudioChunk"/>
      <div v-if="recording" style="color:#2563eb; margin-top:8px;">Merekam suara...</div>
      <div v-if="audioURL" style="margin-top:8px;">
        <audio :src="audioURL" controls style="width:100%;"></audio>
      </div>
    </div>
    <div class="form-footer" style="margin-top:22px;">
      <button type="button" @click="onBack">BACK</button>
      <button type="button" @click="onSubmit" :disabled="!audioBlob || loading">
        <span v-if="loading">Menyimpan...</span>
        <span v-else>SUBMIT</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Recorder from '../components/Interview/Recorder.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useRegisterStore } from '../store/register'

const router = useRouter()
const auth = useAuthStore()
// Ambil biodata dari register store (atau dari localStorage jika reload)
const registerStore = useRegisterStore()
const biodata = computed(() => registerStore.biodata || {})

const recording = ref(false)
const audioBlob = ref(null)
const audioURL = ref("")
const loading = ref(false)

function startRecording() {
  recording.value = true
}
function stopRecording() {
  recording.value = false
}

function handleAudioChunk(blob) {
  audioBlob.value = blob
  audioURL.value = URL.createObjectURL(blob)
  recording.value = false
}

function onBack() {
  router.back()
}

async function onSubmit() {
  if (!audioBlob.value) return
  loading.value = true
  // Kirim audio ke backend sebagai variabel "id_voice"
  const formData = new FormData()
  formData.append('voice', audioBlob.value, 'voice.webm')
  // Anda bisa menambahkan data lain dari register jika perlu:
  formData.append('user_id', auth.user?.id || '')
  // contoh: formData.append('nama', biodata.value.nama || '')

  try {
    // Ganti URL berikut dengan endpoint backend yang sesuai
    const resp = await fetch('/api/auth/enroll-voice', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${auth.token}` },
      body: formData
    })
    if (!resp.ok) throw new Error('Gagal simpan suara')
    alert('Perekaman suara berhasil disimpan!')
    router.push('/interview')
  } catch (e) {
    alert('Gagal menyimpan suara. Coba lagi!')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.voice-text {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 1em;
  margin-bottom: 16px;
  max-height: 330px;
  overflow-y: auto;
  border: 1.5px solid #e1eaf4;
}
.voice-recorder-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
}
.form-footer {
  display: flex;
  justify-content: space-between;
}
button {
  min-width: 120px;
  padding: 10px 0;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.05em;
  background: #2563eb;
  color: white;
  border: none;
  cursor: pointer;
  transition: background .2s;
}
button:active { background: #1e40af; }
button[disabled] { background: #b9c6e6; cursor: not-allowed; }
</style>