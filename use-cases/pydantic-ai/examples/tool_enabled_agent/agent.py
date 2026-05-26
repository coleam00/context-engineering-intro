"""
Tool-Enabled Agent with Web Search and Calculator

Demonstrates PydanticAI tool integration patterns:
- Environment-based model configuration
- Tool registration with @agent.tool decorator
- RunContext for dependency injection
- Parameter validation with type hints
- Error handling and retry mechanisms
- String output (default, no result_type needed)
"""

import logging
import math
import json
import asyncio
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
import aiohttp
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
    """Configuration settings for the tool-enabled agent."""
    
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
class ToolDependencies:
    """Dependencies for tool-enabled agent."""
    session: Optional[aiohttp.ClientSession] = None
    api_timeout: int = 10
    max_search_results: int = 5
    calculation_precision: int = 6
    session_id: Optional[str] = None


SYSTEM_PROMPT = """
You are a helpful research assistant with access to web search and calculation tools.

Your capabilities:
- Web search for current information and facts
- Mathematical calculations and data analysis
- Data processing and formatting
- Source verification and citation

Guidelines:
- Always use tools when you need current information or calculations
- Cite sources when providing factual information
- Show your work for mathematical calculations
- Be precise and accurate in your responses
- If tools fail, explain the limitation and provide what you can
"""


# Create the tool-enabled agent - note: no result_type, defaults to string
tool_agent = Agent(
    get_llm_model(),
    deps_type=ToolDependencies,
    system_prompt=SYSTEM_PROMPT
)


@tool_agent.tool
async def web_search(
    ctx: RunContext[ToolDependencies], 
    query: str,
    max_results: Optional[int] = None
) -> str:
    """
    Search the web for current information.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted search results with titles, snippets, and URLs
    """
    if not ctx.deps.session:
        return "Web search unavailable: No HTTP session configured"
    
    max_results = max_results or ctx.deps.max_search_results
    
    try:
        # Using DuckDuckGo Instant Answer API as a simple example
        # In production, use proper search APIs like Google, Bing, or DuckDuckGo
        search_url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "pretty": "1",
            "no_redirect": "1"
        }
        
        async with ctx.deps.session.get(
            search_url, 
            params=params, 
            timeout=ctx.deps.api_timeout
        ) as response:
            if response.status == 200:
                data = await response.json()
                
                results = []
                
                # Process instant answer if available
                if data.get("AbstractText"):
                    results.append({
                        "title": "Instant Answer",
                        "snippet": data["AbstractText"],
                        "url": data.get("AbstractURL", "")
                    })
                
                # Process related topics
                for topic in data.get("RelatedTopics", [])[:max_results-len(results)]:
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append({
                            "title": topic.get("FirstURL", "").split("/")[-1].replace("_", " "),
                            "snippet": topic["Text"],
                            "url": topic.get("FirstURL", "")
                        })
                
                if not results:
                    return f"No results found for query: {query}"
                
                # Format results
                formatted_results = []
                for i, result in enumerate(results, 1):
                    formatted_results.append(
                        f"{i}. **{result['title']}**\n"
                        f"   {result['snippet']}\n"
                        f"   Source: {result['url']}"
                    )
                
                return "\n\n".join(formatted_results)
            else:
                return f"Search failed with status: {response.status}"
                
    except asyncio.TimeoutError:
        return f"Search timed out after {ctx.deps.api_timeout} seconds"
    except Exception as e:
        return f"Search error: {str(e)}"


