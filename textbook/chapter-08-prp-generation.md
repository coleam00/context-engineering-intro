# Chapter 8: PRP Generation

> **"A good PRP is like a detailed architectural blueprint - it contains everything needed to build successfully, and nothing unnecessary."**

This chapter takes you deep into Product Requirements Prompts (PRPs) - the heart of the Context Engineering system. You'll learn how to generate comprehensive implementation blueprints that lead to one-pass success.

## 🎯 Learning Objectives

By the end of this chapter, you will:
- Understand what makes PRPs different from traditional requirements documents
- Master the `/generate-prp` command and its research process
- Know how to create comprehensive context that enables one-pass implementation
- Recognize quality indicators in PRPs and how to improve them

## 📋 What is a PRP?

**Product Requirements Prompts (PRPs)** are comprehensive implementation blueprints that contain all the context an AI coding assistant needs to successfully build a feature from start to finish.

### **PRP vs. Traditional Documents**

| Traditional PRD | Context Engineering PRP |
|----------------|------------------------|
| **Audience**: Human developers | **Audience**: AI coding assistants |
| **Focus**: What to build | **Focus**: What + How + Why + Context |
| **Length**: 5-20 pages | **Length**: 200-500 lines |
| **Context**: Business requirements | **Context**: Complete implementation context |
| **Validation**: Manual review | **Validation**: Executable tests and gates |
| **Examples**: User stories and mockups | **Examples**: Code patterns and snippets |
| **Success**: Feature meets requirements | **Success**: One-pass working implementation |

### **The PRP Philosophy**

PRPs are built on three core principles:

1. **Context is King**: Include ALL necessary information for implementation success
2. **Validation Loops**: Provide executable tests that enable self-correction
3. **Information Dense**: Use keywords and patterns from the codebase for maximum relevance

## 🔄 The `/generate-prp` Workflow

Let's break down exactly what happens when you run `/generate-prp INITIAL.md`:

### **Phase 1: Requirements Analysis** 📖
```markdown
Input: INITIAL.md
├── FEATURE: What needs to be built
├── EXAMPLES: Code patterns to follow  
├── DOCUMENTATION: External resources
└── OTHER CONSIDERATIONS: Gotchas and constraints

Process:
1. Parse and understand feature requirements
2. Identify complexity level and scope
3. Extract success criteria and constraints
4. Note specific examples and patterns to follow
```

### **Phase 2: Codebase Research** 🔍
```markdown
Research Process:
1. **Pattern Discovery**
   - Search for similar features/implementations
   - Identify existing conventions and styles
   - Find relevant utility functions and helpers
   
2. **Architecture Analysis**  
   - Understand project structure and organization
   - Identify integration points and dependencies
   - Note testing patterns and validation approaches

3. **Convention Extraction**
   - Extract naming conventions
   - Document coding style preferences  
   - Identify error handling patterns
```

**Example Research Output:**
```markdown
## Codebase Analysis Results

### Existing Patterns Found:
- Agent creation pattern in examples/agent/agent.py
- Tool registration in examples/agent/tools.py  
- Multi-provider support in examples/agent/providers.py
- CLI streaming in examples/cli.py

### Architecture Conventions:
- Use Pydantic models for data validation
- Async/await throughout for consistency
- Type hints on all functions
- Docstrings in Google style

### Testing Approach:
- Pytest with fixtures in conftest.py
- Mock external APIs in tests
- 80%+ code coverage requirement
- Integration tests for CLI commands
```

### **Phase 3: External Research** 🌐
```markdown
Documentation Gathering:
1. **API Documentation**
   - Read official documentation for external services
   - Extract key patterns and gotchas
   - Note authentication requirements and rate limits

2. **Library Research**
   - Review library documentation for best practices
   - Identify common pitfalls and solutions
   - Find official code examples

3. **Integration Examples**
   - Search for real-world integration patterns
   - Find troubleshooting guides and solutions
   - Extract security and performance considerations
```

### **Phase 4: Blueprint Creation** 🏗️
```markdown
PRP Structure Generation:
1. **Context Assembly**
   - Combine all research findings
   - Organize information hierarchically
   - Create actionable implementation guidance

2. **Task Decomposition** 
   - Break feature into manageable steps
   - Define clear success criteria for each step
   - Order tasks for optimal implementation flow

3. **Validation Design**
   - Create executable test commands  
   - Define quality gates and checkpoints
   - Plan error recovery strategies
```

### **Phase 5: Quality Assessment** ⭐
```markdown
Quality Checklist:
- [ ] All necessary context included
- [ ] Validation gates are executable
- [ ] References existing patterns  
- [ ] Clear implementation path
- [ ] Error handling documented
- [ ] Confidence score 7-10/10
```

