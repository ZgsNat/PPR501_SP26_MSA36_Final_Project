import axiosClient from '../api/axiosClient';
import { parseXmlToJson } from '../utils/xmlParser';

export const studentService = {
  getAll: async (params) => {
    // params: { page, size, keyword, home_town, min_math }
    const response = await axiosClient.get('/students', { params });
    const json = parseXmlToJson(response.data);

    // Handle XML structure safely
    const meta = json?.response?.metadata || { page: 1, total_pages: 1, total_records: 0 };
    const items = json?.response?.items?.student || [];

    return { metadata: meta, items: items };
  },

  create: async (data) => {
    const response = await axiosClient.post('/student', data);
    return parseXmlToJson(response.data);
  },

  update: async (id, data) => {
    const response = await axiosClient.put(`/student/${id}`, data);
    return parseXmlToJson(response.data);
  },

  delete: async (id) => {
    return await axiosClient.delete(`/student/${id}`);
  },

  exportToExcel: async () => {
    const response = await axiosClient.get('/export/excel', {
      responseType: 'blob',
      headers: { 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
    });
    
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'students_list.xlsx');
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
  }
};