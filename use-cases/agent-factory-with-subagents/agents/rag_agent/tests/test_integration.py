"""End-to-end integration tests for Semantic Search Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelTextResponse

from ..agent import search_agent, search, interactive_search, SearchResponse
from ..dependencies import AgentDependencies
from ..settings import load_settings
from ..tools import semantic_search, hybrid_search, auto_search


class TestEndToEndSearch:
    """Test complete search workflows from query to response."""
    
    @pytest.mark.asyncio
    async def test_complete_semantic_search_workflow(self, test_dependencies, sample_search_results):
        """Test complete semantic search workflow."""
        deps, connection = test_dependencies
        
        # Mock database results
        db_results = [
            {
                'chunk_id': r.chunk_id,
                'document_id': r.document_id,
                'content': r.content,
                'similarity': r.similarity,
                'metadata': r.metadata,
                'document_title': r.document_title,
                'document_source': r.document_source
            }
            for r in sample_search_results
        ]
        connection.fetch.return_value = db_results
        
        # Create function model that simulates complete workflow
        call_count = 0
        
        async def search_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll search for Python programming information.")
            elif call_count == 2:
                return {"auto_search": {"query": "Python programming", "match_count": 10}}
            else:
                return ModelTextResponse(
                    content="Based on my search, I found relevant information about Python programming. "
                           "The results include tutorials and guides that explain Python concepts and syntax. "
                           "Key sources include Python Tutorial and ML Guide documents."
                )
        
        function_model = FunctionModel(search_workflow)
        test_agent = search_agent.override(model=function_model)
        
        # Run complete workflow
        result = await test_agent.run("Find information about Python programming", deps=deps)
        
        # Verify workflow completed
        assert result.data is not None
        assert "Python programming" in result.data
        assert "search" in result.data.lower()
        
        # Verify database was queried
        connection.fetch.assert_called()
        
        # Verify embedding was generated
        deps.openai_client.embeddings.create.assert_called()
    
    @pytest.mark.asyncio
    async def test_complete_hybrid_search_workflow(self, test_dependencies, sample_hybrid_results):
        """Test complete hybrid search workflow."""
        deps, connection = test_dependencies
        connection.fetch.return_value = sample_hybrid_results
        
        # Set preference for hybrid search
        deps.set_user_preference('search_type', 'hybrid')
        
        call_count = 0
        
        async def hybrid_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll perform a hybrid search combining semantic and keyword matching.")
            elif call_count == 2:
                return {"auto_search": {"query": "exact Python syntax", "match_count": 15}}
            else:
                return ModelTextResponse(
                    content="The hybrid search found precise matches for Python syntax. "
                           "Results combine semantic similarity with exact keyword matching. "
                           "This approach is ideal for finding specific technical information."
                )
        
        function_model = FunctionModel(hybrid_workflow)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Find exact Python syntax examples", deps=deps)
        
        assert result.data is not None
        assert "hybrid search" in result.data or "Python syntax" in result.data
        
        # Verify user preference was considered
        assert deps.user_preferences['search_type'] == 'hybrid'
        
        # Verify query was added to history
        assert "Find exact Python syntax examples" in deps.query_history or len(deps.query_history) > 0
    
    @pytest.mark.asyncio
    async def test_search_function_integration(self, mock_database_responses):
        """Test the search function with realistic agent interaction."""
        with patch('..agent.search_agent') as mock_agent:
            # Mock agent behavior
            mock_result = AsyncMock()
            mock_result.data = "Comprehensive search results found. The analysis shows relevant information about machine learning concepts and Python implementations."
            mock_agent.run.return_value = mock_result
            
            # Mock dependency initialization
            with patch.object(AgentDependencies, 'initialize') as mock_init:
                with patch.object(AgentDependencies, 'cleanup') as mock_cleanup:
                    
                    response = await search(
                        query="machine learning with Python",
                        search_type="auto",
                        match_count=20,
                        text_weight=0.4
                    )
                    
                    # Verify response structure
                    assert isinstance(response, SearchResponse)
                    assert response.summary == mock_result.data
                    assert response.search_strategy == "auto"
                    assert response.result_count == 20
                    
                    # Verify agent was called
                    mock_agent.run.assert_called_once()
                    
                    # Verify dependency lifecycle
                    mock_init.assert_called_once()
                    mock_cleanup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_interactive_session_workflow(self, test_dependencies):
        """Test interactive session maintains state across queries."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Initialize interactive session
        session_deps = await interactive_search(deps)
        
        # Verify session is properly initialized
        assert session_deps is deps
        assert session_deps.session_id is not None
        
        # Simulate multiple queries in same session
        queries = [
            "What is Python?",
            "How does machine learning work?", 
            "Show me examples of neural networks"
        ]
        
        call_count = 0
        
        async def session_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count % 2 == 1:  # Odd calls - analysis
                return ModelTextResponse(content="I'll search for information about your query.")
            else:  # Even calls - tool calls
                return {"auto_search": {"query": queries[(call_count // 2) - 1], "match_count": 10}}
        
        function_model = FunctionModel(session_workflow)
        test_agent = search_agent.override(model=function_model)
        
        # Run multiple searches in session
        for query in queries:
            result = await test_agent.run(query, deps=session_deps)
            assert result.data is not None
        
        # Verify session state is maintained
        assert len(session_deps.query_history) == len(queries)
        assert all(q in session_deps.query_history for q in queries)
    
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(self, test_dependencies):
        """Test system recovers from errors gracefully."""
        deps, connection = test_dependencies
        
        # First call fails, second succeeds
        connection.fetch.side_effect = [
            Exception("Database connection failed"),
            [{'chunk_id': 'chunk_1', 'document_id': 'doc_1', 'content': 'Recovery test',
              'similarity': 0.9, 'metadata': {}, 'document_title': 'Test Doc', 
              'document_source': 'test.pdf'}]
        ]
        
        call_count = 0
        
        async def error_recovery_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll try to search for information.")
            elif call_count == 2:
                return {"auto_search": {"query": "test query", "match_count": 10}}
            elif call_count == 3:
                return ModelTextResponse(content="The first search failed, let me try again.")
            elif call_count == 4:
                return {"auto_search": {"query": "test query", "match_count": 10}}
            else:
                return ModelTextResponse(content="Successfully recovered and found information.")
        
        function_model = FunctionModel(error_recovery_workflow)
        test_agent = search_agent.override(model=function_model)
        
        # First attempt should handle error gracefully
        result1 = await test_agent.run("Test error recovery", deps=deps)
        assert result1.data is not None
        
        # Second attempt should succeed
        result2 = await test_agent.run("Test successful recovery", deps=deps)
        assert result2.data is not None
        assert "Successfully recovered" in result2.data


class TestCrossComponentIntegration:
    """Test integration between different agent components."""
    
    @pytest.mark.asyncio
    async def test_settings_to_dependencies_integration(self):
        """Test settings are properly integrated into dependencies."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb',
            'OPENAI_API_KEY': 'test_openai_key',
            'LLM_MODEL': 'gpt-4',
            'DEFAULT_MATCH_COUNT': '25',
            'MAX_MATCH_COUNT': '100'
        }):
            settings = load_settings()
            
            with patch('asyncpg.create_pool') as mock_create_pool:
                with patch('openai.AsyncOpenAI') as mock_openai:
                    mock_pool = AsyncMock()
                    mock_client = AsyncMock()
                    mock_create_pool.return_value = mock_pool
                    mock_openai.return_value = mock_client
                    
                    deps = AgentDependencies()
                    deps.settings = settings
                    await deps.initialize()
                    
                    # Verify settings values are used
                    assert deps.settings.database_url == 'postgresql://test:test@localhost:5432/testdb'
                    assert deps.settings.openai_api_key == 'test_openai_key'
                    assert deps.settings.llm_model == 'gpt-4'
                    assert deps.settings.default_match_count == 25
                    assert deps.settings.max_match_count == 100
                    
                    # Verify pool created with correct settings
                    mock_create_pool.assert_called_once_with(
                        'postgresql://test:test@localhost:5432/testdb',
                        min_size=deps.settings.db_pool_min_size,
                        max_size=deps.settings.db_pool_max_size
                    )
                    
                    # Verify OpenAI client created with correct key
                    mock_openai.assert_called_once_with(
                        api_key='test_openai_key'
                    )
    
    @pytest.mark.asyncio
    async def test_tools_to_agent_integration(self, test_dependencies, sample_search_results):
        """Test tools are properly integrated with the agent."""
        deps, connection = test_dependencies
        
        # Mock different tool results
        semantic_results = [
            {
                'chunk_id': r.chunk_id,
                'document_id': r.document_id,
                'content': r.content,
                'similarity': r.similarity,
                'metadata': r.metadata,
                'document_title': r.document_title,
                'document_source': r.document_source
            }
            for r in sample_search_results
        ]
        
        hybrid_results = [
            {
                'chunk_id': r.chunk_id,
                'document_id': r.document_id,
                'content': r.content,
                'combined_score': r.similarity,
                'vector_similarity': r.similarity,
                'text_similarity': r.similarity - 0.1,
                'metadata': r.metadata,
                'document_title': r.document_title,
                'document_source': r.document_source
            }
            for r in sample_search_results
        ]
        
        connection.fetch.side_effect = [semantic_results, hybrid_results, semantic_results]
        
        # Test all tools work with agent
        call_count = 0
        
        async def multi_tool_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return {"semantic_search": {"query": "test semantic", "match_count": 5}}
            elif call_count == 2:
                return {"hybrid_search": {"query": "test hybrid", "match_count": 5, "text_weight": 0.4}}
            elif call_count == 3:
                return {"auto_search": {"query": "test auto", "match_count": 5}}
            else:
                return ModelTextResponse(content="All search tools tested successfully.")
        
        function_model = FunctionModel(multi_tool_workflow)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Test all search tools", deps=deps)
        
        # Verify all tools were called
        assert connection.fetch.call_count >= 3
        assert result.data is not None
        assert "successfully" in result.data.lower()
    
    @pytest.mark.asyncio
    async def test_preferences_across_tools(self, test_dependencies, sample_hybrid_results):
        """Test user preferences work consistently across all tools."""
        deps, connection = test_dependencies
        connection.fetch.return_value = sample_hybrid_results
        
        # Set user preferences
        deps.set_user_preference('search_type', 'hybrid')
        deps.set_user_preference('text_weight', 0.7)
        deps.set_user_preference('result_count', 15)
        
        # Test preferences are used by auto_search
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        result = await auto_search(ctx, "test query with preferences")
        
        # Should use user preference for search type
        assert result['strategy'] == 'hybrid'
        assert result['reason'] == 'User preference'
        
        # Verify database call used preference values
        connection.fetch.assert_called()
        args = connection.fetch.call_args[0]
        assert args[4] == 0.7  # text_weight parameter
    
    @pytest.mark.asyncio
    async def test_query_history_integration(self, test_dependencies):
        """Test query history is maintained across all interactions."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Make multiple searches that should add to history
        test_queries = [
            "First search query",
            "Second search about AI", 
            "Third query on machine learning",
            "Fourth search on Python"
        ]
        
        for query in test_queries:
            await auto_search(ctx, query)
        
        # Verify all queries added to history
        assert len(deps.query_history) == len(test_queries)
        for query in test_queries:
            assert query in deps.query_history
        
        # Verify history order is maintained
        assert deps.query_history == test_queries


class TestPerformanceIntegration:
    """Test performance aspects of integrated system."""
    
    @pytest.mark.asyncio
    async def test_concurrent_search_requests(self, test_dependencies):
        """Test system handles concurrent search requests."""
        deps, connection = test_dependencies
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'Concurrent test content',
                'similarity': 0.8,
                'metadata': {},
                'document_title': 'Test Doc',
                'document_source': 'test.pdf'
            }
        ]
        
        # Create multiple search tasks
        async def single_search(query_id):
            from pydantic_ai import RunContext
            ctx = RunContext(deps=deps)
            return await semantic_search(ctx, f"Query {query_id}")
        
        # Run concurrent searches
        tasks = [single_search(i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All should complete successfully
        assert len(results) == 5
        for result in results:
            assert isinstance(result, list)
            assert len(result) > 0
        
        # Should have made multiple database calls
        assert connection.fetch.call_count == 5
    
    @pytest.mark.asyncio
    async def test_large_result_set_processing(self, test_dependencies):
        """Test system handles large result sets efficiently."""
        deps, connection = test_dependencies
        
        # Create large result set
        large_results = []
        for i in range(50):  # Maximum allowed results
            large_results.append({
                'chunk_id': f'chunk_{i}',
                'document_id': f'doc_{i}',
                'content': f'Content {i} with substantial text for testing performance',
                'similarity': 0.9 - (i * 0.01),
                'metadata': {'page': i, 'section': f'Section {i}'},
                'document_title': f'Document {i}',
                'document_source': f'source_{i}.pdf'
            })
        
        connection.fetch.return_value = large_results
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Process large result set
        results = await semantic_search(ctx, "large dataset query", match_count=50)
        
        # Should handle all results efficiently
        assert len(results) == 50
        assert all(r.similarity >= 0.4 for r in results)  # All should have reasonable similarity
        assert results[0].similarity > results[-1].similarity  # Should be ordered by similarity
    
    @pytest.mark.asyncio
    async def test_embedding_generation_performance(self, test_dependencies):
        """Test embedding generation performance."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Test embedding generation for various text lengths
        test_texts = [
            "Short query",
            "Medium length query with more words and details about the search topic",
            "Very long query " * 100  # Very long text
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        for text in test_texts:
            result = await semantic_search(ctx, text)
            assert isinstance(result, list)
        
        # Should have generated embeddings for all texts
        assert deps.openai_client.embeddings.create.call_count == len(test_texts)


class TestRobustnessIntegration:
    """Test system robustness and error handling."""
    
    @pytest.mark.asyncio
    async def test_network_failure_recovery(self, test_dependencies):
        """Test system handles network failures gracefully."""
        deps, connection = test_dependencies
        
        # Simulate network failure then recovery
        deps.openai_client.embeddings.create.side_effect = [
            ConnectionError("Network unavailable"),
            MagicMock(data=[MagicMock(embedding=[0.1] * 1536)])
        ]
        
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # First call should fail
        with pytest.raises(ConnectionError):
            await semantic_search(ctx, "network test query")
        
        # Second call should succeed after "network recovery"
        result = await semantic_search(ctx, "recovery test query")
        assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_database_transaction_handling(self, test_dependencies):
        """Test proper database transaction handling."""
        deps, connection = test_dependencies
        
        # Simulate database transaction scenarios
        connection.fetch.side_effect = [
            Exception("Database locked"),
            [{'chunk_id': 'chunk_1', 'document_id': 'doc_1', 'content': 'Recovery success',
              'similarity': 0.95, 'metadata': {}, 'document_title': 'Test', 'document_source': 'test.pdf'}]
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # First attempt fails
        with pytest.raises(Exception, match="Database locked"):
            await semantic_search(ctx, "transaction test")
        
        # Subsequent attempt succeeds
        result = await semantic_search(ctx, "transaction recovery")
        assert len(result) == 1
        assert result[0].content == "Recovery success"
    
    @pytest.mark.asyncio
    async def test_memory_management_with_large_sessions(self, test_dependencies):
        """Test memory management with large interactive sessions."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Simulate large number of queries in session
        for i in range(20):  # More than history limit
            deps.add_to_history(f"Query number {i} with detailed content about search topics")
        
        # History should be properly limited
        assert len(deps.query_history) == 10
        assert deps.query_history[0] == "Query number 10 with detailed content about search topics"
        assert deps.query_history[-1] == "Query number 19 with detailed content about search topics"
        
        # User preferences should still work
        deps.set_user_preference('search_type', 'semantic')
        assert deps.user_preferences['search_type'] == 'semantic'
    
    @pytest.mark.asyncio
    async def test_cleanup_after_errors(self, test_dependencies):
        """Test proper cleanup occurs even after errors."""
        deps, connection = test_dependencies
        
        # Simulate error during operation
        connection.fetch.side_effect = Exception("Critical database error")
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        try:
            await semantic_search(ctx, "cleanup test")
        except Exception:
            pass  # Expected to fail
        
        # Dependencies should still be in valid state for cleanup
        assert deps.db_pool is not None
        assert deps.openai_client is not None
        
        # Cleanup should work normally
        await deps.cleanup()
        assert deps.db_pool is None


class TestScenarioIntegration:
    """Test realistic usage scenarios end-to-end."""
    
    @pytest.mark.asyncio
    async def test_research_workflow_scenario(self, test_dependencies):
        """Test complete research workflow scenario."""
        deps, connection = test_dependencies
        
        # Mock research-relevant results
        research_results = [
            {
                'chunk_id': 'research_1',
                'document_id': 'paper_1', 
                'content': 'Neural networks are computational models inspired by biological neural networks.',
                'similarity': 0.92,
                'metadata': {'type': 'research_paper', 'year': 2023},
                'document_title': 'Deep Learning Fundamentals',
                'document_source': 'nature_ml.pdf'
            },
            {
                'chunk_id': 'research_2',
                'document_id': 'paper_2',
                'content': 'Machine learning algorithms can be broadly categorized into supervised and unsupervised learning.',
                'similarity': 0.88,
                'metadata': {'type': 'textbook', 'chapter': 3},
                'document_title': 'ML Textbook',
                'document_source': 'ml_book.pdf'
            }
        ]
        connection.fetch.return_value = research_results
        
        # Simulate research workflow
        research_queries = [
            "What are neural networks?",
            "Types of machine learning algorithms", 
            "Deep learning applications"
        ]
        
        call_count = 0
        
        async def research_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count % 2 == 1:  # Analysis calls
                return ModelTextResponse(content="I'll search for research information on this topic.")
            else:  # Tool calls
                query_idx = (call_count // 2) - 1
                if query_idx < len(research_queries):
                    return {"auto_search": {"query": research_queries[query_idx], "match_count": 10}}
                else:
                    return ModelTextResponse(content="Research workflow completed successfully.")
        
        function_model = FunctionModel(research_workflow)
        test_agent = search_agent.override(model=function_model)
        
        # Execute research workflow
        for query in research_queries:
            result = await test_agent.run(query, deps=deps)
            assert result.data is not None
            assert "search" in result.data.lower() or "research" in result.data.lower()
        
        # Verify research context maintained
        assert len(deps.query_history) == len(research_queries)
        assert all(q in deps.query_history for q in research_queries)
    
    @pytest.mark.asyncio
    async def test_troubleshooting_workflow_scenario(self, test_dependencies):
        """Test troubleshooting workflow with specific technical queries."""
        deps, connection = test_dependencies
        
        # Mock technical troubleshooting results
        tech_results = [
            {
                'chunk_id': 'tech_1',
                'document_id': 'docs_1',
                'content': 'ImportError: No module named sklearn. Solution: pip install scikit-learn',
                'combined_score': 0.95,
                'vector_similarity': 0.90,
                'text_similarity': 1.0,
                'metadata': {'type': 'troubleshooting', 'language': 'python'},
                'document_title': 'Python Error Solutions',
                'document_source': 'python_docs.pdf'
            }
        ]
        connection.fetch.return_value = tech_results
        
        # Set preference for exact matching
        deps.set_user_preference('search_type', 'hybrid')
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Perform technical search
        result = await auto_search(ctx, 'ImportError: No module named sklearn')
        
        # Should use hybrid search for exact technical terms
        assert result['strategy'] == 'hybrid'
        assert result['reason'] == 'User preference'
        assert len(result['results']) > 0
        
        # Verify technical content found
        tech_content = result['results'][0]
        assert 'ImportError' in tech_content['content']
        assert 'sklearn' in tech_content['content']
    
    @pytest.mark.asyncio
    async def test_learning_workflow_scenario(self, test_dependencies):
        """Test learning workflow with progressive queries."""
        deps, connection = test_dependencies
        
        learning_results = [
            {
                'chunk_id': 'learn_1',
                'document_id': 'tutorial_1',
                'content': 'Python basics: Variables store data values. Example: x = 5',
                'similarity': 0.85,
                'metadata': {'difficulty': 'beginner', 'topic': 'variables'},
                'document_title': 'Python Basics Tutorial',
                'document_source': 'python_tutorial.pdf'
            }
        ]
        connection.fetch.return_value = learning_results
        
        # Simulate progressive learning queries
        learning_progression = [
            "Python basics for beginners",
            "Python variables and data types",
            "Python functions and methods",
            "Advanced Python concepts"
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Perform progressive searches
        for i, query in enumerate(learning_progression):
            result = await auto_search(ctx, query)
            
            # Should find relevant educational content
            assert result['strategy'] in ['semantic', 'hybrid']
            assert len(result['results']) > 0
            
            # Verify query added to history
            assert query in deps.query_history
        
        # Verify complete learning history maintained
        assert len(deps.query_history) == len(learning_progression)
        
        # History should show learning progression
        for query in learning_progression:
            assert query in deps.query_history