# Semantic Search Agent - Dependency Configuration

## Executive Summary
Minimal dependency configuration for a semantic search agent that connects to PostgreSQL with PGVector extension and uses OpenAI for embeddings and LLM operations. Focus on simplicity with essential environment variables and core Python packages.

## Environment Variables Configuration

### Essential Environment Variables (.env.example)
```bash
# LLM Configuration (REQUIRED)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1

# Database Configuration (REQUIRED)
DATABASE_URL=postgresql://username:password@localhost:5432/semantic_search_db

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
DEBUG=false
MAX_RETRIES=3
TIMEOUT_SECONDS=30

# Search Configuration
DEFAULT_SEARCH_LIMIT=10
MAX_SEARCH_LIMIT=50
SIMILARITY_THRESHOLD=0.7
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Connection Pooling
DB_POOL_MIN_SIZE=5
DB_POOL_MAX_SIZE=20
DB_TIMEOUT=30
```

### Environment Variable Validation
- **OPENAI_API_KEY**: Required, must not be empty
- **DATABASE_URL**: Required, must be valid PostgreSQL connection string
- **LLM_MODEL**: Default to "gpt-4o-mini" if not specified
- **EMBEDDING_MODEL**: Default to "text-embedding-3-small"
- **DEFAULT_SEARCH_LIMIT**: Integer between 1-50, default 10

## Settings Configuration (settings.py)

### BaseSettings Class Structure
```python
class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"
    )
    
    # LLM Configuration
    llm_provider: str = Field(default="openai")
    openai_api_key: str = Field(..., description="OpenAI API key")
    llm_model: str = Field(default="gpt-4o-mini")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    # Database Configuration  
    database_url: str = Field(..., description="PostgreSQL connection URL")
    db_pool_min_size: int = Field(default=5)
    db_pool_max_size: int = Field(default=20)
    db_timeout: int = Field(default=30)
    
    # Search Configuration
    embedding_model: str = Field(default="text-embedding-3-small")
    embedding_dimensions: int = Field(default=1536)
    default_search_limit: int = Field(default=10)
    max_search_limit: int = Field(default=50)
    similarity_threshold: float = Field(default=0.7)
    
    # Application Settings
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    max_retries: int = Field(default=3)
    timeout_seconds: int = Field(default=30)
```

## Model Provider Configuration (providers.py)

### Simple OpenAI Provider Setup
```python
def get_llm_model():
    """Get OpenAI model configuration."""
    settings = load_settings()
    
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.openai_api_key
    )
    
    return OpenAIModel(settings.llm_model, provider=provider)

def get_embedding_client():
    """Get OpenAI client for embeddings."""
    settings = load_settings()
    return OpenAI(api_key=settings.openai_api_key)
```

## Agent Dependencies (dependencies.py)

### Simple Dataclass Structure
```python
@dataclass
class SemanticSearchDependencies:
    """Dependencies for semantic search agent."""
    
    # Database connection
    db_pool: Optional[asyncpg.Pool] = None
    
    # OpenAI client for embeddings
    openai_client: Optional[OpenAI] = None
    
    # Configuration
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    default_limit: int = 10
    max_limit: int = 50
    similarity_threshold: float = 0.7
    
    # Runtime context
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    debug: bool = False
    
    @classmethod
    async def create(cls, settings: Settings, **overrides):
        """Create dependencies with initialized connections."""
        
        # Initialize database pool
        db_pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=settings.db_pool_min_size,
            max_size=settings.db_pool_max_size,
            timeout=settings.db_timeout
        )
        
        # Initialize OpenAI client
        openai_client = OpenAI(api_key=settings.openai_api_key)
        
        return cls(
            db_pool=db_pool,
            openai_client=openai_client,
            embedding_model=settings.embedding_model,
            embedding_dimensions=settings.embedding_dimensions,
            default_limit=settings.default_search_limit,
            max_limit=settings.max_search_limit,
            similarity_threshold=settings.similarity_threshold,
            debug=settings.debug,
            **overrides
        )
    
    async def cleanup(self):
        """Cleanup database connections."""
        if self.db_pool:
            await self.db_pool.close()
```

## Python Package Requirements

