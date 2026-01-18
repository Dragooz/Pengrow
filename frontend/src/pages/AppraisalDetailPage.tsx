import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { appraisalService } from '../services/appraisalService';
import { Appraisal, CompetencyRating } from '../types';
import SignatureCanvas from '../components/SignatureCanvas';
import './AppraisalDetailPage.css';

// Define competency criteria
const COMPETENCY_CRITERIA = {
  WORK_EFFICIENCY: [
    'Ability to work without supervision',
    'Knowledge of roles and responsibilities',
    'Work accuracy and correctness',
    'Resourcefulness and creativity',
  ],
  PRODUCTIVITY: [
    'Completes tasks according to instructions',
    'Takes responsibility for work',
    'Sustains productive work',
    'Meets reasonable time estimates',
  ],
  PERSONAL: ['Initiative and ambition', 'Manner and appearance'],
};

const RATING_OPTIONS = [
  { value: 1, label: 'Not Observed' },
  { value: 2, label: 'Weak' },
  { value: 3, label: 'As Expected' },
  { value: 4, label: 'Good' },
  { value: 5, label: 'Exceptional' },
];

const AppraisalDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [appraisal, setAppraisal] = useState<Appraisal | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  // Ratings state
  const [ratings, setRatings] = useState<{ [key: string]: { rating: number; comments: string } }>({});
  const [signature, setSignature] = useState<string>('');

  useEffect(() => {
    if (id) {
      loadAppraisal();
    }
  }, [id]);

  const loadAppraisal = async () => {
    try {
      const data = await appraisalService.getAppraisal(Number(id));
      setAppraisal(data);

      // Load existing ratings if any
      if (data.reviews && data.reviews.length > 0) {
        const myReview = data.reviews[0]; // Assuming current user's review
        if (myReview.competency_ratings) {
          const ratingsMap: any = {};
          myReview.competency_ratings.forEach((rating: CompetencyRating) => {
            ratingsMap[rating.criterion_name] = {
              rating: rating.rating,
              comments: rating.comments,
            };
          });
          setRatings(ratingsMap);
        }
        if (myReview.reviewer_signature_base64) {
          setSignature(myReview.reviewer_signature_base64);
        }
      }
    } catch (err) {
      setError('Failed to load appraisal');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRatingChange = (criterion: string, rating: number) => {
    setRatings((prev) => ({
      ...prev,
      [criterion]: { ...prev[criterion], rating },
    }));
  };

  const handleCommentsChange = (criterion: string, comments: string) => {
    setRatings((prev) => ({
      ...prev,
      [criterion]: { ...prev[criterion], comments },
    }));
  };

  const handleSaveRatings = async () => {
    if (!appraisal || !appraisal.reviews || appraisal.reviews.length === 0) {
      setError('No review found');
      return;
    }

    setSaving(true);
    setError('');

    try {
      const myReview = appraisal.reviews[0];

      // Save or update each rating
      for (const [criterion, data] of Object.entries(ratings)) {
        if (data.rating) {
          // Find category for this criterion
          let category: 'WORK_EFFICIENCY' | 'PRODUCTIVITY' | 'PERSONAL' = 'WORK_EFFICIENCY';
          if (COMPETENCY_CRITERIA.PRODUCTIVITY.includes(criterion)) {
            category = 'PRODUCTIVITY';
          } else if (COMPETENCY_CRITERIA.PERSONAL.includes(criterion)) {
            category = 'PERSONAL';
          }

          await appraisalService.createRating({
            appraisal_review: myReview.id,
            category,
            criterion_name: criterion,
            rating: data.rating as 1 | 2 | 3 | 4 | 5,
            comments: data.comments || '',
          });
        }
      }

      await loadAppraisal();
      alert('Ratings saved successfully!');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to save ratings');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleSaveSignature = async (signatureData: string) => {
    if (!appraisal || !appraisal.reviews || appraisal.reviews.length === 0) {
      setError('No review found');
      return;
    }

    try {
      const myReview = appraisal.reviews[0];
      await appraisalService.updateReview(myReview.id, {
        reviewer_signature_base64: signatureData,
        reviewer_signed_at: new Date().toISOString(),
        is_completed: true,
      });

      setSignature(signatureData);
      await loadAppraisal();
      alert('Signature saved successfully!');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to save signature');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="appraisal-detail-container">
        <p>Loading...</p>
      </div>
    );
  }

  if (!appraisal) {
    return (
      <div className="appraisal-detail-container">
        <p>Appraisal not found</p>
      </div>
    );
  }

  return (
    <div className="appraisal-detail-container">
      <div className="appraisal-detail-header">
        <div>
          <h1>Appraisal for {appraisal.appraisee_name}</h1>
          <p className="subtitle">
            {appraisal.project_name} | {appraisal.cycle_info.period_start} - {appraisal.cycle_info.period_end}
          </p>
        </div>
        <button onClick={() => navigate('/appraisals')} className="btn btn-secondary">
          Back to List
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="appraisal-content">
        {/* Work Efficiency */}
        <section className="rating-section">
          <h2>Work Efficiency</h2>
          {COMPETENCY_CRITERIA.WORK_EFFICIENCY.map((criterion) => (
            <div key={criterion} className="criterion-item">
              <h4>{criterion}</h4>
              <div className="rating-options">
                {RATING_OPTIONS.map((option) => (
                  <label key={option.value} className="rating-option">
                    <input
                      type="radio"
                      name={criterion}
                      value={option.value}
                      checked={ratings[criterion]?.rating === option.value}
                      onChange={() => handleRatingChange(criterion, option.value)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
              <textarea
                placeholder="Comments (optional)"
                value={ratings[criterion]?.comments || ''}
                onChange={(e) => handleCommentsChange(criterion, e.target.value)}
                className="comments-textarea"
              />
            </div>
          ))}
        </section>

        {/* Productivity & Supervisory */}
        <section className="rating-section">
          <h2>Productivity & Supervisory</h2>
          {COMPETENCY_CRITERIA.PRODUCTIVITY.map((criterion) => (
            <div key={criterion} className="criterion-item">
              <h4>{criterion}</h4>
              <div className="rating-options">
                {RATING_OPTIONS.map((option) => (
                  <label key={option.value} className="rating-option">
                    <input
                      type="radio"
                      name={criterion}
                      value={option.value}
                      checked={ratings[criterion]?.rating === option.value}
                      onChange={() => handleRatingChange(criterion, option.value)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
              <textarea
                placeholder="Comments (optional)"
                value={ratings[criterion]?.comments || ''}
                onChange={(e) => handleCommentsChange(criterion, e.target.value)}
                className="comments-textarea"
              />
            </div>
          ))}
        </section>

        {/* Personal Attributes */}
        <section className="rating-section">
          <h2>Personal Attributes</h2>
          {COMPETENCY_CRITERIA.PERSONAL.map((criterion) => (
            <div key={criterion} className="criterion-item">
              <h4>{criterion}</h4>
              <div className="rating-options">
                {RATING_OPTIONS.map((option) => (
                  <label key={option.value} className="rating-option">
                    <input
                      type="radio"
                      name={criterion}
                      value={option.value}
                      checked={ratings[criterion]?.rating === option.value}
                      onChange={() => handleRatingChange(criterion, option.value)}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
              <textarea
                placeholder="Comments (optional)"
                value={ratings[criterion]?.comments || ''}
                onChange={(e) => handleCommentsChange(criterion, e.target.value)}
                className="comments-textarea"
              />
            </div>
          ))}
        </section>

        {/* Save Ratings Button */}
        <div className="actions-section">
          <button onClick={handleSaveRatings} className="btn btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save Ratings'}
          </button>
        </div>

        {/* Signature Section */}
        <section className="signature-section">
          <h2>Reviewer Signature</h2>
          <SignatureCanvas onSave={handleSaveSignature} existingSignature={signature} />
        </section>

        {/* Overall Evaluation Display */}
        {appraisal.overall_evaluation && appraisal.overall_evaluation.overall_rating_avg && (
          <section className="overall-section">
            <h2>Overall Evaluation</h2>
            <p>
              <strong>Average Rating:</strong> {appraisal.overall_evaluation.overall_rating_avg.toFixed(2)} / 5.0
            </p>
            <p>
              <strong>Ready for Advanced Work:</strong>{' '}
              {appraisal.overall_evaluation.ready_for_advanced_work ? 'Yes' : 'No'}
            </p>
            <p>
              <strong>Ready for Promotion:</strong> {appraisal.overall_evaluation.ready_for_promotion ? 'Yes' : 'No'}
            </p>
          </section>
        )}
      </div>
    </div>
  );
};

export default AppraisalDetailPage;
