import axios from 'axios';

const axiosClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',  // We send JSON
    'Accept': 'application/xml'          // We expect XML back
  },
  // Important: We need the raw text to parse XML ourselves
  responseType: 'text', 
});

// Interceptor to handle Blob responses (for Excel download) separately
axiosClient.interceptors.response.use((response) => {
  return response;
}, (error) => {
  console.error("API Error:", error);
  return Promise.reject(error);
});

export default axiosClient;