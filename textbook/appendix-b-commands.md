# Appendix B: Commands Reference

> **"The right command at the right time can transform hours of work into minutes of execution."**

This appendix provides a comprehensive reference for all Claude Code commands, custom slash commands, and Context Engineering workflows available in the template system.

## 🎯 Quick Command Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/generate-prp` | Creates comprehensive PRPs | After writing INITIAL.md |
| `/execute-prp` | Implements features from PRPs | After generating/reviewing PRP |
| `/generate-pydantic-ai-prp` | AI agent-specific PRP generation | For Pydantic AI projects |
| `/execute-pydantic-ai-prp` | AI agent implementation | For Pydantic AI PRPs |

## 📝 Core Commands

### **`/generate-prp` Command**

#### **Purpose**
Generates comprehensive Product Requirements Prompts (PRPs) from INITIAL.md files.

#### **Syntax**
```bash
/generate-prp <path-to-initial-file>

# Examples:
/generate-prp INITIAL.md
/generate-prp features/user-auth.md
/generate-prp requirements/api-redesign.md
```

#### **What It Does**
1. **Reads feature requirements** from the specified INITIAL.md file
2. **Researches codebase** for similar patterns and implementations
3. **Gathers external documentation** from links provided
4. **Creates comprehensive PRP** with implementation blueprint
5. **Saves PRP** to `PRPs/[feature-name].md`

#### **Expected Input Format**
```markdown
## FEATURE:
[Detailed feature description]

## EXAMPLES:
- path/to/example.py - Description of relevant pattern
- path/to/another_example.py - Another relevant pattern

## DOCUMENTATION:
- Library docs: https://example.com/docs
- API reference: https://api.example.com/docs

## OTHER CONSIDERATIONS:
- Important constraint 1
- Gotcha to avoid
- Performance requirement
```

#### **Command Implementation**
```markdown
# From .claude/commands/generate-prp.md

## Research Process
1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRP
   - Note existing conventions to follow

2. **External Research**
   - Library documentation (include specific URLs)
   - Implementation examples
   - Best practices and common pitfalls

## PRP Generation
- Use PRPs/templates/prp_base.md as template
- Include all necessary context for one-pass implementation
- Add executable validation commands
- Score confidence level (1-10) for implementation success
```

#### **Troubleshooting**
```markdown
**Issue**: Generic PRP generated
**Solution**: Add more specific examples and constraints to INITIAL.md

**Issue**: Missing technology-specific guidance
**Solution**: Ensure CLAUDE.md has clear technology stack preferences

**Issue**: Validation commands don't work
**Solution**: Update validation commands in PRP template for your project
```

### **`/execute-prp` Command**

#### **Purpose**
Systematically implements features based on comprehensive PRPs.

#### **Syntax**
```bash
/execute-prp <path-to-prp-file>

# Examples:
/execute-prp PRPs/user-authentication.md
/execute-prp PRPs/api-refactor.md
/execute-prp features/payment-integration.md
```

#### **What It Does**
1. **Loads PRP context** completely and validates understanding
2. **Creates implementation plan** using TodoWrite for task tracking
3. **Executes systematically** following PRP guidance step by step
4. **Validates progress** at each level (syntax, tests, integration)
5. **Ensures completion** by checking all success criteria

#### **Execution Process**
```markdown
## 5-Phase Execution:

Phase 1: Context Loading
- Read entire PRP document
- Understand business goals and technical requirements
- Review all referenced examples and documentation

Phase 2: Planning (ULTRATHINK)
- Break down into manageable tasks
- Identify dependencies and risks
- Create detailed implementation strategy

Phase 3: Implementation
- Execute tasks systematically
- Follow established patterns from examples
- Maintain quality throughout process

Phase 4: Validation
- Run all quality gates from PRP
- Fix any issues discovered
- Ensure all tests pass

Phase 5: Completion
- Verify all success criteria met
- Document implementation decisions
- Extract reusable patterns for future use
```

#### **Command Implementation**
```markdown
# From .claude/commands/execute-prp.md

## Execution Process
1. **Load PRP** - Read and understand all context
2. **ULTRATHINK** - Create comprehensive plan
3. **Execute** - Implement following patterns
4. **Validate** - Run all quality gates
5. **Complete** - Ensure all requirements met

## Key Practices:
- Use TodoWrite tool for task tracking
- Reference PRP throughout implementation
- Run validation commands at each stage
- Document learnings and new patterns
```

#### **Troubleshooting**
```markdown
**Issue**: Implementation doesn't follow project patterns
**Solution**: Check that examples folder has representative patterns

**Issue**: Validation commands fail
**Solution**: Update validation commands for your specific tooling

**Issue**: Generated code is too complex/simple
**Solution**: Adjust PRP complexity and provide better examples
```

## 🤖 Specialized Commands

### **`/generate-pydantic-ai-prp` Command**

#### **Purpose**
Specialized PRP generation for Pydantic AI agent development.

#### **Location**
Available in `use-cases/pydantic-ai/.claude/commands/`

