"""Search tools for Semantic Search Agent."""

from typing import Optional, List, Dict, Any
from pydantic_ai import RunContext
from pydantic import BaseModel, Field
import asyncpg
import json
from dependencies import AgentDependencies


class SearchResult(BaseModel):
    """Model for search results."""
    chunk_id: str
    document_id: str
    content: str
    similarity: float
    metadata: Dict[str, Any]
    document_title: str
    document_source: str


async def semantic_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    match_count: Optional[int] = None
) -> List[SearchResult]:
    """
    Perform pure semantic search using vector similarity.
    
    Args:
        ctx: Agent runtime context with dependencies
        query: Search query text
        match_count: Number of results to return (default: 10)
    
    Returns:
        List of search results ordered by similarity
    """
    try:
        deps = ctx.deps
        
        # Use default if not specified
        if match_count is None:
            match_count = deps.settings.default_match_count
        
        # Validate match count
        match_count = min(match_count, deps.settings.max_match_count)
        
        # Generate embedding for query
        query_embedding = await deps.get_embedding(query)
        
        # Convert embedding to PostgreSQL vector string format
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Execute semantic search
        async with deps.db_pool.acquire() as conn:
            results = await conn.fetch(
                """
                SELECT * FROM match_chunks($1::vector, $2)
                """,
                embedding_str,
                match_count
            )
        
        # Convert to SearchResult objects
        return [
            SearchResult(
                chunk_id=str(row['chunk_id']),
                document_id=str(row['document_id']),
                content=row['content'],
                similarity=row['similarity'],
                metadata=json.loads(row['metadata']) if row['metadata'] else {},
                document_title=row['document_title'],
                document_source=row['document_source']
            )
            for row in results
        ]
    except Exception as e:
        print(e)
        return f"Failed to perform a semantic search: {e}"


async def hybrid_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    match_count: Optional[int] = None,
    text_weight: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Perform hybrid search combining semantic and keyword matching.
    
    Args:
        ctx: Agent runtime context with dependencies
        query: Search query text
        match_count: Number of results to return (default: 10)
        text_weight: Weight for text matching (0-1, default: 0.3)
    
    Returns:
        List of search results with combined scores
    """
    try:
        deps = ctx.deps
        
        # Use defaults if not specified
        if match_count is None:
            match_count = deps.settings.default_match_count
        if text_weight is None:
            text_weight = deps.user_preferences.get('text_weight', deps.settings.default_text_weight)
        
        # Validate parameters
        match_count = min(match_count, deps.settings.max_match_count)
        text_weight = max(0.0, min(1.0, text_weight))
        
        # Generate embedding for query
        query_embedding = await deps.get_embedding(query)
        
        # Convert embedding to PostgreSQL vector string format
        # PostgreSQL vector format: '[1.0,2.0,3.0]' (no spaces after commas)
        embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Execute hybrid search
        async with deps.db_pool.acquire() as conn:
            results = await conn.fetch(
                """
                SELECT * FROM hybrid_search($1::vector, $2, $3, $4)
                """,
                embedding_str,
                query,
                match_count,
                text_weight
            )
        
        # Convert to dictionaries with additional scores
        return [
            {
                'chunk_id': str(row['chunk_id']),
                'document_id': str(row['document_id']),
                'content': row['content'],
                'combined_score': row['combined_score'],
                'vector_similarity': row['vector_similarity'],
                'text_similarity': row['text_similarity'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else {},
                'document_title': row['document_title'],
                'document_source': row['document_source']
            }
            for row in results
        ]
    except Exception as e:
        print(e)
        return f"Failed to perform hybrid search: {e}"
