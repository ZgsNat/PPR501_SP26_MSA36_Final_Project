import React, { useState, useEffect } from 'react';

const initialForm = {
  student_id: '', full_name: '', email: '', phone: '', home_town: '',
  math_score: 0, literature_score: 0, english_score: 0
};

const StudentForm = ({ initialData, onSubmit, onCancel }) => {
  const [form, setForm] = useState(initialForm);
  const isEdit = !!initialData;

  useEffect(() => {
    if (initialData) setForm(initialData);
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <input name="student_id" placeholder="ID" value={form.student_id} onChange={handleChange} disabled={isEdit} required />
      <input name="full_name" placeholder="Full Name" value={form.full_name} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
      <input name="phone" placeholder="Phone" value={form.phone} onChange={handleChange} />
      <input name="home_town" placeholder="Hometown" value={form.home_town} onChange={handleChange} />
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 5 }}>
        <input type="number" step="0.1" name="math_score" placeholder="Math" value={form.math_score} onChange={handleChange} />
        <input type="number" step="0.1" name="literature_score" placeholder="Lit" value={form.literature_score} onChange={handleChange} />
        <input type="number" step="0.1" name="english_score" placeholder="Eng" value={form.english_score} onChange={handleChange} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 10 }}>
        <button type="button" onClick={onCancel}>Cancel</button>
        <button type="submit">{isEdit ? 'Update' : 'Create'}</button>
      </div>
    </form>
  );
};
export default StudentForm;