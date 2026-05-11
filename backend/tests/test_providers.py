import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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


def test_openai_provider_run_agent_is_not_implemented():
    provider = OpenAIProvider()

    with pytest.raises(NotImplementedError, match="OpenAIProvider is not implemented yet"):
        provider.run_agent(None, None)


def test_anthropic_provider_run_agent_is_not_implemented():
    provider = AnthropicProvider()

    with pytest.raises(NotImplementedError, match="AnthropicProvider is not implemented yet"):
        provider.run_agent(None, None)
