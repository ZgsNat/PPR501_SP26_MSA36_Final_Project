import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Container, Typography, Box, Button, TextField, Grid, Paper, Dialog, DialogContent, DialogTitle, Chip, IconButton } from '@mui/material';
import { Add, Download, Search, Edit, Delete } from '@mui/icons-material';
import { useStudents } from '../hooks/useStudents';
import { studentService } from '../services/studentService';
import StudentFormMUI from '../components/students/StudentFormMUI';

const StudentDashboard = () => {
  const { students, metadata, loading, queryParams, handleChangeParams, addStudent, updateStudent, removeStudent } = useStudents();
  const [modalOpen, setModalOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);

  const columns = [
    { field: 'student_id', headerName: 'ID', width: 100 },
    { field: 'full_name', headerName: 'Full Name', flex: 1 },
    { field: 'home_town', headerName: 'Hometown', width: 150 },
    { field: 'math_score', headerName: 'Math', type: 'number', width: 90 },
    { field: 'literature_score', headerName: 'Lit', type: 'number', width: 90 },
    { field: 'english_score', headerName: 'Eng', type: 'number', width: 90 },
    { 
      field: 'average_score', 
      headerName: 'Avg', 
      width: 120,
      renderCell: (params) => {
        const val = params.value;
        const color = val >= 8 ? 'success' : val < 5 ? 'error' : 'primary';
        return <Chip label={val} color={color} size="small" variant="outlined" />;
      }
    },
    {
      field: 'actions', headerName: 'Actions', width: 100, sortable: false,
      renderCell: (params) => (
        <Box>
          <IconButton size="small" color="primary" onClick={() => { setEditingStudent(params.row); setModalOpen(true); }}><Edit fontSize="small" /></IconButton>
          <IconButton size="small" color="error" onClick={() => removeStudent(params.row.student_id)}><Delete fontSize="small" /></IconButton>
        </Box>
      )
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" fontWeight="bold">Students</Typography>
        <Box>
          <Button startIcon={<Download />} onClick={() => studentService.exportToExcel()} sx={{ mr: 1 }}>Excel</Button>
          <Button variant="contained" startIcon={<Add />} onClick={() => { setEditingStudent(null); setModalOpen(true); }}>Add</Button>
        </Box>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={4}><TextField fullWidth size="small" label="Search" name="keyword" value={queryParams.keyword} onChange={(e) => handleChangeParams({keyword: e.target.value, page: 1})} /></Grid>
          <Grid item xs={4}><TextField fullWidth size="small" label="Hometown" name="home_town" value={queryParams.home_town} onChange={(e) => handleChangeParams({home_town: e.target.value, page: 1})} /></Grid>
          <Grid item xs={4}><TextField fullWidth size="small" type="number" label="Min Math" name="min_math" value={queryParams.min_math} onChange={(e) => handleChangeParams({min_math: e.target.value, page: 1})} /></Grid>
        </Grid>
      </Paper>

      <Paper sx={{ height: 450 }}>
        <DataGrid
          rows={students}
          columns={columns}
          loading={loading}
          rowCount={metadata.total_records}
          paginationMode="server"
          paginationModel={{ page: metadata.page - 1, pageSize: queryParams.size }}
          onPaginationModelChange={(m) => handleChangeParams({ page: m.page + 1, size: m.pageSize })}
        />
      </Paper>

      <Dialog open={modalOpen} onClose={() => setModalOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>{editingStudent ? "Edit Student" : "New Student"}</DialogTitle>
        <DialogContent>
          <StudentFormMUI initialData={editingStudent} onCancel={() => setModalOpen(false)} onSubmit={(data) => {
            if (editingStudent) updateStudent(editingStudent.student_id, data);
            else addStudent(data);
            setModalOpen(false);
          }} />
        </DialogContent>
      </Dialog>
    </Container>
  );
};
export default StudentDashboard;