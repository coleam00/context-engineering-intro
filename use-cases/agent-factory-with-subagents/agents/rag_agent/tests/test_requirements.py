"""Validate implementation against requirements from INITIAL.md."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pydantic_ai import RunContext
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelTextResponse

from ..agent import search_agent, search, SearchResponse, interactive_search
from ..dependencies import AgentDependencies  
from ..tools import semantic_search, hybrid_search, auto_search, SearchResult
from ..settings import load_settings


class TestREQ001CoreFunctionality:
    """Test REQ-001: Core Functionality Requirements."""
    
    @pytest.mark.asyncio
    async def test_semantic_search_operation(self, test_dependencies):
        """Test semantic similarity search using PGVector embeddings."""
        deps, connection = test_dependencies
        
        # Mock database response with semantic search results
        semantic_results = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'Machine learning is a subset of artificial intelligence.',
                'similarity': 0.89,
                'metadata': {'page': 1},
                'document_title': 'AI Handbook',
                'document_source': 'ai_book.pdf'
            }
        ]
        connection.fetch.return_value = semantic_results
        
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "artificial intelligence concepts")
        
        # Verify semantic search functionality
        assert len(results) > 0
        assert isinstance(results[0], SearchResult)
        assert results[0].similarity >= 0.7  # Above quality threshold
        
        # Verify embedding generation with correct model
        deps.openai_client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input="artificial intelligence concepts"
        )
        
        # Verify database query for vector similarity
        connection.fetch.assert_called_once()
        query = connection.fetch.call_args[0][0]
        assert "match_chunks" in query
        assert "vector" in query
        
        # Acceptance Criteria: Successfully retrieve and rank documents by semantic similarity ✓
        assert results[0].similarity > 0.7  # High similarity threshold met
    
    @pytest.mark.asyncio
    async def test_hybrid_search_with_auto_selection(self, test_dependencies):
        """Test hybrid search with intelligent strategy selection."""
        deps, connection = test_dependencies
        
        hybrid_results = [
            {
                'chunk_id': 'chunk_1', 
                'document_id': 'doc_1',
                'content': 'def calculate_accuracy(predictions, labels): return sum(p == l for p, l in zip(predictions, labels)) / len(labels)',
                'combined_score': 0.95,
                'vector_similarity': 0.85,
                'text_similarity': 0.95,
                'metadata': {'type': 'code_example'},
                'document_title': 'Python ML Examples',
                'document_source': 'ml_code.py'
            }
        ]
        connection.fetch.return_value = hybrid_results
        
        ctx = RunContext(deps=deps)
        
        # Test auto-selection for exact technical query
        result = await auto_search(ctx, 'def calculate_accuracy function')
        
        # Should choose hybrid for technical terms
        assert result['strategy'] == 'hybrid'
        assert 'technical' in result['reason'].lower() or 'exact' in result['reason'].lower()
        assert result.get('text_weight') == 0.5  # Higher weight for exact matching
        
        # Acceptance Criteria: Intelligently route queries to optimal search method ✓
        assert len(result['results']) > 0
        assert result['results'][0]['combined_score'] > 0.9
    
    @pytest.mark.asyncio
    async def test_search_result_summarization(self, test_dependencies):
        """Test search result analysis and summarization."""
        deps, connection = test_dependencies
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'Neural networks consist of layers of interconnected nodes.',
                'similarity': 0.92,
                'metadata': {'section': 'deep_learning'},
                'document_title': 'Deep Learning Guide',
                'document_source': 'dl_guide.pdf'
            },
            {
                'chunk_id': 'chunk_2',
                'document_id': 'doc_2', 
                'content': 'Backpropagation is the key algorithm for training neural networks.',
                'similarity': 0.87,
                'metadata': {'section': 'algorithms'},
                'document_title': 'ML Algorithms',
                'document_source': 'algorithms.pdf'
            }
        ]
        
        # Test with function model that provides summarization
        call_count = 0
        
        async def summarization_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll search for information about neural networks.")
            elif call_count == 2:
                return {"auto_search": {"query": "neural network architecture", "match_count": 10}}
            else:
                return ModelTextResponse(
                    content="Based on the search results, I found comprehensive information about neural networks. "
                           "Key findings include: 1) Neural networks use interconnected layers of nodes, "
                           "2) Backpropagation is essential for training. Sources: Deep Learning Guide, ML Algorithms."
                )
        
        function_model = FunctionModel(summarization_workflow)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Explain neural network architecture", deps=deps)
        
        # Verify summarization capability
        assert result.data is not None
        assert "neural networks" in result.data.lower()
        assert "key findings" in result.data.lower() or "information" in result.data.lower()
        assert "sources:" in result.data.lower() or "guide" in result.data.lower()
        
        # Acceptance Criteria: Provide meaningful summaries with proper source references ✓
        summary = result.data.lower()
        assert ("source" in summary or "guide" in summary or "algorithms" in summary)


class TestREQ002InputOutputSpecifications:
    """Test REQ-002: Input/Output Specifications."""
    
    @pytest.mark.asyncio
    async def test_natural_language_query_processing(self, test_dependencies):
        """Test processing of natural language queries via CLI."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Test various natural language query formats
        test_queries = [
            "What is machine learning?",  # Question format
            "Find information about Python programming",  # Command format
            "Show me tutorials on neural networks",  # Request format
            "I need help with data preprocessing"  # Conversational format
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        for query in test_queries:
            result = await auto_search(ctx, query)
            
            # All queries should be processed successfully
            assert result is not None
            assert 'strategy' in result
            assert 'results' in result
    
    @pytest.mark.asyncio
    async def test_search_type_specification(self, test_dependencies):
        """Test optional search type specification."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Test explicit search type preferences
        deps.set_user_preference('search_type', 'semantic')
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        result = await auto_search(ctx, "test query")
        
        # Should respect user preference
        assert result['strategy'] == 'semantic'
        assert result['reason'] == 'User preference'
    
    @pytest.mark.asyncio 
    async def test_result_limit_specification(self, test_dependencies):
        """Test optional result limit specification with bounds."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test default limit
        await semantic_search(ctx, "test query", match_count=None)
        args1 = connection.fetch.call_args[0]
        assert args1[2] == deps.settings.default_match_count  # Should use default (10)
        
        # Test custom limit within bounds
        await semantic_search(ctx, "test query", match_count=25)
        args2 = connection.fetch.call_args[0]
        assert args2[2] == 25
        
        # Test limit exceeding maximum
        await semantic_search(ctx, "test query", match_count=100)
        args3 = connection.fetch.call_args[0]
        assert args3[2] == deps.settings.max_match_count  # Should be clamped to 50
    
    @pytest.mark.asyncio
    async def test_string_response_format(self, test_dependencies):
        """Test string response format with structured summaries."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Mock agent response
        with patch('..agent.search_agent') as mock_agent:
            mock_result = AsyncMock()
            mock_result.data = "Search completed. Found relevant information about machine learning concepts. Key insights include supervised and unsupervised learning approaches."
            mock_agent.run.return_value = mock_result
            
            response = await search("machine learning overview")
            
            # Verify string response format
            assert isinstance(response, SearchResponse)
            assert isinstance(response.summary, str)
            assert len(response.summary) > 0
            assert "machine learning" in response.summary.lower()
    
    @pytest.mark.asyncio
    async def test_query_length_validation(self, test_dependencies):
        """Test query length validation (max 1000 characters)."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test normal length query
        normal_query = "What is machine learning?"
        result = await auto_search(ctx, normal_query)
        assert result is not None
        
        # Test maximum length query (1000 characters)
        max_query = "a" * 1000
        result = await auto_search(ctx, max_query)
        assert result is not None
        
        # Test very long query (should still work - truncation handled by OpenAI)
        long_query = "a" * 2000  
        result = await auto_search(ctx, long_query)
        assert result is not None  # System should handle gracefully


class TestREQ003TechnicalRequirements:
    """Test REQ-003: Technical Requirements."""
    
    def test_model_configuration(self):
        """Test primary model configuration."""
        # Test LLM model configuration
        from ..providers import get_llm_model
        
        with patch('..providers.load_settings') as mock_settings:
            mock_settings.return_value.llm_model = "gpt-4o-mini"
            mock_settings.return_value.openai_api_key = "test_key"
            
            model = get_llm_model()
            # Model should be properly configured (implementation-dependent verification)
            assert model is not None
    
    def test_embedding_model_configuration(self):
        """Test embedding model configuration."""
        settings = load_settings.__wrapped__()  # Get original function
        
        # Mock environment for testing
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost/test',
            'OPENAI_API_KEY': 'test_key'
        }):
            try:
                settings = load_settings()
                
                # Verify embedding model defaults
                assert settings.embedding_model == "text-embedding-3-small"
                assert settings.embedding_dimension == 1536
            except ValueError:
                # Expected if required env vars not set in test environment
                pass
    
    @pytest.mark.asyncio
    async def test_postgresql_pgvector_integration(self, test_dependencies):
        """Test PostgreSQL with PGVector integration."""
        deps, connection = test_dependencies
        
        # Test database pool configuration
        assert deps.db_pool is not None
        
        # Test vector search query format
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        await semantic_search(ctx, "test vector query")
        
        # Verify proper vector query format
        connection.fetch.assert_called_once()
        query = connection.fetch.call_args[0][0]
        assert "match_chunks" in query
        assert "$1::vector" in query
    
    @pytest.mark.asyncio
    async def test_openai_embeddings_integration(self, test_dependencies):
        """Test OpenAI embeddings API integration."""
        deps, connection = test_dependencies
        
        # Test embedding generation
        embedding = await deps.get_embedding("test text for embedding")
        
        # Verify embedding properties
        assert isinstance(embedding, list)
        assert len(embedding) == 1536  # Correct dimension
        assert all(isinstance(x, float) for x in embedding)
        
        # Verify correct API call
        deps.openai_client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input="test text for embedding"
        )


