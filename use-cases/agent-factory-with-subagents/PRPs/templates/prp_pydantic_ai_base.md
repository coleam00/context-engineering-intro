---
name: "PydanticAI Agent PRP Template"
description: "Template for generating comprehensive PRPs for PydanticAI agent development projects"
---

## Purpose

[Brief description of the PydanticAI agent to be built and its main purpose]

## Core Principles

1. **PydanticAI Best Practices**: Deep integration with PydanticAI patterns for agent creation, tools, and structured outputs
2. **Production Ready**: Include security, testing, and monitoring for production deployments
3. **Type Safety First**: Leverage PydanticAI's type-safe design and Pydantic validation throughout
4. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

### What NOT to do:
- ❌ **Don't create dozens of tools** - Build only the tools your agent actually needs
- ❌ **Don't over-complicate dependencies** - Keep dependency injection simple and focused
- ❌ **Don't add unnecessary abstractions** - Follow main_agent_reference patterns directly
- ❌ **Don't build complex workflows** unless specifically required
- ❌ **Don't add structured output** unless validation is specifically needed (default to string)
- ❌ **Don't build in the examples/ folder**

### What TO do:
- ✅ **Start simple** - Build the minimum viable agent that meets requirements
- ✅ **Add tools incrementally** - Implement only what the agent needs to function
- ✅ **Follow main_agent_reference** - Use proven patterns, don't reinvent
- ✅ **Use string output by default** - Only add result_type when validation is required
- ✅ **Test early and often** - Use TestModel to validate as you build

### Key Question:
**"Does this agent really need this feature to accomplish its core purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

[Detailed description of what the agent should accomplish]

## Why

[Explanation of why this agent is needed and what problem it solves]

## What

### Agent Type Classification
- [ ] **Chat Agent**: Conversational interface with memory and context
- [ ] **Tool-Enabled Agent**: Agent with external tool integration capabilities
- [ ] **Workflow Agent**: Multi-step task processing and orchestration
- [ ] **Structured Output Agent**: Complex data validation and formatting

### Model Provider Requirements
- [ ] **OpenAI**: `openai:gpt-4o` or `openai:gpt-4o-mini`
- [ ] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022` or `anthropic:claude-3-5-haiku-20241022`
- [ ] **Google**: `gemini-1.5-flash` or `gemini-1.5-pro`
- [ ] **Fallback Strategy**: Multiple provider support with automatic failover

### External Integrations
- [ ] Database connections (specify type: PostgreSQL, MongoDB, etc.)
- [ ] REST API integrations (list required services)
- [ ] File system operations
- [ ] Web scraping or search capabilities
- [ ] Real-time data sources

### Success Criteria
- [ ] Agent successfully handles specified use cases
- [ ] All tools work correctly with proper error handling
- [ ] Structured outputs validate according to Pydantic models
- [ ] Comprehensive test coverage with TestModel and FunctionModel
- [ ] Security measures implemented (API keys, input validation, rate limiting)
- [ ] Performance meets requirements (response time, throughput)

## All Needed Context

### PydanticAI Documentation & Research

```yaml
# MCP servers
- mcp: Archon
  query: "PydanticAI agent creation model providers tools dependencies"
  why: Core framework understanding and latest patterns

# ESSENTIAL PYDANTIC AI DOCUMENTATION - Must be researched
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with getting started guide
  content: Agent creation, model providers, dependency injection patterns

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns
  content: System prompts, output types, execution methods, agent composition

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration
  content: @agent.tool decorators, RunContext usage, parameter validation

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to PydanticAI agents
  content: TestModel, FunctionModel, Agent.override(), pytest patterns

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and authentication
  content: OpenAI, Anthropic, Gemini setup, API key management, fallback models

# Prebuilt examples
- path: examples/
  why: Reference implementations for Pydantic AI agents
  content: A bunch of already built simple Pydantic AI examples to reference including how to set up models and providers

- path: examples/cli.py
  why: Shows real-world interaction with Pydantic AI agents
  content: Conversational CLI with streaming, tool call visibility, and conversation handling - demonstrates how users actually interact with agents
```

### Agent Architecture Research

```yaml
# PydanticAI Architecture Patterns (follow main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Environment-based configuration with pydantic-settings
    - providers.py: Model provider abstraction with get_llm_model()
    - Environment variables for API keys and model selection
    - Never hardcode model strings like "openai:gpt-4o"
  
  agent_definition:
    - Default to string output (no result_type unless structured output needed)
    - Use get_llm_model() from providers.py for model configuration
    - System prompts as string constants or functions
    - Dataclass dependencies for external services
  
  tool_integration:
    - @agent.tool for context-aware tools with RunContext[DepsType]
    - Tool functions as pure functions that can be called independently
    - Proper error handling and logging in tool implementations
    - Dependency injection through RunContext.deps
  
  testing_strategy:
    - TestModel for rapid development validation
    - FunctionModel for custom behavior testing  
    - Agent.override() for test isolation
    - Comprehensive tool testing with mocks
