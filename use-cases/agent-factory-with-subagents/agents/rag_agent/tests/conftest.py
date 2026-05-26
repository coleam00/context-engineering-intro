"""Test configuration and fixtures for Semantic Search Agent tests."""

import pytest
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from unittest.mock import AsyncMock, MagicMock
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelTextResponse

# Import the agent components
from ..agent import search_agent
from ..dependencies import AgentDependencies
from ..settings import Settings
from ..tools import SearchResult


@pytest.fixture
def test_settings():
    """Create test settings object."""
    return Settings(
        database_url="postgresql://test:test@localhost/test",
        openai_api_key="test_key",
        llm_model="gpt-4o-mini",
        embedding_model="text-embedding-3-small",
        default_match_count=10,
        max_match_count=50,
        default_text_weight=0.3,
        db_pool_min_size=1,
        db_pool_max_size=5,
        embedding_dimension=1536
    )


@pytest.fixture
def mock_db_pool():
    """Create mock database pool."""
    pool = AsyncMock()
    connection = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = connection
    pool.acquire.return_value.__aexit__.return_value = None
    return pool, connection


@pytest.fixture
def mock_openai_client():
    """Create mock OpenAI client."""
    client = AsyncMock()
    
    # Mock embedding response
    embedding_response = MagicMock()
    embedding_response.data = [MagicMock()]
    embedding_response.data[0].embedding = [0.1] * 1536  # 1536-dimensional vector
    client.embeddings.create.return_value = embedding_response
    
    return client


@pytest.fixture
async def test_dependencies(test_settings, mock_db_pool, mock_openai_client):
    """Create test dependencies with mocked external services."""
    pool, connection = mock_db_pool
    
    deps = AgentDependencies(
        db_pool=pool,
        openai_client=mock_openai_client,
        settings=test_settings,
        session_id="test_session",
        user_preferences={},
        query_history=[]
    )
    
    return deps, connection


@pytest.fixture
def sample_search_results():
    """Create sample search results for testing."""
    return [
        SearchResult(
            chunk_id="chunk_1",
            document_id="doc_1",
            content="This is a sample chunk about Python programming.",
            similarity=0.85,
            metadata={"page": 1},
            document_title="Python Tutorial",
            document_source="tutorial.pdf"
        ),
        SearchResult(
            chunk_id="chunk_2", 
            document_id="doc_2",
            content="Advanced concepts in machine learning and AI.",
            similarity=0.78,
            metadata={"page": 5},
            document_title="ML Guide",
            document_source="ml_guide.pdf"
        )
    ]


@pytest.fixture
def sample_hybrid_results():
    """Create sample hybrid search results for testing."""
    return [
        {
            'chunk_id': 'chunk_1',
            'document_id': 'doc_1', 
            'content': 'This is a sample chunk about Python programming.',
            'combined_score': 0.85,
            'vector_similarity': 0.80,
            'text_similarity': 0.90,
            'metadata': {'page': 1},
            'document_title': 'Python Tutorial',
            'document_source': 'tutorial.pdf'
        },
        {
            'chunk_id': 'chunk_2',
            'document_id': 'doc_2',
            'content': 'Advanced concepts in machine learning and AI.',
            'combined_score': 0.78,
            'vector_similarity': 0.75,
            'text_similarity': 0.82,
            'metadata': {'page': 5}, 
            'document_title': 'ML Guide',
            'document_source': 'ml_guide.pdf'
        }
    ]


@pytest.fixture
def test_model():
    """Create TestModel for fast agent testing."""
    return TestModel()


@pytest.fixture
def test_agent(test_model):
    """Create agent with TestModel for testing."""
    return search_agent.override(model=test_model)


def create_search_function_model(search_results: List[Dict[str, Any]]) -> FunctionModel:
    """
    Create FunctionModel that simulates search behavior.
    
    Args:
        search_results: Expected search results to return
    
    Returns:
        Configured FunctionModel
    """
    call_count = 0
    
    async def search_function(messages, tools):
        nonlocal call_count
        call_count += 1
        
        if call_count == 1:
            # First call - analyze and decide to search
            return ModelTextResponse(
                content="I'll search the knowledge base for relevant information."
            )
        elif call_count == 2:
            # Second call - perform the search
            return {
                "auto_search": {
                    "query": "test query",
                    "match_count": 10
                }
            }
        else:
            # Final response with summary
            return ModelTextResponse(
                content="Based on the search results, I found relevant information about your query. The results show key insights that address your question."
            )
    
    return FunctionModel(search_function)


@pytest.fixture
def function_model_with_search(sample_search_results):
    """Create FunctionModel configured for search testing."""
    return create_search_function_model([r.dict() for r in sample_search_results])


@pytest.fixture  
def mock_database_responses():
    """Mock database query responses."""
    return {
        'semantic_search': [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'This is a sample chunk about Python programming.',
                'similarity': 0.85,
                'metadata': {'page': 1},
                'document_title': 'Python Tutorial', 
                'document_source': 'tutorial.pdf'
            }
        ],
        'hybrid_search': [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'This is a sample chunk about Python programming.',
                'combined_score': 0.85,
                'vector_similarity': 0.80,
                'text_similarity': 0.90,
                'metadata': {'page': 1},
                'document_title': 'Python Tutorial',
                'document_source': 'tutorial.pdf'
            }
        ]
    }


# Test event loop configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Helper functions for tests
def assert_search_result_valid(result: SearchResult):
    """Assert that a SearchResult object is valid."""
    assert isinstance(result.chunk_id, str)
    assert isinstance(result.document_id, str)
    assert isinstance(result.content, str)
    assert isinstance(result.similarity, float)
    assert 0 <= result.similarity <= 1
    assert isinstance(result.metadata, dict)
    assert isinstance(result.document_title, str)
    assert isinstance(result.document_source, str)


def assert_hybrid_result_valid(result: Dict[str, Any]):
    """Assert that a hybrid search result dictionary is valid."""
    required_keys = [
        'chunk_id', 'document_id', 'content', 'combined_score',
        'vector_similarity', 'text_similarity', 'metadata',
        'document_title', 'document_source'
    ]
    
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"
    
    # Validate score ranges
    assert 0 <= result['combined_score'] <= 1
    assert 0 <= result['vector_similarity'] <= 1
    assert 0 <= result['text_similarity'] <= 1


def create_mock_agent_response(summary: str, sources: List[str] = None) -> str:
    """Create a mock agent response for testing."""
    if sources is None:
        sources = ["Python Tutorial", "ML Guide"]
    
    response_parts = [
        f"Summary: {summary}",
        "",
        "Key findings:",
        "- Finding 1", 
        "- Finding 2",
        "",
        "Sources:",
    ]
    
    for source in sources:
        response_parts.append(f"- {source}")
    
    return "\n".join(response_parts)