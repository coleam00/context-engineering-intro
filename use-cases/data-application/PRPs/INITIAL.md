## FEATURE:

[REPLACE EVERYTHING IN BRACKETS WITH YOUR OWN CONTEXT]
[Provide an overview of the agent you want to build. The more detail the better!]
[Overly simple example: Build a simple research agent using Pydantic AI that can research topics with the Brave API and draft emails with Gmail to share insights.]

## TOOLS:

[Describe the tools you want for your agent(s) - functionality, arguments, what they return, etc. Be as specific as you like - the more specific the better.]

## DEPENDENCIES

[Describe the dependencies needed for the agent tools (for the Pydantic AI RunContext) - things like API keys, DB connections, an HTTP client, etc.]

## SYSTEM PROMPT(S)

[Describe the instructions for the agent(s) here - you can create the entire system prompt here or give a general description to guide the coding assistant]

## EXAMPLES:

[Add any additional example agents/tool implementations from past projects or online resources to the examples/ folder and reference them here.]
[The template contains the following already for Pydantic AI:]

- examples/basic_chat_agent - Basic chat agent with conversation memory
- examples/tool_enabled_agent - Tool-enabled agent with web search capabilities  
- examples/structured_output_agent - Structured output agent for data validation
- examples/testing_examples - Testing examples with TestModel and FunctionModel
- examples/main_agent_reference - Best practices for building Pydantic AI agents

## DOCUMENTATION:

[Add any additional documentation you want it to reference - this can be curated docs you put in PRPs/ai_docs, URLs, etc.]

- Pydantic AI Official Documentation: https://ai.pydantic.dev/
- Agent Creation Guide: https://ai.pydantic.dev/agents/
- Tool Integration: https://ai.pydantic.dev/tools/
- Testing Patterns: https://ai.pydantic.dev/testing/
- Model Providers: https://ai.pydantic.dev/models/

## OTHER CONSIDERATIONS:

- Use environment variables for API key configuration instead of hardcoded model strings
- Keep agents simple - default to string output unless structured output is specifically needed
- Follow the main_agent_reference patterns for configuration and providers
- Always include comprehensive testing with TestModel for development

[Add any additional considerations for the coding assistant, especially "gotchas" you want it to keep in mind.]