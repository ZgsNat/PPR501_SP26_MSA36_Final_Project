import React, { useState, useEffect } from 'react';
import { TextField, Button, Grid, Box, Typography, Divider } from '@mui/material';

const initialForm = {
  student_id: '', full_name: '', email: '', phone: '', home_town: '',
  math_score: 0, literature_score: 0, english_score: 0
};

const StudentFormMUI = ({ initialData, onSubmit, onCancel }) => {
  const [form, setForm] = useState(initialForm);
  const isEdit = !!initialData;

  useEffect(() => { if (initialData) setForm(initialData); }, [initialData]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  return (
    <Box component="form" onSubmit={(e) => { e.preventDefault(); onSubmit(form); }}>
      <Typography variant="overline" color="primary" fontWeight="bold">Personal</Typography>
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={6}><TextField fullWidth label="ID" name="student_id" value={form.student_id} onChange={handleChange} disabled={isEdit} size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Name" name="full_name" value={form.full_name} onChange={handleChange} required size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Email" name="email" value={form.email} onChange={handleChange} size="small" /></Grid>
        <Grid item xs={6}><TextField fullWidth label="Hometown" name="home_town" value={form.home_town} onChange={handleChange} size="small" /></Grid>
      </Grid>
      <Divider />
      <Typography variant="overline" color="primary" fontWeight="bold" sx={{ mt: 2, display: 'block' }}>Scores</Typography>
      <Grid container spacing={2}>
        <Grid item xs={4}><TextField fullWidth type="number" label="Math" name="math_score" value={form.math_score} onChange={handleChange} size="small" /></Grid>
        <Grid item xs={4}><TextField fullWidth type="number" label="Lit" name="literature_score" value={form.literature_score} onChange={handleChange} size="small" /></Grid>
        <Grid item xs={4}><TextField fullWidth type="number" label="Eng" name="english_score" value={form.english_score} onChange={handleChange} size="small" /></Grid>
      </Grid>
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
        <Button onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="contained">Save</Button>
      </Box>
    </Box>
  );
};
export default StudentFormMUI;