---
name: "PydanticAI Template Generator PRP"
description: "Generate comprehensive context engineering template for PydanticAI agent development with tools, memory, and structured outputs"
---

## Purpose

Generate a complete context engineering template package for **PydanticAI** that enables developers to rapidly build intelligent AI agents with tool integration, conversation handling, and structured data validation using the PydanticAI framework.

## Core Principles

1. **PydanticAI Specialization**: Deep integration with PydanticAI patterns for agent creation, tools, and structured outputs
2. **Complete Package Generation**: Create entire template ecosystem with working examples and validation
3. **Type Safety First**: Leverage PydanticAI's type-safe design and Pydantic validation throughout
4. **Production Ready**: Include security, testing, and best practices for production deployments
5. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development

---

## Goal

Generate a complete context engineering template package for **PydanticAI** that includes:

- PydanticAI-specific CLAUDE.md implementation guide with agent patterns
- Specialized PRP generation and execution commands for AI agents
- Domain-specific base PRP template with agent architecture patterns
- Comprehensive working examples (chat agents, tool integration, multi-step workflows)
- PydanticAI-specific validation loops and testing patterns

## Why

- **AI Development Acceleration**: Enable rapid development of production-grade PydanticAI agents
- **Pattern Consistency**: Maintain established AI agent architecture patterns and best practices
- **Quality Assurance**: Ensure comprehensive testing for agent behavior, tools, and outputs
- **Knowledge Capture**: Document PydanticAI-specific patterns, gotchas, and integration strategies
- **Scalable AI Framework**: Create reusable templates for various AI agent use cases

## What

### Template Package Components

**Complete Directory Structure:**
```
use-cases/pydantic-ai/
├── CLAUDE.md                           # PydanticAI implementation guide
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # Agent PRP generation
│   └── execute-pydantic-ai-prp.md      # Agent PRP execution  
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # PydanticAI base PRP template
│   ├── ai_docs/                        # PydanticAI documentation
│   └── INITIAL.md                      # Example agent feature request
├── examples/
│   ├── basic_chat_agent/               # Simple chat agent with memory
│   ├── tool_enabled_agent/             # Web search + calculator tools
│   ├── workflow_agent/                 # Multi-step workflow processing
│   ├── structured_output_agent/        # Custom Pydantic models
│   └── testing_examples/               # Agent testing patterns
├── copy_template.py                    # Template deployment script
└── README.md                           # Comprehensive usage guide
```

**PydanticAI Integration:**
- Agent creation with multiple model providers (OpenAI, Anthropic, Gemini)
- Tool integration patterns and function registration
- Conversation memory and context management using dependencies
- Structured output validation with Pydantic models
- Testing patterns using TestModel and FunctionModel
- Security patterns for API key management and input validation

**Context Engineering Adaptation:**
- PydanticAI-specific research processes and documentation references
- Agent-appropriate validation loops and testing strategies
- AI framework-specialized implementation blueprints
- Integration with base context engineering principles for AI development

### Success Criteria

- [ ] Complete PydanticAI template package structure generated
- [ ] All required files present with PydanticAI-specific content
- [ ] Agent patterns accurately represent PydanticAI best practices
- [ ] Context engineering principles adapted for AI agent development
- [ ] Validation loops appropriate for testing AI agents and tools
- [ ] Template immediately usable for creating PydanticAI projects
- [ ] Integration with base context engineering framework maintained
- [ ] Comprehensive examples and testing documentation included

## All Needed Context

### Documentation & References (RESEARCHED)

```yaml
# IMPORTANT - use the Archon MCP server to get more Pydantic AI documentation!
- mcp: Archon
  why: Official Pydantic AI documentation ready for RAG lookup
  content: All Pydantic AI documentation
# PYDANTIC AI CORE DOCUMENTATION - Essential framework understanding
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with core concepts and getting started
  content: Agent creation, model providers, type safety, dependency injection

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture, system prompts, tools, structured outputs
  content: Agent components, execution methods, configuration options

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration, API key management, fallback models
  content: OpenAI, Anthropic, Gemini integration patterns and authentication

- url: https://ai.pydantic.dev/tools/
  why: Function tool registration, context usage, rich returns, dynamic tools
  content: Tool decorators, parameter validation, documentation patterns

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies, TestModel, FunctionModel, pytest patterns
  content: Unit testing, agent behavior validation, mock model usage

- url: https://ai.pydantic.dev/examples/
  why: Working examples for various PydanticAI use cases
  content: Chat apps, RAG systems, SQL generation, FastAPI integration

# CONTEXT ENGINEERING FOUNDATION - Base framework to adapt
- file: ../../../README.md
  why: Core context engineering principles and workflow to adapt for AI agents

- file: ../../../.claude/commands/generate-prp.md
  why: Base PRP generation patterns to specialize for PydanticAI development

- file: ../../../.claude/commands/execute-prp.md  
  why: Base PRP execution patterns to adapt for AI agent validation

- file: ../../../PRPs/templates/prp_base.md
  why: Base PRP template structure to specialize for PydanticAI domain

# MCP SERVER EXAMPLE - Reference implementation
- file: ../mcp-server/CLAUDE.md
  why: Example of domain-specific implementation guide patterns
  
- file: ../mcp-server/.claude/commands/prp-mcp-create.md
  why: Example of specialized PRP generation command structure
```

