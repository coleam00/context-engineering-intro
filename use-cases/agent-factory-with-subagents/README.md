# 🏭 AI Agent Factory with Claude Code Subagents

A powerful yet simple orchestration framework that leverages Claude Code's subagent capabilities to autonomously build AI agents using Pydantic AI. This system transforms even basic requirements into fully-functional, tested, and documented AI agents through a coordinated workflow of specialized subagents. This can achieve in minutes what traditionally took hours or days of development.

> **Full Example**: For a complete, runnable AI agent built with this framework, see the [Hybrid Search RAG Agent](agents/rag_agent) which includes full setup instructions and documentation.

## 🚦 Getting Started

1. **Request an agent**: Open Claude Code in this directory and ask for an AI Agent (see examples below, your prompt can be simple)
2. **Answer clarifications**: Provide 2-3 quick answers about your needs
3. **Watch the magic**: Subagents work in parallel to build your agent in a new folder in `agents/`
4. **Receive your agent**: Complete with tests, docs, and setup instructions

## 🎯 Why Subagents?

Claude Code subagents have been all the rage, and for good reason. With subagents we get:

### **Parallel Execution & Scalability**
- Run many specialized agents simultaneously, dramatically reducing development time
- Each subagent operates independently with its own context window
- Orchestrate complex workflows without context pollution or token limitations

### **Specialized System Prompts**
- Each subagent has a focused, task-specific prompt optimized for its role
- Prevents prompt dilution and maintains specialized expertise across tasks
- Enables deep domain knowledge without compromising general capabilities

### **Modular Architecture**
- Cleanly separated concerns with independent configuration and tools
- Reusable components that can be versioned and shared across projects
- Easy to extend, modify, or replace individual subagents without affecting others

## 🏗️ Subagent Workflow Architecture

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         ▼
┌─────────────────────┐
│ Phase 0: Clarify    │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ Phase 1: Planner    │
└────────┬────────────┘
         ▼
┌─────────────────────────────────────┐
│     Phase 2: Parallel Development   │
│  ┌─────────────┬─────────────┬──────┴───────┐
│  │   Prompt    │    Tool     │  Dependency  │
│  │  Engineer   │ Integrator  │   Manager    │
│  └─────────────┴─────────────┴──────────────┘
└────────┬────────────────────────────┘
         ▼