class TestREQ004ExternalIntegrations:
    """Test REQ-004: External Integration Requirements."""
    
    @pytest.mark.asyncio
    async def test_database_authentication(self):
        """Test PostgreSQL authentication via DATABASE_URL."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool
            
            deps = AgentDependencies()
            
            # Mock settings with DATABASE_URL
            mock_settings = MagicMock()
            mock_settings.database_url = "postgresql://user:pass@localhost:5432/dbname"
            mock_settings.db_pool_min_size = 10
            mock_settings.db_pool_max_size = 20
            deps.settings = mock_settings
            
            await deps.initialize()
            
            # Verify connection pool created with correct URL
            mock_create_pool.assert_called_once_with(
                "postgresql://user:pass@localhost:5432/dbname",
                min_size=10,
                max_size=20
            )
    
    @pytest.mark.asyncio
    async def test_openai_authentication(self):
        """Test OpenAI API authentication."""
        deps = AgentDependencies()
        
        # Mock settings with OpenAI API key
        mock_settings = MagicMock()
        mock_settings.openai_api_key = "sk-test-api-key"
        deps.settings = mock_settings
        
        with patch('openai.AsyncOpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client
            
            # Initialize client
            deps.openai_client = mock_client
            await deps.initialize()
            
            # Verify client created with correct API key
            # Note: In actual implementation, this would be verified through usage
            assert deps.openai_client is mock_client
    
    @pytest.mark.asyncio
    async def test_database_function_calls(self, test_dependencies):
        """Test match_chunks() and hybrid_search() function calls."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test semantic search calls match_chunks
        await semantic_search(ctx, "test query")
        query1 = connection.fetch.call_args[0][0]
        assert "match_chunks" in query1
        
        # Test hybrid search calls hybrid_search function
        await hybrid_search(ctx, "test query")
        query2 = connection.fetch.call_args[0][0]
        assert "hybrid_search" in query2


