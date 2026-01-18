import api from './api';
import {
  Appraisal,
  AppraisalCreate,
  AppraisalCycle,
  AppraisalReview,
  CompetencyRating,
  OverallEvaluation,
} from '../types';

export const appraisalService = {
  // Appraisal Cycles
  async getCycles(): Promise<AppraisalCycle[]> {
    const response = await api.get<AppraisalCycle[]>('/appraisal-cycles/');
    return response.data;
  },

  async getActiveCycles(): Promise<AppraisalCycle[]> {
    const response = await api.get<AppraisalCycle[]>('/appraisal-cycles/?status=ACTIVE');
    return response.data;
  },

  // Appraisals
  async getAppraisals(): Promise<Appraisal[]> {
    const response = await api.get<Appraisal[]>('/appraisals/');
    return response.data;
  },

  async getAppraisal(id: number): Promise<Appraisal> {
    const response = await api.get<Appraisal>(`/appraisals/${id}/`);
    return response.data;
  },

  async createAppraisal(data: AppraisalCreate): Promise<Appraisal> {
    const response = await api.post<Appraisal>('/appraisals/', data);
    return response.data;
  },

  async updateAppraisal(id: number, data: Partial<Appraisal>): Promise<Appraisal> {
    const response = await api.patch<Appraisal>(`/appraisals/${id}/`, data);
    return response.data;
  },

  async deleteAppraisal(id: number): Promise<void> {
    await api.delete(`/appraisals/${id}/`);
  },

  // Appraisal Reviews
  async getReviews(appraisalId?: number): Promise<AppraisalReview[]> {
    const url = appraisalId
      ? `/appraisal-reviews/?appraisal=${appraisalId}`
      : '/appraisal-reviews/';
    const response = await api.get<AppraisalReview[]>(url);
    return response.data;
  },

  async getReview(id: number): Promise<AppraisalReview> {
    const response = await api.get<AppraisalReview>(`/appraisal-reviews/${id}/`);
    return response.data;
  },

  async updateReview(id: number, data: Partial<AppraisalReview>): Promise<AppraisalReview> {
    const response = await api.patch<AppraisalReview>(`/appraisal-reviews/${id}/`, data);
    return response.data;
  },

  // Competency Ratings
  async getRatings(reviewId?: number): Promise<CompetencyRating[]> {
    const url = reviewId
      ? `/competency-ratings/?appraisal_review=${reviewId}`
      : '/competency-ratings/';
    const response = await api.get<CompetencyRating[]>(url);
    return response.data;
  },

  async createRating(data: Omit<CompetencyRating, 'id' | 'rating_display' | 'created_at'>): Promise<CompetencyRating> {
    const response = await api.post<CompetencyRating>('/competency-ratings/', data);
    return response.data;
  },

  async updateRating(id: number, data: Partial<CompetencyRating>): Promise<CompetencyRating> {
    const response = await api.patch<CompetencyRating>(`/competency-ratings/${id}/`, data);
    return response.data;
  },

  async deleteRating(id: number): Promise<void> {
    await api.delete(`/competency-ratings/${id}/`);
  },

  // Overall Evaluations
  async getOverallEvaluation(appraisalId: number): Promise<OverallEvaluation | null> {
    try {
      const response = await api.get<OverallEvaluation>(`/overall-evaluations/?appraisal=${appraisalId}`);
      return response.data;
    } catch (error) {
      return null;
    }
  },

  async updateOverallEvaluation(id: number, data: Partial<OverallEvaluation>): Promise<OverallEvaluation> {
    const response = await api.patch<OverallEvaluation>(`/overall-evaluations/${id}/`, data);
    return response.data;
  },
};
