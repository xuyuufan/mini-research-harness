import json
import os
from typing import Protocol

from . import models
from .agents import build_plan, make_agent_output
from .prompts import build_agent_run_prompt, build_plan_prompt, build_report_prompt
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
    def __init__(self, api_key: str | None = None, model: str | None = None, client=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required when AGENT_PROVIDER=openai")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.client = client

    def generate_plan(self, project: models.Project, language: str = "en"):
        raw_output = self._call_openai(build_plan_prompt(project, language))
        return self._parse_plan(raw_output)

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        return self._call_openai(build_agent_run_prompt(project, step, language))

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        return self._call_openai(build_report_prompt(project, steps, runs, language))

    def _call_openai(self, prompt: str) -> str:
        if self.client is None:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)

        response = self.client.responses.create(model=self.model, input=prompt)
        text = getattr(response, "output_text", None)
        return text if text is not None else str(response)

    def _parse_plan(self, raw_output: str):
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = None

        if isinstance(parsed, dict):
            parsed = parsed.get("steps") or parsed.get("task_steps")

        if isinstance(parsed, list):
            steps = []
            for index, item in enumerate(parsed[:4], start=1):
                if not isinstance(item, dict):
                    continue
                title = item.get("title") or item.get("name")
                agent = item.get("assigned_agent") or item.get("agent")
                number = item.get("step_number") or item.get("number") or index
                if title and agent:
                    try:
                        step_number = int(number)
                    except (TypeError, ValueError):
                        step_number = index
                    steps.append((step_number, str(title), str(agent)))
            if len(steps) == 4:
                return steps

        summary = " ".join(raw_output.split())[:120] or "Review OpenAI planning output"
        return [
            (1, "Clarify project scope with OpenAI provider", "Planner Agent"),
            (2, "Research project context with OpenAI provider", "Research Agent"),
            (3, f"Synthesize OpenAI plan output: {summary}", "Synthesis Agent"),
            (4, "Prepare final report from OpenAI-assisted workflow", "Reporter Agent"),
        ]


class AnthropicProvider:
    not_implemented_message = "AnthropicProvider is not implemented yet. Use AGENT_PROVIDER=local for now."

    def generate_plan(self, project: models.Project, language: str = "en"):
        # Future implementation should use prompt builders from app.prompts before calling an LLM API.
        raise NotImplementedError(self.not_implemented_message)

    def run_agent(self, project: models.Project, step: models.TaskStep, language: str = "en"):
        # Future implementation should use prompt builders from app.prompts before calling an LLM API.
        raise NotImplementedError(self.not_implemented_message)

    def generate_report(
        self,
        project: models.Project,
        steps: list[models.TaskStep],
        runs: list[models.AgentRun],
        language: str = "en",
    ):
        # Future implementation should use prompt builders from app.prompts before calling an LLM API.
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