### PydanticAI Framework Analysis (FROM RESEARCH)

```typescript
// PydanticAI Architecture Patterns (from official docs)
interface PydanticAIPatterns {
  // Core agent patterns
  agent_creation: {
    model_providers: ["openai:gpt-4o", "anthropic:claude-3-sonnet", "google:gemini-1.5-flash"];
    configuration: ["system_prompt", "deps_type", "output_type", "instructions"];
    execution_methods: ["run()", "run_sync()", "run_stream()", "iter()"];
  };
  
  // Tool integration patterns
  tool_system: {
    registration: ["@agent.tool", "@agent.tool_plain", "tools=[]"];
    context_access: ["RunContext[DepsType]", "ctx.deps", "dependency_injection"];
    return_types: ["str", "ToolReturn", "structured_data", "rich_content"];
    validation: ["parameter_schemas", "docstring_extraction", "type_hints"];
  };
  
  // Testing and validation
  testing_patterns: {
    unit_testing: ["TestModel", "FunctionModel", "Agent.override()"];
    validation: ["capture_run_messages()", "pytest_fixtures", "mock_dependencies"];
    evals: ["model_performance", "agent_behavior", "production_monitoring"];
  };
  
  // Production considerations
  security: {
    api_keys: ["environment_variables", "secure_storage", "key_rotation"];
    input_validation: ["pydantic_models", "parameter_validation", "sanitization"];
    monitoring: ["logfire_integration", "usage_tracking", "error_handling"];
  };
}
```

### Development Workflow Analysis (FROM RESEARCH)

```yaml
# PydanticAI Development Patterns (researched from docs and examples)
project_structure:
  basic_pattern: |
    my_agent/
    ├── agent.py          # Main agent definition
    ├── tools.py          # Tool functions
    ├── models.py         # Pydantic output models
    ├── dependencies.py   # Context dependencies
    └── tests/
        ├── test_agent.py
        └── test_tools.py

  advanced_pattern: |
    agents_project/
    ├── agents/
    │   ├── __init__.py
    │   ├── chat_agent.py
    │   └── workflow_agent.py
    ├── tools/
    │   ├── __init__.py
    │   ├── web_search.py
    │   └── calculator.py
    ├── models/
    │   ├── __init__.py
    │   └── outputs.py
    ├── dependencies/
    │   ├── __init__.py
    │   └── database.py
    ├── tests/
    └── examples/

package_management:
  installation: "pip install pydantic-ai"
  optional_deps: "pip install 'pydantic-ai[examples]'"
  dev_deps: "pip install pytest pytest-asyncio inline-snapshot dirty-equals"

testing_workflow:
  unit_tests: "pytest tests/ -v"
  agent_testing: "Use TestModel for fast validation"
  integration_tests: "Use real models with rate limiting"
  evals: "Run performance benchmarks separately"

environment_setup:
  api_keys: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
  development: "Set ALLOW_MODEL_REQUESTS=False for testing"
  production: "Configure proper logging and monitoring"
```

### Security and Best Practices (FROM RESEARCH)

```typescript
// Security patterns specific to PydanticAI (from research)
interface PydanticAISecurity {
  // API key management
  api_security: {
    storage: "environment_variables_only";
    access_control: "minimal_required_permissions";
    monitoring: "usage_tracking_and_alerts";
  };
  
  // Input validation and sanitization
  input_security: {
    validation: "pydantic_models_for_all_inputs";
    sanitization: "escape_user_content";
    rate_limiting: "prevent_abuse_patterns";
    content_filtering: "block_malicious_prompts";
  };
  
  // Prompt injection prevention
  prompt_security: {
    system_prompts: "clear_instruction_boundaries";
    user_input: "validate_and_sanitize";
    tool_calls: "parameter_validation";
    output_filtering: "structured_response_validation";
  };
  
  // Production considerations
  production_security: {
    monitoring: "logfire_integration_recommended";
    error_handling: "no_sensitive_data_in_logs";
    dependency_injection: "secure_context_management";
    testing: "security_focused_unit_tests";
  };
}
```

