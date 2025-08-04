"""
Configuration management for the novel extractor system.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # LLM Configuration
    llm_api_key: str = Field(..., description="API key for LLM provider")
    llm_provider: str = Field(default="openai", description="LLM provider name")
    llm_model: str = Field(default="gpt-4", description="Model to use")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", description="Base URL for LLM API"
    )

    # Context Configuration
    max_context_length: int = Field(default=8192, description="Maximum context tokens")
    compression_threshold: float = Field(
        default=0.8, description="Compression trigger (0-1)"
    )
    reserved_response_tokens: int = Field(
        default=2000, description="Tokens reserved for LLM response"
    )

    # Retry Configuration
    max_retries: int = Field(default=3, description="Maximum API retry attempts")
    retry_delay: float = Field(
        default=1.0, description="Initial retry delay in seconds"
    )

    # File Configuration
    settings_dir: str = Field(
        default="settings", description="Directory for novel settings files"
    )

    @field_validator("compression_threshold")
    @classmethod
    def validate_compression_threshold(cls, v: float) -> float:
        """
        Validate compression threshold is between 0 and 1.

        Args:
            v: Compression threshold value

        Returns:
            float: Validated threshold

        Raises:
            ValueError: If threshold is not between 0 and 1
        """
        if not 0 < v <= 1:
            raise ValueError("Compression threshold must be between 0 and 1")
        return v

    @field_validator("max_context_length")
    @classmethod
    def validate_max_context_length(cls, v: int) -> int:
        """
        Validate context length is positive.

        Args:
            v: Maximum context length

        Returns:
            int: Validated context length

        Raises:
            ValueError: If context length is not positive
        """
        if v <= 0:
            raise ValueError("Max context length must be positive")
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def settings_path(self) -> str:
        """
        Get absolute path to settings directory.

        Returns:
            str: Absolute path to settings directory
        """
        return os.path.abspath(self.settings_dir)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application settings
    """
    return Settings()
