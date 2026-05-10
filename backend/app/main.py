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


def normalize_language(language: str):
    return "zh" if language.lower().startswith("zh") else "en"


def zh(text: str):
    return text.encode("ascii").decode("unicode_escape")


ZH_TEXT = {
    "the_task": r"\u4efb\u52a1",
    "plan_scope": r"\u660e\u786e {subject} \u7684\u8303\u56f4",
    "plan_research": r"\u6536\u96c6\u7ea6\u675f\u3001\u5047\u8bbe\u548c\u53c2\u8003\u4fe1\u606f",
    "plan_synthesis": r"\u628a\u8c03\u7814\u7ed3\u679c\u6574\u7406\u6210\u5b9e\u65bd\u8ba1\u5212",
    "plan_report": r"\u751f\u6210\u5305\u542b\u51b3\u7b56\u548c\u540e\u7eed\u884c\u52a8\u7684\u6700\u7ec8\u62a5\u544a",
    "no_description": r"\u672a\u63d0\u4f9b\u4efb\u52a1\u63cf\u8ff0\u3002",
    "planner_output": (
        r"\u5df2\u9501\u5b9a\u9879\u76ee '{name}' \u7684\u8303\u56f4\u3002"
        r"\u4efb\u52a1\u7b80\u4ecb\uff1a{description} "
        r"\u8be5 workflow \u4f1a\u5206\u522b\u8ffd\u8e2a\u8ba1\u5212\u3001"
        r"\u6267\u884c\u65e5\u5fd7\u548c\u62a5\u544a\u4ea7\u7269\u3002"
    ),
    "research_output": (
        r"\u8c03\u7814\u8bb0\u5f55\uff1a\u5148\u8bc6\u522b\u7528\u6237\u76ee\u6807\u3001"
        r"\u9884\u671f\u4ea4\u4ed8\u7269\u3001\u672c\u5730\u8fd0\u884c\u7ea6\u675f\u3001"
        r"\u6570\u636e\u5b9e\u4f53\u548c UI \u5c55\u793a\u533a\u57df\u3002"
    ),
    "synthesis_output": (
        r"\u5b9e\u65bd\u7b56\u7565\uff1a\u4fdd\u7559\u786e\u5b9a\u6027\u7684\u672c\u5730 agents\uff0c"
        r"\u6301\u4e45\u5316\u6bcf\u4e2a\u6b65\u9aa4\uff0c\u5e76\u63d0\u4f9b\u524d\u7aef"
        r"\u53ef\u76f4\u63a5\u6e32\u67d3\u7684\u9879\u76ee\u8be6\u60c5\u63a5\u53e3\u3002"
    ),
    "reporter_output": (
        r"\u62a5\u544a\u8349\u7a3f\u5df2\u5b8c\u6210\uff1a\u603b\u7ed3\u76ee\u6807\u3001"
        r"workflow \u8f68\u8ff9\u3001\u8f93\u51fa\uff0c\u4ee5\u53ca\u5b83\u548c\u666e\u901a chatbot \u7684\u533a\u522b\u3002"
    ),
    "report_title": r"\u7814\u7a76 Workflow \u62a5\u544a\uff1a{name}",
    "goal": r"\u76ee\u6807",
    "workflow_status": r"Workflow \u72b6\u6001",
    "completed": r"\u5df2\u5b8c\u6210 {completed} / {total} \u4e2a\u6b65\u9aa4\u3002",
    "tracked_plan": r"\u53ef\u8ffd\u8e2a\u8ba1\u5212",
    "execution_trace": r"Agent \u6267\u884c\u8f68\u8ff9",
    "not_chatbot": r"\u4e3a\u4ec0\u4e48\u5b83\u4e0d\u662f\u666e\u901a chatbot",
    "not_chatbot_body": (
        r"\u8fd9\u4e2a harness \u4f1a\u4fdd\u5b58\u9879\u76ee\u3001\u8ba1\u5212\u6b65\u9aa4\u3001"
        r"\u7ed3\u6784\u5316 agent run \u548c\u6700\u7ec8\u62a5\u544a\u4ea7\u7269\u3002"
        r"\u666e\u901a chatbot \u901a\u5e38\u53ea\u7559\u4e0b\u975e\u7ed3\u6784\u5316\u5bf9\u8bdd\uff1b"
        r"\u8fd9\u4e2a workflow \u8ba9\u8d1f\u8d23\u4eba\u3001\u72b6\u6001\u3001\u8f93\u51fa\u548c"
        r"\u6700\u7ec8\u4ea4\u4ed8\u7269\u90fd\u53ef\u4ee5\u88ab\u68c0\u67e5\u548c\u590d\u73b0\u3002"
    ),
    "no_project_description": r"\u672a\u63d0\u4f9b\u9879\u76ee\u63cf\u8ff0\u3002",
    "step_line": r"- \u6b65\u9aa4 {number}: {title} [{status}] \u5206\u914d\u7ed9 {agent}",
}