### Common Gotchas and Edge Cases (FROM RESEARCH)

```yaml
# PydanticAI-specific gotchas discovered through research
agent_gotchas:
  model_limits:
    issue: "Different models have different token limits and capabilities"
    solution: "Use FallbackModel for automatic model switching"
    validation: "Test with multiple model providers"
  
  async_patterns:
    issue: "Mixing sync and async agent calls can cause issues"
    solution: "Consistent async/await patterns throughout"
    validation: "Test both sync and async execution paths"
  
  dependency_injection:
    issue: "Complex dependency graphs can be hard to debug"
    solution: "Keep dependencies simple and well-typed"
    validation: "Unit test dependencies in isolation"

tool_integration_gotchas:
  parameter_validation:
    issue: "Tools may receive unexpected parameter types"
    solution: "Use strict Pydantic models for tool parameters"
    validation: "Test tools with invalid inputs"
  
  context_management:
    issue: "RunContext state can become inconsistent"
    solution: "Design stateless tools when possible"
    validation: "Test context isolation between runs"
  
  error_handling:
    issue: "Tool errors can crash entire agent runs"
    solution: "Implement retry mechanisms and graceful degradation"
    validation: "Test error scenarios and recovery"

testing_gotchas:
  model_costs:
    issue: "Real model testing can be expensive"
    solution: "Use TestModel and FunctionModel for development"
    validation: "Separate unit tests from expensive eval runs"
  
  async_testing:
    issue: "Async agent testing requires special setup"
    solution: "Use pytest-asyncio and proper fixtures"
    validation: "Test both sync and async code paths"
  
  deterministic_behavior:
    issue: "AI responses are inherently non-deterministic"
    solution: "Focus on testing tool calls and structured outputs"
    validation: "Use inline-snapshot for complex assertions"
```

## Implementation Blueprint

### Technology Research Phase (COMPLETED)

**Comprehensive PydanticAI Analysis Complete:**

✅ **Core Framework Analysis:** 
- PydanticAI architecture, agent creation patterns, model provider integration
- Project structure conventions from official docs and examples
- Dependency injection system and type-safe design principles
- Development workflow with async/sync patterns and streaming support

✅ **Tool System Investigation:**
- Function tool registration patterns (@agent.tool vs @agent.tool_plain)
- Context management with RunContext and dependency injection
- Parameter validation, docstring extraction, and schema generation
- Rich return types and multi-modal content support

✅ **Testing Framework Analysis:**
- TestModel and FunctionModel for unit testing without API calls
- Agent.override() patterns for test isolation
- Pytest integration with async testing and fixtures
- Evaluation strategies for model performance vs unit testing

✅ **Security and Production Patterns:**
- API key management with environment variables and secure storage
- Input validation using Pydantic models and parameter schemas
- Rate limiting, monitoring, and Logfire integration
- Common security vulnerabilities and prevention strategies

### Template Package Generation

Create complete PydanticAI context engineering template based on research findings:

