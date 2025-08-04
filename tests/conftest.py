"""
Pytest configuration and fixtures.
"""

import pytest
import tempfile
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from config.settings import Settings
from novel_extractor.llm_client import LLMClient, LLMResponse
from novel_extractor.settings_manager import SettingsManager
from novel_extractor.context_manager import ContextManager


@pytest.fixture
def mock_settings():
    """
    Create mock settings for testing.
    """
    return Settings(
        llm_api_key="test-api-key",
        llm_provider="openai",
        llm_model="gpt-4",
        llm_base_url="https://api.openai.com/v1",
        max_context_length=8192,
        compression_threshold=0.8,
        reserved_response_tokens=2000,
        max_retries=3,
        retry_delay=1.0,
        settings_dir="test_settings",
    )


@pytest.fixture
def temp_settings_dir():
    """
    Create temporary settings directory.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_llm_client():
    """
    Create mock LLM client.
    """
    client = Mock(spec=LLMClient)

    # Mock the generate method to return an async function
    async def mock_generate(*args, **kwargs):
        return LLMResponse(content="Mocked LLM response", usage={"total_tokens": 100})

    client.generate = AsyncMock(side_effect=mock_generate)
    client.create_message = Mock(
        side_effect=lambda role, content: {"role": role, "content": content}
    )

    return client


@pytest.fixture
def sample_novel_content():
    """
    Sample novel content for testing.
    """
    return """Chapter 1: The Beginning

It was a dark and stormy night. Sarah walked through the empty streets, 
her footsteps echoing against the wet pavement. She clutched the mysterious 
letter in her pocket, wondering who could have sent it.

"Meet me at midnight," it had said, signed only with a cryptic symbol.

Chapter 2: The Meeting

The clock tower struck twelve as Sarah arrived at the designated location. 
A figure emerged from the shadows - it was Marcus, her old friend from 
university. But something was different about him now.

"Sarah," he said urgently, "I need your help. They're after the artifact."
"""


@pytest.fixture
def sample_novel_file(temp_settings_dir, sample_novel_content):
    """
    Create a temporary novel file.
    """
    novel_path = Path(temp_settings_dir) / "test_novel.txt"
    novel_path.write_text(sample_novel_content, encoding="utf-8")
    return str(novel_path)


@pytest.fixture
def settings_manager_with_temp_dir(temp_settings_dir):
    """
    Create settings manager with temporary directory.
    """
    return SettingsManager(settings_dir=temp_settings_dir)


@pytest.fixture
def context_manager():
    """
    Create context manager for testing.
    """
    return ContextManager(model="gpt-4", max_tokens=8192)
