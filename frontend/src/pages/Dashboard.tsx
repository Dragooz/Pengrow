import React from 'react';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome, {user?.full_name || user?.username}!</h1>
        <p>Employee Appraisal Dashboard</p>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h3>My Profile</h3>
            <div className="profile-info">
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Position:</strong> {user?.position || 'Not set'}</p>
              <p><strong>Division:</strong> {user?.division || 'Not set'}</p>
            </div>
          </div>

          <div className="dashboard-card">
            <h3>Quick Stats</h3>
            <div className="stats-info">
              <p>My Projects: <strong>Loading...</strong></p>
              <p>Pending Appraisals: <strong>Loading...</strong></p>
              <p>Completed Appraisals: <strong>Loading...</strong></p>
            </div>
          </div>

          <div className="dashboard-card">
            <h3>Recent Activity</h3>
            <div className="activity-info">
              <p>No recent activity</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
