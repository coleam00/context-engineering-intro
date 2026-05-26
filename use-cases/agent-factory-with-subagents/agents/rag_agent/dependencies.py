"""Dependencies for Semantic Search Agent."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import asyncpg
import openai
from settings import load_settings


@dataclass
class AgentDependencies:
    """Dependencies injected into the agent context."""
    
    # Core dependencies
    db_pool: Optional[asyncpg.Pool] = None
    openai_client: Optional[openai.AsyncOpenAI] = None
    settings: Optional[Any] = None
    
    # Session context
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    query_history: list = field(default_factory=list)
    
    async def initialize(self):
        """Initialize external connections."""
        if not self.settings:
            self.settings = load_settings()
        
        # Initialize database pool
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                self.settings.database_url,
                min_size=self.settings.db_pool_min_size,
                max_size=self.settings.db_pool_max_size
            )
        
        # Initialize OpenAI client (or compatible provider)
        if not self.openai_client:
            self.openai_client = openai.AsyncOpenAI(
                api_key=self.settings.llm_api_key,
                base_url=self.settings.llm_base_url
            )
    
    async def cleanup(self):
        """Clean up external connections."""
        if self.db_pool:
            await self.db_pool.close()
            self.db_pool = None
    
    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using OpenAI."""
        if not self.openai_client:
            await self.initialize()
        
        response = await self.openai_client.embeddings.create(
            model=self.settings.embedding_model,
            input=text
        )
        # Return as list of floats - asyncpg will handle conversion
        return response.data[0].embedding
    
    def set_user_preference(self, key: str, value: Any):
        """Set a user preference for the session."""
        self.user_preferences[key] = value
    
    def add_to_history(self, query: str):
        """Add a query to the search history."""
        self.query_history.append(query)
        # Keep only last 10 queries
        if len(self.query_history) > 10:
            self.query_history.pop(0)