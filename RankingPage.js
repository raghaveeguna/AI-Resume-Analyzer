import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';

function RankingPage() {
  const [rankedCandidates, setRankedCandidates] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchRankedCandidates();
  }, []);

  const fetchRankedCandidates = async () => {
    setLoading(true);
    try {
      // Replace with your actual backend API endpoint
      const response = await axios.get('http://localhost:8000/candidates/rank/', {
        headers: {
          // Add authorization header if your API requires it
          // 'Authorization': `Bearer ${yourAuthToken}`,
        },
      });
      setRankedCandidates(response.data.ranked_candidates);
      setMessage(response.data.message);
      setError('');
      console.log(response.data);
    } catch (err) {
      setError('Error fetching ranked candidates: ' + (err.response?.data?.detail || err.message));
      setMessage('');
      setRankedCandidates([]);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Candidate Ranking</h2>
      <button onClick={fetchRankedCandidates} className="button" disabled={loading}>Refresh Ranking</button>
      {loading && <p>Loading rankings...</p>}
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}

      {rankedCandidates.length > 0 ? (
        <div className="ranking-list">
          <h3>Ranked Candidates:</h3>
          <ul>
            {rankedCandidates.map((candidate, index) => (
              <li key={candidate.resume_id}>
                <strong>{index + 1}. {candidate.filename}</strong> - Score: {candidate.score.toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      ) : (
        !loading && !error && <p>No candidates ranked yet. Upload resumes and analyze job descriptions first.</p>
      )}
    </div>
  );
}

export default RankingPage;
