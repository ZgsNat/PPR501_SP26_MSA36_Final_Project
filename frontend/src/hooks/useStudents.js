import { useState, useEffect, useCallback } from 'react';
import { studentService } from '../services/studentService';

export const useStudents = () => {
  const [students, setStudents] = useState([]);
  const [metadata, setMetadata] = useState({ page: 1, total_pages: 1 });
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ keyword: '', home_town: '', min_math: '' });

  const fetchStudents = useCallback(async (page = 1) => {
    setLoading(true);
    try {
      const result = await studentService.getAll({ page, size: 10, ...filters });
      setStudents(result.items);
      setMetadata(result.metadata);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchStudents(1);
  }, [fetchStudents]);

  const addStudent = async (data) => {
    await studentService.create(data);
    fetchStudents(metadata.page);
  };

  const updateStudent = async (id, data) => {
    await studentService.update(id, data);
    fetchStudents(metadata.page);
  };

  const removeStudent = async (id) => {
    if (window.confirm(`Delete student ${id}?`)) {
      await studentService.delete(id);
      fetchStudents(metadata.page);
    }
  };

  return { 
    students, metadata, loading, filters, setFilters, 
    fetchStudents, addStudent, updateStudent, removeStudent 
  };
};