┌─────────────────────┐
│ Phase 3: Implement  │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ Phase 4: Validator  │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│ Phase 5: Delivery   │
└─────────────────────┘
```

### Workflow Phases for the AI Agent Factory

1. **Phase 0: Clarification** - Main agent asks targeted questions to understand requirements
2. **Phase 1: Requirements Documentation** - Planner subagent creates comprehensive specifications
3. **Phase 2: Parallel Component Development** - Three specialized subagents work simultaneously:
   - **Prompt Engineer**: Designs optimal system prompts
   - **Tool Integrator**: Plans tool implementations and API integrations
   - **Dependency Manager**: Configures environment and dependencies
4. **Phase 3: Implementation** - Main agent builds the complete agent using specifications
5. **Phase 4: Validation** - Validator subagent creates tests and verifies functionality
6. **Phase 5: Delivery** - Documentation and final packaging

## 📁 Project Structure

```
.
├── CLAUDE.md                    # Central orchestration rules and workflow
├── agents/                      # Generated AI agents
│   ├── rag_agent/               # Example: Complete RAG agent implementation
│   └── your_agent_here/         # Whatever agent you create with the factory will go here
├── examples/                    # Pydantic AI patterns and references
│   ├── main_agent_reference/    # Reference implementation patterns
│   └── rag_pipeline/            # RAG infrastructure components
│   CLAUDE.md                    # The global rules that instruct Claude Code on the AI Agent Factory workflow
└── README.md                    # This file
```

## 🤖 The Subagents

### **pydantic-ai-planner**
Creates minimal, focused requirements documents (INITIAL.md) with MVP mindset. Analyzes user needs and produces clear specifications for agent development.

### **pydantic-ai-prompt-engineer**
Designs concise system prompts (100-300 words) that define agent behavior. Specializes in creating clear, effective prompts for Pydantic AI agents.

### **pydantic-ai-tool-integrator**
Plans tool specifications focusing on 2-3 essential functions. Defines tool parameters, error handling, and integration patterns.

### **pydantic-ai-dependency-manager**
Configures minimal dependencies and environment variables. Sets up model providers, database connections, and agent initialization.

### **pydantic-ai-validator**
Creates comprehensive test suites using TestModel and FunctionModel. Validates requirements, tests functionality, and ensures production readiness.

## 🎨 CLAUDE.md - The Orchestration Engine

The `CLAUDE.md` file is the heart of the system, containing:

- **Workflow triggers**: Patterns that activate the agent factory
- **Phase definitions**: Detailed instructions for each development phase
- **Subagent prompts**: Specialized instructions for each subagent
- **Quality gates**: Validation criteria for each phase
- **Integration rules**: How components work together

Key features:
- Automatic workflow recognition from user requests
- Parallel subagent invocation for optimal performance
- Archon integration for project management (optional)
- Comprehensive error handling and recovery

## 🚀 Example Prompts

### Simple Agents
```
"Build an AI agent that can search the web"
"Create an agent for summarizing documents"
"I need an assistant that can query databases"
```

### Complex Agents
```
"Build a customer support agent that integrates with Slack and searches our knowledge base"
"Create a data analysis agent that can query PostgreSQL and generate visualizations"
"Implement a content generation agent with brand voice customization and SEO optimization"
```

### Domain-Specific Agents
```
"Build a financial analysis agent that can process earnings reports"
"Create a code review agent that follows our team's style guide"
"Implement a research agent that can search academic papers and summarize findings"
```

## 🔗 Optional Archon Integration

When [Archon](https://archon.diy) is available through MCP, the system provides enhanced project management:

- **Automatic project creation** with task tracking
- **Status updates** as each phase progresses
- **RAG-powered research** during implementation
- **Persistent project history** for iteration and improvement

The Archon integration is optional—the system works perfectly without it, using local TodoWrite for task tracking.

## 💡 Key Benefits

### **Speed**
- Complete agent in 10-15 minutes vs hours of manual development
- Parallel processing reduces sequential bottlenecks
- Automated testing and validation included

### **Quality**
- Consistent architecture following best practices
- Comprehensive testing with 80%+ coverage
- Production-ready with error handling and logging

### **Flexibility**
- Works with any LLM provider (OpenAI, Anthropic, Gemini, Ollama)
- Supports various databases (PostgreSQL, SQLite, Redis)
- Extensible for custom requirements

### **Maintainability**
- Clean separation of concerns
- Well-documented code and APIs
- Reusable components and patterns

## 📚 Pydantic AI Integration

All agents are built using [Pydantic AI](https://ai.pydantic.dev/), providing:

- **Type Safety**: Full type hints and runtime validation
- **Structured Outputs**: Reliable, schema-validated responses
- **Dependency Injection**: Clean separation of concerns
- **Testing Support**: TestModel and FunctionModel for comprehensive testing
- **Multi-Provider**: Support for OpenAI, Anthropic, Gemini, and more

## 🛠️ Components Explained

### Planning Documents
Each agent includes four planning documents:
- `INITIAL.md` - Requirements and specifications
- `prompts.md` - System prompt design
- `tools.md` - Tool specifications
- `dependencies.md` - Configuration and dependencies

### Implementation Files
- `agent.py` - Main agent logic
- `tools.py` - Tool implementations
- `settings.py` - Environment configuration
- `providers.py` - LLM providers
- `dependencies.py` - Dependency injection
- `cli.py` - Command-line interface

### Testing & Validation
- Comprehensive test suite with pytest
- TestModel for development testing
- FunctionModel for behavior validation
- Integration tests for end-to-end verification

The system handles everything else from requirements analysis to implementation, testing, and documentation.

## 🔮 Future Enhancements

- Additional specialized subagents for specific domains
- Enhanced pattern library for common use cases
- Automated deployment pipeline generation
- Cross-agent communication protocols
- Real-time collaboration features
