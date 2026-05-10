from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine

app = FastAPI(title="Mini Research Harness API")

# Create database tables on startup for this beginner-friendly demo.
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project": schemas.ProjectOut.model_validate(project),
        "task_steps": [schemas.TaskStepOut.model_validate(step) for step in project.task_steps],
    }


@app.post("/projects/{project_id}/plan", response_model=list[schemas.TaskStepOut])
def generate_plan(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Mock plan generation for now.
    mock_steps = [
        (1, "Understand the task scope", "Planner Agent"),
        (2, "Collect references and examples", "Research Agent"),
        (3, "Draft implementation strategy", "Coder Agent"),
    ]

    db.query(models.TaskStep).filter(models.TaskStep.project_id == project_id).delete()
    for number, title, agent in mock_steps:
        db.add(models.TaskStep(project_id=project_id, step_number=number, title=title, assigned_agent=agent, status="pending"))

    db.commit()
    return db.query(models.TaskStep).filter(models.TaskStep.project_id == project_id).order_by(models.TaskStep.step_number).all()


@app.post("/projects/{project_id}/agent-runs", response_model=schemas.AgentRunOut)
def create_agent_run(project_id: int, payload: schemas.AgentRunCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Mock execution output.
    output = f"Mock output from {payload.agent_name}: completed sample analysis for project {project_id}."
    run = models.AgentRun(
        project_id=project_id,
        task_step_id=payload.task_step_id,
        agent_name=payload.agent_name,
        status="completed",
        output=output,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@app.get("/projects/{project_id}/agent-runs", response_model=list[schemas.AgentRunOut])
def list_agent_runs(project_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.AgentRun)
        .filter(models.AgentRun.project_id == project_id)
        .order_by(models.AgentRun.id.desc())
        .all()
    )
