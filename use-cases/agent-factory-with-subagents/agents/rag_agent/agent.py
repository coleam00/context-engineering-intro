"""Main agent implementation for Semantic Search."""

from pydantic_ai import Agent, RunContext
from typing import Any

from providers import get_llm_model
from dependencies import AgentDependencies
from prompts import MAIN_SYSTEM_PROMPT
from tools import semantic_search, hybrid_search


# Initialize the semantic search agent
search_agent = Agent(
    get_llm_model(),
    deps_type=AgentDependencies,
    system_prompt=MAIN_SYSTEM_PROMPT
)

# Register search tools
search_agent.tool(semantic_search)
search_agent.tool(hybrid_search)
