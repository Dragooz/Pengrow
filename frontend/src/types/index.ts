// User types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  company: number | null;
  position: string;
  division: string;
  date_joined: string | null;
  last_promotion_date: string | null;
  is_active: boolean;
  is_staff: boolean;
}

// Company types
export interface Company {
  id: number;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Project types
export interface Project {
  id: number;
  company: number;
  company_name: string;
  name: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectMembership {
  id: number;
  project: number;
  project_name: string;
  user: number;
  user_name: string;
  user_email: string;
  role: 'REPORTER' | 'MEMBER';
  joined_at: string;
  created_at: string;
}

// Appraisal Cycle types
export interface AppraisalCycle {
  id: number;
  company: number;
  company_name: string;
  period_start: string;
  period_end: string;
  status: 'DRAFT' | 'ACTIVE' | 'CLOSED';
  created_at: string;
  updated_at: string;
}

// Competency Rating types
export interface CompetencyRating {
  id: number;
  appraisal_review: number;
  category: 'WORK_EFFICIENCY' | 'PRODUCTIVITY' | 'PERSONAL';
  criterion_name: string;
  rating: 1 | 2 | 3 | 4 | 5;
  rating_display: string;
  comments: string;
  created_at: string;
}

// Appraisal Review types
export interface AppraisalReview {
  id: number;
  appraisal: number;
  reviewer: number;
  reviewer_name: string;
  is_completed: boolean;
  reviewer_signature_base64: string;
  reviewer_signed_at: string | null;
  competency_ratings: CompetencyRating[];
  created_at: string;
  updated_at: string;
}

// Overall Evaluation types
export interface OverallEvaluation {
  id: number;
  appraisal: number;
  overall_rating_avg: number | null;
  ready_for_advanced_work: boolean;
  ready_for_promotion: boolean;
  summary_comment: string;
  appraisee_signature_base64: string;
  appraisee_signed_at: string | null;
  hr_signature_base64: string;
  hr_signed_at: string | null;
  finalized_at: string | null;
  created_at: string;
  updated_at: string;
}

// Appraisal types
export interface Appraisal {
  id: number;
  cycle: number;
  cycle_info: {
    period_start: string;
    period_end: string;
    status: string;
  };
  appraisee: number;
  appraisee_name: string;
  project: number;
  project_name: string;
  discussion_date: string | null;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
  reviews: AppraisalReview[];
  overall_evaluation: OverallEvaluation | null;
  created_at: string;
  updated_at: string;
}

export interface AppraisalCreate {
  cycle: number;
  appraisee: number;
  project: number;
  discussion_date: string;
  status?: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
}

// Auth types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}
