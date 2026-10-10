"""Defines the root_agent for the assistant package."""

from google.adk import Agent

from agents.assistant.prompts import ASSISTANT_INSTRUCTION
from agents.assistant.tools import calculate, get_current_utc_time, text_statistics
from agents.config import DEFAULT_MODEL

root_agent = Agent(
    name="assistant",
    model=DEFAULT_MODEL,
    description=(
        "A versatile AI assistant equipped with arithmetic, UTC time, and text analysis tools."
    ),
    instruction=ASSISTANT_INSTRUCTION,
    tools=[calculate, get_current_utc_time, text_statistics],
)
