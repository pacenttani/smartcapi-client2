import { reactive } from 'vue';

const state = reactive({
  transcripts: [],
  audioChunks: [],
  questionnaire: {
    nama: "",
    alamat: "",
    tempat_lahir: "",
    tanggal_lahir: "",
    usia: null,
    pendidikan: "",
    pekerjaan: "",
    hobi: "",
    nomor_telepon: "",
    alamat_email: ""
  }
});

export function useInterviewStore() {
  function addTranscript(transcript) {
    state.transcripts.push(transcript);
  }
  function setQuestionnaire(data) {
    Object.assign(state.questionnaire, data);
  }
  function addAudioChunk(chunk) {
    state.audioChunks.push(chunk);
  }
  function reset() {
    state.transcripts = [];
    state.audioChunks = [];
    state.questionnaire = {
      nama: "",
      alamat: "",
      tempat_lahir: "",
      tanggal_lahir: "",
      usia: null,
      pendidikan: "",
      pekerjaan: "",
      hobi: "",
      nomor_telepon: "",
      alamat_email: ""
    };
  }
  return { ...state, addTranscript, setQuestionnaire, addAudioChunk, reset };
}