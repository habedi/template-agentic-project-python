"""Tests for the research workflow module."""

from agents.config import DEFAULT_MODEL
from agents.workflow.agent import researcher_agent, root_agent, writer_agent
from google.adk import Agent, Workflow
from google.adk.models.registry import LLMRegistry


def test_workflow_structure() -> None:
    assert isinstance(root_agent, Workflow)
    assert root_agent.name == "research_workflow"


def test_workflow_sub_agents() -> None:
    assert isinstance(researcher_agent, Agent)
    assert researcher_agent.name == "researcher"
    assert researcher_agent.model == DEFAULT_MODEL
    assert len(researcher_agent.tools) == 1

    assert isinstance(writer_agent, Agent)
    assert writer_agent.name == "writer"
    assert writer_agent.model == DEFAULT_MODEL

    # Verify that the model can be resolved by LLMRegistry
    assert isinstance(researcher_agent.model, str)
    llm = LLMRegistry.new_llm(researcher_agent.model)
    assert llm is not None
