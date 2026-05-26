# Execute Template Generation PRP

Execute a comprehensive template generation PRP to create a complete context engineering template package for a specific technology/framework.

## PRP File: $ARGUMENTS

## Execution Process

1. **Load Template Generation PRP**
   - Read the specified template generation PRP file completely
   - Understand the target technology and all requirements
   - Review all web research findings documented in the PRP
   - Follow all instructions for template package creation

2. **ULTRATHINK - Template Package Design**
   - Create comprehensive implementation plan
   - Plan the complete template package structure based on PRP research
   - Design domain-specific context engineering adaptations
   - Map technology patterns to context engineering principles
   - Plan all required files and their relationships

3. **Generate Complete Template Package**
   - Create complete directory structure for the technology use case
   - Generate domain-specific CLAUDE.md with global rules
   - Create specialized template PRP generation and execution commands
   - Develop domain-specific base PRP template with research findings
   - Include comprehensive examples and documentation from web research

4. **Validate Template Package**
   - Run all validation commands specified in the PRP
   - Verify all required files are created and properly formatted
   - Test template structure completeness and accuracy
   - Check integration with base context engineering framework

5. **Quality Assurance**
   - Ensure template follows all context engineering principles
   - Verify domain-specific patterns are accurately represented
   - Check validation loops are appropriate and executable for the technology
   - Confirm template is immediately usable for the target technology

6. **Complete Implementation**
   - Review template package against all PRP requirements
   - Ensure all success criteria from the PRP are met
   - Validate template is production-ready

## Template Package Requirements

Create a complete use case template with this exact structure:

### Required Directory Structure
```
use-cases/{technology-name}/
├── CLAUDE.md                                    # Domain global rules
├── .claude/commands/
│   ├── generate-{technology}-prp.md            # Domain PRP generation
│   └── execute-{technology}-prp.md             # Domain PRP execution
├── PRPs/
│   ├── templates/
│   │   └── prp_{technology}_base.md            # Domain base PRP template
│   ├── ai_docs/                                # Domain documentation (optional)
│   └── INITIAL.md                              # Example feature request
├── examples/                                   # Domain code examples
├── copy_template.py                            # Template deployment script
└── README.md                                   # Comprehensive usage guide
```

### Content Requirements Based on PRP Research

**CLAUDE.md** must include (global rules for the domain):
- Technology-specific tooling and package management commands
- Domain architectural patterns and conventions
- Framework-specific development workflow procedures
- Security and best practices specific to the technology
- Common gotchas and integration points

**Domain PRP Commands** must include:
- Technology-specific research processes and web search strategies
- Domain documentation gathering approaches based on PRP findings
- Framework-appropriate validation loops and testing patterns
- Specialized implementation blueprints for the technology

**Base PRP Template** must include:
- Pre-filled domain context from web research conducted in PRP
- Technology-specific success criteria and validation gates
- Framework-appropriate implementation patterns and examples
- Domain-specialized documentation references and gotchas

**Copy Script (copy_template.py)** must include:
- Accept target directory as command line argument
- Copy entire template directory structure to target location
- Include ALL files: CLAUDE.md, .claude/, PRPs/, examples/, README.md
- Handle directory creation and error handling gracefully
- Provide clear success feedback with next steps

**README.md** must include:
- Clear description of template purpose and capabilities
- Copy script usage instructions (prominently placed near top)
- Complete PRP framework workflow explanation (3-step process)
- Template structure overview with file explanations
- Technology-specific examples and capabilities
- Common gotchas and troubleshooting guidance

## Validation Requirements

### Structure Validation
```bash
# Verify complete structure exists
find use-cases/{technology-name} -type f -name "*.md" | sort
ls -la use-cases/{technology-name}/.claude/commands/
ls -la use-cases/{technology-name}/PRPs/templates/

# Check required files exist
test -f use-cases/{technology-name}/CLAUDE.md
test -f use-cases/{technology-name}/README.md
test -f use-cases/{technology-name}/PRPs/INITIAL.md
test -f use-cases/{technology-name}/copy_template.py

# Test copy script functionality
python use-cases/{technology-name}/copy_template.py 2>&1 | grep -q "Usage:" || echo "Copy script needs proper usage message"
```

### Content Validation
```bash
# Check for incomplete content
grep -r "TODO\|PLACEHOLDER\|WEBSEARCH_NEEDED" use-cases/{technology-name}/
grep -r "{technology}" use-cases/{technology-name}/ | wc -l  # Should be 0

# Verify domain-specific content exists
grep -r "framework\|library\|technology" use-cases/{technology-name}/CLAUDE.md
grep -r "WebSearch\|web search" use-cases/{technology-name}/.claude/commands/

# Verify README has required sections
grep -q "Quick Start.*Copy Template" use-cases/{technology-name}/README.md
grep -q "PRP Framework Workflow" use-cases/{technology-name}/README.md
grep -q "python copy_template.py" use-cases/{technology-name}/README.md
```

### Functionality Testing
```bash
# Test template functionality
cd use-cases/{technology-name}

# Verify commands are properly named
ls .claude/commands/ | grep "{technology}"

# Test INITIAL.md example exists and is comprehensive
wc -l PRPs/INITIAL.md  # Should be substantial, not just a few lines
```

## Success Criteria

- [ ] Complete template package structure created exactly as specified
- [ ] All required files present and properly formatted
- [ ] Domain-specific content accurately represents technology based on PRP research
- [ ] Context engineering principles properly adapted for the technology
- [ ] Validation loops appropriate and executable for the framework
- [ ] Template package immediately usable for building projects in the domain
- [ ] Integration with base context engineering framework maintained
- [ ] All web research findings from PRP properly integrated into template
- [ ] Examples and documentation comprehensive and technology-specific
- [ ] Copy script (copy_template.py) functional and properly documented
- [ ] README includes copy script instructions prominently at top
- [ ] README explains complete PRP framework workflow with concrete examples

Note: If any validation fails, analyze the error, fix the template package components, and re-validate until all criteria pass. The template must be production-ready and immediately usable for developers working with the target technology.