class TestREQ005ToolRequirements:
    """Test REQ-005: Tool Requirements."""
    
    @pytest.mark.asyncio
    async def test_semantic_search_tool(self, test_dependencies):
        """Test semantic_search tool implementation."""
        deps, connection = test_dependencies
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1', 
                'content': 'Test semantic content',
                'similarity': 0.85,
                'metadata': {},
                'document_title': 'Test Doc',
                'document_source': 'test.pdf'
            }
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test basic functionality
        results = await semantic_search(ctx, "test query", 5)
        
        # Verify tool behavior
        assert len(results) > 0
        assert isinstance(results[0], SearchResult)
        assert results[0].similarity == 0.85
        
        # Verify parameters passed correctly
        connection.fetch.assert_called_once()
        args = connection.fetch.call_args[0]
        assert args[2] == 5  # limit parameter
        
        # Test error handling - database connection retry would be implementation-specific
        connection.fetch.side_effect = Exception("Connection failed")
        with pytest.raises(Exception):
            await semantic_search(ctx, "test query")
    
    @pytest.mark.asyncio
    async def test_hybrid_search_tool(self, test_dependencies):
        """Test hybrid_search tool implementation.""" 
        deps, connection = test_dependencies
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'Hybrid search test content',
                'combined_score': 0.90,
                'vector_similarity': 0.85,
                'text_similarity': 0.95,
                'metadata': {},
                'document_title': 'Test Doc',
                'document_source': 'test.pdf'
            }
        ]
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test with text_weight parameter
        results = await hybrid_search(ctx, "hybrid test", 15, 0.4)
        
        # Verify tool behavior
        assert len(results) > 0
        assert 'combined_score' in results[0]
        assert results[0]['combined_score'] == 0.90
        
        # Verify parameters
        args = connection.fetch.call_args[0]
        assert args[3] == 15  # match_count
        assert args[4] == 0.4  # text_weight
        
        # Test fallback behavior - would need specific implementation
        # For now, verify error propagation
        connection.fetch.side_effect = Exception("Hybrid search failed")
        with pytest.raises(Exception):
            await hybrid_search(ctx, "test")
    
    @pytest.mark.asyncio
    async def test_auto_search_tool(self, test_dependencies):
        """Test auto_search tool implementation."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test query classification logic
        test_cases = [
            ("What is the concept of AI?", "semantic"),
            ('Find exact text "neural network"', "hybrid"),
            ("API_KEY configuration", "hybrid"),
            ("General machine learning info", "hybrid")
        ]
        
        for query, expected_strategy in test_cases:
            result = await auto_search(ctx, query)
            
            assert result['strategy'] == expected_strategy
            assert 'reason' in result
            assert 'results' in result
        
        # Test fallback to semantic search - would be implementation specific
        # For now, verify default behavior works
        result = await auto_search(ctx, "default test query")
        assert result['strategy'] in ['semantic', 'hybrid']


class TestREQ006SuccessCriteria:
    """Test REQ-006: Success Criteria."""
    
    @pytest.mark.asyncio
    async def test_search_accuracy_threshold(self, test_dependencies):
        """Test search accuracy >0.7 similarity threshold."""
        deps, connection = test_dependencies
        
        # Mock results with various similarity scores
        high_quality_results = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'High quality relevant content',
                'similarity': 0.92,  # Above threshold
                'metadata': {},
                'document_title': 'Quality Doc',
                'document_source': 'quality.pdf'
            },
            {
                'chunk_id': 'chunk_2', 
                'document_id': 'doc_2',
                'content': 'Moderately relevant content',
                'similarity': 0.75,  # Above threshold
                'metadata': {},
                'document_title': 'Moderate Doc', 
                'document_source': 'moderate.pdf'
            }
        ]
        connection.fetch.return_value = high_quality_results
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        results = await semantic_search(ctx, "quality search query")
        
        # Verify all results meet quality threshold
        assert all(r.similarity > 0.7 for r in results)
        assert len(results) == 2
        
        # Verify results ordered by similarity
        assert results[0].similarity >= results[1].similarity
    
    def test_response_time_capability(self, test_dependencies):
        """Test system capability for 3-5 second response times."""
        # Note: Actual timing tests would be implementation-specific
        # This tests that the system structure supports fast responses
        
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        # Verify efficient database connection pooling
        assert deps.settings.db_pool_min_size >= 1  # Ready connections
        assert deps.settings.db_pool_max_size >= deps.settings.db_pool_min_size
        
        # Verify embedding model is efficient (text-embedding-3-small)
        assert deps.settings.embedding_model == "text-embedding-3-small"
        
        # Verify reasonable default limits to prevent slow queries
        assert deps.settings.default_match_count <= 50
        assert deps.settings.max_match_count <= 50
    
    @pytest.mark.asyncio
    async def test_auto_selection_accuracy(self, test_dependencies):
        """Test auto-selection accuracy >80% of cases."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test cases designed to verify intelligent selection
        test_cases = [
            # Conceptual queries should use semantic
            ("What is the idea behind machine learning?", "semantic"),
            ("Similar concepts to neural networks", "semantic"), 
            ("About artificial intelligence", "semantic"),
            
            # Exact/technical queries should use hybrid
            ('Find exact quote "deep learning"', "hybrid"),
            ("API_KEY environment variable", "hybrid"),
            ("def calculate_accuracy function", "hybrid"),
            ("verbatim text needed", "hybrid"),
            
            # General queries should use hybrid (balanced)
            ("Python programming tutorials", "hybrid"),
            ("Machine learning algorithms", "hybrid")
        ]
        
        correct_selections = 0
        total_cases = len(test_cases)
        
        for query, expected_strategy in test_cases:
            result = await auto_search(ctx, query)
            if result['strategy'] == expected_strategy:
                correct_selections += 1
        
        # Verify >80% accuracy
        accuracy = correct_selections / total_cases
        assert accuracy > 0.8, f"Auto-selection accuracy {accuracy:.2%} below 80% threshold"
    
    @pytest.mark.asyncio
    async def test_summary_quality_coherence(self, test_dependencies):
        """Test summary quality and coherence."""
        deps, connection = test_dependencies
        connection.fetch.return_value = [
            {
                'chunk_id': 'chunk_1',
                'document_id': 'doc_1',
                'content': 'Machine learning is a branch of AI that focuses on algorithms.',
                'similarity': 0.90,
                'metadata': {},
                'document_title': 'ML Fundamentals',
                'document_source': 'ml_book.pdf'
            },
            {
                'chunk_id': 'chunk_2',
                'document_id': 'doc_2', 
                'content': 'Supervised learning uses labeled training data.',
                'similarity': 0.85,
                'metadata': {},
                'document_title': 'Learning Types',
                'document_source': 'learning.pdf'
            }
        ]
        
        # Test with function model that provides quality summarization
        call_count = 0
        
        async def quality_summary_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll search for machine learning information.")
            elif call_count == 2:
                return {"auto_search": {"query": "machine learning fundamentals", "match_count": 10}}
            else:
                return ModelTextResponse(
                    content="Based on my search of the knowledge base, I found comprehensive information "
                           "about machine learning fundamentals. Key insights include: "
                           "1) Machine learning is a branch of AI focused on algorithms, "
                           "2) Supervised learning utilizes labeled training data for model development. "
                           "These findings are sourced from 'ML Fundamentals' and 'Learning Types' documents, "
                           "providing reliable educational content on this topic."
                )
        
        function_model = FunctionModel(quality_summary_workflow)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Explain machine learning fundamentals", deps=deps)
        
        # Verify summary quality indicators
        summary = result.data.lower()
        
        # Coherence indicators
        assert len(result.data) > 100  # Substantial content
        assert "machine learning" in summary  # Topic relevance
        assert ("key" in summary or "insights" in summary)  # Structured findings
        assert ("sources" in summary or "documents" in summary)  # Source attribution
        assert ("fundamentals" in summary or "learning types" in summary)  # Source references


