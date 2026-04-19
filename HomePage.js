import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

function HomePage() {
  return (
    <div className="container">
      <h1>Welcome to AI Resume Analyzer</h1>
      <p>Your intelligent solution for resume parsing, keyword extraction, and candidate ranking.</p>
      <div className="button-group">
        <Link to="/login" className="button">Login</Link>
        <Link to="/register" className="button">Register</Link>
        <Link to="/dashboard" className="button">Dashboard</Link>
      </div>
    </div>
  );
}

export default HomePage;
