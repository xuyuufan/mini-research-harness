from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine

app = FastAPI(title="Mini Research Harness API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup for this local development harness.
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ordered_steps(db: Session, project_id: int):
    return (
        db.query(models.TaskStep)
        .filter(models.TaskStep.project_id == project_id)
        .order_by(models.TaskStep.step_number)
        .all()
    )


def ordered_runs(db: Session, project_id: int):
    return (
        db.query(models.AgentRun)
        .filter(models.AgentRun.project_id == project_id)
        .order_by(models.AgentRun.id)
        .all()
    )


def ordered_artifacts(db: Session, project_id: int):
    return (
        db.query(models.Artifact)
        .filter(models.Artifact.project_id == project_id)
        .order_by(models.Artifact.id.desc())
        .all()
    )


def require_project(project_id: int, db: Session):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def build_plan(project: models.Project):
    subject = project.name.strip() or "the task"
    return [
        (1, f"Clarify scope for {subject}", "Planner Agent"),
        (2, "Collect constraints, assumptions, and reference points", "Research Agent"),
        (3, "Turn findings into an implementation plan", "Synthesis Agent"),
        (4, "Create a final report with decisions and next actions", "Reporter Agent"),
    ]


def make_agent_output(project: models.Project, step: models.TaskStep):
    description = project.description.strip() or "No description was provided."
    if step.assigned_agent == "Planner Agent":
        return (
            f"Scope locked for '{project.name}'. Task brief: {description} "
            "The workflow will track plan, execution logs, and report artifacts separately."
        )
    if step.assigned_agent == "Research Agent":
        return (
            "Research notes: identify the user goal, expected deliverables, local run constraints, "
            "data entities, and UI surfaces before implementation."
        )
    if step.assigned_agent == "Synthesis Agent":
        return (
            "Implementation strategy: keep deterministic local agents, persist every step, "
            "and expose a project detail endpoint that the UI can render directly."
        )
    return (
        "Report draft completed: summarize objective, workflow trace, outputs, and how this differs "
        "from a plain chatbot transcript."
    )


def make_report(project: models.Project, steps: list[models.TaskStep], runs: list[models.AgentRun]):
    completed = sum(1 for step in steps if step.status == "completed")
    run_lines = "\n".join(
        f"- {run.agent_name}: {run.output}" for run in runs
    )
    step_lines = "\n".join(
        f"- Step {step.step_number}: {step.title} [{step.status}] assigned to {step.assigned_agent}"
        for step in steps
    )
    return f"""# Research Workflow Report: {project.name}

## Goal
{project.description or "No project description was provided."}

## Workflow Status
{completed} of {len(steps)} steps completed.

## Tracked Plan
{step_lines}

## Agent Execution Trace
{run_lines}

## Why this is not a plain chatbot
This harness stores a project, a planned sequence of task steps, structured agent runs, and a final report artifact. A normal chatbot usually leaves work as an unstructured conversation; this workflow makes ownership, status, outputs, and the final deliverable inspectable and repeatable.
"""


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/projects", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@app.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.id.desc()).all()


@app.get("/projects/{project_id}", response_model=schemas.ProjectDetailOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = require_project(project_id, db)
    return {
        "project": project,
        "task_steps": ordered_steps(db, project_id),
        "agent_runs": ordered_runs(db, project_id),
        "artifacts": ordered_artifacts(db, project_id),
    }


@app.post("/projects/{project_id}/plan", response_model=list[schemas.TaskStepOut])
def generate_plan(project_id: int, db: Session = Depends(get_db)):
    project = require_project(project_id, db)

    db.query(models.Artifact).filter(models.Artifact.project_id == project_id).delete()
    db.query(models.AgentRun).filter(models.AgentRun.project_id == project_id).delete()
    db.query(models.TaskStep).filter(models.TaskStep.project_id == project_id).delete()

    for number, title, agent in build_plan(project):
        db.add(
            models.TaskStep(
                project_id=project_id,
                step_number=number,
                title=title,
                assigned_agent=agent,
                status="pending",
            )
        )

    db.commit()
    return ordered_steps(db, project_id)


@app.post("/projects/{project_id}/agent-runs", response_model=schemas.AgentRunOut)
def create_agent_run(project_id: int, payload: schemas.AgentRunCreate, db: Session = Depends(get_db)):
    project = require_project(project_id, db)
    step = None
    if payload.task_step_id is not None:
        step = (
            db.query(models.TaskStep)
            .filter(models.TaskStep.project_id == project_id, models.TaskStep.id == payload.task_step_id)
            .first()
        )
        if not step:
            raise HTTPException(status_code=404, detail="Task step not found")

    output = make_agent_output(
        project,
        step
        or models.TaskStep(
            project_id=project_id,
            step_number=0,
            title="Manual run",
            assigned_agent=payload.agent_name,
        ),
    )
    run = models.AgentRun(
        project_id=project_id,
        task_step_id=payload.task_step_id,
        agent_name=payload.agent_name,
        status="completed",
        output=output,
    )
    if step:
        step.status = "completed"
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@app.get("/projects/{project_id}/agent-runs", response_model=list[schemas.AgentRunOut])
def list_agent_runs(project_id: int, db: Session = Depends(get_db)):
    require_project(project_id, db)
    return ordered_runs(db, project_id)


@app.post("/projects/{project_id}/execute", response_model=schemas.WorkflowRunOut)
def execute_workflow(project_id: int, db: Session = Depends(get_db)):
    project = require_project(project_id, db)
    steps = ordered_steps(db, project_id)
    if not steps:
        generate_plan(project_id, db)
        steps = ordered_steps(db, project_id)

    db.query(models.Artifact).filter(models.Artifact.project_id == project_id).delete()
    db.query(models.AgentRun).filter(models.AgentRun.project_id == project_id).delete()

    runs = []
    for step in steps:
        step.status = "running"
        db.flush()
        run = models.AgentRun(
            project_id=project_id,
            task_step_id=step.id,
            agent_name=step.assigned_agent,
            status="completed",
            output=make_agent_output(project, step),
        )
        step.status = "completed"
        db.add(run)
        runs.append(run)

    db.flush()
    report = models.Artifact(
        project_id=project_id,
        agent_run_id=runs[-1].id if runs else None,
        name="Final Research Report",
        artifact_type="markdown",
        content=make_report(project, steps, runs),
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "project": project,
        "task_steps": ordered_steps(db, project_id),
        "agent_runs": ordered_runs(db, project_id),
        "report": report,
    }


@app.get("/projects/{project_id}/artifacts", response_model=list[schemas.ArtifactOut])
def list_artifacts(project_id: int, db: Session = Depends(get_db)):
    require_project(project_id, db)
    return ordered_artifacts(db, project_id)


@app.get("/workflow-explanation")
def workflow_explanation():
    return {
        "chatbot": "A chatbot keeps context mainly as conversational turns.",
        "harness": "This harness persists projects, task steps, agent runs, statuses, and report artifacts.",
        "benefit": "The work can be inspected, resumed, tested, and explained as a project workflow.",
    }