#### **Syntax**
```bash
/generate-pydantic-ai-prp <path-to-initial-file>

# Example:
/generate-pydantic-ai-prp PRPs/INITIAL.md
```

#### **Specialized Features**
- **Agent-specific patterns** from Pydantic AI best practices
- **Tool integration guidance** for external APIs and services
- **Testing strategies** using TestModel and FunctionModel
- **Environment configuration** patterns for AI agents
- **Multi-agent architectures** and agent-as-tool patterns

#### **Expected Context**
```markdown
## FEATURE:
Pydantic AI agent with specific capabilities:
- Tool integration (APIs, databases, external services)
- Conversation memory and context management
- Structured outputs and data validation
- Error handling and recovery patterns

## EXAMPLES:
- examples/basic_chat_agent/ - Simple conversational patterns
- examples/tool_enabled_agent/ - Tool integration patterns
- examples/testing_examples/ - Agent testing approaches

## DOCUMENTATION:
- Pydantic AI: https://ai.pydantic.dev/
- Specific API docs for tools being integrated

## OTHER CONSIDERATIONS:
- Environment setup for API keys and configuration
- Tool error handling and fallback strategies
- Testing approach to avoid API costs during development
```

### **`/execute-pydantic-ai-prp` Command**

#### **Purpose**
Implements Pydantic AI agents following specialized patterns.

#### **Syntax**
```bash
/execute-pydantic-ai-prp <path-to-prp-file>
```

#### **Specialized Implementation**
- **Agent configuration** with environment-based model selection
- **Tool registration** using `@agent.tool` decorator patterns
- **Testing setup** with TestModel and FunctionModel
- **Dependency injection** using RunContext patterns
- **Error handling** for external service failures

## 🛠️ Custom Command Creation

### **Creating Your Own Commands**

#### **Command File Structure**
```markdown
# .claude/commands/my-custom-command.md

# Command Name
Brief description of what this command does.

## Parameters: $ARGUMENTS
Explanation of what arguments this command accepts.

## Process Description
1. Step-by-step description of what the command does
2. Research or analysis phase
3. Implementation or generation phase
4. Validation or completion phase

## Expected Outputs
- What files will be created or modified
- What validation should be run
- What success looks like

## Quality Checklist
- [ ] Specific validation criteria
- [ ] Success indicators
- [ ] Common failure modes to check
```

#### **Example Custom Command**
```markdown
# .claude/commands/generate-api-docs.md

# Generate API Documentation
Automatically generate comprehensive API documentation from FastAPI application.

## Feature file: $ARGUMENTS
Generate OpenAPI documentation and user guides for the API endpoints defined in the specified module.

## Process
1. **API Analysis**
   - Scan FastAPI application for all endpoints
   - Extract route definitions, parameters, and responses
   - Identify authentication and authorization requirements

2. **Documentation Generation**
   - Generate OpenAPI specification
   - Create user-friendly endpoint documentation
   - Add example requests and responses
   - Include authentication guides

3. **Validation**
   - Verify OpenAPI spec is valid
   - Test example requests actually work
   - Check documentation completeness

## Output Files
- `docs/api-spec.json` - OpenAPI specification
- `docs/api-guide.md` - User-friendly documentation
- `docs/examples/` - Request/response examples

## Quality Checklist
- [ ] All endpoints documented with examples
- [ ] Authentication requirements clearly explained
- [ ] Error responses documented
- [ ] OpenAPI spec validates successfully
- [ ] Examples can be executed successfully
```

### **Domain-Specific Command Templates**

#### **Frontend Component Command**
```markdown
# .claude/commands/generate-react-component.md

# Generate React Component
Create production-ready React component with TypeScript, tests, and documentation.

## Component specification: $ARGUMENTS
Read component requirements and generate complete React component implementation.

## Research Process
1. **Pattern Analysis**
   - Review existing components for patterns
   - Identify reusable hooks and utilities
   - Note styling and theming approaches

2. **Component Design**
   - Plan component props and state
   - Design hook usage and lifecycle
   - Plan accessibility and responsive design

## Implementation
- TypeScript component with proper typing
- Unit tests with React Testing Library
- Storybook stories for component showcase
- CSS modules or styled-components
- Documentation with usage examples

## Validation
```bash
npm run type-check     # TypeScript validation
npm run test           # Unit tests
npm run lint           # ESLint validation
npm run build          # Build validation
```
```

#### **Database Migration Command**
```markdown
# .claude/commands/generate-migration.md

# Generate Database Migration
Create database migration with proper rollback and validation.

## Migration specification: $ARGUMENTS
Read migration requirements and generate safe, reversible database migration.

## Research Process
1. **Schema Analysis**
   - Review current database schema
   - Identify affected tables and relationships
   - Plan migration strategy and rollback

2. **Safety Validation**
   - Ensure migration is reversible
   - Check for data loss risks
   - Validate constraint and index changes

## Implementation
- Forward migration with proper constraints
- Rollback migration that reverses all changes
- Data validation scripts
- Performance impact assessment
- Documentation of breaking changes

## Validation
```bash
python manage.py makemigrations --dry-run  # Dry run test
python manage.py migrate --plan             # Migration plan
python scripts/test_migration.py           # Custom validation
```
```

