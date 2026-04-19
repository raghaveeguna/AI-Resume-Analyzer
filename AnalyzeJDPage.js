import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function AnalyzeJDPage() {
  const [jdText, setJdText] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [extractedKeywords, setExtractedKeywords] = useState([]);

  const handleJdTextChange = (event) => {
    setJdText(event.target.value);
    setMessage('');
    setError('');
    setExtractedKeywords([]);
  };

  const handleAnalyzeJD = async () => {
    if (!jdText.trim()) {
      setError('Please enter job description text.');
      return;
    }

    try {
      // Replace with your actual backend API endpoint
      const response = await axios.post('http://localhost:8000/analyze-job-description/', { jd_text: jdText }, {
        headers: {
          'Content-Type': 'application/json',
          // Add authorization header if your API requires it
          // 'Authorization': `Bearer ${yourAuthToken}`,
        },
      });
      setMessage(response.data.message);
      setExtractedKeywords(response.data.extracted_keywords);
      setError('');
      console.log(response.data);
    } catch (err) {
      setError('Error analyzing job description: ' + (err.response?.data?.detail || err.message));
      setMessage('');
      setExtractedKeywords([]);
    }
  };

  return (
    <div className="container">
      <h2>Analyze Job Description</h2>
      <textarea
        placeholder="Paste job description here..."
        value={jdText}
        onChange={handleJdTextChange}
        rows="10"
        cols="50"
      ></textarea>
      <button onClick={handleAnalyzeJD} className="button">Analyze JD</button>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
      {extractedKeywords.length > 0 && (
        <div>
          <h3>Extracted Keywords:</h3>
          <ul>
            {extractedKeywords.map((keyword, index) => (
              <li key={index}>{keyword.value} ({keyword.type})</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default AnalyzeJDPage;
