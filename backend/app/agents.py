from . import models
from .i18n import get_copy


def build_plan(project: models.Project, language: str = "en"):
    text = get_copy(language)
    subject = project.name.strip() or text["default_subject"]

    return [
        (1, text["plan_scope"].format(subject=subject), "Planner Agent"),
        (2, text["plan_research"], "Research Agent"),
        (3, text["plan_synthesis"], "Synthesis Agent"),
        (4, text["plan_report"], "Reporter Agent"),
    ]


def make_agent_output(project: models.Project, step: models.TaskStep, language: str = "en"):
    text = get_copy(language)
    description = project.description.strip() or text["no_description"]

    if step.assigned_agent == "Planner Agent":
        return text["planner_output"].format(name=project.name, description=description)
    if step.assigned_agent == "Research Agent":
        return text["research_output"]
    if step.assigned_agent == "Synthesis Agent":
        return text["synthesis_output"]
    return text["reporter_output"]
