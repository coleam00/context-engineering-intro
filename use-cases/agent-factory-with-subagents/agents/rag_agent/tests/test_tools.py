"""Test search tools functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from pydantic_ai import RunContext

from ..tools import semantic_search, hybrid_search, auto_search, SearchResult
from ..dependencies import AgentDependencies


class TestSemanticSearch:
    """Test semantic search tool functionality."""
    
    @pytest.mark.asyncio
    async def test_semantic_search_basic(self, test_dependencies, mock_database_responses):
        """Test basic semantic search functionality."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "Python programming")
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], SearchResult)
        assert results[0].similarity >= 0.7  # Quality threshold
    
    @pytest.mark.asyncio
    async def test_semantic_search_with_custom_count(self, test_dependencies, mock_database_responses):
        """Test semantic search with custom match count."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "Python programming", match_count=5)
        
        # Verify correct parameters passed to database
        connection.fetch.assert_called_once()
        args = connection.fetch.call_args[0]
        assert args[2] == 5  # match_count parameter
    
    @pytest.mark.asyncio
    async def test_semantic_search_respects_max_count(self, test_dependencies, mock_database_responses):
        """Test semantic search respects maximum count limit."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        # Request more than max allowed
        results = await semantic_search(ctx, "Python programming", match_count=100)
        
        # Should be limited to max_match_count (50)
        connection.fetch.assert_called_once()
        args = connection.fetch.call_args[0]
        assert args[2] == deps.settings.max_match_count
    
    @pytest.mark.asyncio
    async def test_semantic_search_generates_embedding(self, test_dependencies, mock_database_responses):
        """Test semantic search generates query embedding."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        await semantic_search(ctx, "Python programming")
        
        # Verify embedding was generated
        deps.openai_client.embeddings.create.assert_called_once()
        call_args = deps.openai_client.embeddings.create.call_args
        assert call_args[1]['input'] == "Python programming"
        assert call_args[1]['model'] == deps.settings.embedding_model
    
    @pytest.mark.asyncio
    async def test_semantic_search_database_error(self, test_dependencies):
        """Test semantic search handles database errors."""
        deps, connection = test_dependencies
        connection.fetch.side_effect = Exception("Database error")
        
        ctx = RunContext(deps=deps)
        
        with pytest.raises(Exception, match="Database error"):
            await semantic_search(ctx, "Python programming")
    
    @pytest.mark.asyncio
    async def test_semantic_search_empty_results(self, test_dependencies):
        """Test semantic search handles empty results."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []  # No results
        
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "nonexistent query")
        
        assert isinstance(results, list)
        assert len(results) == 0
    
    @pytest.mark.asyncio
    async def test_semantic_search_result_structure(self, test_dependencies, mock_database_responses):
        """Test semantic search result structure is correct."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "Python programming")
        
        result = results[0]
        assert hasattr(result, 'chunk_id')
        assert hasattr(result, 'document_id') 
        assert hasattr(result, 'content')
        assert hasattr(result, 'similarity')
        assert hasattr(result, 'metadata')
        assert hasattr(result, 'document_title')
        assert hasattr(result, 'document_source')
        
        # Validate types
        assert isinstance(result.chunk_id, str)
        assert isinstance(result.document_id, str)
        assert isinstance(result.content, str)
        assert isinstance(result.similarity, float)
        assert isinstance(result.metadata, dict)
        assert isinstance(result.document_title, str)
        assert isinstance(result.document_source, str)


class TestHybridSearch:
    """Test hybrid search tool functionality."""
    
    @pytest.mark.asyncio
    async def test_hybrid_search_basic(self, test_dependencies, mock_database_responses):
        """Test basic hybrid search functionality."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        ctx = RunContext(deps=deps)
        results = await hybrid_search(ctx, "Python programming")
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert isinstance(results[0], dict)
        assert 'combined_score' in results[0]
        assert 'vector_similarity' in results[0]
        assert 'text_similarity' in results[0]
    
    @pytest.mark.asyncio
    async def test_hybrid_search_with_text_weight(self, test_dependencies, mock_database_responses):
        """Test hybrid search with custom text weight."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        ctx = RunContext(deps=deps)
        results = await hybrid_search(ctx, "Python programming", text_weight=0.5)
        
        # Verify text_weight parameter passed to database
        connection.fetch.assert_called_once()
        args = connection.fetch.call_args[0]
        assert args[4] == 0.5  # text_weight parameter
    
    @pytest.mark.asyncio
    async def test_hybrid_search_text_weight_validation(self, test_dependencies, mock_database_responses):
        """Test hybrid search validates text weight bounds."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        ctx = RunContext(deps=deps)
        
        # Test with invalid text weights
        await hybrid_search(ctx, "Python programming", text_weight=-0.5)
        args1 = connection.fetch.call_args[0]
        assert args1[4] == 0.0  # Should be clamped to 0
        
        await hybrid_search(ctx, "Python programming", text_weight=1.5)
        args2 = connection.fetch.call_args[0]
        assert args2[4] == 1.0  # Should be clamped to 1
    
    @pytest.mark.asyncio
    async def test_hybrid_search_uses_user_preference(self, test_dependencies, mock_database_responses):
        """Test hybrid search uses user preference for text weight."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        # Set user preference
        deps.user_preferences['text_weight'] = 0.7
        
        ctx = RunContext(deps=deps)
        await hybrid_search(ctx, "Python programming")
        
        # Should use preference value
        args = connection.fetch.call_args[0]
        assert args[4] == 0.7
    
    @pytest.mark.asyncio
    async def test_hybrid_search_result_structure(self, test_dependencies, mock_database_responses):
        """Test hybrid search result structure is correct."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        ctx = RunContext(deps=deps)
        results = await hybrid_search(ctx, "Python programming")
        
        result = results[0]
        required_keys = [
            'chunk_id', 'document_id', 'content', 'combined_score',
            'vector_similarity', 'text_similarity', 'metadata', 
            'document_title', 'document_source'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        
        # Validate score ranges
        assert 0 <= result['combined_score'] <= 1
        assert 0 <= result['vector_similarity'] <= 1 
        assert 0 <= result['text_similarity'] <= 1


class TestAutoSearch:
    """Test auto search tool functionality."""
    
    @pytest.mark.asyncio
    async def test_auto_search_conceptual_query(self, test_dependencies, sample_search_results):
        """Test auto search chooses semantic for conceptual queries."""
        deps, connection = test_dependencies
        
        # Mock semantic search results
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
        connection.fetch.return_value = semantic_results
        
        ctx = RunContext(deps=deps)
        result = await auto_search(ctx, "What is the concept of machine learning?")
        
        assert result['strategy'] == 'semantic'
        assert 'conceptual' in result['reason'].lower()
        assert 'results' in result
    
    @pytest.mark.asyncio
    async def test_auto_search_exact_query(self, test_dependencies, sample_hybrid_results):
        """Test auto search chooses hybrid for exact queries."""
        deps, connection = test_dependencies
        connection.fetch.return_value = sample_hybrid_results
        
        ctx = RunContext(deps=deps)
        result = await auto_search(ctx, 'Find exact quote "machine learning"')
        
        assert result['strategy'] == 'hybrid'
        assert 'exact' in result['reason'].lower()
        assert result.get('text_weight') == 0.5  # Higher text weight for exact matches
    
    @pytest.mark.asyncio
    async def test_auto_search_technical_query(self, test_dependencies, sample_hybrid_results):
        """Test auto search chooses hybrid for technical queries."""
        deps, connection = test_dependencies
        connection.fetch.return_value = sample_hybrid_results
        
        ctx = RunContext(deps=deps)
        result = await auto_search(ctx, "API documentation for sklearn.linear_model")
        
        assert result['strategy'] == 'hybrid'
        assert 'technical' in result['reason'].lower()
        assert result.get('text_weight') == 0.5
    
    @pytest.mark.asyncio
    async def test_auto_search_general_query(self, test_dependencies, sample_hybrid_results):
        """Test auto search uses hybrid for general queries."""
        deps, connection = test_dependencies
        connection.fetch.return_value = sample_hybrid_results
        
        ctx = RunContext(deps=deps)
        result = await auto_search(ctx, "Python programming tutorials")
        
        assert result['strategy'] == 'hybrid'
        assert 'balanced' in result['reason'].lower()
        assert result.get('text_weight') == 0.3  # Default weight
    
    @pytest.mark.asyncio
    async def test_auto_search_user_preference_override(self, test_dependencies, sample_search_results):
        """Test auto search respects user preference override."""
        deps, connection = test_dependencies
        
        # Mock different result types based on search type
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
        
        # Set user preference for semantic search
        deps.user_preferences['search_type'] = 'semantic'
        connection.fetch.return_value = semantic_results
        
        ctx = RunContext(deps=deps)
        result = await auto_search(ctx, "Any query here")
        
        assert result['strategy'] == 'semantic'
        assert result['reason'] == 'User preference'
    
    @pytest.mark.asyncio
    async def test_auto_search_adds_to_history(self, test_dependencies, sample_search_results):
        """Test auto search adds query to history."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        query = "Test query for history"
        
        ctx = RunContext(deps=deps) 
        await auto_search(ctx, query)
        
        assert query in deps.query_history
    
    @pytest.mark.asyncio
    async def test_auto_search_query_analysis_patterns(self, test_dependencies):
        """Test auto search query analysis patterns."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        test_cases = [
            ("What is the idea behind neural networks?", "semantic", "conceptual"),
            ('Find specific text "deep learning"', "hybrid", "exact"),
            ("Show me API_KEY configuration", "hybrid", "technical"),  
            ("About machine learning", "semantic", "conceptual"),
            ("Python tutorials", "hybrid", "balanced"),
            ("Exact verbatim quote needed", "hybrid", "exact"),
            ("Similar concepts to AI", "semantic", "conceptual")
        ]
        
        ctx = RunContext(deps=deps)
        
        for query, expected_strategy, expected_reason_contains in test_cases:
            result = await auto_search(ctx, query)
            
            assert result['strategy'] == expected_strategy, f"Wrong strategy for '{query}'"
            assert expected_reason_contains in result['reason'].lower(), f"Wrong reason for '{query}'"


