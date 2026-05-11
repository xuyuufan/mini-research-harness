import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.providers import LocalMockProvider, get_provider


def test_get_provider_defaults_to_local(monkeypatch):
    monkeypatch.delenv("AGENT_PROVIDER", raising=False)

    provider = get_provider()

    assert isinstance(provider, LocalMockProvider)


def test_get_provider_returns_local_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "local")

    provider = get_provider()

    assert isinstance(provider, LocalMockProvider)


def test_get_provider_rejects_unknown_provider(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="unsupported provider"):
        get_provider()
