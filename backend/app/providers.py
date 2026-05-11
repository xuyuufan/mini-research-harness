from typing import Protocol

from . import models
from .agents import build_plan, make_agent_output
from .reporting import make_report


class AgentProvider(Protocol):
    def generate_plan(self, project: models.Project, language: str = "en"):
        ...

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        ...

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        ...


class LocalMockProvider:
    def generate_plan(self, project: models.Project, language: str = "en"):
        return build_plan(project, language)

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        return make_agent_output(project, step, language)

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        return make_report(project, steps, runs, language)
