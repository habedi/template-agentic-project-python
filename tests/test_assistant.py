"""Tests for the assistant agent module."""

import os

from agents.assistant.agent import root_agent
from agents.assistant.prompts import ASSISTANT_INSTRUCTION
from agents.config import DEFAULT_MODEL, normalize_model_name
from google.adk import Agent
from google.adk.models.registry import LLMRegistry


def test_assistant_agent_structure() -> None:
    assert isinstance(root_agent, Agent)
    assert root_agent.name == "assistant"
    assert root_agent.description is not None
    assert root_agent.instruction == ASSISTANT_INSTRUCTION
    assert len(root_agent.tools) == 3


def test_assistant_agent_tools() -> None:
    tool_funcs = root_agent.tools
    tool_names = [fn.__name__ for fn in tool_funcs if hasattr(fn, "__name__")]
    assert "calculate" in tool_names
    assert "get_current_utc_time" in tool_names
    assert "text_statistics" in tool_names


def test_default_model_configuration() -> None:
    expected_model = normalize_model_name(os.getenv("MODEL_NAME", "openai/google/gemma-4-12B"))
    assert root_agent.model == expected_model
    assert expected_model == DEFAULT_MODEL


def test_normalize_model_name() -> None:
    assert normalize_model_name("google/gemma-4-12B") == "openai/google/gemma-4-12B"
    assert normalize_model_name("gemma-4-12b") == "openai/gemma-4-12b"
    assert normalize_model_name("openai/google/gemma-4-12B") == "openai/google/gemma-4-12B"
    assert normalize_model_name("gemini-2.5-flash") == "gemini-2.5-flash"


def test_local_model_resolution() -> None:
    # Verify that the ADK LLMRegistry resolves the local Llama.cpp model.
    assert isinstance(root_agent.model, str)
    llm = LLMRegistry.new_llm(root_agent.model)
    assert llm is not None
    assert llm.model == root_agent.model
