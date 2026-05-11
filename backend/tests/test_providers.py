import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import models
from app.providers import AnthropicProvider, LocalMockProvider, OpenAIProvider, get_provider


def test_get_provider_defaults_to_local(monkeypatch):
    monkeypatch.delenv("AGENT_PROVIDER", raising=False)

    provider = get_provider()

    assert isinstance(provider, LocalMockProvider)


def test_get_provider_returns_local_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "local")

    provider = get_provider()

    assert isinstance(provider, LocalMockProvider)


def test_get_provider_returns_openai_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    provider = get_provider()

    assert isinstance(provider, OpenAIProvider)


def test_get_provider_returns_anthropic_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "anthropic")

    provider = get_provider()

    assert isinstance(provider, AnthropicProvider)


def test_get_provider_rejects_unknown_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="unsupported provider"):
        get_provider()


def test_local_provider_does_not_require_openai_api_key(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "local")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    provider = get_provider()

    assert isinstance(provider, LocalMockProvider)


def test_openai_provider_requires_api_key(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY is required when AGENT_PROVIDER=openai"):
        get_provider()


def test_openai_provider_run_agent_returns_openai_response(monkeypatch):
    provider = OpenAIProvider(api_key="test-key")
    monkeypatch.setattr(provider, "_call_openai", lambda prompt: "fake agent output")
    project = models.Project(name="Demo", description="Test OpenAI provider.")
    step = models.TaskStep(title="Research", assigned_agent="Research Agent", status="pending")

    output = provider.run_agent(project, step)

    assert output == "fake agent output"


def test_openai_provider_generate_report_returns_openai_markdown(monkeypatch):
    provider = OpenAIProvider(api_key="test-key")
    monkeypatch.setattr(provider, "_call_openai", lambda prompt: "# Fake report")
    project = models.Project(name="Demo", description="Test OpenAI provider.")
    step = models.TaskStep(step_number=1, title="Research", assigned_agent="Research Agent", status="completed")
    run = models.AgentRun(agent_name="Research Agent", status="completed", output="Done")

    report = provider.generate_report(project, [step], [run])

    assert report == "# Fake report"


def test_openai_provider_generate_plan_parses_json(monkeypatch):
    provider = OpenAIProvider(api_key="test-key")
    fake_plan = [
        {"step_number": 1, "title": "Scope", "assigned_agent": "Planner Agent"},
        {"step_number": 2, "title": "Research", "assigned_agent": "Research Agent"},
        {"step_number": 3, "title": "Synthesize", "assigned_agent": "Synthesis Agent"},
        {"step_number": 4, "title": "Report", "assigned_agent": "Reporter Agent"},
    ]
    monkeypatch.setattr(provider, "_call_openai", lambda prompt: json.dumps(fake_plan))

    plan = provider.generate_plan(models.Project(name="Demo", description="Test OpenAI provider."))

    assert plan == [
        (1, "Scope", "Planner Agent"),
        (2, "Research", "Research Agent"),
        (3, "Synthesize", "Synthesis Agent"),
        (4, "Report", "Reporter Agent"),
    ]


def test_openai_provider_generate_plan_falls_back_when_json_parse_fails(monkeypatch):
    provider = OpenAIProvider(api_key="test-key")
    monkeypatch.setattr(provider, "_call_openai", lambda prompt: "not json but still useful")

    plan = provider.generate_plan(models.Project(name="Demo", description="Test OpenAI provider."))

    assert len(plan) == 4
    assert "not json but still useful" in plan[2][1]


def test_anthropic_provider_run_agent_is_not_implemented():
    provider = AnthropicProvider()

    with pytest.raises(NotImplementedError, match="AnthropicProvider is not implemented yet"):
        provider.run_agent(None, None)
