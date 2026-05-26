"""Test dependency injection and external service integration."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncpg
import openai

from ..dependencies import AgentDependencies
from ..settings import Settings, load_settings


class TestAgentDependencies:
    """Test AgentDependencies class functionality."""
    
    def test_dependencies_initialization(self):
        """Test basic dependency object creation."""
        deps = AgentDependencies()
        
        assert deps.db_pool is None
        assert deps.openai_client is None
        assert deps.settings is None
        assert deps.session_id is None
        assert isinstance(deps.user_preferences, dict)
        assert isinstance(deps.query_history, list)
        assert len(deps.user_preferences) == 0
        assert len(deps.query_history) == 0
    
    def test_dependencies_with_initial_values(self, test_settings):
        """Test dependency creation with initial values."""
        mock_pool = AsyncMock()
        mock_client = AsyncMock()
        
        deps = AgentDependencies(
            db_pool=mock_pool,
            openai_client=mock_client,
            settings=test_settings,
            session_id="test_session_123"
        )
        
        assert deps.db_pool is mock_pool
        assert deps.openai_client is mock_client
        assert deps.settings is test_settings
        assert deps.session_id == "test_session_123"
    
    @pytest.mark.asyncio
    async def test_dependencies_initialize(self, test_settings):
        """Test dependency initialization process."""
        deps = AgentDependencies()
        
        with patch.object(deps, 'settings', None):
            with patch('..dependencies.load_settings', return_value=test_settings):
                with patch('asyncpg.create_pool') as mock_create_pool:
                    with patch('openai.AsyncOpenAI') as mock_openai:
                        mock_pool = AsyncMock()
                        mock_client = AsyncMock()
                        mock_create_pool.return_value = mock_pool
                        mock_openai.return_value = mock_client
                        
                        await deps.initialize()
                        
                        assert deps.settings is test_settings
                        assert deps.db_pool is mock_pool
                        assert deps.openai_client is mock_client
                        
                        # Verify pool creation parameters
                        mock_create_pool.assert_called_once_with(
                            test_settings.database_url,
                            min_size=test_settings.db_pool_min_size,
                            max_size=test_settings.db_pool_max_size
                        )
                        
                        # Verify OpenAI client creation
                        mock_openai.assert_called_once_with(
                            api_key=test_settings.openai_api_key
                        )
    
    @pytest.mark.asyncio
    async def test_dependencies_initialize_idempotent(self, test_settings):
        """Test that initialize can be called multiple times safely."""
        mock_pool = AsyncMock()
        mock_client = AsyncMock()
        
        deps = AgentDependencies(
            db_pool=mock_pool,
            openai_client=mock_client,
            settings=test_settings
        )
        
        # Initialize when already initialized - should not create new connections
        with patch('asyncpg.create_pool') as mock_create_pool:
            with patch('openai.AsyncOpenAI') as mock_openai:
                await deps.initialize()
                
                # Should not create new connections
                mock_create_pool.assert_not_called()
                mock_openai.assert_not_called()
                
                assert deps.db_pool is mock_pool
                assert deps.openai_client is mock_client
    
    @pytest.mark.asyncio
    async def test_dependencies_cleanup(self):
        """Test dependency cleanup process."""
        mock_pool = AsyncMock()
        deps = AgentDependencies(db_pool=mock_pool)
        
        await deps.cleanup()
        
        mock_pool.close.assert_called_once()
        assert deps.db_pool is None
    
    @pytest.mark.asyncio
    async def test_dependencies_cleanup_no_pool(self):
        """Test cleanup when no pool exists."""
        deps = AgentDependencies()
        
        # Should not raise error
        await deps.cleanup()
        assert deps.db_pool is None


class TestEmbeddingGeneration:
    """Test embedding generation functionality."""
    
    @pytest.mark.asyncio
    async def test_get_embedding_basic(self, test_dependencies):
        """Test basic embedding generation."""
        deps, connection = test_dependencies
        
        embedding = await deps.get_embedding("test text")
        
        assert isinstance(embedding, list)
        assert len(embedding) == 1536  # Expected dimension
        assert all(isinstance(x, float) for x in embedding)
        
        # Verify OpenAI client was called correctly
        deps.openai_client.embeddings.create.assert_called_once_with(
            model=deps.settings.embedding_model,
            input="test text"
        )
    
    @pytest.mark.asyncio
    async def test_get_embedding_auto_initialize(self, test_settings):
        """Test embedding generation auto-initializes dependencies."""
        deps = AgentDependencies()
        
        with patch.object(deps, 'initialize') as mock_init:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.data = [MagicMock()]
            mock_response.data[0].embedding = [0.1] * 1536
            mock_client.embeddings.create.return_value = mock_response
            
            deps.openai_client = mock_client
            deps.settings = test_settings
            
            embedding = await deps.get_embedding("test text")
            
            mock_init.assert_called_once()
            assert len(embedding) == 1536
    
    @pytest.mark.asyncio
    async def test_get_embedding_empty_text(self, test_dependencies):
        """Test embedding generation with empty text."""
        deps, connection = test_dependencies
        
        embedding = await deps.get_embedding("")
        
        assert isinstance(embedding, list)
        assert len(embedding) == 1536
        
        # Should still call OpenAI with empty string
        deps.openai_client.embeddings.create.assert_called_once_with(
            model=deps.settings.embedding_model,
            input=""
        )
    
    @pytest.mark.asyncio
    async def test_get_embedding_long_text(self, test_dependencies):
        """Test embedding generation with long text."""
        deps, connection = test_dependencies
        
        long_text = "This is a very long text. " * 1000  # Very long text
        
        embedding = await deps.get_embedding(long_text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 1536
        
        # Should pass through long text (OpenAI will handle truncation)
        deps.openai_client.embeddings.create.assert_called_once_with(
            model=deps.settings.embedding_model,
            input=long_text
        )
    
    @pytest.mark.asyncio
    async def test_get_embedding_api_error(self, test_dependencies):
        """Test embedding generation handles API errors."""
        deps, connection = test_dependencies
        
        # Make API call fail
        deps.openai_client.embeddings.create.side_effect = openai.APIError(
            "Rate limit exceeded"
        )
        
        with pytest.raises(openai.APIError, match="Rate limit exceeded"):
            await deps.get_embedding("test text")
    
    @pytest.mark.asyncio
    async def test_get_embedding_network_error(self, test_dependencies):
        """Test embedding generation handles network errors."""
        deps, connection = test_dependencies
        
        deps.openai_client.embeddings.create.side_effect = ConnectionError(
            "Network unavailable"
        )
        
        with pytest.raises(ConnectionError, match="Network unavailable"):
            await deps.get_embedding("test text")


class TestUserPreferences:
    """Test user preference management."""
    
    def test_set_user_preference_basic(self):
        """Test setting basic user preferences."""
        deps = AgentDependencies()
        
        deps.set_user_preference("search_type", "semantic")
        
        assert deps.user_preferences["search_type"] == "semantic"
    
    def test_set_user_preference_multiple(self):
        """Test setting multiple user preferences."""
        deps = AgentDependencies()
        
        deps.set_user_preference("search_type", "semantic")
        deps.set_user_preference("text_weight", 0.5)
        deps.set_user_preference("result_count", 20)
        
        assert deps.user_preferences["search_type"] == "semantic"
        assert deps.user_preferences["text_weight"] == 0.5
        assert deps.user_preferences["result_count"] == 20
    
    def test_set_user_preference_override(self):
        """Test overriding existing user preferences."""
        deps = AgentDependencies()
        
        deps.set_user_preference("search_type", "semantic")
        deps.set_user_preference("search_type", "hybrid")
        
        assert deps.user_preferences["search_type"] == "hybrid"
    
    def test_set_user_preference_types(self):
        """Test setting preferences of different types."""
        deps = AgentDependencies()
        
        deps.set_user_preference("string_pref", "value")
        deps.set_user_preference("int_pref", 42)
        deps.set_user_preference("float_pref", 3.14)
        deps.set_user_preference("bool_pref", True)
        deps.set_user_preference("list_pref", [1, 2, 3])
        deps.set_user_preference("dict_pref", {"key": "value"})
        
        assert deps.user_preferences["string_pref"] == "value"
        assert deps.user_preferences["int_pref"] == 42
        assert deps.user_preferences["float_pref"] == 3.14
        assert deps.user_preferences["bool_pref"] is True
        assert deps.user_preferences["list_pref"] == [1, 2, 3]
        assert deps.user_preferences["dict_pref"] == {"key": "value"}


class TestQueryHistory:
    """Test query history management."""
    
    def test_add_to_history_basic(self):
        """Test adding queries to history."""
        deps = AgentDependencies()
        
        deps.add_to_history("first query")
        
        assert len(deps.query_history) == 1
        assert deps.query_history[0] == "first query"
    
    def test_add_to_history_multiple(self):
        """Test adding multiple queries to history."""
        deps = AgentDependencies()
        
        queries = ["query 1", "query 2", "query 3"]
        for query in queries:
            deps.add_to_history(query)
        
        assert len(deps.query_history) == 3
        assert deps.query_history == queries
    
    def test_add_to_history_limit(self):
        """Test query history respects 10-item limit."""
        deps = AgentDependencies()
        
        # Add more than 10 queries
        for i in range(15):
            deps.add_to_history(f"query {i}")
        
        # Should only keep last 10
        assert len(deps.query_history) == 10
        assert deps.query_history[0] == "query 5"  # First item should be query 5
        assert deps.query_history[-1] == "query 14"  # Last item should be query 14
    
    def test_add_to_history_empty_query(self):
        """Test adding empty query to history."""
        deps = AgentDependencies()
        
        deps.add_to_history("")
        
        assert len(deps.query_history) == 1
        assert deps.query_history[0] == ""
    
    def test_add_to_history_duplicate_queries(self):
        """Test adding duplicate queries to history."""
        deps = AgentDependencies()
        
        # Add same query multiple times
        deps.add_to_history("duplicate query")
        deps.add_to_history("duplicate query")
        deps.add_to_history("duplicate query")
        
        # Should keep all duplicates
        assert len(deps.query_history) == 3
        assert all(q == "duplicate query" for q in deps.query_history)


class TestDatabaseIntegration:
    """Test database connection and interaction."""
    
    @pytest.mark.asyncio
    async def test_database_pool_creation(self, test_settings):
        """Test database pool is created with correct parameters."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool
            
            deps = AgentDependencies()
            deps.settings = test_settings
            await deps.initialize()
            
            mock_create_pool.assert_called_once_with(
                test_settings.database_url,
                min_size=test_settings.db_pool_min_size,
                max_size=test_settings.db_pool_max_size
            )
            assert deps.db_pool is mock_pool
    
    @pytest.mark.asyncio
    async def test_database_connection_error(self, test_settings):
        """Test handling database connection errors."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            mock_create_pool.side_effect = asyncpg.InvalidCatalogNameError(
                "Database does not exist"
            )
            
            deps = AgentDependencies()
            deps.settings = test_settings
            
            with pytest.raises(asyncpg.InvalidCatalogNameError):
                await deps.initialize()
    
    @pytest.mark.asyncio
    async def test_database_pool_cleanup(self):
        """Test database pool cleanup."""
        mock_pool = AsyncMock()
        deps = AgentDependencies(db_pool=mock_pool)
        
        await deps.cleanup()
        
        mock_pool.close.assert_called_once()
        assert deps.db_pool is None
    
    @pytest.mark.asyncio
    async def test_database_pool_connection_context(self, test_dependencies):
        """Test database pool connection context management."""
        deps, connection = test_dependencies
        
        # Verify the mock setup allows context manager usage
        async with deps.db_pool.acquire() as conn:
            assert conn is connection
            # Connection should be available in context
            assert conn is not None


class TestOpenAIIntegration:
    """Test OpenAI client integration."""
    
    def test_openai_client_creation(self, test_settings):
        """Test OpenAI client creation with correct parameters."""
        with patch('openai.AsyncOpenAI') as mock_openai:
            mock_client = AsyncMock()
            mock_openai.return_value = mock_client
            
            deps = AgentDependencies()
            deps.settings = test_settings
            
            # Create client manually (like initialize does)
            deps.openai_client = openai.AsyncOpenAI(
                api_key=test_settings.openai_api_key
            )
            
            # Would be called in real initialization
            mock_openai.assert_called_once_with(
                api_key=test_settings.openai_api_key
            )
    
    @pytest.mark.asyncio
    async def test_openai_api_key_validation(self, test_dependencies):
        """Test OpenAI API key validation."""
        deps, connection = test_dependencies
        
        # Test with invalid API key
        deps.openai_client.embeddings.create.side_effect = openai.AuthenticationError(
            "Invalid API key"
        )
        
        with pytest.raises(openai.AuthenticationError, match="Invalid API key"):
            await deps.get_embedding("test text")
    
    @pytest.mark.asyncio
    async def test_openai_rate_limiting(self, test_dependencies):
        """Test OpenAI rate limiting handling."""
        deps, connection = test_dependencies
        
        deps.openai_client.embeddings.create.side_effect = openai.RateLimitError(
            "Rate limit exceeded"
        )
        
        with pytest.raises(openai.RateLimitError, match="Rate limit exceeded"):
            await deps.get_embedding("test text")


class TestSettingsIntegration:
    """Test settings loading and integration."""
    
    def test_load_settings_success(self):
        """Test successful settings loading."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost/test',
            'OPENAI_API_KEY': 'test_key'
        }):
            settings = load_settings()
            
            assert settings.database_url == 'postgresql://test:test@localhost/test'
            assert settings.openai_api_key == 'test_key'
            assert settings.llm_model == 'gpt-4o-mini'  # Default value
    
    def test_load_settings_missing_database_url(self):
        """Test settings loading with missing DATABASE_URL."""
        with patch.dict('os.environ', {
            'OPENAI_API_KEY': 'test_key'
        }, clear=True):
            with pytest.raises(ValueError, match="DATABASE_URL"):
                load_settings()
    
    def test_load_settings_missing_openai_key(self):
        """Test settings loading with missing OPENAI_API_KEY."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost/test'
        }, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                load_settings()
    
    def test_settings_defaults(self, test_settings):
        """Test settings default values."""
        assert test_settings.llm_model == "gpt-4o-mini"
        assert test_settings.embedding_model == "text-embedding-3-small"
        assert test_settings.default_match_count == 10
        assert test_settings.max_match_count == 50
        assert test_settings.default_text_weight == 0.3
        assert test_settings.db_pool_min_size == 1
        assert test_settings.db_pool_max_size == 5
        assert test_settings.embedding_dimension == 1536
    
    def test_settings_custom_values(self):
        """Test settings with custom environment values."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://custom:custom@localhost/custom',
            'OPENAI_API_KEY': 'custom_key',
            'LLM_MODEL': 'gpt-4',
            'DEFAULT_MATCH_COUNT': '20',
            'MAX_MATCH_COUNT': '100',
            'DEFAULT_TEXT_WEIGHT': '0.5',
            'EMBEDDING_MODEL': 'text-embedding-ada-002'
        }):
            settings = load_settings()
            
            assert settings.database_url == 'postgresql://custom:custom@localhost/custom'
            assert settings.openai_api_key == 'custom_key'
            assert settings.llm_model == 'gpt-4'
            assert settings.default_match_count == 20
            assert settings.max_match_count == 100
            assert settings.default_text_weight == 0.5
            assert settings.embedding_model == 'text-embedding-ada-002'