class TestToolParameterValidation:
    """Test tool parameter validation."""
    
    @pytest.mark.asyncio
    async def test_semantic_search_none_match_count(self, test_dependencies, mock_database_responses):
        """Test semantic search handles None match_count."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        await semantic_search(ctx, "test query", match_count=None)
        
        # Should use default from settings
        args = connection.fetch.call_args[0]
        assert args[2] == deps.settings.default_match_count
    
    @pytest.mark.asyncio
    async def test_hybrid_search_none_text_weight(self, test_dependencies, mock_database_responses):
        """Test hybrid search handles None text_weight."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['hybrid_search']
        
        ctx = RunContext(deps=deps)
        await hybrid_search(ctx, "test query", text_weight=None)
        
        # Should use default
        args = connection.fetch.call_args[0]
        assert args[4] == deps.settings.default_text_weight
    
    @pytest.mark.asyncio
    async def test_tools_with_empty_query(self, test_dependencies):
        """Test tools handle empty query strings."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        ctx = RunContext(deps=deps)
        
        # All tools should handle empty queries without error
        await semantic_search(ctx, "")
        await hybrid_search(ctx, "")
        await auto_search(ctx, "")
        
        # Should still call database with empty query
        assert connection.fetch.call_count == 3


class TestToolErrorHandling:
    """Test tool error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_tools_handle_database_connection_error(self, test_dependencies):
        """Test tools handle database connection errors."""
        deps, connection = test_dependencies
        connection.fetch.side_effect = ConnectionError("Database unavailable")
        
        ctx = RunContext(deps=deps)
        
        # All tools should propagate database errors
        with pytest.raises(ConnectionError):
            await semantic_search(ctx, "test query")
        
        with pytest.raises(ConnectionError):
            await hybrid_search(ctx, "test query")
        
        with pytest.raises(ConnectionError):
            await auto_search(ctx, "test query")
    
    @pytest.mark.asyncio
    async def test_tools_handle_embedding_error(self, test_dependencies, mock_database_responses):
        """Test tools handle embedding generation errors."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        # Make embedding generation fail
        deps.openai_client.embeddings.create.side_effect = Exception("OpenAI API error")
        
        ctx = RunContext(deps=deps)
        
        with pytest.raises(Exception, match="OpenAI API error"):
            await semantic_search(ctx, "test query")
        
        with pytest.raises(Exception, match="OpenAI API error"):
            await hybrid_search(ctx, "test query")
        
        with pytest.raises(Exception, match="OpenAI API error"): 
            await auto_search(ctx, "test query")
    
    @pytest.mark.asyncio
    async def test_tools_handle_malformed_database_results(self, test_dependencies):
        """Test tools handle malformed database results."""
        deps, connection = test_dependencies
        
        # Return malformed results missing required fields
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                # Missing other required fields
            }
        ]
        
        ctx = RunContext(deps=deps)
        
        # Should raise KeyError for missing fields
        with pytest.raises(KeyError):
            await semantic_search(ctx, "test query")


class TestToolPerformance:
    """Test tool performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_tools_with_large_result_sets(self, test_dependencies):
        """Test tools handle large result sets efficiently."""
        deps, connection = test_dependencies
        
        # Create large mock result set
        large_results = []
        for i in range(50):  # Maximum allowed
            large_results.append({
                'chunk_id': f'chunk_{i}',
                'document_id': f'doc_{i}',
                'content': f'Content {i} with some text for testing',
                'similarity': 0.8 - (i * 0.01),  # Decreasing similarity
                'combined_score': 0.8 - (i * 0.01),
                'vector_similarity': 0.8 - (i * 0.01),
                'text_similarity': 0.75 - (i * 0.01),
                'metadata': {'page': i},
                'document_title': f'Document {i}',
                'document_source': f'source_{i}.pdf'
            })
        
        connection.fetch.return_value = large_results
        
        ctx = RunContext(deps=deps)
        
        # Test semantic search with max results
        semantic_results = await semantic_search(ctx, "test query", match_count=50)
        assert len(semantic_results) == 50
        
        # Test hybrid search with max results
        hybrid_results = await hybrid_search(ctx, "test query", match_count=50)  
        assert len(hybrid_results) == 50
        
        # Test auto search
        auto_result = await auto_search(ctx, "test query", match_count=50)
        assert len(auto_result['results']) == 50
    
    @pytest.mark.asyncio
    async def test_tool_embedding_caching(self, test_dependencies, mock_database_responses):
        """Test that embedding calls are made for each search (no caching at tool level)."""
        deps, connection = test_dependencies
        connection.fetch.return_value = mock_database_responses['semantic_search']
        
        ctx = RunContext(deps=deps)
        
        # Make multiple searches with same query
        await semantic_search(ctx, "same query")
        await semantic_search(ctx, "same query")
        
        # Each search should call embedding API (no caching in tools)
        assert deps.openai_client.embeddings.create.call_count == 2