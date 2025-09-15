import { defineStore } from 'pinia'

export const useRegisterStore = defineStore('register', {
  state: () => ({
    // Biodata akan diisi saat user registrasi sebelum ke halaman perekaman suara
    biodata: {
      nama: "",
      kota_asal: "",
      usia: "",
      jenis_kelamin: "",
      alamat: "",
      institusi_pendidikan: "",
      gelar_akademik: "",
      posisi_pekerjaan: "",
      perusahaan: "",
      deskripsi_tugas: "",
      status_keluarga: ""
    }
  }),
  actions: {
    setBiodata(data) {
      this.biodata = { ...this.biodata, ...data }
      // Simpan ke localStorage agar persist antar halaman
      localStorage.setItem('biodata', JSON.stringify(this.biodata))
    },
    loadBiodata() {
      const data = localStorage.getItem('biodata')
      if (data) {
        this.biodata = JSON.parse(data)
      }
    },
    clearBiodata() {
      this.biodata = {
        nama: "",
        kota_asal: "",
        usia: "",
        jenis_kelamin: "",
        alamat: "",
        institusi_pendidikan: "",
        gelar_akademik: "",
        posisi_pekerjaan: "",
        perusahaan: "",
        deskripsi_tugas: "",
        status_keluarga: ""
      }
      localStorage.removeItem('biodata')
    }
  }
})