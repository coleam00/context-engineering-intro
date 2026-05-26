# Tools for Semantic Search Agent

## Tool Implementation Specifications

Based on the requirements from INITIAL.md, this agent needs 3 essential tools for semantic search functionality with automatic search type selection.

### Tool 1: semantic_search

**Purpose**: Execute semantic similarity search using PGVector embeddings  
**Pattern**: `@agent.tool` (context-aware, needs database access)  
**Parameters**:
- `query` (str): The search query to find semantically similar content
- `limit` (int, default=10): Maximum number of results to return (1-50)

**Implementation Pattern**:
```python
@agent.tool
async def semantic_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Perform semantic similarity search using vector embeddings.
    
    Args:
        query: Natural language search query
        limit: Maximum number of results (1-50)
    
    Returns:
        List of search results with content, similarity scores, and metadata
    """
```

**Functionality**:
- Generate query embedding using OpenAI text-embedding-3-small
- Call `match_chunks(query_embedding, match_count)` database function
- Return results with similarity scores above 0.7 threshold
- Handle database connection errors with retry logic
- Validate limit parameter (1-50 range)

**Error Handling**:
- Retry database connections up to 3 times
- Fallback to empty results if embedding generation fails
- Log search metrics for performance monitoring

### Tool 2: hybrid_search

**Purpose**: Execute combined semantic + keyword search for enhanced results  
**Pattern**: `@agent.tool` (context-aware, needs database access)  
**Parameters**:
- `query` (str): The search query for both semantic and text matching
- `limit` (int, default=10): Maximum number of results to return (1-50)
- `text_weight` (float, default=0.3): Weight for text search component (0.0-1.0)

**Implementation Pattern**:
```python
@agent.tool
async def hybrid_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10,
    text_weight: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Perform hybrid search combining semantic and keyword matching.
    
    Args:
        query: Search query for both vector and text search
        limit: Maximum number of results (1-50)
        text_weight: Weight for text search component (0.0-1.0)
    
    Returns:
        List of search results with combined ranking scores
    """
```

**Functionality**:
- Generate query embedding for semantic component
- Call `hybrid_search(query_embedding, query_text, match_count, text_weight)` database function
- Combine vector similarity with full-text search results
- Return ranked results with composite scores
- Validate text_weight parameter (0.0-1.0 range)

**Error Handling**:
- Fallback to pure semantic search if text search component fails
- Retry database operations with exponential backoff
- Handle malformed query text gracefully

### Tool 3: auto_search

**Purpose**: Automatically select optimal search type based on query analysis  
**Pattern**: `@agent.tool` (context-aware, orchestrates other tools)  
**Parameters**:
- `query` (str): The search query to analyze and execute
- `limit` (int, default=10): Maximum number of results to return (1-50)

**Implementation Pattern**:
```python
@agent.tool
async def auto_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Automatically select and execute optimal search strategy.
    
    Args:
        query: Natural language search query
        limit: Maximum number of results (1-50)
    
    Returns:
        Search results with metadata about search type used
    """
```

**Functionality**:
- Analyze query characteristics to determine optimal search type
- Route to semantic_search for conceptual/abstract queries
- Route to hybrid_search for queries with specific keywords or names
- Return results with metadata indicating search method used
- Default to semantic search if classification is uncertain

**Search Type Classification Logic**:
- **Semantic Search**: Abstract concepts, "what is", "how to", philosophical queries
- **Hybrid Search**: Queries with proper nouns, specific terms, technical jargon
- **Decision Factors**: Query length, presence of quotes, technical terminology

**Error Handling**:
- Default to semantic search on classification failure
- Cascade through search types if initial method fails
- Log decision reasoning for analytics

## Utility Functions

### Database Connection Management
```python
async def get_database_connection(ctx: RunContext[AgentDependencies]) -> asyncpg.Connection:
    """Get database connection with retry logic."""
```

### Embedding Generation
```python
async def generate_embedding(ctx: RunContext[AgentDependencies], text: str) -> List[float]:
    """Generate embedding using OpenAI API with caching."""
```

### Result Processing
```python
def format_search_results(results: List, search_type: str) -> Dict[str, Any]:
    """Standardize result format across search types."""
```

## Parameter Validation

All tools include validation for:
- Query length: 1-1000 characters
- Result limit: 1-50 results
- Text weight: 0.0-1.0 for hybrid search
- Non-empty string queries

## Performance Considerations

- **Caching**: Cache embeddings for repeated queries (5-minute TTL)
- **Connection Pooling**: Reuse database connections across tool calls
- **Rate Limiting**: Respect OpenAI API rate limits with retry logic
- **Timeout Handling**: 30-second timeout for database operations

## Dependencies Required

```python
from typing import Dict, Any, List, Optional
from pydantic_ai import RunContext
import asyncpg
import openai
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
```

## Integration Notes

- Tools work with `AgentDependencies` containing database URL and API keys
- All tools return consistent result format for easy chaining
- Error responses include helpful context for user feedback
- Logging integrated for search analytics and debugging

## Testing Strategy

- **Unit Tests**: Individual tool parameter validation and logic
- **Integration Tests**: End-to-end database connectivity and search operations
- **Mock Tests**: Test with TestModel to avoid external API calls
- **Performance Tests**: Search response times under load

This tool specification provides the minimal yet complete set of functions needed for the semantic search agent, following Pydantic AI best practices with proper error handling, parameter validation, and performance optimization.