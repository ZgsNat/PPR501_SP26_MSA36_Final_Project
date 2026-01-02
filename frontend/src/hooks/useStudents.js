import { useState, useEffect, useCallback } from 'react';
import { studentService } from '../services/studentService';

export const useStudents = () => {
  const [students, setStudents] = useState([]);
  const [metadata, setMetadata] = useState({ page: 1, total_pages: 1, total_records: 0 });
  const [loading, setLoading] = useState(false);
  const [queryParams, setQueryParams] = useState({ page: 1, size: 5, keyword: '', home_town: '', min_math: '' });

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    try {
      const result = await studentService.getAll(queryParams);
      
      const enhancedItems = result.items.map(s => {
          const avg = (s.math_score + s.literature_score + s.english_score) / 3;
          return {
            ...s,
            id: s.student_id, // Required for MUI DataGrid
            average_score: parseFloat(avg.toFixed(1))
          };
      });

      setStudents(enhancedItems);
      setMetadata(result.metadata);
    } catch (error) {
      console.error("Fetch Error:", error);
    } finally {
      setLoading(false);
    }
  }, [queryParams]);

  useEffect(() => { fetchStudents(); }, [fetchStudents]);

  const handleChangeParams = (newParams) => setQueryParams(p => ({ ...p, ...newParams }));

  return { 
    students, metadata, loading, queryParams, handleChangeParams,
    addStudent: async (d) => { await studentService.create(d); fetchStudents(); },
    updateStudent: async (id, d) => { await studentService.update(id, d); fetchStudents(); },
    removeStudent: async (id) => { if (window.confirm("Delete?")) { await studentService.delete(id); fetchStudents(); } }
  };
};