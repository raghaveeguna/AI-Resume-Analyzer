import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function UploadResumePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage('');
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Replace with your actual backend API endpoint
      const response = await axios.post('http://localhost:8000/upload-resume/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          // Add authorization header if your API requires it
          // 'Authorization': `Bearer ${yourAuthToken}`,
        },
      });
      setMessage(response.data.message);
      setError('');
      console.log(response.data);
    } catch (err) {
      setError('Error uploading resume: ' + (err.response?.data?.detail || err.message));
      setMessage('');
    }
  };

  return (
    <div className="container">
      <h2>Upload Resume</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} className="button">Upload</button>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default UploadResumePage;
