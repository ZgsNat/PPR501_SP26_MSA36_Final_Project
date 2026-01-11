import React from 'react';

const StudentTable = ({ data, onEdit, onDelete }) => (
  <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: 'white', minWidth: 800 }}>
        <thead>
          <tr style={{ background: '#f0f0f0', textAlign: 'left', borderBottom: '2px solid #ddd' }}>
            <th style={{ padding: 10 }}>ID</th>
            <th style={{ padding: 10 }}>Name</th>
            <th style={{ padding: 10 }}>Birth Date</th>
            <th style={{ padding: 10 }}>Phone</th>
            <th style={{ padding: 10 }}>Hometown</th>
            <th style={{ padding: 10 }}>Scores (M-L-E)</th>
            <th style={{ padding: 10 }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map(sv => (
            <tr key={sv.student_id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 10 }}>{sv.student_id}</td>
              <td style={{ padding: 10 }}>{sv.full_name}</td>
              <td style={{ padding: 10 }}>{sv.birth_date || '—'}</td>
              <td style={{ padding: 10 }}>{sv.phone || '—'}</td>
              <td style={{ padding: 10 }}>{sv.home_town || '—'}</td>
              <td style={{ padding: 10 }}>
                {/* Hiển thị điểm dạng thô để thấy độ bẩn */}
                {sv.math_score ?? 'N/A'} - {sv.literature_score ?? 'N/A'} - {sv.english_score ?? 'N/A'}
              </td>
              <td style={{ padding: 10 }}>
                <button onClick={() => onEdit(sv)} style={{ marginRight: 5, cursor: 'pointer' }}>Edit</button>
                <button onClick={() => onDelete(sv.student_id)} style={{ color: 'red', cursor: 'pointer' }}>Del</button>
              </td>
            </tr>
          ))}
          {data.length === 0 && (
              <tr><td colSpan="7" style={{textAlign:'center', padding: 20}}>No dirty data found</td></tr>
          )}
        </tbody>
      </table>
  </div>
);
export default StudentTable;