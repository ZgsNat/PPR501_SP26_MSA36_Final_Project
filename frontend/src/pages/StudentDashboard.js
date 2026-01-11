import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { 
  Container, Typography, Box, Button, TextField, Grid, Paper, 
  Dialog, DialogContent, DialogTitle, Chip, IconButton, Tooltip,
  Snackbar, Alert 
} from '@mui/material';
import { 
  Add, Download, Edit, Delete, WarningAmber 
} from '@mui/icons-material';

// --- IMPORT ĐÚNG ĐƯỜNG DẪN ---
import { useStudents } from '../hooks/useStudents'; 
import { studentService } from '../services/studentService';
import StudentFormMUI from '../components/students/StudentFormMUI';
// -----------------------------

const StudentDashboard = () => {
  // Lấy data và logic từ Hook (bao gồm cả notification state mới thêm)
  const { 
    students, metadata, loading, queryParams, handleChangeParams, 
    addStudent, updateStudent, removeStudent, 
    notification, handleCloseNotification 
  } = useStudents();

  const [modalOpen, setModalOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);

  // --- HELPER: Hiển thị điểm số (xử lý màu sắc + cảnh báo data bẩn) ---
  const renderScore = (params) => {
    const val = params.value;
    if (val === null || val === undefined) return <span style={{color: '#ccc'}}>N/A</span>;
    const num = parseFloat(val);
    
    // Nếu điểm < 0 hoặc > 10 -> Data bẩn -> Hiện cảnh báo đỏ
    if (num < 0 || num > 10) {
        return <Chip label={val} color="error" size="small" variant="filled" icon={<WarningAmber />} />;
    }
    return val;
  };

  // --- CẤU HÌNH CỘT (Đã tối ưu độ rộng) ---
  const columns = [
    { field: 'student_id', headerName: 'ID', width: 90 },
    
    // Dùng flex: 1 để tên tự giãn ra lấp khoảng trống
    { field: 'full_name', headerName: 'Full Name', minWidth: 150, flex: 1 },
    
    { field: 'birth_date', headerName: 'Birthday', width: 100, 
      renderCell: (params) => params.value || <span style={{fontStyle:'italic', color:'#999'}}>Unknown</span> 
    },
    { field: 'phone', headerName: 'Phone', width: 110,
      renderCell: (params) => params.value || <span style={{fontStyle:'italic', color:'#999'}}>—</span>
    },
    
    // Email dài nên cho flex lớn hơn chút
    { field: 'email', headerName: 'Email', minWidth: 180, flex: 1.5, 
       renderCell: (params) => params.value ? <Tooltip title={params.value}><div style={{overflow:'hidden', textOverflow:'ellipsis'}}>{params.value}</div></Tooltip> : "—"
    },
    
    { field: 'home_town', headerName: 'Hometown', width: 120 },
    
    // Các cột điểm chỉ cần hẹp
    { field: 'math_score', headerName: 'Math', width: 70, renderCell: renderScore },
    { field: 'literature_score', headerName: 'Lit', width: 70, renderCell: renderScore },
    { field: 'english_score', headerName: 'Eng', width: 70, renderCell: renderScore },
    
    { 
      field: 'average_score', 
      headerName: 'Avg', 
      width: 80,
      renderCell: (params) => {
        const val = params.value;
        if (val === null) return <Chip label="Err" size="small" />;
        // Logic màu sắc: > 10 hoặc < 0 là lỗi (đen), còn lại theo thang điểm
        if (val < 0 || val > 10) return <Chip label={val} sx={{bgcolor: '#333', color: 'white'}} size="small" />;
        const color = val >= 8 ? 'success' : val < 5 ? 'error' : 'primary';
        return <Chip label={val} color={color} size="small" variant="outlined" />;
      }
    },
    {
      field: 'actions', headerName: 'Act', width: 80, sortable: false,
      renderCell: (params) => (
        <Box>
          <IconButton size="small" color="primary" onClick={() => { setEditingStudent(params.row); setModalOpen(true); }}><Edit fontSize="small" /></IconButton>
          <IconButton size="small" color="error" onClick={() => removeStudent(params.row.student_id)}><Delete fontSize="small" /></IconButton>
        </Box>
      )
    }
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* HEADER */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" fontWeight="bold">Student Management</Typography>
        <Box>
          <Button variant="contained" startIcon={<Add />} onClick={() => { setEditingStudent(null); setModalOpen(true); }}>Add</Button>
        </Box>
      </Box>

      {/* FILTER SEARCH */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField fullWidth size="small" label="Search Keyword" value={queryParams.keyword} 
              onChange={(e) => handleChangeParams({keyword: e.target.value, page: 1})} 
            />
          </Grid>
          <Grid item xs={6} md={4}>
            <TextField fullWidth size="small" label="Hometown Filter" value={queryParams.home_town} 
              onChange={(e) => handleChangeParams({home_town: e.target.value, page: 1})} 
            />
          </Grid>
          <Grid item xs={6} md={4}>
            <TextField fullWidth size="small" type="number" label="Min Math Score" value={queryParams.min_math} 
              onChange={(e) => handleChangeParams({min_math: e.target.value, page: 1})} 
            />
          </Grid>
        </Grid>
      </Paper>

      {/* DATA GRID TABLE */}
      <Paper sx={{ width: '100%' }}>
        <DataGrid
          rows={students}
          columns={columns}
          loading={loading}
          autoHeight // Tự động co giãn chiều cao theo số lượng dòng
          density="comfortable"
          
          // Pagination Server-side
          rowCount={metadata.total_records}
          paginationMode="server"
          paginationModel={{ page: metadata.page - 1, pageSize: queryParams.size }}
          onPaginationModelChange={(m) => handleChangeParams({ page: m.page + 1, size: m.pageSize })}
          pageSizeOptions={[5, 10, 20, 100]}

          // Style Header
          sx={{
            '& .MuiDataGrid-columnHeaders': {
                backgroundColor: '#f5f5f5',
                fontWeight: 'bold',
            },
          }}
        />
      </Paper>

      {/* MODAL FORM (ADD/EDIT) */}
      <Dialog open={modalOpen} onClose={() => setModalOpen(false)} fullWidth maxWidth="md">
        <DialogTitle>{editingStudent ? "Edit Student" : "New Student"}</DialogTitle>
        <DialogContent>
          <StudentFormMUI 
            initialData={editingStudent} 
            onCancel={() => setModalOpen(false)} 
            onSubmit={(data) => {
              if (editingStudent) updateStudent(editingStudent.student_id, data);
              else addStudent(data);
              setModalOpen(false);
            }} 
          />
        </DialogContent>
      </Dialog>

      {/* NOTIFICATION SNACKBAR (Thay thế alert/crash) */}
      <Snackbar 
        open={notification.open} 
        autoHideDuration={6000} 
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert onClose={handleCloseNotification} severity={notification.severity} sx={{ width: '100%' }} variant="filled">
          {notification.message}
        </Alert>
      </Snackbar>

    </Container>
  );
};

export default StudentDashboard;