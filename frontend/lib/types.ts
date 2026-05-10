export type Project = {
  id: number;
  name: string;
  description: string;
  created_at: string;
};

export type TaskStep = {
  id: number;
  project_id: number;
  step_number: number;
  title: string;
  assigned_agent: string;
  status: "pending" | "running" | "completed" | string;
};

export type AgentRun = {
  id: number;
  project_id: number;
  task_step_id: number | null;
  agent_name: string;
  status: string;
  output: string;
  created_at: string;
};

export type Artifact = {
  id: number;
  project_id: number;
  agent_run_id: number | null;
  name: string;
  artifact_type: string;
  content: string;
  created_at: string;
};

export type ProjectDetail = {
  project: Project;
  task_steps: TaskStep[];
  agent_runs: AgentRun[];
  artifacts: Artifact[];
};

export type WorkflowRun = {
  project: Project;
  task_steps: TaskStep[];
  agent_runs: AgentRun[];
  report: Artifact;
};

export type Language = "en" | "zh";
