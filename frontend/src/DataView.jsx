import React from 'react';

const DataView = ({ encroachmentData }) => {
  return (
    <div style={{ margin: '20px', textAlign: 'left' }}>
      <h2>Detected Encroachments</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f2f2f2' }}>
            <th style={tableHeaderStyle}>Type</th>
            <th style={tableHeaderStyle}>Location</th>
            <th style={tableHeaderStyle}>Affected Area (sq m)</th>
            <th style={tableHeaderStyle}>Nearest Boundary</th>
          </tr>
        </thead>
        <tbody>
          {encroachmentData.map((enc, index) => (
            <tr key={index}>
              <td style={tableCellStyle}>{enc.type}</td>
              <td style={tableCellStyle}>{enc.location}</td>
              <td style={tableCellStyle}>{enc.affected_area_sq_m.toFixed(4)}</td>
              <td style={tableCellStyle}>{enc.nearest_boundary_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const tableHeaderStyle = {
  padding: '12px',
  textAlign: 'left',
  borderBottom: '1px solid #ddd',
};

const tableCellStyle = {
  padding: '12px',
  borderBottom: '1px solid #ddd',
};

export default DataView;