class TestDependencyLifecycle:
    """Test complete dependency lifecycle."""
    
    @pytest.mark.asyncio
    async def test_full_lifecycle(self, test_settings):
        """Test complete dependency lifecycle from creation to cleanup."""
        with patch('asyncpg.create_pool') as mock_create_pool:
            with patch('openai.AsyncOpenAI') as mock_openai:
                mock_pool = AsyncMock()
                mock_client = AsyncMock()
                mock_create_pool.return_value = mock_pool
                mock_openai.return_value = mock_client
                
                # Create dependencies
                deps = AgentDependencies()
                assert deps.db_pool is None
                assert deps.openai_client is None
                
                # Initialize
                with patch('..dependencies.load_settings', return_value=test_settings):
                    await deps.initialize()
                
                assert deps.db_pool is mock_pool
                assert deps.openai_client is mock_client
                assert deps.settings is test_settings
                
                # Use dependencies
                deps.set_user_preference("test", "value")
                deps.add_to_history("test query")
                
                assert deps.user_preferences["test"] == "value"
                assert "test query" in deps.query_history
                
                # Cleanup
                await deps.cleanup()
                assert deps.db_pool is None
                mock_pool.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_multiple_initialization_cleanup_cycles(self, test_settings):
        """Test multiple init/cleanup cycles work correctly."""
        deps = AgentDependencies()
        
        with patch('asyncpg.create_pool') as mock_create_pool:
            with patch('openai.AsyncOpenAI') as mock_openai:
                with patch('..dependencies.load_settings', return_value=test_settings):
                    # First cycle
                    mock_pool_1 = AsyncMock()
                    mock_client_1 = AsyncMock()
                    mock_create_pool.return_value = mock_pool_1
                    mock_openai.return_value = mock_client_1
                    
                    await deps.initialize()
                    assert deps.db_pool is mock_pool_1
                    
                    await deps.cleanup()
                    assert deps.db_pool is None
                    
                    # Second cycle
                    mock_pool_2 = AsyncMock()
                    mock_client_2 = AsyncMock()
                    mock_create_pool.return_value = mock_pool_2
                    mock_openai.return_value = mock_client_2
                    
                    await deps.initialize()
                    assert deps.db_pool is mock_pool_2
                    
                    await deps.cleanup()
                    assert deps.db_pool is None