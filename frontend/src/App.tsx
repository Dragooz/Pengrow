import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ProjectsPage from './pages/ProjectsPage';
import AppraisalsPage from './pages/AppraisalsPage';
import AppraisalCreatePage from './pages/AppraisalCreatePage';
import AppraisalDetailPage from './pages/AppraisalDetailPage';
import './App.css';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <AuthProvider>
          <Routes>
          {/* Public route */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Navigate to="/dashboard" replace />
              </ProtectedRoute>
            }
          />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <Dashboard />
                </>
              </ProtectedRoute>
            }
          />

          <Route
            path="/projects"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <ProjectsPage />
                </>
              </ProtectedRoute>
            }
          />

          <Route
            path="/appraisals"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <AppraisalsPage />
                </>
              </ProtectedRoute>
            }
          />

          <Route
            path="/appraisals/create"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <AppraisalCreatePage />
                </>
              </ProtectedRoute>
            }
          />

          <Route
            path="/appraisals/:id"
            element={
              <ProtectedRoute>
                <>
                  <Navbar />
                  <AppraisalDetailPage />
                </>
              </ProtectedRoute>
            }
          />

          {/* Fallback route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
