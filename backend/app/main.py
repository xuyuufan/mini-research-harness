from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .agents import build_plan, make_agent_output
from .database import Base, SessionLocal, engine
from .i18n import get_copy
from .reporting import make_report

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


def reset_project_workflow(db: Session, project_id: int):
    db.query(models.Artifact).filter(models.Artifact.project_id == project_id).delete()
    db.query(models.AgentRun).filter(models.AgentRun.project_id == project_id).delete()
    db.query(models.TaskStep).filter(models.TaskStep.project_id == project_id).delete()


def add_plan_steps(db: Session, project: models.Project, language: str):
    for number, title, agent in build_plan(project, language):
        db.add(
            models.TaskStep(
                project_id=project.id,
                step_number=number,
                title=title,
                assigned_agent=agent,
                status="pending",
            )
        )


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
def generate_plan(project_id: int, language: str = "en", db: Session = Depends(get_db)):
    project = require_project(project_id, db)
    reset_project_workflow(db, project_id)
    add_plan_steps(db, project, language)
    db.commit()
    return ordered_steps(db, project_id)


@app.post("/projects/{project_id}/agent-runs", response_model=schemas.AgentRunOut)
def create_agent_run(project_id: int, payload: schemas.AgentRunCreate, language: str = "en", db: Session = Depends(get_db)):
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
        language,
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
def execute_workflow(project_id: int, language: str = "en", db: Session = Depends(get_db)):
    project = require_project(project_id, db)
    steps = ordered_steps(db, project_id)
    if not steps:
        add_plan_steps(db, project, language)
        db.flush()
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
            output=make_agent_output(project, step, language),
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
        content=make_report(project, steps, runs, language),
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
def workflow_explanation(language: str = "en"):
    return get_copy(language)["workflow_explanation"]
