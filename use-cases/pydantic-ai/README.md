# Pydantic AI Context Engineering Template

A comprehensive template for building production-grade AI agents using Pydantic AI with context engineering best practices, tools integration, structured outputs, and comprehensive testing patterns.

## 🚀 Quick Start - Copy Template

**Get started in 2 minutes:**

```bash
# Clone the context engineering repository
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/pydantic-ai

# 1. Copy this template to your new project
python copy_template.py /path/to/my-agent-project

# 2. Navigate to your project
cd /path/to/my-agent-project

# 3. Start building with the PRP workflow
# Fill out PRPs/INITIAL.md with the agent you want to create

# 4. Generate the PRP based on your detailed requirements (validate the PRP after generating!)
/generate-pydantic-ai-prp PRPs/INITIAL.md

# 5. Execute the PRP to create your Pydantic AI agent
/execute-pydantic-ai-prp PRPs/generated_prp.md
```

If you are not using Claude Code, you can simply tell your AI coding assistant to use the generate-pydantic-ai-prp and execute-pydantic-ai-prp slash commands in .claude/commands as prompts.

## 📖 What is This Template?

This template provides everything you need to build sophisticated Pydantic AI agents using proven context engineering workflows. It combines:

- **Pydantic AI Best Practices**: Type-safe agents with tools, structured outputs, and dependency injection
- **Context Engineering Workflows**: Proven PRP (Product Requirements Prompts) methodology
- **Working Examples**: Complete agent implementations you can learn from and extend

## 🎯 PRP Framework Workflow

This template uses a 3-step context engineering workflow for building AI agents:

### 1. **Define Requirements** (`PRPs/INITIAL.md`)
Start by clearly defining what your agent needs to do:
```markdown
# Customer Support Agent - Initial Requirements

## Overview
Build an intelligent customer support agent that can handle inquiries, 
access customer data, and escalate issues appropriately.

## Core Requirements
- Multi-turn conversations with context and memory
- Customer authentication and account access
- Account balance and transaction queries
- Payment processing and refund handling
...
```

### 2. **Generate Implementation Plan** 
```bash
/generate-pydantic-ai-prp PRPs/INITIAL.md
```
This creates a comprehensive 'Product Requirements Prompts' document that includes:
- Pydantic AI technology research and best practices
- Agent architecture design with tools and dependencies
- Implementation roadmap with validation loops
- Security patterns and production considerations

### 3. **Execute Implementation**
```bash
/execute-pydantic-ai-prp PRPs/your_agent.md
```
This implements the complete agent based on the PRP, including:
- Agent creation with proper model provider configuration
- Tool integration with error handling and validation
- Structured output models with Pydantic validation
- Comprehensive testing with TestModel and FunctionModel

## 📂 Template Structure

```
pydantic-ai/
├── CLAUDE.md                           # Pydantic AI global development rules
├── copy_template.py                    # Template deployment script
├── .claude/commands/
│   ├── generate-pydantic-ai-prp.md     # PRP generation for agents
│   └── execute-pydantic-ai-prp.md      # PRP execution for agents
├── PRPs/
│   ├── templates/
│   │   └── prp_pydantic_ai_base.md     # Base PRP template for agents
│   └── INITIAL.md                      # Example agent requirements
├── examples/
│   ├── basic_chat_agent/               # Simple conversational agent
│   │   ├── agent.py                    # Agent with memory and context
│   │   └── README.md                   # Usage guide
│   ├── tool_enabled_agent/             # Agent with external tools
│   │   ├── agent.py                    # Web search + calculator tools
│   │   └── requirements.txt            # Dependencies
│   └── testing_examples/               # Comprehensive testing patterns
│       ├── test_agent_patterns.py      # TestModel, FunctionModel examples
│       └── pytest.ini                  # Test configuration
└── README.md                           # This file
```

## 🤖 Agent Examples Included

### 1. Main Agent Reference (`examples/main_agent_reference/`)
**The canonical reference implementation** showing proper Pydantic AI patterns:
- Environment-based configuration with `settings.py` and `providers.py`
- Clean separation of concerns between email and research agents
- Proper file structure to separate prompts, tools, agents, and Pydantic models
- Tool integration with external APIs (Gmail, Brave Search)

**Key Files:**
- `settings.py`: Environment configuration with pydantic-settings
- `providers.py`: Model provider abstraction with `get_llm_model()`
- `research_agent.py`: Multi-tool agent with web search and email integration
- `email_agent.py`: Specialized agent for Gmail draft creation

### 2. Basic Chat Agent (`examples/basic_chat_agent/`)
A simple conversational agent demonstrating core patterns:
- **Environment-based model configuration** (follows main_agent_reference)
- **String output by default** (no `result_type` unless needed)
- System prompts (static and dynamic)
- Conversation memory with dependency injection

**Key Features:**
- Simple string responses (not structured output)
- Settings-based configuration pattern
- Conversation context tracking
- Clean, minimal implementation

### 3. Tool-Enabled Agent (`examples/tool_enabled_agent/`)
An agent with tool integration capabilities:
- **Environment-based configuration** (follows main_agent_reference)
- **String output by default** (no unnecessary structure)
- Web search and calculation tools
- Error handling and retry mechanisms

**Key Features:**
- `@agent.tool` decorator patterns
- RunContext for dependency injection
- Tool error handling and recovery
- Simple string responses from tools

### 4. Structured Output Agent (`examples/structured_output_agent/`)
**NEW**: Shows when to use `result_type` for data validation:
- **Environment-based configuration** (follows main_agent_reference)
- **Structured output with Pydantic validation** (when specifically needed)
- Data analysis with statistical tools
- Professional report generation

**Key Features:**
- Demonstrates proper use of `result_type`
- Pydantic validation for business reports
- Data analysis tools with numerical statistics
- Clear documentation on when to use structured vs string output

### 5. Testing Examples (`examples/testing_examples/`)
Comprehensive testing patterns for Pydantic AI agents:
- TestModel for rapid development validation
- FunctionModel for custom behavior testing
- Agent.override() for test isolation
- Pytest fixtures and async testing

**Key Features:**
- Unit testing without API costs
- Mock dependency injection
- Tool validation and error scenario testing
- Integration testing patterns

## 📚 Additional Resources

- **Official Pydantic AI Documentation**: https://ai.pydantic.dev/
- **Context Engineering Methodology**: See main repository README

## 🆘 Support & Contributing

- **Issues**: Report problems with the template or examples
- **Improvements**: Contribute additional examples or patterns
- **Questions**: Ask about Pydantic AI integration or context engineering

This template is part of the larger Context Engineering framework. See the main repository for more context engineering templates and methodologies.

---

**Ready to build production-grade AI agents?** Start with `python copy_template.py my-agent-project` and follow the PRP workflow! 🚀