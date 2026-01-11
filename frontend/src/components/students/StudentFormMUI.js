import React, { useState, useEffect } from 'react';
import { TextField, Button, Grid, Box, Typography, Divider } from '@mui/material';

// Giá trị mặc định là chuỗi rỗng '' để tránh lỗi Uncontrolled Input
const initialForm = {
  student_id: '', full_name: '', email: '', phone: '', home_town: '', birth_date: '',
  math_score: '', literature_score: '', english_score: ''
};

const StudentFormMUI = ({ initialData, onSubmit, onCancel }) => {
  const [form, setForm] = useState(initialForm);
  const isEdit = !!initialData;

  useEffect(() => { 
      if (initialData) {
          // QUAN TRỌNG: Chuyển đổi null/undefined thành ''
          const cleanData = {};
          Object.keys(initialForm).forEach(key => {
              cleanData[key] = (initialData[key] !== null && initialData[key] !== undefined) ? initialData[key] : '';
          });
          setForm(cleanData); 
      }
  }, [initialData]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  return (
    <Box component="form" onSubmit={(e) => { e.preventDefault(); onSubmit(form); }} sx={{ mt: 1 }}>
      <Typography variant="overline" color="primary" fontWeight="bold">Personal Info</Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={6}><TextField fullWidth label="ID" name="student_id" value={form.student_id} onChange={handleChange} disabled={isEdit} size="small" required /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Full Name" name="full_name" value={form.full_name} onChange={handleChange} required size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Birth Date" name="birth_date" value={form.birth_date} onChange={handleChange} size="small" placeholder="dd/mm/yyyy" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Phone" name="phone" value={form.phone} onChange={handleChange} size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Email" name="email" value={form.email} onChange={handleChange} size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Hometown" name="home_town" value={form.home_town} onChange={handleChange} size="small" /></Grid>
      </Grid>
      
      <Divider />
      <Typography variant="overline" color="primary" fontWeight="bold" sx={{ mt: 2, display: 'block' }}>Academic Scores</Typography>
      <Grid container spacing={2}>
        <Grid item xs={4}><TextField fullWidth type="number" label="Math" name="math_score" value={form.math_score} onChange={handleChange} size="small" inputProps={{ step: "0.01" }} /></Grid>
        <Grid item xs={4}><TextField fullWidth type="number" label="Literature" name="literature_score" value={form.literature_score} onChange={handleChange} size="small" inputProps={{ step: "0.01" }} /></Grid>
        <Grid item xs={4}><TextField fullWidth type="number" label="English" name="english_score" value={form.english_score} onChange={handleChange} size="small" inputProps={{ step: "0.01" }} /></Grid>
      </Grid>
      
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
        <Button onClick={onCancel} color="inherit">Cancel</Button>
        <Button type="submit" variant="contained">Save Changes</Button>
      </Box>
    </Box>
  );
};
export default StudentFormMUI;