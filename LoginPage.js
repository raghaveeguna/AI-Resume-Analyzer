import React, { useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import '../App.css';

function LoginPage() {
  const emailRef = useRef();
  const passwordRef = useRef();
  const { login } = useAuth();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      setError('');
      setLoading(true);
      await login(emailRef.current.value, passwordRef.current.value);
      navigate('/dashboard');
    } catch (err) {
      setError('Failed to log in: ' + err.message);
    }
    setLoading(false);
  }

  return (
    <div className="container">
      <h2>Log In</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Email</label>
          <input type="email" ref={emailRef} required />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" ref={passwordRef} required />
        </div>
        <button disabled={loading} type="submit" className="button">Log In</button>
      </form>
      <div className="text-center">
        Need an account? <Link to="/register">Sign Up</Link>
      </div>
    </div>
  );
}

export default LoginPage;
