import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { appraisalService } from '../services/appraisalService';
import { Appraisal } from '../types';
import './AppraisalsPage.css';

const AppraisalsPage: React.FC = () => {
  const [appraisals, setAppraisals] = useState<Appraisal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadAppraisals = async () => {
      try {
        const data = await appraisalService.getAppraisals();
        setAppraisals(data);
      } catch (err) {
        setError('Failed to load appraisals');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadAppraisals();
  }, []);

  if (loading) {
    return (
      <div className="appraisals-container">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="appraisals-container">
      <div className="appraisals-header">
        <h1>Appraisals</h1>
        <Link to="/appraisals/create" className="btn btn-primary">
          Create New Appraisal
        </Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {appraisals.length === 0 ? (
        <div className="empty-state">
          <p>No appraisals found.</p>
          <Link to="/appraisals/create" className="btn btn-primary">
            Create Your First Appraisal
          </Link>
        </div>
      ) : (
        <div className="appraisals-grid">
          {appraisals.map((appraisal) => (
            <div key={appraisal.id} className="appraisal-card">
              <div className="appraisal-header">
                <h3>{appraisal.appraisee_name}</h3>
                <span className={`status-badge status-${appraisal.status.toLowerCase()}`}>
                  {appraisal.status}
                </span>
              </div>
              <div className="appraisal-details">
                <p>
                  <strong>Project:</strong> {appraisal.project_name}
                </p>
                <p>
                  <strong>Period:</strong> {appraisal.cycle_info.period_start} - {appraisal.cycle_info.period_end}
                </p>
                <p>
                  <strong>Discussion Date:</strong> {appraisal.discussion_date || 'Not set'}
                </p>
                <p>
                  <strong>Reviews:</strong> {appraisal.reviews?.length || 0}
                </p>
              </div>
              <Link to={`/appraisals/${appraisal.id}`} className="btn btn-secondary btn-small">
                View Details
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AppraisalsPage;
