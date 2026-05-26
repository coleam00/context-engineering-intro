"""
Basic Chat Agent with Memory and Context

A simple conversational agent that demonstrates core PydanticAI patterns:
- Environment-based model configuration
- System prompts for personality and behavior
- Basic conversation handling with memory
- String output (default, no result_type needed)
"""

import logging
from dataclasses import dataclass
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration settings for the chat agent."""
    
    # LLM Configuration
    llm_provider: str = Field(default="openai")
    llm_api_key: str = Field(...)
    llm_model: str = Field(default="gpt-4")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_llm_model() -> OpenAIModel:
    """Get configured LLM model from environment settings."""
    try:
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key
        )
        return OpenAIModel(settings.llm_model, provider=provider)
    except Exception:
        # For testing without env vars
        import os
        os.environ.setdefault("LLM_API_KEY", "test-key")
        settings = Settings()
        provider = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key="test-key"
        )
        return OpenAIModel(settings.llm_model, provider=provider)


@dataclass
class ConversationContext:
    """Simple context for conversation state management."""
    user_name: Optional[str] = None
    conversation_count: int = 0
    preferred_language: str = "English"
    session_id: Optional[str] = None


SYSTEM_PROMPT = """
You are a friendly and helpful AI assistant. 

Your personality:
- Warm and approachable
- Knowledgeable but humble
- Patient and understanding
- Encouraging and supportive

Guidelines:
- Keep responses conversational and natural
- Be helpful without being overwhelming
- Ask follow-up questions when appropriate
- Remember context from the conversation
- Adapt your tone to match the user's needs
"""


# Create the basic chat agent - note: no result_type, defaults to string
chat_agent = Agent(
    get_llm_model(),
    deps_type=ConversationContext,
    system_prompt=SYSTEM_PROMPT
)


@chat_agent.system_prompt
def dynamic_context_prompt(ctx) -> str:
    """Dynamic system prompt that includes conversation context."""
    prompt_parts = []
    
    if ctx.deps.user_name:
        prompt_parts.append(f"The user's name is {ctx.deps.user_name}.")
    
    if ctx.deps.conversation_count > 0:
        prompt_parts.append(f"This is message #{ctx.deps.conversation_count + 1} in your conversation.")
    
    if ctx.deps.preferred_language != "English":
        prompt_parts.append(f"The user prefers to communicate in {ctx.deps.preferred_language}.")
    
    return " ".join(prompt_parts) if prompt_parts else ""


async def chat_with_agent(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    Main function to chat with the agent.
    
    Args:
        message: User's message to the agent
        context: Optional conversation context for memory
    
    Returns:
        String response from the agent
    """
    if context is None:
        context = ConversationContext()
    
    # Increment conversation count
    context.conversation_count += 1
    
    # Run the agent with the message and context
    result = await chat_agent.run(message, deps=context)
    
    return result.data


def chat_with_agent_sync(message: str, context: Optional[ConversationContext] = None) -> str:
    """
    Synchronous version of chat_with_agent for simple use cases.
    
    Args:
        message: User's message to the agent
        context: Optional conversation context for memory
    
    Returns:
        String response from the agent
    """
    if context is None:
        context = ConversationContext()
    
    # Increment conversation count
    context.conversation_count += 1
    
    # Run the agent synchronously
    result = chat_agent.run_sync(message, deps=context)
    
    return result.data


# Example usage and demonstration
if __name__ == "__main__":
    import asyncio
    
    async def demo_conversation():
        """Demonstrate the basic chat agent with a simple conversation."""
        print("=== Basic Chat Agent Demo ===\n")
        
        # Create conversation context
        context = ConversationContext(
            user_name="Alex",
            preferred_language="English"
        )
        
        # Sample conversation
        messages = [
            "Hello! My name is Alex, nice to meet you.",
            "Can you help me understand what PydanticAI is?",
            "That's interesting! What makes it different from other AI frameworks?",
            "Thanks for the explanation. Can you recommend some good resources to learn more?"
        ]
        
        for message in messages:
            print(f"User: {message}")
            
            response = await chat_with_agent(message, context)
            
            print(f"Agent: {response}")
            print("-" * 50)
    
    # Run the demo
    asyncio.run(demo_conversation())