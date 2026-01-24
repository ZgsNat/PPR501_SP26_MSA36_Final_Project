import axiosClient from '../api/axiosClient';
import { parseXmlToJson } from '../utils/xmlParser';

export const studentService = {
  getAll: async (params) => {
    const cleanParams = Object.fromEntries(
      Object.entries(params).filter(([_, v]) => v != null && v !== '')
    );

    const response = await axiosClient.get('/students', { params: cleanParams });
    const json = parseXmlToJson(response.data);
    const meta = json?.response?.metadata || { page: 1, total_pages: 1, total_records: 0 };
    
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
    const { student_id, ...updateData } = data;
    const response = await axiosClient.put(`/student/${id}`, updateData);
    return parseXmlToJson(response.data);
  },

  delete: async (id) => {
    return await axiosClient.delete(`/student/${id}`);
  },
};