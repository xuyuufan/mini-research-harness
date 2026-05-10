from datetime import datetime
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str = ""


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskStepOut(BaseModel):
    id: int
    project_id: int
    step_number: int
    title: str
    assigned_agent: str
    status: str

    class Config:
        from_attributes = True


class AgentRunCreate(BaseModel):
    task_step_id: int | None = None
    agent_name: str


class AgentRunOut(BaseModel):
    id: int
    project_id: int
    task_step_id: int | None
    agent_name: str
    status: str
    output: str
    created_at: datetime

    class Config:
        from_attributes = True


class ArtifactOut(BaseModel):
    id: int
    project_id: int
    agent_run_id: int | None
    name: str
    artifact_type: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectDetailOut(BaseModel):
    project: ProjectOut
    task_steps: list[TaskStepOut]
    agent_runs: list[AgentRunOut]
    artifacts: list[ArtifactOut]


class WorkflowRunOut(BaseModel):
    project: ProjectOut
    task_steps: list[TaskStepOut]
    agent_runs: list[AgentRunOut]
    report: ArtifactOut