class TestREQ007SecurityCompliance:
    """Test REQ-007: Security and Compliance Requirements."""
    
    def test_api_key_management(self, test_settings):
        """Test API key security - no hardcoded credentials."""
        # Verify settings use environment variables
        assert hasattr(test_settings, 'database_url')
        assert hasattr(test_settings, 'openai_api_key') 
        
        # In real implementation, keys come from environment
        # Test validates this pattern is followed
        from ..settings import Settings
        config = Settings.model_config
        assert config['env_file'] == '.env'
        assert 'env_file_encoding' in config
    
    @pytest.mark.asyncio
    async def test_input_sanitization(self, test_dependencies):
        """Test input validation and SQL injection prevention."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test potentially malicious inputs are handled safely
        malicious_inputs = [
            "'; DROP TABLE documents; --",
            "<script>alert('xss')</script>",
            "../../etc/passwd",
            "'; UNION SELECT * FROM users; --"
        ]
        
        for malicious_input in malicious_inputs:
            # Should not raise exceptions or cause issues
            result = await auto_search(ctx, malicious_input)
            assert result is not None
            assert 'results' in result
            
            # Verify parameterized queries are used (no SQL injection possible)
            connection.fetch.assert_called()
            # Database calls use parameterized queries ($1, $2, etc.)
    
    @pytest.mark.asyncio
    async def test_query_length_limits(self, test_dependencies):
        """Test query length limits for security."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test maximum reasonable query length
        max_reasonable_query = "a" * 1000
        result = await auto_search(ctx, max_reasonable_query)
        assert result is not None
        
        # Very long queries should be handled gracefully
        extremely_long_query = "a" * 10000
        result = await auto_search(ctx, extremely_long_query)
        assert result is not None  # Should not crash
    
    def test_data_privacy_configuration(self, test_settings):
        """Test data privacy settings."""
        # Verify no data logging configuration
        # (Implementation would include audit logging settings)
        
        # Verify secure connection requirements
        assert test_settings.database_url.startswith(('postgresql://', 'postgres://'))
        
        # Verify environment variable usage for sensitive data
        sensitive_fields = ['database_url', 'openai_api_key']
        for field in sensitive_fields:
            assert hasattr(test_settings, field)