```

### Security and Production Considerations

```yaml
# PydanticAI Security Patterns (research required)
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
    secure_storage: "Never commit API keys to version control"
    rotation_strategy: "Plan for key rotation and management"
  
  input_validation:
    sanitization: "Validate all user inputs with Pydantic models"
    prompt_injection: "Implement prompt injection prevention strategies"
    rate_limiting: "Prevent abuse with proper throttling"
  
  output_security:
    data_filtering: "Ensure no sensitive data in agent responses"
    content_validation: "Validate output structure and content"
    logging_safety: "Safe logging without exposing secrets"
```

### Common PydanticAI Gotchas (research and document)

```yaml
# Agent-specific gotchas to research and address
implementation_gotchas:
  async_patterns:
    issue: "Mixing sync and async agent calls inconsistently"
    research: "PydanticAI async/await best practices"
    solution: "[To be documented based on research]"
  
  model_limits:
    issue: "Different models have different capabilities and token limits"
    research: "Model provider comparison and capabilities"
    solution: "[To be documented based on research]"
  
  dependency_complexity:
    issue: "Complex dependency graphs can be hard to debug"
    research: "Dependency injection best practices in PydanticAI"
    solution: "[To be documented based on research]"
  
  tool_error_handling:
    issue: "Tool failures can crash entire agent runs"
    research: "Error handling and retry patterns for tools"
    solution: "[To be documented based on research]"
```

## Implementation Blueprint

### Technology Research Phase

**RESEARCH REQUIRED - Complete before implementation:**

✅ **PydanticAI Framework Deep Dive:**
- [ ] Agent creation patterns and best practices
- [ ] Model provider configuration and fallback strategies
- [ ] Tool integration patterns (@agent.tool vs @agent.tool_plain)
- [ ] Dependency injection system and type safety
- [ ] Testing strategies with TestModel and FunctionModel

✅ **Agent Architecture Investigation:**
- [ ] Project structure conventions (agent.py, tools.py, models.py, dependencies.py)
- [ ] System prompt design (static vs dynamic)
- [ ] Structured output validation with Pydantic models
- [ ] Async/sync patterns and streaming support
- [ ] Error handling and retry mechanisms

✅ **Security and Production Patterns:**
- [ ] API key management and secure configuration
- [ ] Input validation and prompt injection prevention
- [ ] Rate limiting and monitoring strategies
- [ ] Logging and observability patterns
- [ ] Deployment and scaling considerations

### Agent Implementation Plan

```yaml
Implementation Task 1 - Agent Architecture Setup (Follow main_agent_reference):
  CREATE agent project structure:
    - settings.py: Environment-based configuration with pydantic-settings
    - providers.py: Model provider abstraction with get_llm_model()
    - agent.py: Main agent definition (default string output)
    - tools.py: Tool functions with proper decorators
    - dependencies.py: External service integrations (dataclasses)
    - tests/: Comprehensive test suite

Implementation Task 2 - Core Agent Development:
  IMPLEMENT agent.py following main_agent_reference patterns:
    - Use get_llm_model() from providers.py for model configuration
    - System prompt as string constant or function
    - Dependency injection with dataclass
    - NO result_type unless structured output specifically needed
    - Error handling and logging

Implementation Task 3 - Tool Integration:
  DEVELOP tools.py:
    - Tool functions with @agent.tool decorators
    - RunContext[DepsType] integration for dependency access
    - Parameter validation with proper type hints
    - Error handling and retry mechanisms
    - Tool documentation and schema generation

Implementation Task 4 - Data Models and Dependencies:
  CREATE models.py and dependencies.py:
    - Pydantic models for structured outputs
    - Dependency classes for external services
    - Input validation models for tools
    - Custom validators and constraints

Implementation Task 5 - Comprehensive Testing:
  IMPLEMENT testing suite:
    - TestModel integration for rapid development
    - FunctionModel tests for custom behavior
    - Agent.override() patterns for isolation
    - Integration tests with real providers
    - Tool validation and error scenario testing

Implementation Task 6 - Security and Configuration:
  SETUP security patterns:
    - Environment variable management for API keys
    - Input sanitization and validation
    - Rate limiting implementation
    - Secure logging and monitoring
    - Production deployment configuration