def build_plan(project: models.Project, language: str = "en"):
    if normalize_language(language) == "zh":
        subject = project.name.strip() or zh(ZH_TEXT["the_task"])
        return [
            (1, zh(ZH_TEXT["plan_scope"]).format(subject=subject), "Planner Agent"),
            (2, zh(ZH_TEXT["plan_research"]), "Research Agent"),
            (3, zh(ZH_TEXT["plan_synthesis"]), "Synthesis Agent"),
            (4, zh(ZH_TEXT["plan_report"]), "Reporter Agent"),
        ]

    subject = project.name.strip() or "the task"
    return [
        (1, f"Clarify scope for {subject}", "Planner Agent"),
        (2, "Collect constraints, assumptions, and reference points", "Research Agent"),
        (3, "Turn findings into an implementation plan", "Synthesis Agent"),
        (4, "Create a final report with decisions and next actions", "Reporter Agent"),
    ]


def make_agent_output(project: models.Project, step: models.TaskStep, language: str = "en"):
    if normalize_language(language) == "zh":
        description = project.description.strip() or zh(ZH_TEXT["no_description"])
        if step.assigned_agent == "Planner Agent":
            return zh(ZH_TEXT["planner_output"]).format(name=project.name, description=description)
        if step.assigned_agent == "Research Agent":
            return zh(ZH_TEXT["research_output"])
        if step.assigned_agent == "Synthesis Agent":
            return zh(ZH_TEXT["synthesis_output"])
        return zh(ZH_TEXT["reporter_output"])

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


def make_report(project: models.Project, steps: list[models.TaskStep], runs: list[models.AgentRun], language: str = "en"):
    completed = sum(1 for step in steps if step.status == "completed")
    run_lines = "\n".join(f"- {run.agent_name}: {run.output}" for run in runs)

    if normalize_language(language) == "zh":
        step_lines = "\n".join(
            zh(ZH_TEXT["step_line"]).format(
                number=step.step_number,
                title=step.title,
                status=step.status,
                agent=step.assigned_agent,
            )
            for step in steps
        )
        return f"""# {zh(ZH_TEXT["report_title"]).format(name=project.name)}

## {zh(ZH_TEXT["goal"])}
{project.description or zh(ZH_TEXT["no_project_description"])}

## {zh(ZH_TEXT["workflow_status"])}
{zh(ZH_TEXT["completed"]).format(completed=completed, total=len(steps))}

## {zh(ZH_TEXT["tracked_plan"])}
{step_lines}

## {zh(ZH_TEXT["execution_trace"])}
{run_lines}

## {zh(ZH_TEXT["not_chatbot"])}
{zh(ZH_TEXT["not_chatbot_body"])}
"""

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
def generate_plan(project_id: int, language: str = "en", db: Session = Depends(get_db)):
    project = require_project(project_id, db)

    db.query(models.Artifact).filter(models.Artifact.project_id == project_id).delete()
    db.query(models.AgentRun).filter(models.AgentRun.project_id == project_id).delete()
    db.query(models.TaskStep).filter(models.TaskStep.project_id == project_id).delete()

    for number, title, agent in build_plan(project, language):
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
        generate_plan(project_id, language, db)
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
    if normalize_language(language) == "zh":
        return {
            "chatbot": zh(r"\u666e\u901a chatbot \u4e3b\u8981\u628a\u4e0a\u4e0b\u6587\u4fdd\u5b58\u4e3a\u5bf9\u8bdd\u8f6e\u6b21\u3002"),
            "harness": zh(r"\u8fd9\u4e2a harness \u4f1a\u6301\u4e45\u5316\u9879\u76ee\u3001\u4efb\u52a1\u6b65\u9aa4\u3001agent run\u3001\u72b6\u6001\u548c\u62a5\u544a\u4ea7\u7269\u3002"),
            "benefit": zh(r"\u8fd9\u8ba9\u5de5\u4f5c\u53ef\u4ee5\u88ab\u68c0\u67e5\u3001\u7ee7\u7eed\u3001\u6d4b\u8bd5\uff0c\u5e76\u4f5c\u4e3a\u9879\u76ee workflow \u6765\u89e3\u91ca\u3002"),
        }
    return {
        "chatbot": "A chatbot keeps context mainly as conversational turns.",
        "harness": "This harness persists projects, task steps, agent runs, statuses, and report artifacts.",
        "benefit": "The work can be inspected, resumed, tested, and explained as a project workflow.",
    }
