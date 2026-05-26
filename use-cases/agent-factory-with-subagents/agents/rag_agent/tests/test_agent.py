"""Test core agent functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelTextResponse

from ..agent import search_agent, search, SearchResponse, interactive_search
from ..dependencies import AgentDependencies


class TestAgentInitialization:
    """Test agent initialization and configuration."""
    
    def test_agent_has_correct_model_type(self, test_agent):
        """Test agent is configured with correct model type."""
        assert test_agent.model is not None
        assert isinstance(test_agent.model, TestModel)
    
    def test_agent_has_dependencies_type(self, test_agent):
        """Test agent has correct dependencies type."""
        assert test_agent.deps_type == AgentDependencies
    
    def test_agent_has_system_prompt(self, test_agent):
        """Test agent has system prompt configured."""
        assert test_agent.system_prompt is not None
        assert len(test_agent.system_prompt) > 0
        assert "semantic search" in test_agent.system_prompt.lower()
    
    def test_agent_has_registered_tools(self, test_agent):
        """Test agent has all required tools registered."""
        tool_names = [tool.name for tool in test_agent.tool_defs]
        expected_tools = ['semantic_search', 'hybrid_search', 'auto_search', 'set_search_preference']
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Missing tool: {expected_tool}"


class TestAgentBasicFunctionality:
    """Test basic agent functionality with TestModel."""
    
    @pytest.mark.asyncio
    async def test_agent_responds_to_simple_query(self, test_agent, test_dependencies):
        """Test agent provides response to simple query."""
        deps, connection = test_dependencies
        
        result = await test_agent.run(
            "Search for Python tutorials",
            deps=deps
        )
        
        assert result.data is not None
        assert isinstance(result.data, str)
        assert len(result.all_messages()) > 0
    
    @pytest.mark.asyncio 
    async def test_agent_with_empty_query(self, test_agent, test_dependencies):
        """Test agent handles empty query gracefully."""
        deps, connection = test_dependencies
        
        result = await test_agent.run("", deps=deps)
        
        # Should still provide a response
        assert result.data is not None
        assert isinstance(result.data, str)
    
    @pytest.mark.asyncio
    async def test_agent_with_long_query(self, test_agent, test_dependencies):
        """Test agent handles long queries."""
        deps, connection = test_dependencies
        
        long_query = "This is a very long query " * 50  # 350+ characters
        result = await test_agent.run(long_query, deps=deps)
        
        assert result.data is not None
        assert isinstance(result.data, str)


class TestAgentToolCalling:
    """Test agent tool calling behavior."""
    
    @pytest.mark.asyncio
    async def test_agent_calls_search_tools(self, test_dependencies, mock_database_responses):
        """Test agent calls appropriate search tools."""
        deps, connection = test_dependencies
        
        # Configure mock database responses
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        # Create function model that calls tools
        call_count = 0
        
        async def search_function(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll search for that information.")
            elif call_count == 2:
                return {"auto_search": {"query": "test query", "match_count": 10}}
            else:
                return ModelTextResponse(content="Based on the search results, here's what I found...")
        
        function_model = FunctionModel(search_function)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Search for Python tutorials", deps=deps)
        
        # Verify tool was called
        messages = result.all_messages()
        tool_calls = [msg for msg in messages if hasattr(msg, 'tool_name')]
        assert len(tool_calls) > 0, "No tool calls found"
        
        # Verify auto_search was called
        auto_search_calls = [msg for msg in tool_calls if getattr(msg, 'tool_name', None) == 'auto_search']
        assert len(auto_search_calls) > 0, "auto_search tool was not called"
    
    @pytest.mark.asyncio
    async def test_agent_calls_preference_tool(self, test_dependencies):
        """Test agent calls preference setting tool."""
        deps, connection = test_dependencies
        
        call_count = 0
        
        async def preference_function(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return {"set_search_preference": {"preference_type": "search_type", "value": "semantic"}}
            else:
                return ModelTextResponse(content="Preference set successfully.")
        
        function_model = FunctionModel(preference_function)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Set search preference to semantic", deps=deps)
        
        # Verify preference was set
        assert deps.user_preferences.get('search_type') == 'semantic'
        assert result.data is not None


class TestSearchFunction:
    """Test the standalone search function."""
    
    @pytest.mark.asyncio
    async def test_search_function_with_defaults(self):
        """Test search function with default parameters."""
        with patch('..agent.search_agent') as mock_agent:
            # Mock agent run result
            mock_result = AsyncMock()
            mock_result.data = "Search results found"
            mock_agent.run.return_value = mock_result
            
            response = await search("test query")
            
            assert isinstance(response, SearchResponse)
            assert response.summary == "Search results found"
            assert response.search_strategy == "auto"
            assert response.result_count == 10
    
    @pytest.mark.asyncio
    async def test_search_function_with_custom_params(self):
        """Test search function with custom parameters."""
        with patch('..agent.search_agent') as mock_agent:
            mock_result = AsyncMock() 
            mock_result.data = "Custom search results"
            mock_agent.run.return_value = mock_result
            
            response = await search(
                query="custom query",
                search_type="semantic",
                match_count=20,
                text_weight=0.5
            )
            
            assert isinstance(response, SearchResponse)
            assert response.summary == "Custom search results"
            assert response.result_count == 20
    
    @pytest.mark.asyncio
    async def test_search_function_with_existing_deps(self, test_dependencies):
        """Test search function with provided dependencies."""
        deps, connection = test_dependencies
        
        with patch('..agent.search_agent') as mock_agent:
            mock_result = AsyncMock()
            mock_result.data = "Search with deps"
            mock_agent.run.return_value = mock_result
            
            response = await search("test query", deps=deps)
            
            assert isinstance(response, SearchResponse)
            assert response.summary == "Search with deps"
            # Should not call cleanup since deps were provided
            assert deps.db_pool is not None


class TestInteractiveSearch:
    """Test interactive search functionality."""
    
    @pytest.mark.asyncio
    async def test_interactive_search_creates_deps(self):
        """Test interactive search creates new dependencies."""
        with patch.object(AgentDependencies, 'initialize') as mock_init:
            deps = await interactive_search()
            
            assert isinstance(deps, AgentDependencies)
            assert deps.session_id is not None
            mock_init.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_interactive_search_reuses_deps(self, test_dependencies):
        """Test interactive search reuses existing dependencies."""
        existing_deps, connection = test_dependencies
        
        deps = await interactive_search(existing_deps)
        
        assert deps is existing_deps
        assert deps.session_id == "test_session"


class TestAgentErrorHandling:
    """Test agent error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_agent_handles_database_error(self, test_agent, test_dependencies):
        """Test agent handles database connection errors."""
        deps, connection = test_dependencies
        
        # Simulate database error
        connection.fetch.side_effect = Exception("Database connection failed")
        
        # Should not raise exception, agent should handle gracefully
        result = await test_agent.run("Search for something", deps=deps)
        
        assert result.data is not None
        # Agent should provide some response even if search fails
        assert isinstance(result.data, str)
    
    @pytest.mark.asyncio
    async def test_agent_handles_invalid_dependencies(self, test_agent):
        """Test agent behavior with invalid dependencies."""
        # Create deps without proper initialization
        invalid_deps = AgentDependencies()
        
        # Should handle missing database pool gracefully
        result = await test_agent.run("Search query", deps=invalid_deps)
        
        assert result.data is not None
        assert isinstance(result.data, str)


