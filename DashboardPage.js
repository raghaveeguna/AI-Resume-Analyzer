import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import '../App.css';

function DashboardPage() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    try {
      await logout();
      navigate('/login');
    } catch {
      console.error('Failed to log out');
    }
  }

  return (
    <div className="container">
      <h2>Dashboard</h2>
      {currentUser && <p>Welcome, {currentUser.email}!</p>}
      <div className="button-group">
        <Link to="/upload-resume" className="button">Upload Resume</Link>
        <Link to="/analyze-jd" className="button">Analyze Job Description</Link>
        <Link to="/rank-candidates" className="button">Rank Candidates</Link>
        <button onClick={handleLogout} className="button">Log Out</button>
      </div>
    </div>
  );
}

export default DashboardPage;
