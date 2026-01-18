import api from './api';
import { Project, ProjectMembership } from '../types';

export const projectService = {
  async getProjects(): Promise<Project[]> {
    const response = await api.get<Project[]>('/projects/');
    return response.data;
  },

  async getProject(id: number): Promise<Project> {
    const response = await api.get<Project>(`/projects/${id}/`);
    return response.data;
  },

  async getProjectMembers(projectId: number): Promise<ProjectMembership[]> {
    const response = await api.get<ProjectMembership[]>(`/projects/${projectId}/members/`);
    return response.data;
  },

  async getProjectReporters(projectId: number): Promise<ProjectMembership[]> {
    const response = await api.get<ProjectMembership[]>(`/projects/${projectId}/reporters/`);
    return response.data;
  },
};
