# Appendix A: Templates Reference

> **"Good templates are like good recipes - they provide structure while allowing for creativity and customization."**

This appendix provides copy-paste templates for all the key Context Engineering components. Use these as starting points for your own projects.

## 🎯 Quick Reference

| Template | Use When | Customization Level |
|----------|----------|-------------------|
| [CLAUDE.md Template](#claude-md-template) | Starting new project | High - Adapt for your stack |
| [INITIAL.md Template](#initial-md-template) | Defining new feature | Medium - Fill in specifics |
| [PRP Template](#prp-template) | Manual PRP creation | Low - Use generated PRPs |
| [Examples README](#examples-readme-template) | Organizing examples | Medium - Add your patterns |
| [Validation Commands](#validation-commands-template) | Setting up quality gates | High - Match your tooling |

## 📋 CLAUDE.md Template

### **Basic Template (Copy-Paste Ready)**

```markdown
### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use [YOUR_ENVIRONMENT]** (e.g., venv_linux, .venv, conda env) whenever executing commands.

### 🧱 Code Structure & Modularity
- **Never create a file longer than [FILE_SIZE_LIMIT] lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use [CONFIG_LIBRARY]** for environment variables (e.g., python_dotenv, pydantic-settings).

### 🧪 Testing & Reliability
- **Always create [TEST_FRAMEWORK] tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

### 📎 Style & Conventions
- **Use [PRIMARY_LANGUAGE]** as the primary language.
- **Follow [STYLE_GUIDE]** and use type hints where applicable.
- **Use [FORMATTING_TOOL]** for code formatting (e.g., black, prettier).
- Write **docstrings for every function** using the [DOCSTRING_STYLE] style:
  ```[language]
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.
```

### **Language-Specific Customizations**

#### **Python Project**
```markdown
- **Use Python 3.8+** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation** and `fastapi` for APIs if applicable.
- Use `pytest` for testing with fixtures in `conftest.py`.
- **Environment**: Use `venv` or `conda` environment activation.
- **Linting**: `ruff check . && mypy . && black .`
```

#### **TypeScript/Node.js Project**
```markdown
- **Use TypeScript** for all new code.
- **Follow ESLint configuration** and format with `prettier`.
- **Use `jest` for testing** with proper async/await patterns.
- **Environment**: Use `npm` or `yarn` for dependency management.
- **Linting**: `npm run lint && npm run type-check && npm test`
```

#### **Go Project**
```markdown
- **Use Go 1.19+** following standard Go conventions.
- **Format with `gofmt`** and lint with `golangci-lint`.
- **Use standard library testing** with testify for assertions.
- **Environment**: Use Go modules for dependency management.
- **Linting**: `go fmt ./... && go vet ./... && golangci-lint run && go test ./...`
```

## 📝 INITIAL.md Template

### **Basic Template**

```markdown
## FEATURE:
[Describe what you want to build - be specific about functionality and requirements. 
Include user stories, technical requirements, and success criteria.]

Example:
- REST API for user authentication with JWT tokens
- Support registration, login, password reset, and profile management
- Must integrate with existing user database
- Should handle rate limiting and security best practices

## EXAMPLES:
[List any example files in the examples/ folder and explain how they should be used.
Reference specific files and patterns to follow.]

Example:
- `examples/api/auth_routes.py` - Follow this pattern for API route structure
- `examples/models/user.py` - Use this User model pattern for database integration
- `examples/auth/jwt_handler.py` - JWT token generation and validation patterns
- `examples/tests/test_auth.py` - Testing approach for authentication features

## DOCUMENTATION:
[Include links to relevant documentation, APIs, or external resources needed.]

Example:
- FastAPI Authentication: https://fastapi.tiangolo.com/tutorial/security/
- JWT.io Documentation: https://jwt.io/introduction/
- Bcrypt for Python: https://pypi.org/project/bcrypt/
- Rate limiting with slowapi: https://github.com/laurentS/slowapi

## OTHER CONSIDERATIONS:
[Mention any gotchas, specific requirements, or things AI assistants commonly miss.]

Example:
- Use bcrypt for password hashing (never plain text or MD5)
- Implement rate limiting: max 5 login attempts per minute per IP
- JWT tokens should expire in 24 hours with refresh token mechanism
- Password reset tokens should expire in 15 minutes
- All endpoints must have comprehensive error handling
- Follow existing database migration patterns in migrations/
```

### **Domain-Specific Templates**

#### **API Development**
```markdown
## FEATURE:
[REST API endpoint description with HTTP methods, request/response formats]

## EXAMPLES:
- `examples/api/` - API route patterns and middleware
- `examples/models/` - Data model patterns
- `examples/serializers/` - Request/response serialization

## DOCUMENTATION:
- [API framework docs]
- [Database ORM docs]
- [Authentication library docs]

## OTHER CONSIDERATIONS:
- Error handling and HTTP status codes
- Request validation and sanitization
- Rate limiting and security headers
- API versioning strategy
```

#### **Frontend Component**
```markdown
## FEATURE:
[UI component description with props, state, and behavior]

## EXAMPLES:
- `examples/components/` - Component structure and patterns
- `examples/hooks/` - Custom hook patterns
- `examples/styles/` - Styling approach and theme usage

## DOCUMENTATION:
- [Framework docs (React, Vue, etc.)]
- [Component library docs]
- [Testing library docs]

## OTHER CONSIDERATIONS:
- Accessibility requirements (ARIA labels, keyboard navigation)
- Responsive design breakpoints
- Loading and error states
- Prop validation and TypeScript types
```

#### **Data Pipeline**
```markdown
## FEATURE:
[Data processing pipeline with input sources, transformations, and outputs]

## EXAMPLES:
- `examples/pipelines/` - ETL pipeline patterns
- `examples/processors/` - Data transformation patterns
- `examples/connectors/` - Data source connection patterns

## DOCUMENTATION:
- [Data processing framework docs]
- [Database connection docs]
- [Data validation library docs]

## OTHER CONSIDERATIONS:
- Error handling and data quality checks
- Performance optimization for large datasets
- Monitoring and alerting for pipeline failures
- Data schema validation and evolution
```

## 🎯 PRP Template

### **Manual PRP Creation Template**
*Note: Usually generated automatically, but useful for understanding structure*

```markdown
name: "[Feature Name]: [Brief Description]"
description: |
  ## Purpose
  [Clear description of what this feature accomplishes]

  ## Core Principles
  1. **Context is King**: Include ALL necessary documentation, examples, and caveats
  2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
  3. **Information Dense**: Use keywords and patterns from the codebase
  4. **Progressive Success**: Start simple, validate, then enhance

---

## Goal
[Detailed description of the end goal and why it's valuable]

## Why
- **Business value**: [How this helps users/business]
- **Technical value**: [How this improves the system]
- **Problems solved**: [What pain points this addresses]

## What
[Detailed specification of functionality and behavior]

### Success Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]
- [ ] All tests pass and code meets quality standards

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: [documentation URL]
  why: [why this documentation is relevant]
  
- file: [example file path]
  why: [why this example is relevant]
```

### Current Codebase Structure
```
[Current relevant file structure]
```

### Desired Codebase Structure
```
[Files and directories to be added]
```

### Known Gotchas & Library Quirks
```[language]
# CRITICAL: [Important constraint or gotcha]
# CRITICAL: [Another important constraint]
```

## Implementation Blueprint

### Data Models and Structure
```[language]
[Key data structures and models]
```

### List of Tasks to be Completed
```yaml
Task 1: [Task name]
CREATE [file path]:
  - PATTERN: [Pattern to follow from examples]
  - [Specific requirements]

Task 2: [Task name]
UPDATE [file path]:
  - PATTERN: [Pattern to follow]
  - [Specific requirements]
```

### Per Task Pseudocode
```[language]
# Task 1: [Task name]
[Detailed pseudocode showing approach]
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      [Environment variables needed]

CONFIG:
  - [Configuration requirements]
  
DEPENDENCIES:
  - Update requirements with:
    - [dependency 1]
    - [dependency 2]
```

## Validation Loop

### Level 1: Syntax & Style
```bash
[Linting and formatting commands]
```

### Level 2: Unit Tests
```bash
[Unit test commands]
```

### Level 3: Integration Test
```bash
[Integration test commands and expected behavior]
```

## Final Validation Checklist
- [ ] All tests pass: `[test command]`
- [ ] No linting errors: `[lint command]`
- [ ] [Feature-specific validation]
- [ ] Error cases handled gracefully
- [ ] Documentation updated

---

## Anti-Patterns to Avoid
- ❌ [Anti-pattern 1 and why to avoid it]
- ❌ [Anti-pattern 2 and why to avoid it]

## Confidence Score: [X]/10

[Explanation of confidence level and any uncertainties]
```

## 📚 Examples README Template

### **examples/README.md Template**

```markdown
# Examples Library

This folder contains code examples and patterns used throughout the project. These examples serve as templates and references for consistent implementation.

## 📁 Structure

### **Core Patterns**
- [`basic_example.py`](basic_example.py) - Basic implementation pattern for [domain]
- [`advanced_example.py`](advanced_example.py) - Advanced features and edge cases

### **Integration Patterns**
- [`api_integration.py`](api_integration.py) - External API integration patterns
- [`database_integration.py`](database_integration.py) - Database connection and query patterns

### **Testing Patterns**
- [`test_example.py`](test_example.py) - Unit testing approach and fixtures
- [`integration_test_example.py`](integration_test_example.py) - Integration testing patterns

## 🎯 How to Use These Examples

### **For New Features**
1. **Find similar examples** - Look for patterns that match your use case
2. **Copy the structure** - Don't copy code directly, but follow the patterns
3. **Adapt to your needs** - Modify for your specific requirements
4. **Add your own examples** - Contribute new patterns back to this library

### **Pattern Guidelines**

#### **✅ Good Example Characteristics**
- **Complete**: Shows full implementation, not just snippets
- **Realistic**: Uses real project patterns and constraints
- **Documented**: Clear comments explaining the why, not just the what
- **Tested**: Includes corresponding test examples
- **Current**: Uses up-to-date libraries and patterns

#### **❌ Avoid These in Examples**
- **Outdated patterns**: Old library versions or deprecated approaches
- **Incomplete code**: Partial implementations that don't work
- **No context**: Code without explanation of when/why to use it
- **Complex first**: Start simple, advanced examples build on basics

## 📖 Example Categories

### **[Category 1: e.g., API Routes]**
**Purpose**: [What these examples demonstrate]

**Key Files**:
- `[file1].py` - [What it shows]
- `[file2].py` - [What it shows]

**Patterns Demonstrated**:
- [Pattern 1]: [Description]
- [Pattern 2]: [Description]

**When to Use**: [Guidance on when to apply these patterns]

### **[Category 2: e.g., Data Models]**
**Purpose**: [What these examples demonstrate]

**Key Files**:
- `[file1].py` - [What it shows]
- `[file2].py` - [What it shows]

**Patterns Demonstrated**:
- [Pattern 1]: [Description]
- [Pattern 2]: [Description]

**When to Use**: [Guidance on when to apply these patterns]

## 🔄 Updating Examples

### **When to Add New Examples**
- You solve a problem that's likely to recur
- You create a new pattern that others should follow
- You integrate with a new external system
- You implement a complex algorithm or business logic

### **Example Quality Checklist**
- [ ] **Complete**: Can be run/tested independently
- [ ] **Documented**: Clear docstrings and comments
- [ ] **Consistent**: Follows project style and patterns
- [ ] **Tested**: Has corresponding test examples
- [ ] **Updated**: This README reflects the new example

### **Contribution Guidelines**
1. **Follow naming conventions**: Use descriptive, consistent names
2. **Add documentation**: Update this README when adding examples
3. **Include tests**: Every example should have a test counterpart
4. **Remove deprecated examples**: Clean up outdated patterns
```

## ⚙️ Validation Commands Template

### **Common Validation Patterns**

#### **Python Projects**
```bash
# Level 1: Syntax & Style (< 10 seconds)
ruff check . --fix              # Linting and auto-fix
black . --check                 # Code formatting check
mypy .                         # Type checking
isort . --check                # Import sorting

# Level 2: Unit Tests (< 2 minutes)
pytest tests/ -v --cov=src --cov-report=term-missing
pytest tests/unit/ -x          # Stop on first failure

# Level 3: Integration Tests (< 5 minutes)
pytest tests/integration/ -v
pytest tests/ --cov=. --cov-report=html

# Level 4: Full Validation Suite
pytest tests/ --cov=. --cov-fail-under=80
bandit -r src/                 # Security scanning
safety check                   # Dependency vulnerability check
```

#### **Node.js/TypeScript Projects**
```bash
# Level 1: Syntax & Style
npm run lint                   # ESLint checking
npm run type-check            # TypeScript compilation
npm run format:check          # Prettier formatting check

# Level 2: Unit Tests
npm test                      # Jest unit tests
npm run test:coverage         # With coverage report

# Level 3: Integration Tests
npm run test:integration      # Integration test suite
npm run test:e2e             # End-to-end tests

# Level 4: Full Validation Suite
npm run build                # Production build
npm audit                    # Security audit
npm run test:ci              # Complete CI test suite
```

#### **Go Projects**
```bash
# Level 1: Syntax & Style
go fmt ./...                  # Format code
go vet ./...                  # Static analysis
golangci-lint run            # Comprehensive linting

# Level 2: Unit Tests
go test ./... -v             # Run all tests
go test ./... -cover         # With coverage
go test ./... -race          # Race condition detection

# Level 3: Integration Tests
go test ./... -tags=integration
go test ./... -bench=.       # Benchmark tests

# Level 4: Full Validation Suite
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out
gosec ./...                  # Security scanning
```

#### **Custom Validation Commands**
```bash
# Project-specific validations
python scripts/validate_config.py     # Custom configuration validation
python scripts/check_migrations.py    # Database migration validation
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# API-specific validations
python scripts/test_api_endpoints.py  # API endpoint smoke tests
newman run postman_collection.json    # Postman collection tests

# Data validation
python scripts/validate_data_schema.py # Data schema compliance
python scripts/check_data_quality.py   # Data quality metrics
```

## 🎯 Quick Copy-Paste Checklist

### **Starting a New Project**
```markdown
✅ Copy CLAUDE.md template and customize for your stack
✅ Create examples/ directory with README
✅ Set up validation commands for your tooling
✅ Create INITIAL.md template for your domain
✅ Test the workflow with a simple feature
```

### **Adding a New Feature**
```markdown
✅ Fill out INITIAL.md with specific requirements
✅ Reference relevant examples and documentation
✅ Generate PRP using /generate-prp command
✅ Review PRP for completeness and accuracy
✅ Execute PRP using /execute-prp command
✅ Validate all quality gates pass
✅ Add new patterns to examples/ if reusable
```

### **Quality Gate Checklist**
```markdown
✅ Syntax and style validation passes
✅ Unit tests pass with adequate coverage
✅ Integration tests pass
✅ Security scans show no critical issues
✅ Performance benchmarks meet requirements
✅ Documentation is updated
✅ Examples are added for new patterns
```

---

*This appendix serves as your quick-reference guide for implementing Context Engineering in your projects. Bookmark it and customize the templates for your specific needs.*