## 📋 Workflow Commands

### **Development Workflow Commands**

#### **Quality Gate Command**
```bash
# .claude/commands/run-quality-gates.md

# Run Quality Gates
Execute all quality validation for current changes.

## Process
1. **Fast Validation** (< 10 seconds)
   - Code formatting and style
   - Type checking
   - Import validation

2. **Component Testing** (< 2 minutes)
   - Unit tests for changed components
   - Coverage validation
   - Smoke tests

3. **Integration Testing** (< 5 minutes)
   - API endpoint testing
   - Database integration tests
   - External service integration

4. **Full Validation** (< 10 minutes)
   - Complete test suite
   - Security scanning
   - Performance validation
```

#### **Context Sync Command**
```bash
# .claude/commands/sync-context.md

# Sync Context
Update context system with latest patterns and improvements.

## Process
1. **Pattern Detection**
   - Scan recent commits for new patterns
   - Identify successful implementations
   - Extract reusable components

2. **Context Updates**
   - Add new examples to examples/
   - Update CLAUDE.md with new rules
   - Refresh documentation references

3. **Validation**
   - Test context changes with sample PRPs
   - Verify example quality and consistency
   - Update validation commands if needed
```

### **Team Collaboration Commands**

#### **Context Review Command**
```bash
# .claude/commands/review-context-changes.md

# Review Context Changes
Systematically review and approve context system changes.

## Review Process
1. **Change Analysis**
   - What context was added, modified, or removed?
   - What was the motivation for changes?
   - What impact will changes have on team?

2. **Quality Assessment**
   - Are new examples clear and reusable?
   - Do rule changes improve consistency?
   - Are validation commands appropriate?

3. **Approval Process**
   - Technical review of context accuracy
   - Team discussion of adoption strategy
   - Gradual rollout plan for major changes
```

## 🔧 Troubleshooting Commands

### **Common Issues and Solutions**

#### **Context Debugging Commands**

```bash
# Debug why PRP generation is producing poor results
/debug-context INITIAL.md

# Validate that examples are being found and used correctly
/validate-examples

# Check if CLAUDE.md rules are being followed
/check-rule-compliance

# Test PRP execution pipeline without making changes
/dry-run-prp PRPs/test-feature.md
```

#### **Environment Validation Commands**

```bash
# Verify Claude Code setup and permissions
/check-claude-setup

# Validate that all required tools are available
/validate-environment

# Test that validation commands work correctly
/test-validation-pipeline

# Check for common configuration issues
/diagnose-setup-issues
```

## 📊 Command Usage Analytics

### **Tracking Command Effectiveness**

```markdown
## Usage Metrics to Track:

### Command Success Rate:
- How often do commands complete successfully?
- What are common failure modes?
- Which commands need improvement?

### Implementation Quality:
- Do command outputs meet quality standards?
- How often does generated code need manual fixes?
- Are validation commands catching issues effectively?

### Team Adoption:
- Which commands are used most frequently?
- Are teams following recommended workflows?
- What barriers prevent command usage?

### Time Savings:
- How much time do commands save vs. manual implementation?
- Which commands provide the highest ROI?
- Where should command development be prioritized?
```

## ✅ Command Reference Checklist

Use this checklist when working with commands:

### **Before Running Commands:**
- [ ] Required files (INITIAL.md, examples) are complete
- [ ] CLAUDE.md has relevant rules and patterns
- [ ] Environment is properly configured
- [ ] Dependencies are installed and available

### **During Command Execution:**
- [ ] Monitor progress and intervene if needed
- [ ] Validate intermediate outputs
- [ ] Check that patterns are being followed
- [ ] Ensure quality gates are passing

### **After Command Completion:**
- [ ] Review all generated/modified files
- [ ] Run complete validation pipeline
- [ ] Test functionality manually
- [ ] Extract new patterns for future use
- [ ] Update context based on learnings

## 🎯 Quick Reference Cards

### **Emergency Commands**
```bash
# When things go wrong, start here:
/validate-environment      # Check basic setup
/check-claude-setup       # Verify Claude Code configuration
/diagnose-setup-issues    # Identify common problems
```

### **Daily Development Commands**
```bash
# Most commonly used commands:
/generate-prp INITIAL.md  # Create implementation blueprint
/execute-prp PRPs/feature.md  # Implement feature
/run-quality-gates        # Validate changes
```

### **Maintenance Commands**
```bash
# Weekly/monthly maintenance:
/sync-context            # Update context with new patterns
/review-context-changes  # Review and approve updates
/validate-examples       # Ensure examples are current
```

---

*This appendix serves as your complete reference for all Context Engineering commands and workflows. Bookmark it for quick access during development.*