```

## Validation Loop

### Level 1: Agent Structure Validation

```bash
# Verify complete agent project structure
find agent_project -name "*.py" | sort
test -f agent_project/agent.py && echo "Agent definition present"
test -f agent_project/tools.py && echo "Tools module present"
test -f agent_project/models.py && echo "Models module present"
test -f agent_project/dependencies.py && echo "Dependencies module present"

# Verify proper PydanticAI imports
grep -q "from pydantic_ai import Agent" agent_project/agent.py
grep -q "@agent.tool" agent_project/tools.py
grep -q "from pydantic import BaseModel" agent_project/models.py

# Expected: All required files with proper PydanticAI patterns
# If missing: Generate missing components with correct patterns
```

### Level 2: Agent Functionality Validation

```bash
# Test agent can be imported and instantiated
python -c "
from agent_project.agent import agent
print('Agent created successfully')
print(f'Model: {agent.model}')
print(f'Tools: {len(agent.tools)}')
"

# Test with TestModel for validation
python -c "
from pydantic_ai.models.test import TestModel
from agent_project.agent import agent
test_model = TestModel()
with agent.override(model=test_model):
    result = agent.run_sync('Test message')
    print(f'Agent response: {result.output}')
"

# Expected: Agent instantiation works, tools registered, TestModel validation passes
# If failing: Debug agent configuration and tool registration
```

### Level 3: Comprehensive Testing Validation

```bash
# Run complete test suite
cd agent_project
python -m pytest tests/ -v

# Test specific agent behavior
python -m pytest tests/test_agent.py::test_agent_response -v
python -m pytest tests/test_tools.py::test_tool_validation -v
python -m pytest tests/test_models.py::test_output_validation -v

# Expected: All tests pass, comprehensive coverage achieved
# If failing: Fix implementation based on test failures
```

### Level 4: Production Readiness Validation

```bash
# Verify security patterns
grep -r "API_KEY" agent_project/ | grep -v ".py:" # Should not expose keys
test -f agent_project/.env.example && echo "Environment template present"

# Check error handling
grep -r "try:" agent_project/ | wc -l  # Should have error handling
grep -r "except" agent_project/ | wc -l  # Should have exception handling

# Verify logging setup
grep -r "logging\|logger" agent_project/ | wc -l  # Should have logging

# Expected: Security measures in place, error handling comprehensive, logging configured
# If issues: Implement missing security and production patterns
```

## Final Validation Checklist

### Agent Implementation Completeness

- [ ] Complete agent project structure: `agent.py`, `tools.py`, `models.py`, `dependencies.py`
- [ ] Agent instantiation with proper model provider configuration
- [ ] Tool registration with @agent.tool decorators and RunContext integration
- [ ] Structured outputs with Pydantic model validation
- [ ] Dependency injection properly configured and tested
- [ ] Comprehensive test suite with TestModel and FunctionModel

### PydanticAI Best Practices

- [ ] Type safety throughout with proper type hints and validation
- [ ] Security patterns implemented (API keys, input validation, rate limiting)
- [ ] Error handling and retry mechanisms for robust operation
- [ ] Async/sync patterns consistent and appropriate
- [ ] Documentation and code comments for maintainability

### Production Readiness

- [ ] Environment configuration with .env files and validation
- [ ] Logging and monitoring setup for observability
- [ ] Performance optimization and resource management
- [ ] Deployment readiness with proper configuration management
- [ ] Maintenance and update strategies documented

---

## Anti-Patterns to Avoid

### PydanticAI Agent Development

- ❌ Don't skip TestModel validation - always test with TestModel during development
- ❌ Don't hardcode API keys - use environment variables for all credentials
- ❌ Don't ignore async patterns - PydanticAI has specific async/sync requirements
- ❌ Don't create complex tool chains - keep tools focused and composable
- ❌ Don't skip error handling - implement comprehensive retry and fallback mechanisms

### Agent Architecture

- ❌ Don't mix agent types - clearly separate chat, tool, workflow, and structured output patterns
- ❌ Don't ignore dependency injection - use proper type-safe dependency management
- ❌ Don't skip output validation - always use Pydantic models for structured responses
- ❌ Don't forget tool documentation - ensure all tools have proper descriptions and schemas

### Security and Production

- ❌ Don't expose sensitive data - validate all outputs and logs for security
- ❌ Don't skip input validation - sanitize and validate all user inputs
- ❌ Don't ignore rate limiting - implement proper throttling for external services
- ❌ Don't deploy without monitoring - include proper observability from the start

**RESEARCH STATUS: [TO BE COMPLETED]** - Complete comprehensive PydanticAI research before implementation begins.