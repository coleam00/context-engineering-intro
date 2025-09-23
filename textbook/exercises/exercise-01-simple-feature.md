# Exercise 1: Simple Feature Implementation

> **"The best way to learn Context Engineering is to practice it on a real feature you actually need."**

This hands-on exercise will guide you through the complete Context Engineering workflow, from requirements definition to working code. You'll build a simple but useful feature using the PRP (Product Requirements Prompt) methodology.

## 🎯 Exercise Objectives

By the end of this exercise, you will have:
- Created your first INITIAL.md feature specification
- Generated a comprehensive PRP using the template system
- Implemented a working feature following Context Engineering principles
- Validated your implementation with quality gates
- Added examples to your project's pattern library

## 📋 Prerequisites

Before starting this exercise:
- [ ] You have the Context Engineering template set up
- [ ] You understand the basic workflow from Chapters 1-4
- [ ] You have Claude Code configured (or similar AI coding assistant)
- [ ] You have a development environment ready

## 🚀 Exercise Overview

We'll build a **Configuration Validator** - a utility that validates configuration files and provides helpful error messages. This is:
- **Simple enough** for your first Context Engineering project
- **Useful enough** that you'll actually use it
- **Complex enough** to demonstrate the full workflow
- **Generic enough** to apply patterns to other features

## 📝 Phase 1: Requirements Definition (15 minutes)

### **Step 1.1: Create Your INITIAL.md**

Create a new file `INITIAL.md` (or use a different name like `config-validator-requirements.md`) with the following content, customizing for your specific project:

```markdown
## FEATURE:
Configuration file validator that checks project configuration files (JSON, YAML, TOML) for:
- Required fields and proper data types
- Valid enum values and ranges
- Cross-field dependencies and constraints
- Provides clear error messages with line numbers and suggestions

The validator should be usable both as a CLI tool and as an importable library.

## EXAMPLES:
- examples/validation/schema_validator.py - JSON schema validation patterns (if exists)
- examples/cli/argument_parser.py - CLI interface patterns (if exists)  
- examples/config/settings.py - Configuration loading patterns (if exists)
- examples/errors/custom_exceptions.py - Error handling patterns (if exists)

[Note: If you don't have these examples yet, that's fine - the PRP generation will help identify what examples would be valuable]

## DOCUMENTATION:
- JSON Schema validation: https://json-schema.org/understanding-json-schema/
- Pydantic validation (if using Python): https://docs.pydantic.dev/latest/
- Click CLI framework (if using Python): https://click.palletsprojects.com/
- YAML parsing: PyYAML documentation or equivalent for your language

## OTHER CONSIDERATIONS:
- Should handle multiple configuration file formats (JSON, YAML, TOML)
- Error messages should include file path, line number, and suggested fixes
- CLI should have options for different validation levels (strict, warnings, info)
- Should be fast enough for use in CI/CD pipelines
- Include comprehensive tests for various error conditions
- Consider configuration schema evolution (backward compatibility)
```

### **Step 1.2: Review and Customize**

Take 5 minutes to customize this template for your specific needs:

**If you're working in JavaScript/TypeScript:**
- Replace Pydantic with Joi, Zod, or similar validation library
- Replace Click with Commander.js or similar CLI framework
- Adjust file formats based on your ecosystem (package.json, tsconfig.json, etc.)

**If you're working in Go:**
- Reference Go's flag package or Cobra for CLI
- Use Go's JSON/YAML packages
- Focus on struct validation patterns

**If you're working in a different domain:**
- Adapt the configuration validation concept to your domain
- Could be API request validation, data pipeline validation, etc.
- Keep the same level of specificity and context

### **Step 1.3: Identify Your Context Gaps**

Look at your INITIAL.md and identify what context you're missing:

**Questions to consider:**
- Do you have examples of CLI tools in your project?
- Do you have established error handling patterns?
- What validation libraries does your project already use?
- How does your project typically structure utilities vs. libraries?

