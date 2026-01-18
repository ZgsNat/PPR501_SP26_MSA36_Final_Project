import axiosClient from '../api/axiosClient';
import { parseXmlToJson } from '../utils/xmlParser';

export const studentService = {
  getAll: async (params) => {
    // --- FIX START ---
    // Remove keys that are null, undefined, or empty strings ("")
    // This prevents sending "min_math=''" which crashes FastAPI
    const cleanParams = Object.fromEntries(
      Object.entries(params).filter(([_, v]) => v != null && v !== '')
    );
    // --- FIX END ---

    const response = await axiosClient.get('/students', { params: cleanParams });
    const json = parseXmlToJson(response.data);

    // Handle XML structure safely
    // Note: If only 1 student exists, XML parsers sometimes return an object instead of an array.
    // However, your xmlParser.js 'isArray' setting should fix this.
    const meta = json?.response?.metadata || { page: 1, total_pages: 1, total_records: 0 };
    
    // Safety check: ensure items is always an array
    let items = json?.response?.items?.student || [];
    if (!Array.isArray(items)) {
        items = [items];
    }

    return { metadata: meta, items: items };
  },

  create: async (data) => {
    const response = await axiosClient.post('/student', data);
    return parseXmlToJson(response.data);
  },

  update: async (id, data) => {
    // Remove student_id from the body to avoid backend conflicts if it's strict
    const { student_id, ...updateData } = data;
    const response = await axiosClient.put(`/student/${id}`, updateData);
    return parseXmlToJson(response.data);
  },

  delete: async (id) => {
    return await axiosClient.delete(`/student/${id}`);
  },

  // exportToExcel: async () => {
  //   const response = await axiosClient.get('/export/excel', {
  //     responseType: 'blob',
  //     headers: { 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
  //   });
    
  //   const url = window.URL.createObjectURL(new Blob([response.data]));
  //   const link = document.createElement('a');
  //   link.href = url;
  //   link.setAttribute('download', 'students_list.xlsx');
  //   document.body.appendChild(link);
  //   link.click();
  //   link.parentNode.removeChild(link);
  // }
};