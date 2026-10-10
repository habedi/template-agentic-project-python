"""Defines an ADK workflow graph connecting a researcher agent and a writer agent."""

from google.adk import Agent, Workflow

from agents.config import DEFAULT_MODEL
from agents.workflow.prompts import RESEARCHER_INSTRUCTION, WRITER_INSTRUCTION
from agents.workflow.tools import gather_topic_points

# Define worker agents.
researcher_agent = Agent(
    name="researcher",
    model=DEFAULT_MODEL,
    description="Researches and gathers structured points on a topic.",
    instruction=RESEARCHER_INSTRUCTION,
    tools=[gather_topic_points],
)

writer_agent = Agent(
    name="writer",
    model=DEFAULT_MODEL,
    description="Synthesizes research findings into a brief summary.",
    instruction=WRITER_INSTRUCTION,
)

# Compose the agents into a sequential execution graph.
root_agent = Workflow(
    name="research_workflow",
    edges=[("START", researcher_agent, writer_agent)],
)