## 📊 Anatomy of a High-Quality PRP

Let's dissect the `EXAMPLE_multi_agent_prp.md` to understand what makes it effective:

### **Header Section - Clear Identity**
```markdown
name: "Multi-Agent System: Research Agent with Email Draft Sub-Agent"
description: |
  ## Purpose
  Build a Pydantic AI multi-agent system where a primary Research Agent 
  uses Brave Search API and has an Email Draft Agent (using Gmail API) as a tool.
```
**Why this works**: Immediately clear what's being built and why.

### **Goal Section - Business Context**
```markdown
## Goal
Create a production-ready multi-agent system where users can research topics 
via CLI, and the Research Agent can delegate email drafting tasks to an Email Draft Agent.

## Why
- **Business value**: Automates research and email drafting workflows
- **Integration**: Demonstrates advanced Pydantic AI multi-agent patterns
- **Problems solved**: Reduces manual work for research-based email communications
```
**Why this works**: Provides business justification and technical rationale.

### **Success Criteria - Measurable Outcomes**
```markdown
### Success Criteria
- [ ] Research Agent successfully searches via Brave API
- [ ] Email Agent creates Gmail drafts with proper authentication
- [ ] Research Agent can invoke Email Agent as a tool
- [ ] CLI provides streaming responses with tool visibility
- [ ] All tests pass and code meets quality standards
```
**Why this works**: Clear, testable criteria for implementation success.

### **Context Section - Complete Information**
```markdown
## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://ai.pydantic.dev/agents/
  why: Core agent creation patterns
  
- url: https://ai.pydantic.dev/multi-agent-applications/
  why: Multi-agent system patterns, especially agent-as-tool
  
- file: examples/agent/agent.py
  why: Pattern for agent creation, tool registration, dependencies
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Pydantic AI requires async throughout
# CRITICAL: Gmail API requires OAuth2 flow on first run
# CRITICAL: Agent-as-tool pattern requires passing ctx.usage for token tracking
```
**Why this works**: Prevents common implementation failures with specific warnings.

### **Implementation Blueprint - Step-by-Step Plan**
```markdown
## Implementation Blueprint

### List of tasks to be completed
```yaml
Task 1: Setup Configuration and Environment
CREATE config/settings.py:
  - PATTERN: Use pydantic-settings like examples use os.getenv
  - Load environment variables with defaults
  - Validate required API keys present

Task 2: Implement Brave Search Tool
CREATE tools/brave_search.py:
  - PATTERN: Async functions like examples/agent/tools.py
  - Simple REST client using httpx
  - Handle rate limits and errors gracefully
```
**Why this works**: Clear progression from setup to implementation to testing.

### **Validation Loop - Quality Gates**
```markdown
## Validation Loop

### Level 1: Syntax & Style
```bash
ruff check --fix && mypy .
```

### Level 2: Unit Tests
```bash
pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing
```

### Level 3: Integration Test  
```bash
python cli.py
# Expected interaction:
# You: Research latest AI safety developments
# 🤖 Assistant: [Streams research results]
```
**Why this works**: Progressive validation from syntax to real-world usage.

## 🛠️ Mastering the `/generate-prp` Command

### **Command Structure**
```bash
/generate-prp <feature-file>

# Examples:
/generate-prp INITIAL.md
/generate-prp features/user-auth.md
/generate-prp requirements/api-redesign.md
```

### **What the Command Does**

Let's look at the actual command implementation:

```markdown
# From .claude/commands/generate-prp.md

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

3. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

## PRP Generation

Using PRPs/templates/prp_base.md as template:

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

### Validation Gates (Must be Executable)
```bash
# Syntax/Style
ruff check --fix && mypy .

# Unit Tests
uv run pytest tests/ -v
```

## Quality Checklist
- [ ] All necessary context included
- [ ] Validation gates are executable by AI
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented

Score the PRP on a scale of 1-10 (confidence level to succeed in one-pass implementation)
```

### **Advanced Usage Patterns**

**For Complex Features:**
```bash
# Break down large features into smaller PRPs
/generate-prp auth-system-phase1.md  # Core authentication
/generate-prp auth-system-phase2.md  # OAuth integration  
/generate-prp auth-system-phase3.md  # Permission system
```

**For Different Domains:**
```bash
# Domain-specific PRPs
/generate-prp frontend-component.md   # UI component
/generate-prp api-endpoint.md         # Backend API
/generate-prp database-migration.md   # Data layer
/generate-prp deployment-config.md    # Infrastructure
```

