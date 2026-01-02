import React from 'react';

const StudentTable = ({ data, onEdit, onDelete }) => (
  <table style={{ width: '100%', borderCollapse: 'collapse', background: 'white' }}>
    <thead>
      <tr style={{ background: '#f0f0f0', textAlign: 'left' }}>
        <th style={{ padding: 10 }}>ID</th>
        <th style={{ padding: 10 }}>Name</th>
        <th style={{ padding: 10 }}>Email</th>
        <th style={{ padding: 10 }}>Hometown</th>
        <th style={{ padding: 10 }}>Math</th>
        <th style={{ padding: 10 }}>Actions</th>
      </tr>
    </thead>
    <tbody>
      {data.map(sv => (
        <tr key={sv.student_id} style={{ borderBottom: '1px solid #eee' }}>
          <td style={{ padding: 10 }}>{sv.student_id}</td>
          <td style={{ padding: 10 }}>{sv.full_name}</td>
          <td style={{ padding: 10 }}>{sv.email}</td>
          <td style={{ padding: 10 }}>{sv.home_town}</td>
          <td style={{ padding: 10 }}>{sv.math_score}</td>
          <td style={{ padding: 10 }}>
            <button onClick={() => onEdit(sv)} style={{ marginRight: 5 }}>Edit</button>
            <button onClick={() => onDelete(sv.student_id)}>Del</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);
export default StudentTable;