import { Project, ProjectDetail, TaskStep, WorkflowRun } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function listProjects() {
  return request<Project[]>("/projects");
}

export function createProject(name: string, description: string) {
  return request<Project>("/projects", {
    method: "POST",
    body: JSON.stringify({ name, description }),
  });
}

export function getProject(projectId: number) {
  return request<ProjectDetail>(`/projects/${projectId}`);
}

export function generatePlan(projectId: number) {
  return request<TaskStep[]>(`/projects/${projectId}/plan`, { method: "POST" });
}

export function executeWorkflow(projectId: number) {
  return request<WorkflowRun>(`/projects/${projectId}/execute`, { method: "POST" });
}