## 📈 PRP Quality Metrics

### **Confidence Scoring (1-10)**

**Score 9-10: Excellent PRP**
- Complete context with all necessary documentation
- Comprehensive examples and patterns from codebase
- Detailed gotchas and error handling
- Executable validation gates
- Clear task decomposition
- High probability of one-pass success

**Score 7-8: Good PRP**  
- Most necessary context included
- Some examples and patterns
- Basic validation gates
- Generally clear implementation path
- May require 1-2 iterations

**Score 5-6: Adequate PRP**
- Basic context provided
- Limited examples
- Some validation gates
- Implementation path somewhat unclear
- Will likely require multiple iterations

**Score 1-4: Poor PRP**
- Insufficient context
- No examples or patterns
- Missing validation gates
- Unclear implementation approach
- High probability of failure

### **Quality Indicators**

**✅ High-Quality PRP Characteristics:**
- References specific files from the codebase
- Includes URL links to official documentation
- Has executable validation commands
- Mentions specific gotchas and pitfalls
- Provides pseudocode for complex logic
- Orders tasks logically
- Includes error handling strategies

**❌ Low-Quality PRP Warning Signs:**
- Vague or generic requirements
- No references to existing code patterns
- Missing documentation links
- No validation or testing strategy
- Unclear task ordering
- No consideration of error cases

### **Improvement Strategies**

**To Improve Context Density:**
```markdown
# Instead of: "Use authentication"
# Write: "Use JWT authentication following the pattern in examples/auth/jwt_handler.py, 
# storing tokens in httpOnly cookies as shown in examples/auth/middleware.py"

# Instead of: "Handle errors properly"  
# Write: "Catch APIError exceptions and return appropriate HTTP status codes:
# 401 for authentication failures, 429 for rate limits, 500 for server errors.
# See examples/api/error_handlers.py for the exact pattern."
```

**To Improve Validation:**
```bash
# Instead of: "Make sure it works"
# Provide: 
pytest tests/test_auth.py::test_jwt_login -v
curl -X POST localhost:8000/auth/login -d '{"username":"test","password":"test"}'
python -c "import jwt; print('JWT library working')"
```

## 🧪 PRP Generation Examples

### **Example 1: Simple Feature PRP**

**Input (INITIAL.md):**
```markdown
## FEATURE:
Add password reset functionality to user authentication system

## EXAMPLES:
- examples/auth/login.py - existing auth patterns
- examples/email/sender.py - email sending utility

## DOCUMENTATION:
- FastAPI docs: https://fastapi.tiangolo.com/tutorial/security/
- SendGrid API: https://docs.sendgrid.com/api-reference/mail-send

## OTHER CONSIDERATIONS:  
- Reset tokens should expire in 15 minutes
- Use existing email templates from templates/auth/
```

**Generated PRP Highlights:**
```markdown
## Implementation Blueprint

Task 1: Create Password Reset Token System
CREATE auth/reset_tokens.py:
- PATTERN: Follow JWT pattern from examples/auth/jwt_handler.py
- Generate secure random tokens with 15-minute expiration
- Store tokens in Redis with automatic expiration

Task 2: Add Reset Request Endpoint
CREATE auth/routes.py (extend existing):
- PATTERN: Follow route pattern from examples/auth/login.py
- Validate email exists in database
- Generate reset token and send email
- Rate limit to prevent abuse (max 3 requests per hour)

## Validation Loop

### Level 1: Unit Tests
```bash
pytest tests/auth/test_password_reset.py -v
# Tests token generation, expiration, email sending, rate limiting
```

### Level 2: Integration Test
```bash
# Test complete flow
curl -X POST localhost:8000/auth/request-reset -d '{"email":"test@example.com"}'
# Check email received with valid reset link
curl -X POST localhost:8000/auth/reset-password -d '{"token":"...", "new_password":"..."}'
```

**Confidence Score: 8/10** - High confidence due to existing auth patterns and clear requirements.
```

### **Example 2: Complex Integration PRP**

**Input (INITIAL.md):**
```markdown
## FEATURE:
Integrate Stripe payment processing with subscription management

## EXAMPLES:
- examples/api/webhooks.py - webhook handling patterns
- examples/database/models.py - SQLAlchemy model patterns

## DOCUMENTATION:
- Stripe API: https://stripe.com/docs/api
- Stripe Webhooks: https://stripe.com/docs/webhooks

## OTHER CONSIDERATIONS:
- Handle webhook signature verification for security
- Support multiple subscription tiers (basic, premium, enterprise)
- Graceful handling of failed payments with retry logic
```

