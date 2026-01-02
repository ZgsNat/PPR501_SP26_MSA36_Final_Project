import React, { useState } from 'react';
import { useStudents } from '../hooks/useStudents';
import { studentService } from '../services/studentService';
// Import components from the correct paths shown in your image
import StudentTable from '../components/students/StudentTable';
import StudentFilter from '../components/students/StudentFilter';
import StudentForm from '../components/students/StudentForm';
import Pagination from '../components/common/Pagination';
import Modal from '../components/common/Modal';

const StudentDashboard = () => {
  const { students, metadata, loading, filters, setFilters, fetchStudents, addStudent, updateStudent, removeStudent } = useStudents();
  const [modalOpen, setModalOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);

  const handleEdit = (student) => {
    setEditingStudent(student);
    setModalOpen(true);
  };

  const handleAdd = () => {
    setEditingStudent(null);
    setModalOpen(true);
  };

  const handleSubmit = async (data) => {
    if (editingStudent) await updateStudent(editingStudent.student_id, data);
    else await addStudent(data);
    setModalOpen(false);
  };

  return (
    <div style={{ padding: 20, maxWidth: 1000, margin: '0 auto' }}>
      <h1>Student Management</h1>
      <div style={{ marginBottom: 15 }}>
        <button onClick={handleAdd}>+ Add Student</button>
        <button onClick={() => studentService.exportToExcel()} style={{ marginLeft: 10 }}>Export Excel</button>
      </div>

      <StudentFilter filters={filters} setFilters={setFilters} />

      {loading ? <p>Loading...</p> : (
        <>
          <StudentTable data={students} onEdit={handleEdit} onDelete={removeStudent} />
          <Pagination currentPage={metadata.page} totalPages={metadata.total_pages} onPageChange={fetchStudents} />
        </>
      )}

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editingStudent ? "Edit Student" : "Add Student"}>
        <StudentForm initialData={editingStudent} onSubmit={handleSubmit} onCancel={() => setModalOpen(false)} />
      </Modal>
    </div>
  );
};
export default StudentDashboard;