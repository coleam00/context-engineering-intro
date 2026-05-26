# Template Generator - Global Rules for Context Engineering

This file contains the global rules and principles that apply to ALL context engineering work, regardless of what template or project you're building. These rules never change and should be followed consistently.

## 🔄 Context Engineering Core Principles

**IMPORTANT: These principles apply to ALL context engineering work:**

### PRP Framework Workflow
- **Always start with INITIAL.md** - Define requirements before generating PRPs
- **Use the PRP pattern**: INITIAL.md → `/generate-template-prp INITIAL.md` → `/execute-template-prp PRPs/filename.md`
- **Follow validation loops** - Each PRP must include executable validation steps
- **Context is King** - Include ALL necessary documentation, examples, and patterns

### Research Methodology
- **Web search first** - Always do extensive web research before implementation
- **Documentation deep dive** - Study official docs, best practices, and common patterns
- **Pattern extraction** - Identify reusable patterns and architectural conventions
- **Gotcha documentation** - Document common pitfalls and edge cases

## 📚 Project Awareness & Context

- **Use consistent naming conventions** and file structure patterns
- **Follow established directory organization** patterns
- **Leverage examples extensively** - Study existing patterns before creating new ones

## 🧱 Code Structure & Modularity

- **Never create files longer than 500 lines** - Split into modules when approaching limit
- **Organize code into clearly separated modules** grouped by feature or responsibility
- **Use clear, consistent imports** (prefer relative imports within packages)
- **Follow established coding standards** and conventions

## ✅ Task Management

- **Break complex tasks into smaller steps** with clear completion criteria
- **Mark tasks complete immediately** after finishing them
- **Update task status in real-time** as work progresses

## 📎 Documentation Standards

- **Write comprehensive documentation** for every component
- **Include clear usage examples** with working code
- **Document all gotchas and edge cases** to prevent common errors
- **Maintain up-to-date references** to external documentation

## 🔍 Research Standards

- **Web search is your best friend** - Use it extensively for technology research
- **Study official documentation thoroughly** before implementation
- **Research established patterns** and best practices for the technology
- **Document all findings comprehensively** in PRPs and implementation guides

## 🎯 Implementation Standards

- **Follow the PRP workflow religiously** - Don't skip steps
- **Always validate before proceeding** to the next step
- **Use existing patterns as templates** rather than creating from scratch
- **Include comprehensive error handling** in all implementations

## 🚫 Anti-Patterns to Always Avoid

- ❌ Don't skip research - Always understand the technology deeply first
- ❌ Don't create generic solutions - Always specialize for the specific use case
- ❌ Don't ignore validation - Every step must include verification
- ❌ Don't assume knowledge - Document everything explicitly
- ❌ Don't skip examples - Always include working code examples
- ❌ Don't forget edge cases - Include error handling and gotchas

## 🔧 Tool Usage Standards

- **Use web search extensively** for research and documentation
- **Follow established command patterns** for slash commands
- **Use validation loops** to ensure quality at each step

These global rules apply regardless of whether you're generating templates, implementing features, or doing research. They form the foundation of effective context engineering work.