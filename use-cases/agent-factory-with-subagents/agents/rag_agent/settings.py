"""Settings configuration for Semantic Search Agent."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database Configuration
    database_url: str = Field(
        ...,
        description="PostgreSQL connection URL with PGVector extension"
    )
    
    # LLM Configuration (OpenAI-compatible)
    llm_provider: str = Field(
        default="openai",
        description="LLM provider (openai, anthropic, gemini, ollama, etc.)"
    )
    
    llm_api_key: str = Field(
        ...,
        description="API key for the LLM provider"
    )
    
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Model to use for search and summarization"
    )
    
    llm_base_url: Optional[str] = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API (for OpenAI-compatible providers)"
    )
    
    # Search Configuration
    default_match_count: int = Field(
        default=10,
        description="Default number of search results to return"
    )
    
    max_match_count: int = Field(
        default=50,
        description="Maximum number of search results allowed"
    )
    
    default_text_weight: float = Field(
        default=0.3,
        description="Default text weight for hybrid search (0-1)"
    )
    
    # Connection Pool Configuration
    db_pool_min_size: int = Field(
        default=10,
        description="Minimum database connection pool size"
    )
    
    db_pool_max_size: int = Field(
        default=20,
        description="Maximum database connection pool size"
    )
    
    # Embedding Configuration
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model"
    )
    
    embedding_dimension: int = Field(
        default=1536,
        description="Embedding vector dimension"
    )


def load_settings() -> Settings:
    """Load settings with proper error handling."""
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "database_url" in str(e).lower():
            error_msg += "\nMake sure to set DATABASE_URL in your .env file"
        if "openai_api_key" in str(e).lower():
            error_msg += "\nMake sure to set OPENAI_API_KEY in your .env file"
        raise ValueError(error_msg) from e