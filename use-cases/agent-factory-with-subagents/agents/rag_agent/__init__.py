"""Semantic Search Agent Package."""

from agent import search_agent
from dependencies import AgentDependencies
from settings import Settings, load_settings
from providers import get_llm_model, get_embedding_model

__version__ = "1.0.0"

__all__ = [
    "search_agent",
    "AgentDependencies",
    "Settings",
    "load_settings",
    "get_llm_model",
    "get_embedding_model",
]