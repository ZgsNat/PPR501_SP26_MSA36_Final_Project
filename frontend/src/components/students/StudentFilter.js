import React from 'react';

const StudentFilter = ({ filters, setFilters }) => {
  const handleChange = (e) => setFilters(prev => ({ ...prev, [e.target.name]: e.target.value }));
  return (
    <div style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
      <input name="keyword" placeholder="Search..." value={filters.keyword} onChange={handleChange} style={{ padding: 8 }} />
      <input name="home_town" placeholder="Hometown" value={filters.home_town} onChange={handleChange} style={{ padding: 8 }} />
      <input name="min_math" type="number" placeholder="Min Math" value={filters.min_math} onChange={handleChange} style={{ padding: 8 }} />
    </div>
  );
};
export default StudentFilter;