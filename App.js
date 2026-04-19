import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

// Import pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import UploadResumePage from './pages/UploadResumePage';
import AnalyzeJDPage from './pages/AnalyzeJDPage';
import RankingPage from './pages/RankingPage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<HomePage />} />
            
            {/* Protected Routes */}
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <DashboardPage />
                </PrivateRoute>
              }
            />
            <Route 
              path="/upload-resume" 
              element={
                <PrivateRoute>
                  <UploadResumePage />
                </PrivateRoute>
              }
            />
            <Route 
              path="/analyze-jd" 
              element={
                <PrivateRoute>
                  <AnalyzeJDPage />
                </PrivateRoute>
              }
            />
            <Route 
              path="/rank-candidates" 
              element={
                <PrivateRoute>
                  <RankingPage />
                </PrivateRoute>
              }
            />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