class TestAgentResponseQuality:
    """Test quality of agent responses."""
    
    @pytest.mark.asyncio
    async def test_agent_response_mentions_search(self, test_agent, test_dependencies):
        """Test agent response mentions search-related terms."""
        deps, connection = test_dependencies
        
        result = await test_agent.run("Find information about machine learning", deps=deps)
        
        response_lower = result.data.lower()
        search_terms = ['search', 'find', 'information', 'results']
        
        # At least one search-related term should be mentioned
        assert any(term in response_lower for term in search_terms)
    
    @pytest.mark.asyncio
    async def test_agent_response_reasonable_length(self, test_agent, test_dependencies):
        """Test agent responses are reasonable length."""
        deps, connection = test_dependencies
        
        result = await test_agent.run("What is Python?", deps=deps)
        
        # Response should be substantial but not excessive
        assert 10 <= len(result.data) <= 2000
    
    @pytest.mark.asyncio
    async def test_agent_handles_different_query_types(self, test_agent, test_dependencies):
        """Test agent handles different types of queries."""
        deps, connection = test_dependencies
        
        queries = [
            "What is Python?",  # Conceptual
            "Find exact quote about 'machine learning'",  # Exact match
            "Show me tutorials",  # General
            "API documentation for requests library"  # Technical
        ]
        
        for query in queries:
            result = await test_agent.run(query, deps=deps)
            
            assert result.data is not None
            assert isinstance(result.data, str)
            assert len(result.data) > 0


class TestAgentMemoryAndContext:
    """Test agent memory and context handling."""
    
    @pytest.mark.asyncio
    async def test_agent_maintains_session_context(self, test_dependencies):
        """Test agent can maintain session context."""
        deps, connection = test_dependencies
        
        # Set some preferences
        deps.set_user_preference('search_type', 'semantic')
        deps.add_to_history('previous query')
        
        test_agent = search_agent.override(model=TestModel())
        
        result = await test_agent.run("Another query", deps=deps)
        
        # Verify context is maintained
        assert deps.user_preferences['search_type'] == 'semantic'
        assert 'previous query' in deps.query_history
        assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_agent_query_history_limit(self, test_dependencies):
        """Test query history is properly limited."""
        deps, connection = test_dependencies
        
        # Add more than 10 queries
        for i in range(15):
            deps.add_to_history(f"query {i}")
        
        # Should only keep last 10
        assert len(deps.query_history) == 10
        assert deps.query_history[0] == "query 5"
        assert deps.query_history[-1] == "query 14"