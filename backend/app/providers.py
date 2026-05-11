import os
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


class OpenAIProvider:
    not_implemented_message = "OpenAIProvider is not implemented yet. Use AGENT_PROVIDER=local for now."

    def generate_plan(self, project: models.Project, language: str = "en"):
        raise NotImplementedError(self.not_implemented_message)

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        raise NotImplementedError(self.not_implemented_message)

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        raise NotImplementedError(self.not_implemented_message)


class AnthropicProvider:
    not_implemented_message = "AnthropicProvider is not implemented yet. Use AGENT_PROVIDER=local for now."

    def generate_plan(self, project: models.Project, language: str = "en"):
        raise NotImplementedError(self.not_implemented_message)

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        raise NotImplementedError(self.not_implemented_message)

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        raise NotImplementedError(self.not_implemented_message)


def get_provider() -> AgentProvider:
    provider_name = os.environ.get("AGENT_PROVIDER", "local")

    if provider_name == "local":
        return LocalMockProvider()
    if provider_name == "openai":
        return OpenAIProvider()
    if provider_name == "anthropic":
        return AnthropicProvider()

    raise ValueError(f"unsupported provider: {provider_name}")