```yaml
Generation Task 1 - Create PydanticAI Template Directory Structure:
  CREATE complete use case directory structure:
    - use-cases/pydantic-ai/
    - .claude/commands/ with PydanticAI-specific slash commands
    - PRPs/templates/ with agent-focused base template
    - examples/ with working agent implementations
    - All subdirectories per template package requirements

Generation Task 2 - Generate PydanticAI-Specific CLAUDE.md:
  CREATE PydanticAI global rules file including:
    - PydanticAI agent creation and tool integration patterns
    - Model provider configuration and API key management
    - Agent architecture patterns (chat, workflow, tool-enabled)
    - Testing strategies with TestModel/FunctionModel
    - Security best practices for AI agents and tool integration
    - Common gotchas: async patterns, context management, model limits

Generation Task 3 - Create PydanticAI PRP Commands:
  GENERATE domain-specific slash commands:
    - generate-pydantic-ai-prp.md with agent research patterns
    - execute-pydantic-ai-prp.md with AI agent validation loops
    - Include PydanticAI documentation references and research strategies
    - Agent-specific success criteria and testing requirements

Generation Task 4 - Develop PydanticAI Base PRP Template:
  CREATE specialized prp_pydantic_ai_base.md template:
    - Pre-filled with agent architecture patterns from research
    - PydanticAI-specific success criteria and validation gates
    - Official documentation references and model provider guides
    - Agent testing patterns with TestModel and validation strategies

Generation Task 5 - Create Working PydanticAI Examples:
  GENERATE comprehensive example agents:
    - basic_chat_agent: Simple conversation with memory
    - tool_enabled_agent: Web search and calculator integration
    - workflow_agent: Multi-step task processing
    - structured_output_agent: Custom Pydantic models
    - testing_examples: Unit tests and validation patterns
    - Include configuration files and environment setup

Generation Task 6 - Create Template Copy Script:
  CREATE Python script for template deployment:
    - copy_template.py with command-line interface
    - Copies entire PydanticAI template structure to target location
    - Handles all files: CLAUDE.md, commands, PRPs, examples, etc.
    - Error handling and success feedback with next steps

Generation Task 7 - Generate Comprehensive README:
  CREATE PydanticAI-specific README.md:
    - Clear description: "PydanticAI Context Engineering Template"
    - Template copy script usage (prominently at top)
    - PRP framework workflow for AI agent development
    - Template structure with PydanticAI-specific explanations
    - Quick start guide with agent creation examples
    - Working examples overview and testing patterns
```

### PydanticAI Specialization Details

```typescript
// Template specialization for PydanticAI
const pydantic_ai_specialization = {
  agent_patterns: [
    "chat_agent_with_memory",
    "tool_integrated_agent", 
    "workflow_processing_agent",
    "structured_output_agent"
  ],
  
  validation: [
    "agent_behavior_testing",
    "tool_function_validation", 
    "output_schema_verification",
    "model_provider_compatibility"
  ],
  
  examples: [
    "basic_conversation_agent",
    "web_search_calculator_tools",
    "multi_step_workflow_processing",
    "custom_pydantic_output_models",
    "comprehensive_testing_suite"
  ],
  
  gotchas: [
    "async_sync_mixing_issues",
    "model_token_limits",
    "dependency_injection_complexity",
    "tool_error_handling_failures",
    "context_state_management"
  ],
  
  security: [
    "api_key_environment_management",
    "input_validation_pydantic_models",
    "prompt_injection_prevention",
    "rate_limiting_implementation",
    "secure_tool_parameter_handling"
  ]
};
```

### Integration Points

```yaml
CONTEXT_ENGINEERING_FRAMEWORK:
  - base_workflow: Inherit PRP generation/execution, adapt for AI agent development
  - validation_principles: Extend with AI-specific testing (agent behavior, tool validation)
  - documentation_standards: Maintain consistency while specializing for PydanticAI

PYDANTIC_AI_INTEGRATION:
  - agent_architecture: Include chat, tool-enabled, and workflow agent patterns
  - model_providers: Support OpenAI, Anthropic, Gemini configuration patterns
  - testing_framework: Use TestModel/FunctionModel for development validation
  - production_patterns: Include security, monitoring, and deployment considerations

TEMPLATE_STRUCTURE:
  - directory_organization: Follow use case template patterns with AI-specific examples
  - file_naming: generate-pydantic-ai-prp.md, prp_pydantic_ai_base.md
  - content_format: Markdown with agent code examples and configuration
  - command_patterns: Extend slash commands for AI agent development workflows
```

## Validation Loop

### Level 1: PydanticAI Template Structure Validation

```bash
# Verify complete PydanticAI template package structure
find use-cases/pydantic-ai -type f | sort
ls -la use-cases/pydantic-ai/.claude/commands/
ls -la use-cases/pydantic-ai/PRPs/templates/
ls -la use-cases/pydantic-ai/examples/

# Verify copy script and agent examples
test -f use-cases/pydantic-ai/copy_template.py
ls use-cases/pydantic-ai/examples/*/agent.py 2>/dev/null | wc -l  # Should have agent files
python use-cases/pydantic-ai/copy_template.py --help 2>/dev/null || echo "Copy script needs help"

# Expected: All required files including working agent examples
# If missing: Generate missing components with PydanticAI patterns
```

### Level 2: PydanticAI Content Quality Validation

