import React, { useState } from 'react';

const UploadForm = ({ token, onTaskQueued }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/analyze_image/', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      onTaskQueued(data.task_id);

    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} required />
      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : 'Analyze Image'}
      </button>
    </form>
  );
};

export default UploadForm;