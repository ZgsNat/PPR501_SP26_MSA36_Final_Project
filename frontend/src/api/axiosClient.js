import axios from 'axios';

const axiosClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/xml'
  },
  responseType: 'text', 
});

axiosClient.interceptors.response.use((response) => {
  return response;
}, (error) => {
  console.error("API Error:", error);
  return Promise.reject(error);
});

export default axiosClient;