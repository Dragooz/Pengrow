import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { appraisalService } from '../services/appraisalService';
import { Project, ProjectMembership, AppraisalCycle, AppraisalCreate } from '../types';
import './AppraisalCreatePage.css';

const AppraisalCreatePage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Form state
  const [projects, setProjects] = useState<Project[]>([]);
  const [cycles, setCycles] = useState<AppraisalCycle[]>([]);
  const [members, setMembers] = useState<ProjectMembership[]>([]);

  const [selectedCycle, setSelectedCycle] = useState<number | ''>('');
  const [selectedProject, setSelectedProject] = useState<number | ''>('');
  const [selectedAppraisee, setSelectedAppraisee] = useState<number | ''>('');
  const [discussionDate, setDiscussionDate] = useState('');

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        const [projectsData, cyclesData] = await Promise.all([
          projectService.getProjects(),
          appraisalService.getActiveCycles(),
        ]);
        setProjects(projectsData);
        setCycles(cyclesData);
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      }
    };
    loadData();
  }, []);

  // Load project members when project is selected
  useEffect(() => {
    if (selectedProject) {
      const loadMembers = async () => {
        try {
          const membersData = await projectService.getProjectMembers(Number(selectedProject));
          // Filter out reporters, only show members who can be appraised
          setMembers(membersData);
        } catch (err) {
          setError('Failed to load project members');
          console.error(err);
        }
      };
      loadMembers();
    } else {
      setMembers([]);
      setSelectedAppraisee('');
    }
  }, [selectedProject]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const appraisalData: AppraisalCreate = {
        cycle: Number(selectedCycle),
        project: Number(selectedProject),
        appraisee: Number(selectedAppraisee),
        discussion_date: discussionDate,
        status: 'PENDING',
      };

      const created = await appraisalService.createAppraisal(appraisalData);
      navigate(`/appraisals/${created.id}`);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to create appraisal');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="appraisal-create-container">
      <h1>Create New Appraisal</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="appraisal-create-form">
        <div className="form-group">
          <label htmlFor="cycle">Appraisal Cycle *</label>
          <select
            id="cycle"
            value={selectedCycle}
            onChange={(e) => setSelectedCycle(e.target.value ? Number(e.target.value) : '')}
            required
            disabled={loading}
          >
            <option value="">Select a cycle</option>
            {cycles.map((cycle) => (
              <option key={cycle.id} value={cycle.id}>
                {cycle.period_start} to {cycle.period_end} ({cycle.status})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="project">Project *</label>
          <select
            id="project"
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value ? Number(e.target.value) : '')}
            required
            disabled={loading}
          >
            <option value="">Select a project</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="appraisee">Appraisee *</label>
          <select
            id="appraisee"
            value={selectedAppraisee}
            onChange={(e) => setSelectedAppraisee(e.target.value ? Number(e.target.value) : '')}
            required
            disabled={loading || !selectedProject}
          >
            <option value="">Select an appraisee</option>
            {members.map((member) => (
              <option key={member.id} value={member.user}>
                {member.user_name} ({member.user_email}) - {member.role}
              </option>
            ))}
          </select>
          {!selectedProject && <small>Please select a project first</small>}
        </div>

        <div className="form-group">
          <label htmlFor="discussionDate">Discussion Date *</label>
          <input
            type="date"
            id="discussionDate"
            value={discussionDate}
            onChange={(e) => setDiscussionDate(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div className="form-actions">
          <button type="button" onClick={() => navigate('/appraisals')} className="btn btn-secondary" disabled={loading}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Creating...' : 'Create Appraisal'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AppraisalCreatePage;