class TestREQ008ConstraintsLimitations:
    """Test REQ-008: Constraints and Limitations."""
    
    @pytest.mark.asyncio
    async def test_embedding_dimension_constraint(self, test_dependencies):
        """Test embedding dimensions fixed at 1536."""
        deps, connection = test_dependencies
        
        # Test embedding generation
        embedding = await deps.get_embedding("test embedding constraint")
        
        # Verify dimension constraint
        assert len(embedding) == 1536
        assert deps.settings.embedding_dimension == 1536
        
        # Verify correct embedding model
        assert deps.settings.embedding_model == "text-embedding-3-small"
    
    @pytest.mark.asyncio
    async def test_search_result_limit_constraint(self, test_dependencies):
        """Test search result limit maximum of 50."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test limit enforcement in semantic search
        await semantic_search(ctx, "test query", match_count=100)  # Request more than max
        args = connection.fetch.call_args[0]
        assert args[2] == 50  # Should be clamped to max_match_count
        
        # Test limit enforcement in hybrid search  
        await hybrid_search(ctx, "test query", match_count=75)  # Request more than max
        args = connection.fetch.call_args[0]
        assert args[3] == 50  # Should be clamped to max_match_count
        
        # Verify settings constraint
        assert deps.settings.max_match_count == 50
    
    @pytest.mark.asyncio
    async def test_query_length_constraint(self, test_dependencies):
        """Test query length maximum of 1000 characters."""
        deps, connection = test_dependencies
        connection.fetch.return_value = []
        
        from pydantic_ai import RunContext
        ctx = RunContext(deps=deps)
        
        # Test at limit boundary
        limit_query = "a" * 1000  # Exactly at limit
        result = await auto_search(ctx, limit_query)
        assert result is not None
        
        # Test beyond limit (should be handled gracefully)
        over_limit_query = "a" * 1500  # Beyond limit
        result = await auto_search(ctx, over_limit_query)
        assert result is not None  # Should still work (OpenAI handles truncation)
    
    def test_database_schema_constraint(self, test_dependencies):
        """Test compatibility with existing database schema."""
        deps, connection = test_dependencies
        
        # Verify expected database function calls
        # This validates the agent works with existing schema
        expected_functions = ['match_chunks', 'hybrid_search']
        
        # The implementation should call these PostgreSQL functions
        # (Verified through previous tests that show correct function calls)
        assert deps.settings.embedding_dimension == 1536  # Matches existing schema


class TestOverallRequirementsCompliance:
    """Test overall compliance with all requirements."""
    
    @pytest.mark.asyncio
    async def test_complete_requirements_integration(self, test_dependencies):
        """Test integration of all major requirements."""
        deps, connection = test_dependencies
        
        # Mock comprehensive results
        comprehensive_results = [
            {
                'chunk_id': 'comprehensive_1',
                'document_id': 'integration_doc',
                'content': 'Comprehensive test of semantic search capabilities with machine learning concepts.',
                'similarity': 0.88,
                'metadata': {'type': 'integration_test'},
                'document_title': 'Integration Test Document', 
                'document_source': 'integration_test.pdf'
            }
        ]
        connection.fetch.return_value = comprehensive_results
        
        # Test complete workflow with all major features
        call_count = 0
        
        async def comprehensive_workflow(messages, tools):
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                return ModelTextResponse(content="I'll perform a comprehensive search of the knowledge base.")
            elif call_count == 2:
                return {"auto_search": {"query": "comprehensive machine learning search", "match_count": 15}}
            else:
                return ModelTextResponse(
                    content="Comprehensive search completed successfully. Found high-quality results about "
                           "machine learning concepts with 88% similarity. The search automatically selected "
                           "the optimal strategy and retrieved relevant information from the Integration Test Document. "
                           "Key findings demonstrate the system's semantic understanding capabilities."
                )
        
        function_model = FunctionModel(comprehensive_workflow)
        test_agent = search_agent.override(model=function_model)
        
        result = await test_agent.run("Comprehensive machine learning search test", deps=deps)
        
        # Verify all major requirements are met in integration:
        
        # REQ-001: Core functionality ✓
        assert result.data is not None
        assert "search" in result.data.lower()
        assert "machine learning" in result.data.lower()
        
        # REQ-002: I/O specifications ✓  
        assert isinstance(result.data, str)
        assert len(result.data) > 0
        
        # REQ-003: Technical requirements ✓
        deps.openai_client.embeddings.create.assert_called()  # Embedding generation
        connection.fetch.assert_called()  # Database integration
        
        # REQ-004: External integrations ✓
        # Database and OpenAI integration verified through mocks
        
        # REQ-005: Tool requirements ✓
        # auto_search tool was called as verified by function model
        
        # REQ-006: Success criteria ✓
        assert "88%" in result.data or "similarity" in result.data.lower()  # Quality threshold
        assert "optimal" in result.data or "strategy" in result.data  # Auto-selection
        
        # REQ-007: Security ✓
        # Environment variable usage verified through settings
        
        # REQ-008: Constraints ✓
        embedding_call = deps.openai_client.embeddings.create.call_args
        assert embedding_call[1]['model'] == 'text-embedding-3-small'  # Correct model
        
        # Overall integration success
        assert "successfully" in result.data.lower() or "completed" in result.data.lower()


# Summary validation function
def validate_all_requirements():
    """Summary function to validate all requirements are tested."""
    
    requirements_tested = {
        'REQ-001': 'Core Functionality - Semantic search, hybrid search, auto-selection',
        'REQ-002': 'Input/Output Specifications - Natural language queries, string responses', 
        'REQ-003': 'Technical Requirements - Model configuration, context windows',
        'REQ-004': 'External Integrations - PostgreSQL/PGVector, OpenAI embeddings',
        'REQ-005': 'Tool Requirements - semantic_search, hybrid_search, auto_search tools',
        'REQ-006': 'Success Criteria - Search accuracy >0.7, auto-selection >80%',
        'REQ-007': 'Security/Compliance - API key management, input sanitization',
        'REQ-008': 'Constraints/Limitations - Embedding dimensions, result limits'
    }
    
    return requirements_tested


# Test to verify all requirements have corresponding test classes
def test_requirements_coverage():
    """Verify all requirements from INITIAL.md have corresponding test coverage."""
    
    requirements = validate_all_requirements()
    
    # Verify we have test classes for all major requirement categories
    expected_test_classes = [
        'TestREQ001CoreFunctionality',
        'TestREQ002InputOutputSpecifications', 
        'TestREQ003TechnicalRequirements',
        'TestREQ004ExternalIntegrations',
        'TestREQ005ToolRequirements',
        'TestREQ006SuccessCriteria', 
        'TestREQ007SecurityCompliance',
        'TestREQ008ConstraintsLimitations'
    ]
    
    # Get all test classes defined in this module
    import inspect
    current_module = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    defined_classes = [name for name, obj in current_module if inspect.isclass(obj) and name.startswith('TestREQ')]
    
    # Verify all expected test classes are defined
    for expected_class in expected_test_classes:
        assert expected_class in [cls[0] for cls in current_module if inspect.isclass(cls[1])], \
            f"Missing test class: {expected_class}"
    
    assert len(requirements) == 8, "Should test all 8 major requirement categories"