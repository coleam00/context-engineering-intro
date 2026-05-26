"""
Simplified provider configuration for OpenAI models only.
"""

import os
from typing import Optional
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_llm_model() -> OpenAIModel:
    """
    Get LLM model configuration for OpenAI.
    
    Returns:
        Configured OpenAI model
    """
    llm_choice = os.getenv('LLM_CHOICE', 'gpt-4.1-mini')
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return OpenAIModel(llm_choice, provider=OpenAIProvider(api_key=api_key))


def get_embedding_client() -> openai.AsyncOpenAI:
    """
    Get OpenAI client for embeddings.
    
    Returns:
        Configured OpenAI client for embeddings
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return openai.AsyncOpenAI(api_key=api_key)


def get_embedding_model() -> str:
    """
    Get embedding model name.
    
    Returns:
        Embedding model name
    """
    return os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')


def get_ingestion_model() -> OpenAIModel:
    """
    Get model for ingestion tasks (uses same model as main LLM).
    
    Returns:
        Configured model for ingestion tasks
    """
    return get_llm_model()


def validate_configuration() -> bool:
    """
    Validate that required environment variables are set.
    
    Returns:
        True if configuration is valid
    """
    required_vars = [
        'OPENAI_API_KEY',
        'DATABASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True


def get_model_info() -> dict:
    """
    Get information about current model configuration.
    
    Returns:
        Dictionary with model configuration info
    """
    return {
        "llm_provider": "openai",
        "llm_model": os.getenv('LLM_CHOICE', 'gpt-4.1-mini'),
        "embedding_provider": "openai",
        "embedding_model": get_embedding_model(),
    }