```bash
# Verify PydanticAI-specific content accuracy
grep -r "from pydantic_ai import Agent" use-cases/pydantic-ai/examples/
grep -r "@agent.tool" use-cases/pydantic-ai/examples/
grep -r "TestModel\|FunctionModel" use-cases/pydantic-ai/

# Check for PydanticAI patterns and avoid generic content
grep -r "TODO\|PLACEHOLDER" use-cases/pydantic-ai/
grep -r "openai:gpt-4o\|anthropic:" use-cases/pydantic-ai/
grep -r "RunContext\|deps_type" use-cases/pydantic-ai/

# Expected: Real PydanticAI code, no placeholders, agent patterns present
# If issues: Add proper PydanticAI-specific patterns and examples
```

### Level 3: PydanticAI Functional Validation

```bash
# Test PydanticAI template functionality
cd use-cases/pydantic-ai

# Test PRP generation with agent focus
/generate-pydantic-ai-prp INITIAL.md
ls PRPs/*.md | grep -v templates | head -1  # Should generate agent PRP

# Verify agent examples can be parsed (syntax check)
python -m py_compile examples/basic_chat_agent/agent.py 2>/dev/null && echo "Basic agent syntax OK"
python -m py_compile examples/tool_enabled_agent/agent.py 2>/dev/null && echo "Tool agent syntax OK"

# Expected: PRP generation works, agent examples have valid syntax
# If failing: Debug PydanticAI command patterns and fix agent code
```

### Level 4: PydanticAI Integration Testing

```bash
# Verify PydanticAI specialization maintains base framework compatibility
diff -r ../../.claude/commands/ .claude/commands/ | head -10
grep -r "Context is King" . | wc -l  # Should inherit base principles
grep -r "pydantic.ai.dev\|PydanticAI" . | wc -l  # Should have specializations

# Test agent examples have proper dependencies
grep -r "pydantic_ai" examples/ | wc -l  # Should import PydanticAI
grep -r "pytest" examples/testing_examples/ | wc -l  # Should have tests

# Expected: Proper specialization, working agent patterns, testing included
# If issues: Adjust to maintain compatibility while adding PydanticAI features
```

## Final Validation Checklist

### PydanticAI Template Package Completeness

- [ ] Complete directory structure: `tree use-cases/pydantic-ai`
- [ ] PydanticAI-specific files: CLAUDE.md with agent patterns, specialized commands
- [ ] Copy script present: `copy_template.py` with proper PydanticAI functionality
- [ ] README comprehensive: Includes agent development workflow and copy instructions
- [ ] Agent examples working: All examples use real PydanticAI code patterns
- [ ] Testing patterns included: TestModel/FunctionModel examples and validation
- [ ] Documentation complete: PydanticAI-specific patterns and gotchas documented

### Quality and Usability for PydanticAI

- [ ] No placeholder content: `grep -r "TODO\|PLACEHOLDER"` returns empty
- [ ] PydanticAI specialization: Agent patterns, tools, testing properly documented
- [ ] Validation loops work: All commands executable with agent-specific functionality
- [ ] Framework integration: Works with base context engineering for AI development
- [ ] Ready for AI development: Developers can immediately create PydanticAI agents

### PydanticAI Framework Integration

- [ ] Inherits base principles: Context engineering workflow preserved for AI agents
- [ ] Proper AI specialization: PydanticAI patterns, security, testing included
- [ ] Command compatibility: Slash commands work for agent development workflows
- [ ] Documentation consistency: Follows patterns while specializing for AI development
- [ ] Maintainable structure: Easy to update as PydanticAI framework evolves

---

## Anti-Patterns to Avoid

### PydanticAI Template Generation

- ❌ Don't create generic AI templates - research PydanticAI specifics thoroughly
- ❌ Don't skip agent architecture research - understand tools, memory, validation
- ❌ Don't use placeholder agent code - include real, working PydanticAI examples
- ❌ Don't ignore testing patterns - TestModel/FunctionModel are critical for AI

### PydanticAI Content Quality

- ❌ Don't assume AI patterns - document PydanticAI-specific gotchas explicitly
- ❌ Don't skip security research - API keys, input validation, prompt injection critical
- ❌ Don't ignore model providers - include OpenAI, Anthropic, Gemini patterns
- ❌ Don't forget async patterns - PydanticAI has specific async/sync considerations

### PydanticAI Framework Integration

- ❌ Don't break context engineering - maintain PRP workflow for AI development
- ❌ Don't duplicate base functionality - extend and specialize appropriately
- ❌ Don't ignore AI-specific validation - agent behavior testing is unique requirement
- ❌ Don't skip real examples - include working agents with tools and validation

**CONFIDENCE SCORE: 9/10** - Comprehensive PydanticAI research completed, framework patterns understood, ready to generate specialized context engineering template for AI agent development.