# Create PRP

## Feature file: $ARGUMENTS

Generate a complete PRP for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

The AI agent only gets the context you are appending to the PRP and training data. Assuma the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the PRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

## Research Process

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRP
   - Note existing conventions to follow
   - Check test patterns for validation approach

2. **External Research**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls
   - Use Archon MCP server to gather latest Pydantic AI documentation
   - Web search for specific patterns and best practices relevant to the agent type
   - Research model provider capabilities and limitations
   - Investigate tool integration patterns and security considerations
   - Document async/sync patterns and testing strategies   

3. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

4. **Analyzing Initial Requirements**
   - Read and understand the agent feature requirements
   - Identify the type of agent needed (chat, tool-enabled, workflow, structured output)
   - Determine required model providers and external integrations
   - Assess complexity and scope of the agent implementation

5. **Agent Architecture Planning**
   - Design agent structure (agent.py, tools.py, models.py, dependencies.py)
   - Plan dependency injection patterns and external service integrations
   - Design structured output models using Pydantic validation
   - Plan tool registration and parameter validation strategies
   - Design testing approach with TestModel/FunctionModel patterns

6. **Implementation Blueprint Creation**
   - Create detailed agent implementation steps
   - Plan model provider configuration and fallback strategies
   - Design tool error handling and retry mechanisms
   - Plan security implementation (API keys, input validation, rate limiting)
   - Design validation loops with agent behavior testing

## PRP Generation

Using PRPs/templates/prp_pydantic_aibase.md as template:

### Critical Context to Include and pass to the AI agent as part of the PRP
- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint
- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- list tasks to be completed to fullfill the PRP in the order they should be completed

### Validation Gates (Must be Executable) eg for python
```bash
# Syntax/Style
ruff check --fix && mypy .

# Unit Tests
uv run pytest tests/ -v

```

*** CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE PRP ***

*** ULTRATHINK ABOUT THE PRP AND PLAN YOUR APPROACH THEN START WRITING THE PRP ***

## Output
Save as: `PRPs/{feature-name}.md`

## Quality Checklist
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context.