**Document your gaps** (you'll fill these during the exercise):
```markdown
## Context Gaps Identified:
- [ ] No CLI examples - need to establish CLI patterns
- [ ] No validation examples - need validation error patterns  
- [ ] Unclear project structure - need to establish utility organization
- [ ] No testing examples for CLI tools
```

## 🔍 Phase 2: PRP Generation (20 minutes)

### **Step 2.1: Generate Your PRP**

If you have Claude Code set up:
```bash
/generate-prp INITIAL.md
```

If you don't have Claude Code, manually prompt your AI assistant:
```
Read the feature requirements in INITIAL.md and create a comprehensive Product Requirements Prompt (PRP) for implementing a configuration validator. Follow the PRP template structure from PRPs/templates/ and include:

1. Complete context research from the current codebase
2. External documentation and best practices
3. Step-by-step implementation plan with validation gates
4. Code examples and patterns to follow
5. Error handling and edge case considerations
6. Comprehensive testing strategy

Research the codebase first to understand existing patterns, then create a detailed implementation blueprint.
```

### **Step 2.2: Review Generated PRP**

Your PRP should include sections like:
- **Context Analysis**: What patterns exist in your codebase
- **Implementation Blueprint**: Step-by-step tasks
- **Validation Strategy**: How to test and verify success
- **Quality Gates**: Automated checks that must pass

**Quality Check Questions:**
- Does it reference specific files from your codebase?
- Does it include executable validation commands?
- Does it break down the feature into manageable tasks?
- Does it consider error handling and edge cases?

### **Step 2.3: Customize and Improve PRP**

Spend 5-10 minutes improving your PRP:

**Add missing context** if the generated PRP is too generic:
```markdown
## Additional Context for Our Project:
- We use [specific library] for configuration management
- Error messages should follow the pattern in src/errors/formatting.py
- CLI tools in our project use the structure from tools/cli_template.py
- All utilities must include both library and CLI interfaces
```

**Refine validation commands** for your specific tooling:
```bash
# Instead of generic:
pytest tests/ -v

# Be specific to your project:
pytest tests/unit/test_config_validator.py -v --cov=src/validation
```

## 🛠️ Phase 3: Implementation (45 minutes)

### **Step 3.1: Execute Your PRP**

If using Claude Code:
```bash
/execute-prp PRPs/config-validator-prp.md
```

If using manual prompts:
```
Please implement the configuration validator feature based on the comprehensive PRP document. Follow the implementation plan step by step, create all the specified files, and ensure all validation gates pass.

Use the TodoWrite tool to track progress through each task in the implementation blueprint.
```

### **Step 3.2: Monitor Implementation Progress**

The AI should break down the implementation into tasks and work through them systematically. You should see:

**Task Examples:**
- [ ] Create configuration schema models
- [ ] Implement validation logic
- [ ] Add CLI interface
- [ ] Create error formatting utilities
- [ ] Add comprehensive tests
- [ ] Create library interface

**Watch for Quality Indicators:**
- Files are created following your project's patterns
- Code includes proper error handling
- Tests are comprehensive and test edge cases
- Documentation is included

### **Step 3.3: Validate Each Step**

As the AI completes each task, run the validation commands:

```bash
# Quick validation after each major step:
[your-lint-command]  # e.g., ruff check . or npm run lint
[your-type-check]    # e.g., mypy . or npm run type-check
```

Don't wait until the end - catch issues early!

## ✅ Phase 4: Validation and Testing (20 minutes)

### **Step 4.1: Run All Quality Gates**

Execute all the validation commands specified in your PRP:

**Level 1: Syntax & Style**
```bash
# Run your project's style checks
[linting-command]
[formatting-command] 
[type-checking-command]
```

**Level 2: Unit Tests**
```bash
# Run comprehensive tests
[test-command-with-coverage]
```

**Level 3: Integration Testing**
```bash
# Test the actual CLI and library interfaces
[cli-test-command]
[integration-test-command]
```

### **Step 4.2: Manual Feature Testing**

Test your configuration validator manually:

**Create test configuration files:**
```json
// test-config-valid.json
{
  "name": "test-app",
  "version": "1.0.0",
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

```json
// test-config-invalid.json
{
  "name": 123,
  "version": "invalid-version",
  "database": {
    "host": "",
    "port": "not-a-number"
  }
}
```

**Test CLI interface:**
```bash
# Should succeed
python -m config_validator test-config-valid.json

# Should show helpful errors
python -m config_validator test-config-invalid.json
```

**Test library interface:**
```python
# Should work from Python code
from config_validator import validate_config
result = validate_config("test-config-valid.json")
assert result.is_valid
```

### **Step 4.3: Fix Any Issues**

If validation fails:
1. **Identify the specific issue** from error messages
2. **Ask the AI to fix it** using the PRP context
3. **Re-run validation** to confirm fix
4. **Update examples** if you discover new patterns

## 📚 Phase 5: Learning Extraction (15 minutes)

### **Step 5.1: Update Your Examples Library**

Add the patterns you've created to your examples folder:

```
examples/
├── validation/
│   ├── config_validator.py      # Main validation patterns
│   └── error_formatting.py     # Error message patterns
├── cli/
│   └── validator_cli.py         # CLI interface patterns
└── tests/
    ├── test_validation.py       # Unit testing patterns
    └── test_cli_integration.py  # CLI testing patterns
```

### **Step 5.2: Document Lessons Learned**

Create or update `examples/README.md` with what you learned:

```markdown
## Configuration Validation Patterns

### What We Built
A configuration file validator that demonstrates:
- Multi-format file parsing (JSON, YAML, TOML)
- Schema-based validation with helpful errors
- CLI and library interface patterns
- Comprehensive error formatting

### Key Patterns
- **Error Context**: Always include file path, line number, and suggestions
- **CLI Design**: Separate CLI logic from core functionality
- **Testing Strategy**: Test both valid and invalid configurations
- **Library Interface**: Make functionality available both as CLI and library

### When to Use
- When you need to validate structured configuration
- When building CLI tools that process files
- When you want comprehensive error reporting
- When you need both programmatic and command-line interfaces
```

### **Step 5.3: Update Your CLAUDE.md**

Add any new patterns or preferences you discovered:

```markdown
### 📊 Configuration and Validation
- **Use [validation library]** for data validation
- **Error messages** should include file path, line number, and suggestions
- **CLI tools** should separate argument parsing from core logic
- **Both interfaces**: Provide both library and CLI interfaces for utilities
```

## 🎯 Exercise Completion Checklist

Before moving on, ensure you have:

**✅ Requirements & Planning**
- [ ] Created comprehensive INITIAL.md with specific requirements
- [ ] Generated detailed PRP with implementation plan
- [ ] Customized PRP for your project's specific patterns

**✅ Implementation**
- [ ] Built working configuration validator
- [ ] Followed established project patterns
- [ ] Included both CLI and library interfaces
- [ ] Added comprehensive error handling

**✅ Validation**
- [ ] All code quality checks pass
- [ ] Unit tests pass with good coverage
- [ ] Integration tests work with real files
- [ ] Manual testing confirms functionality

**✅ Knowledge Capture**
- [ ] Added new patterns to examples library
- [ ] Documented lessons learned
- [ ] Updated CLAUDE.md with new preferences
- [ ] Identified reusable patterns for future features

## 🔄 Reflection Questions

Take a few minutes to reflect on your experience:

1. **What surprised you** about the Context Engineering workflow?
2. **Where did the PRP help most?** What problems did it prevent?
3. **What context was missing** that would have made the process smoother?
4. **How did the quality** of the generated code compare to what you usually get from AI assistants?
5. **What patterns will you reuse** in future features?

## 📈 Success Metrics

**Excellent Exercise Completion (9-10/10):**
- Feature works perfectly on first implementation
- Code follows all project patterns consistently  
- Tests are comprehensive and all pass
- Examples and documentation are thorough
- You identified 3+ reusable patterns

**Good Exercise Completion (7-8/10):**
- Feature works with minor iterations
- Code mostly follows project patterns
- Tests cover main functionality
- Some examples and documentation added
- You identified 1-2 reusable patterns

**Adequate Exercise Completion (5-6/10):**
- Feature works after several fixes
- Code quality is acceptable
- Basic tests pass
- Minimal documentation added
- Learning occurred but not systematized

## 🚀 Next Steps

**Ready for more complexity?**
👉 **[Exercise 2: Multi-Agent System](exercise-02-multi-agent.md)**

**Want to deepen your understanding first?**
👉 Go back and read [Chapter 5: CLAUDE.md Rules](../chapter-05-claude-md-rules.md) or [Chapter 6: INITIAL.md Patterns](../chapter-06-initial-md-patterns.md)

**Want to see more examples?**
👉 Explore the [use-cases/](../../use-cases/) folder for more complex implementations

---

## 💡 Troubleshooting Common Issues

**"My PRP is too generic"**
- Add more specific examples to your INITIAL.md
- Include more project-specific context and constraints
- Reference specific files and patterns from your codebase

**"The implementation doesn't follow my project's patterns"**
- Ensure your examples/ folder has representative patterns
- Update CLAUDE.md with more specific style guidelines
- Add project-specific constraints to your INITIAL.md

**"Tests are failing or incomplete"**
- Review existing test patterns in your codebase
- Add test examples to your examples/ folder
- Specify test requirements more clearly in INITIAL.md

**"Generated code is too complex/too simple"**
- Adjust the complexity level in your feature requirements
- Provide examples at the appropriate complexity level
- Use the progressive complexity approach (start simple, enhance)

Remember: **Context Engineering is iterative**. Each feature you build improves your context system for the next one!