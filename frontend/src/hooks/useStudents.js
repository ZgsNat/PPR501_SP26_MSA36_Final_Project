import { useState, useEffect, useCallback } from 'react';
import { studentService } from '../services/studentService';

export const useStudents = () => {
  const [students, setStudents] = useState([]);
  const [metadata, setMetadata] = useState({ page: 1, total_pages: 1, total_records: 0 });
  const [loading, setLoading] = useState(false);
  const [queryParams, setQueryParams] = useState({ page: 1, size: 5, keyword: '', home_town: '', min_math: '' });

  // --- 1. THÊM STATE ĐỂ QUẢN LÝ THÔNG BÁO (SUCCESS/ERROR) ---
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' }); // severity: success | error | warning

  // --- 2. HÀM HELPER: Bóc tách lỗi từ XML Backend ---
  const handleError = (error) => {
    let message = "An unknown error occurred";
    
    if (error.response) {
      // Backend trả về XML, ta cần parse nó ra
      const data = error.response.data; 
      
      // Nếu data là string (XML), ta dùng DOMParser để lấy thẻ <detail>
      if (typeof data === 'string') {
        try {
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(data, "text/xml");
          const detail = xmlDoc.getElementsByTagName("detail")[0]?.textContent;
          const errorName = xmlDoc.getElementsByTagName("error")[0]?.textContent;
          
          if (detail) {
            message = `${errorName || 'Error'}: ${detail}`;
          }
        } catch (e) {
          console.error("XML Parse Error", e);
        }
      } 
      // Fallback nếu không parse được XML nhưng có status text
      else {
        message = `Error ${error.response.status}: ${error.response.statusText}`;
      }
    } else if (error.message) {
      message = error.message;
    }

    // Set thông báo lỗi để hiện lên màn hình
    setNotification({ open: true, message: message, severity: 'error' });
  };

  const handleCloseNotification = () => setNotification({ ...notification, open: false });

  // --- 3. CẬP NHẬT CÁC HÀM GỌI API ---

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    try {
      const result = await studentService.getAll(queryParams);
      // ... (giữ nguyên logic xử lý data bẩn ở đây như bài trước) ...
      const enhancedItems = result.items.map(s => {
          const m = parseFloat(s.math_score);
          const l = parseFloat(s.literature_score);
          const e = parseFloat(s.english_score);
          let avg = null;
          if (!isNaN(m) && !isNaN(l) && !isNaN(e)) {
            avg = parseFloat(((m + l + e) / 3).toFixed(2));
          }
          return { ...s, id: s.student_id, average_score: avg };
      });
      setStudents(enhancedItems);
      setMetadata(result.metadata);
    } catch (error) {
      handleError(error); // <--- Bắt lỗi tại đây
    } finally {
      setLoading(false);
    }
  }, [queryParams]);

  useEffect(() => { fetchStudents(); }, [fetchStudents]);

  const handleChangeParams = (newParams) => setQueryParams(p => ({ ...p, ...newParams }));

  const addStudent = async (d) => { 
    try {
      await studentService.create(d); 
      setNotification({ open: true, message: 'Create success!', severity: 'success' }); // Thông báo xanh
      fetchStudents(); 
    } catch (e) { handleError(e); } // Thông báo đỏ
  };

  const updateStudent = async (id, d) => { 
    try {
      await studentService.update(id, d); 
      setNotification({ open: true, message: 'Update success!', severity: 'success' });
      fetchStudents(); 
    } catch (e) { handleError(e); }
  };

  const removeStudent = async (id) => { 
    if (window.confirm("Delete?")) { 
      try {
        await studentService.delete(id); 
        setNotification({ open: true, message: 'Delete success!', severity: 'success' });
        fetchStudents(); 
      } catch (e) { handleError(e); }
    } 
  };

  return { 
    students, metadata, loading, queryParams, handleChangeParams,
    addStudent, updateStudent, removeStudent,
    // Export thêm notification cho Dashboard dùng
    notification, handleCloseNotification 
  };
};