@tool_agent.tool
def calculate(
    ctx: RunContext[ToolDependencies],
    expression: str,
    description: Optional[str] = None
) -> str:
    """
    Perform mathematical calculations safely.
    
    Args:
        expression: Mathematical expression to evaluate
        description: Optional description of what's being calculated
    
    Returns:
        Calculation result with formatted output
    """
    try:
        # Safe evaluation - only allow mathematical operations
        allowed_names = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow, "sqrt": math.sqrt,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log, "log10": math.log10, "exp": math.exp,
            "pi": math.pi, "e": math.e
        }
        
        # Remove any potentially dangerous operations
        safe_expression = expression.replace("__", "").replace("import", "")
        
        # Evaluate the expression
        result = eval(safe_expression, {"__builtins__": {}}, allowed_names)
        
        # Format result with appropriate precision
        if isinstance(result, float):
            result = round(result, ctx.deps.calculation_precision)
        
        output = f"Calculation: {expression} = {result}"
        if description:
            output = f"{description}\n{output}"
        
        return output
        
    except Exception as e:
        return f"Calculation error: {str(e)}\nExpression: {expression}"


@tool_agent.tool
def format_data(
    ctx: RunContext[ToolDependencies],
    data: str,
    format_type: str = "table"
) -> str:
    """
    Format data into structured output.
    
    Args:
        data: Raw data to format
        format_type: Type of formatting (table, list, json)
    
    Returns:
        Formatted data string
    """
    try:
        lines = data.strip().split('\n')
        
        if format_type == "table":
            # Simple table formatting
            if len(lines) > 1:
                header = lines[0]
                rows = lines[1:]
                
                # Basic table formatting
                formatted = f"| {header} |\n"
                formatted += f"|{'-' * (len(header) + 2)}|\n"
                for row in rows[:10]:  # Limit to 10 rows
                    formatted += f"| {row} |\n"
                
                return formatted
            else:
                return data
                
        elif format_type == "list":
            # Bullet point list
            formatted_lines = [f"• {line.strip()}" for line in lines if line.strip()]
            return "\n".join(formatted_lines)
            
        elif format_type == "json":
            # Try to parse and format as JSON
            try:
                parsed = json.loads(data)
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                # If not valid JSON, create simple key-value structure
                items = {}
                for i, line in enumerate(lines):
                    items[f"item_{i+1}"] = line.strip()
                return json.dumps(items, indent=2)
        
        return data
        
    except Exception as e:
        return f"Formatting error: {str(e)}"


@tool_agent.tool
def get_current_time(ctx: RunContext[ToolDependencies]) -> str:
    """
    Get the current date and time.
    
    Returns:
        Current timestamp in a readable format
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")


async def ask_agent(
    question: str, 
    dependencies: Optional[ToolDependencies] = None
) -> str:
    """
    Ask the tool-enabled agent a question.
    
    Args:
        question: Question or request for the agent
        dependencies: Optional tool dependencies
    
    Returns:
        String response from the agent
    """
    if dependencies is None:
        # Create HTTP session for web search
        session = aiohttp.ClientSession()
        dependencies = ToolDependencies(session=session)
    
    try:
        result = await tool_agent.run(question, deps=dependencies)
        return result.data
    finally:
        # Clean up session if we created it
        if dependencies.session and not dependencies.session.closed:
            await dependencies.session.close()


def ask_agent_sync(question: str) -> str:
    """
    Synchronous version of ask_agent.
    
    Args:
        question: Question or request for the agent
    
    Returns:
        String response from the agent
    """
    return asyncio.run(ask_agent(question))


# Example usage and demonstration
if __name__ == "__main__":
    async def demo_tools():
        """Demonstrate the tool-enabled agent capabilities."""
        print("=== Tool-Enabled Agent Demo ===\n")
        
        # Create dependencies with HTTP session
        session = aiohttp.ClientSession()
        dependencies = ToolDependencies(session=session)
        
        try:
            # Sample questions that exercise different tools
            questions = [
                "What's the current time?",
                "Calculate the square root of 144 plus 25% of 200",
                "Search for recent news about artificial intelligence",
                "Format this data as a table: Name,Age\nAlice,25\nBob,30\nCharlie,35"
            ]
            
            for question in questions:
                print(f"Question: {question}")
                
                response = await ask_agent(question, dependencies)
                
                print(f"Answer: {response}")
                print("-" * 60)
                
        finally:
            await session.close()
    
    # Run the demo
    asyncio.run(demo_tools())