### Core Dependencies (requirements.txt)
```txt
# Pydantic AI Framework
pydantic-ai>=0.1.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Environment Management
python-dotenv>=1.0.0

# OpenAI Integration
openai>=1.0.0

# Database
asyncpg>=0.28.0

# CLI and Utilities
rich>=13.0.0
click>=8.1.0

# Vector Operations
numpy>=1.24.0

# Async Support
httpx>=0.25.0
aiofiles>=23.0.0

# Development and Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
ruff>=0.1.0
```

### Optional Performance Dependencies
```txt
# Enhanced Performance (optional)
uvloop>=0.19.0  # Faster async event loop on Unix
orjson>=3.9.0   # Faster JSON processing
```

## Database Connection Management

### Connection Pool Configuration
- **Minimum Pool Size**: 5 connections for baseline availability
- **Maximum Pool Size**: 20 connections to handle concurrent requests
- **Connection Timeout**: 30 seconds for robustness
- **Query Timeout**: 30 seconds for search operations
- **Retry Logic**: 3 attempts with exponential backoff

### Required Database Schema
```sql
-- Ensure PGVector extension is enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Expected table structure (not created by agent)
-- chunks table with embedding column (1536 dimensions)
-- match_chunks() and hybrid_search() functions available
```

## Security Configuration

### API Key Management
- Store all secrets in `.env` file (never committed)
- Validate API keys on startup
- Use environment variable validation
- Implement key rotation support for production

### Database Security
- Use parameterized queries only
- Enable SSL connections in production
- Implement connection pooling limits
- Log connection attempts for monitoring

### Input Validation
- Query length limits (max 1000 characters)
- Search result limits (1-50 range)
- Embedding dimension validation
- SQL injection prevention

## Error Handling Patterns

### Database Connection Errors
```python
# Retry logic with exponential backoff
max_retries = 3
base_delay = 1.0
```

### OpenAI API Errors
```python
# Handle rate limiting, API errors
# Fallback to cached embeddings when possible
```

### Search Operation Errors
```python
# Graceful degradation from hybrid to semantic search
# Empty result handling
# Timeout handling
```

## Testing Configuration

### Test Dependencies Structure
```python
@dataclass 
class TestDependencies:
    """Simplified dependencies for testing."""
    
    # Mock database operations
    mock_db_results: List[dict] = field(default_factory=list)
    
    # Mock embedding responses
    mock_embeddings: List[List[float]] = field(default_factory=list)
    
    # Test configuration
    debug: bool = True
    default_limit: int = 5
```

### Test Environment Variables
```bash
# Test-specific overrides
DATABASE_URL=postgresql://test:test@localhost:5432/test_db
OPENAI_API_KEY=test-key-for-mock-responses
LLM_MODEL=gpt-4o-mini
DEBUG=true
LOG_LEVEL=DEBUG
```

## Performance Considerations

### Connection Pooling
- Database pool sized for expected concurrent users
- Connection reuse to minimize overhead
- Proper cleanup to prevent resource leaks

### Embedding Operations
- Cache frequently used embeddings
- Batch embedding generation when possible
- Use appropriate embedding model for cost/performance balance

### Memory Management
- Limit search result sizes
- Stream large responses when needed
- Clean up temporary objects

## Production Deployment

### Environment-Specific Settings
- **Development**: Debug enabled, verbose logging
- **Production**: Connection pooling optimized, minimal logging
- **Testing**: Mock connections, isolated database

### Monitoring and Logging
- Connection pool metrics
- Search operation timing
- API call tracking
- Error rate monitoring

## Quality Checklist

- [x] Essential environment variables defined
- [x] Single model provider (OpenAI) configured
- [x] Simple dataclass dependencies structure
- [x] Minimal Python packages identified
- [x] Database connection pooling specified
- [x] Security measures outlined
- [x] Error handling patterns defined
- [x] Testing configuration provided
- [x] Performance considerations addressed
- [x] Production deployment guidelines included

## Dependencies Summary

**Total Python Packages**: 12 core + 4 development
**Environment Variables**: 15 total (5 required)  
**External Services**: 2 (PostgreSQL + PGVector, OpenAI API)
**Configuration Complexity**: Low - Single model provider, simple dataclass
**Initialization Time**: ~2-3 seconds for database pool + OpenAI client

This minimal dependency configuration provides all essential functionality while maintaining simplicity and avoiding over-engineering. The focus is on the core semantic search capabilities with proper database connection management and OpenAI integration.