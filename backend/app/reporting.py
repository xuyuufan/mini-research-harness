from . import models
from .i18n import get_copy


def make_report(project: models.Project, steps: list[models.TaskStep], runs: list[models.AgentRun], language: str = "en"):
    text = get_copy(language)
    completed = sum(1 for step in steps if step.status == "completed")
    step_lines = "\n".join(
        text["step_line"].format(
            number=step.step_number,
            title=step.title,
            status=step.status,
            agent=step.assigned_agent,
        )
        for step in steps
    )
    run_lines = "\n".join(f"- {run.agent_name}: {run.output}" for run in runs)

    return f"""# {text["report_title"].format(name=project.name)}

## {text["goal"]}
{project.description or text["no_project_description"]}

## {text["workflow_status"]}
{text["completed"].format(completed=completed, total=len(steps))}

## {text["tracked_plan"]}
{step_lines}

## {text["execution_trace"]}
{run_lines}

## {text["not_chatbot"]}
{text["not_chatbot_body"]}
"""
