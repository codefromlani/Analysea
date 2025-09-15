import React from 'react';

const MetricCard = ({ title, value }) => {
  return (
    <div style={{
      backgroundColor: '#f5f5f5',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      textAlign: 'left',
      minWidth: '200px',
      margin: '10px'
    }}>
      <h1 style={{ fontSize: '2.5rem', margin: '0 0 10px 0' }}>{value}</h1>
      <p style={{ margin: '0', color: '#555' }}>{title}</p>
    </div>
  );
};

export default MetricCard;