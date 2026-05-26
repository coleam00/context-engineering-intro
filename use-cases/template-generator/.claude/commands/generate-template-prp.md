# Generate Template PRP

## Feature file: $ARGUMENTS

Generate a comprehensive PRP for creating context engineering templates for specific technology domains based on the detailed requirements in the INITIAL.md file. This follows the standard PRP framework workflow: INITIAL.md → generate-template-prp → execute-template-prp.

**CRITICAL: Web search and documentation research is your best friend. Use it extensively throughout this process.**

## Research Process

1. **Read and Understand Requirements**
   - Read the specified INITIAL.md file thoroughly
   - Understand the target technology and specific template requirements
   - Note any specific features, examples, or documentation mentioned
   - Identify the scope and complexity of the template needed

2. **Extensive Web Research (CRITICAL)**
   - **Web search the target technology extensively** - this is essential
   - Study official documentation, APIs, and getting started guides
   - Research best practices and common architectural patterns
   - Find real-world implementation examples and tutorials
   - Identify common gotchas, pitfalls, and edge cases
   - Look for established project structure conventions

3. **Technology Pattern Analysis**
   - Examine successful implementations found through web research
   - Identify project structure and file organization patterns
   - Extract reusable code patterns and configuration templates
   - Document framework-specific development workflows
   - Note testing frameworks and validation approaches

4. **Context Engineering Adaptation**
   - Map discovered technology patterns to context engineering principles
   - Plan how to adapt the PRP framework for this specific technology
   - Design domain-specific validation requirements
   - Plan template package structure and components

## PRP Generation

Using PRPs/templates/prp_template_base.md as the foundation:

### Critical Context to Include from Web Research

**Technology Documentation (from web search)**:
- Official framework documentation URLs with specific sections
- Getting started guides and tutorials
- API references and best practices guides
- Community resources and example repositories

**Implementation Patterns (from research)**:
- Framework-specific project structures and conventions
- Configuration management approaches
- Development workflow patterns
- Testing and validation approaches

**Real-World Examples**:
- Links to successful implementations found online
- Code snippets and configuration examples
- Common integration patterns
- Deployment and setup procedures

### Implementation Blueprint

Based on web research findings:
- **Technology Analysis**: Document framework characteristics and patterns
- **Template Structure**: Plan complete template package components
- **Specialization Strategy**: How to adapt context engineering for this technology
- **Validation Design**: Technology-appropriate testing and validation loops

### Validation Gates (Must be Executable)

```bash
# Template Structure Validation
ls -la use-cases/{technology-name}/
find use-cases/{technology-name}/ -name "*.md" | wc -l  # Should have all required files

# Template Content Validation  
grep -r "TODO\|PLACEHOLDER" use-cases/{technology-name}/  # Should be empty
grep -r "WEBSEARCH_NEEDED" use-cases/{technology-name}/  # Should be empty

# Template Functionality Testing
cd use-cases/{technology-name}
/generate-{technology}-prp INITIAL.md  # Test domain-specific PRP generation
```

*** CRITICAL: Do extensive web research before writing the PRP ***
*** Use WebSearch tool extensively to understand the technology deeply ***

## Output

Save as: `PRPs/template-{technology-name}.md`

## Quality Checklist

- [ ] Extensive web research completed on target technology
- [ ] Official documentation thoroughly reviewed
- [ ] Real-world examples and patterns identified
- [ ] Complete template package structure planned
- [ ] Domain-specific validation designed
- [ ] All web research findings documented in PRP
- [ ] Technology-specific gotchas and patterns captured

Score the PRP on a scale of 1-10 (confidence level for creating comprehensive, immediately usable templates based on thorough technology research).

Remember: The goal is creating complete, specialized template packages that make context engineering trivial to apply to any technology domain through comprehensive research and documentation.