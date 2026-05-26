# 🚀 AI Coding Workflows

A comprehensive framework for developing effective AI coding workflows, with three phases - **Planning**, **Implementation**, and **Validation**.

## 🧠 Primary Mental Model

The core philosophy centers around **Context Engineering** - systematically preparing and organizing information to maximize the effectiveness of AI coding assistants.

## 📋 Phase 1: Planning

### 1. 🎨 Vibe Planning
Use the `/primer` slash command to kickstart your exploration:
- **New projects**: Research online resources, similar projects, explore architecture and tech stack options
- **Existing projects**: Analyze and understand the current codebase using the **Codebase Analyst** sub-agent
- Focus: Unstructured exploration of ideas, concepts, and possibilities

### 2. 📝 Create INITIAL.md (PRD)
Generate a detailed Product Requirements Document:
- **New projects**: High-level MVP with supporting documentation references
- **Existing projects**: Focused, detailed requirements with integration points

### 3. ⚙️ Context Engineering Components
Prepare these essential elements using slash commands:

- **RAG** (Retrieval-Augmented Generation)
- **Task Management**
- **Memory Systems**
- **Prompt Engineering**

#### 🛠️ Supporting Tools:
- Archon
- PRP Framework
- Web Search
- GitHub Spec Kit

### 📊 Plan of Attack
Use the `/create-plan` slash command to generate a structured implementation strategy based on your INITIAL.md and context engineering setup.

## ⚡ Phase 2: Implementation

### 🎯 Execute Task by Task
- Use the `/execute-plan` slash command to systematically work through your plan of attack
- Follow the structured plan created during planning
- Leverage the context engineering foundation

### 🔍 Trust but Verify
Monitor the AI assistant to ensure it:
- Uses MCP servers correctly
- Reads/edits appropriate files
- Leverages task management properly
- Produces clear "thinking" tokens showing understanding

## ✅ Phase 3: Validation

### 📊 Code Review Process
**AI Assistant Validation**:
- Performs automated code review using the **Validator** sub-agent
- Runs unit tests
- Runs integration tests

**Human Validation**:
- Strategic oversight
- Manual testing

## 🔧 Key Components

### 🌐 Global Rules
- Subagents coordination (**Codebase Analyst** & **Validator**)
- Slash commands integration (`/primer`, `/create-plan`, `/execute-plan`)
- Consistent workflows across phases

### 🎯 Slash Commands Reference
- **`/primer`**: Initialize vibe planning phase with exploration prompts
- **`/create-plan`**: Generate structured plan of attack from PRD
- **`/execute-plan`**: Systematically implement the created plan

### 🤖 Sub-Agents
- **Codebase Analyst**: Specializes in understanding and analyzing existing codebases
- **Validator**: Focuses on systematic code review and quality assurance

### 🏆 Success Factors
- **Structured approach**: Each phase builds on the previous
- **Context preparation**: Thorough setup enables better AI performance  
- **Iterative refinement**: Trust but verify at each step
- **Tool integration**: Leverage specialized tools for specific tasks

This framework transforms ad-hoc AI interactions into a systematic, repeatable process that consistently produces high-quality code and documentation. 🎉