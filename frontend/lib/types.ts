export type Project = {
  id: number;
  name: string;
  description: string;
};

export type TaskStep = {
  step_number: number;
  title: string;
  assigned_agent: string;
  status: string;
};

export type AgentRun = {
  id: number;
  agent_name: string;
  step_title: string;
  status: string;
  output: string;
};