**Generated PRP Highlights:**
```markdown
## Known Gotchas & Library Quirks
```python
# CRITICAL: Stripe webhook signatures must be verified to prevent fraud
# CRITICAL: Handle idempotency keys for safe retries
# CRITICAL: Webhook endpoints must respond within 10 seconds
# CRITICAL: Failed payments should pause service, not cancel subscription
```

## Implementation Blueprint

### Data models and structure
```python
# models/subscription.py - Following SQLAlchemy pattern from examples/
class Subscription(BaseModel):
    stripe_subscription_id: str = Field(..., index=True)
    user_id: int = Field(..., foreign_key="users.id")
    tier: SubscriptionTier = Field(...)
    status: SubscriptionStatus = Field(...)
    current_period_end: datetime = Field(...)
    
class Payment(BaseModel):
    stripe_payment_intent_id: str = Field(..., index=True)
    subscription_id: int = Field(..., foreign_key="subscriptions.id")
    amount: int = Field(...)  # Amount in cents
    currency: str = Field(default="usd")
    status: PaymentStatus = Field(...)
```

## Validation Loop

### Level 3: Stripe Integration Test
```bash
# Test webhook handling with Stripe CLI
stripe listen --forward-to localhost:8000/webhooks/stripe
stripe trigger payment_intent.succeeded
stripe trigger invoice.payment_failed

# Verify database state after each webhook
python scripts/check_subscription_status.py --user-id 123
```

**Confidence Score: 7/10** - Good confidence but integration complexity requires careful testing.
```

## 🔧 Customizing PRP Generation

### **Project-Specific Templates**

You can customize the PRP generation process by modifying `PRPs/templates/prp_base.md`:

```markdown
# Add your project-specific sections:

## Security Considerations
[For security-focused projects]

## Performance Requirements  
[For high-performance applications]

## Accessibility Requirements
[For user-facing applications]

## Compliance Checklist
[For regulated industries]
```

### **Domain-Specific Research**

Enhance the research process for your domain:

```markdown
# Add to .claude/commands/generate-prp.md:

## Additional Research (for our domain):
1. **Security Analysis**
   - Check for common vulnerabilities in similar features
   - Review OWASP guidelines for this functionality
   - Identify security testing requirements

2. **Performance Considerations**
   - Research scalability patterns for this feature type
   - Identify potential bottlenecks and optimization opportunities
   - Define performance benchmarks and testing approach
```

### **Quality Gate Customization**

Tailor validation commands to your project:

```bash
# For a Django project:
python manage.py test
python manage.py check --deploy
coverage run --source='.' manage.py test && coverage report

# For a React project:  
npm test -- --coverage --watchAll=false
npm run lint
npm run type-check

# For a Go project:
go test ./... -cover
go vet ./...
golangci-lint run
```

## ✅ Chapter 8 Checklist

Before moving to Chapter 9, ensure you understand:

- [ ] **PRP Purpose**: Why PRPs are different from traditional requirements documents
- [ ] **Generation Process**: The five phases of `/generate-prp` execution
- [ ] **Quality Indicators**: What makes a PRP effective for one-pass implementation
- [ ] **Context Density**: How to include comprehensive but relevant information
- [ ] **Validation Design**: Creating executable quality gates that enable self-correction

## 🎯 Key Takeaways

1. **PRPs are implementation blueprints** - They contain everything needed to build successfully
2. **Research drives quality** - The more comprehensive the research, the better the PRP
3. **Context density matters** - Include specific examples, gotchas, and patterns
4. **Validation enables iteration** - Executable quality gates allow self-correction
5. **Confidence scoring works** - High-scoring PRPs really do succeed more often

## 📚 Next Steps

Ready to learn how to execute PRPs and turn them into working code?

👉 **[Chapter 9: PRP Execution](chapter-09-prp-execution.md)**

In Chapter 9, you'll master the `/execute-prp` command and learn how to systematically implement features from your comprehensive PRPs.

---

## 🔬 PRP Analysis Exercise

**Choose one of these options:**

**Option A: Analyze the Example PRP**
1. Open `PRPs/EXAMPLE_multi_agent_prp.md`
2. Identify 5 specific context elements that make it effective
3. Find examples of gotchas and specific patterns referenced
4. Note the validation strategy and quality gates

**Option B: Generate Your Own PRP**
1. Create a simple INITIAL.md for a feature you need
2. Run `/generate-prp INITIAL.md` (if you have Claude Code setup)
3. Review the generated PRP for quality and completeness
4. Identify areas where more context would be helpful

*This hands-on practice will deepen your understanding of what makes PRPs effective.*