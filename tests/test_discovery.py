"""Tests for ADK AgentLoader discovery and loading."""

from pathlib import Path

from google.adk.cli.cli import AgentLoader


def test_agent_loader_discovery() -> None:
    agents_dir = Path("agents")
    assert agents_dir.is_dir()

    loader = AgentLoader(str(agents_dir))
    discovered = loader.list_agents()

    assert "assistant" in discovered
    assert "workflow" in discovered


def test_agent_loader_loads_assistant() -> None:
    loader = AgentLoader("agents")
    loaded = loader.load_agent("assistant")
    assert loaded is not None
    assert loaded.name == "assistant"


def test_agent_loader_loads_workflow() -> None:
    loader = AgentLoader("agents")
    loaded = loader.load_agent("workflow")
    assert loaded is not None
    assert loaded.name == "research_workflow"
