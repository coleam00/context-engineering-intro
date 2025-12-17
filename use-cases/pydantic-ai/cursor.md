# PydanticAI Context Engineering - Global Rules for AI Agent Development

This file contains the global rules and principles that apply to ALL PydanticAI agent development work. These rules are specialized for building production-grade AI agents with tools, memory, and structured outputs.

## 🔄 PydanticAI Core Principles

**IMPORTANT: These principles apply to ALL PydanticAI agent development:**

### Agent Development Workflow
- **Always start with INITIAL.md** - Define agent requirements before generating PRPs
- **Use the PRP pattern**: INITIAL.md → `/generate-pydantic-ai-prp INITIAL.md` → `/execute-pydantic-ai-prp PRPs/filename.md`
- **Follow validation loops** - Each PRP must include agent testing with TestModel/FunctionModel
- **Context is King** - Include ALL necessary PydanticAI patterns, examples, and documentation

### Research Methodology for AI Agents
- **Web search extensively** - Always research PydanticAI patterns and best practices
- **Study official documentation** - ai.pydantic.dev is the authoritative source
- **Pattern extraction** - Identify reusable agent architectures and tool patterns
- **Gotcha documentation** - Document async patterns, model limits, and context management issues

## 📚 Project Awareness & Context

- **Use a virtual environment** to run all code and tests. If one isn't already in the codebase when needed, create it
- **Use consistent PydanticAI naming conventions** and agent structure patterns
- **Follow established agent directory organization** patterns (agent.py, tools.py, models.py)
- **Leverage PydanticAI examples extensively** - Study existing patterns before creating new agents

## 🧱 Agent Structure & Modularity

- **Never create files longer than 500 lines** - Split into modules when approaching limit
- **Organize agent code into clearly separated modules** grouped by responsibility:
  - `agent.py` - Main agent definition and execution logic
  - `tools.py` - Tool functions used by the agent
  - `models.py` - Pydantic output models and dependency classes
  - `dependencies.py` - Context dependencies and external service integrations
- **Use clear, consistent imports** - Import from pydantic_ai package appropriately
- **Use python-dotenv and load_dotenv()** for environment variables - Follow examples/main_agent_reference/settings.py pattern
- **Never hardcode sensitive information** - Always use .env files for API keys and configuration

## 🤖 PydanticAI Development Standards

### Agent Creation Patterns
- **Use model-agnostic design** - Support multiple providers (OpenAI, Anthropic, Gemini)
- **Implement dependency injection** - Use deps_type for external services and context
- **Define structured outputs** - Use Pydantic models for result validation
- **Include comprehensive system prompts** - Both static and dynamic instructions

### Tool Integration Standards
- **Use @agent.tool decorator** for context-aware tools with RunContext[DepsType]
- **Use @agent.tool_plain decorator** for simple tools without context dependencies
- **Implement proper parameter validation** - Use Pydantic models for tool parameters
- **Handle tool errors gracefully** - Implement retry mechanisms and error recovery

### Environment Variable Configuration with python-dotenv
```python
# Use python-dotenv and pydantic-settings for proper configuration management
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(default="gpt-4", description="Model name to use")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", 
        description="Base URL for the LLM API"
    )

def load_settings() -> Settings:
    """Load settings with proper error handling and environment loading."""
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file"
        raise ValueError(error_msg) from e

def get_llm_model():
    """Get configured LLM model with proper environment loading."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url, 
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
```

### Testing Standards for AI Agents
- **Use TestModel for development** - Fast validation without API calls
- **Use FunctionModel for custom behavior** - Control agent responses in tests
- **Use Agent.override() for testing** - Replace models in test contexts
- **Test both sync and async patterns** - Ensure compatibility with different execution modes
- **Test tool validation** - Verify tool parameter schemas and error handling

## ✅ Task Management for AI Development

- **Break agent development into clear steps** with specific completion criteria
- **Mark tasks complete immediately** after finishing agent implementations
- **Update task status in real-time** as agent development progresses
- **Test agent behavior** before marking implementation tasks complete

## 📎 PydanticAI Coding Standards

### Agent Architecture
```python
# Follow main_agent_reference patterns - no result_type unless structured output needed
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from .settings import load_settings

@dataclass
class AgentDependencies:
    """Dependencies for agent execution"""
    api_key: str
    session_id: str = None

# Load settings with proper dotenv handling
settings = load_settings()

# Simple agent with string output (default)
agent = Agent(
    get_llm_model(),  # Uses load_settings() internally
    deps_type=AgentDependencies,
    system_prompt="You are a helpful assistant..."
)

@agent.tool
async def example_tool(
    ctx: RunContext[AgentDependencies], 
    query: str
) -> str:
    """Tool with proper context access"""
    return await external_api_call(ctx.deps.api_key, query)
```

### Security Best Practices
- **API key management** - Use python-dotenv with .env files, never commit keys to version control
- **Environment variable loading** - Always use load_dotenv() following examples/main_agent_reference/settings.py
- **Input validation** - Use Pydantic models for all tool parameters
- **Rate limiting** - Implement proper request throttling for external APIs
- **Prompt injection prevention** - Validate and sanitize user inputs
- **Error handling** - Never expose sensitive information in error messages

### Common PydanticAI Gotchas
- **Async/sync mixing issues** - Be consistent with async/await patterns throughout
- **Model token limits** - Different models have different context limits, plan accordingly
- **Dependency injection complexity** - Keep dependency graphs simple and well-typed
- **Tool error handling failures** - Always implement proper retry and fallback mechanisms
- **Context state management** - Design stateless tools when possible for reliability

## 🔍 Research Standards for AI Agents

- **Use Archon MCP server** - Leverage available PydanticAI documentation via RAG
- **Study official examples** - ai.pydantic.dev/examples has working implementations
- **Research model capabilities** - Understand provider-specific features and limitations
- **Document integration patterns** - Include external service integration examples

## 🎯 Implementation Standards for AI Agents

- **Follow the PRP workflow religiously** - Don't skip agent validation steps
- **Always test with TestModel first** - Validate agent logic before using real models
- **Use existing agent patterns** rather than creating from scratch
- **Include comprehensive error handling** for tool failures and model errors
- **Test streaming patterns** when implementing real-time agent interactions

## 🚫 Anti-Patterns to Always Avoid

- ❌ Don't skip agent testing - Always use TestModel/FunctionModel for validation
- ❌ Don't hardcode model strings - Use environment-based configuration like main_agent_reference
- ❌ Don't use result_type unless structured output is specifically needed - default to string
- ❌ Don't ignore async patterns - PydanticAI has specific async/sync considerations
- ❌ Don't create complex dependency graphs - Keep dependencies simple and testable
- ❌ Don't forget tool error handling - Implement proper retry and graceful degradation
- ❌ Don't skip input validation - Use Pydantic models for all external inputs

## 🔧 Tool Usage Standards for AI Development

- **Use web search extensively** for PydanticAI research and documentation
- **Follow PydanticAI command patterns** for slash commands and agent workflows
- **Use agent validation loops** to ensure quality at each development step
- **Test with multiple model providers** to ensure agent compatibility

## 🧪 Testing & Reliability for AI Agents

- **Always create comprehensive agent tests** for tools, outputs, and error handling
- **Test agent behavior with TestModel** before using real model providers
- **Include edge case testing** for tool failures and model provider issues
- **Test both structured and unstructured outputs** to ensure agent flexibility
- **Validate dependency injection** works correctly in test environments

These global rules apply specifically to PydanticAI agent development and ensure production-ready AI applications with proper error handling, testing, and security practices.