import axios from 'axios';

const BASE_URL = "http://localhost:8000/api";

// Axios-based API endpoints
export const api = {
  login(data) {
    return axios.post(`${BASE_URL}/login`, data);
  },
  register(data) {
    return axios.post(`${BASE_URL}/register`, data);
  },
  getSettings() {
    return axios.get(`${BASE_URL}/settings`);
  },
  fetchSurveyResults(id) {
    return axios.get(`${BASE_URL}/survey/${id}`);
  },
  // Manual interview data submission (uses Axios for consistency)
  sendManualInterview(data) {
    return axios.post(`${BASE_URL}/interview/manual`, data);
  },
  // Audio submission for AI mode (uses Axios for consistency)
  sendAudioToBackend(blob) {
    const formData = new FormData();
    formData.append('audio', blob);
    return axios.post(`${BASE_URL}/interview/ai-audio`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};

// For legacy fetch usage (if needed elsewhere in the codebase)
export async function sendManualInterviewFetch(data) {
  await fetch(`${BASE_URL}/interview/manual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}

export async function sendAudioToBackendFetch(blob) {
  const formData = new FormData();
  formData.append('audio', blob);
  await fetch(`${BASE_URL}/interview/ai-audio`, {
    method: 'POST',
    body: formData
  });
}