# Template Generator - Meta-Framework for Context Engineering

This template generator creates complete context engineering template packages for any technology domain. It's a meta-template that generates specialized templates for frameworks like Pydantic AI, Supabase, CrewAI, etc.

## 🚀 Quick Start

```bash
# 1. Define your template requirements in detail
# Edit PRPs/INITIAL.md with specific technology and requirements

# 2. Generate comprehensive template PRP
/generate-template-prp PRPs/INITIAL.md

# 3. Execute the PRP to create complete template package
/execute-template-prp PRPs/template-{technology-name}.md
```

## 📚 What This Creates

This meta-template generates complete context engineering template packages with:

### Generated Template Structure
```
use-cases/{technology-name}/
├── CLAUDE.md                          # Technology-specific global rules
├── .claude/commands/
│   ├── generate-{tech}-prp.md        # Domain PRP generation
│   └── execute-{tech}-prp.md         # Domain PRP execution
├── PRPs/
│   ├── templates/
│   │   └── prp_{tech}_base.md        # Technology-specific base PRP
│   ├── ai_docs/                      # Domain documentation
│   └── INITIAL.md                    # Example feature request
├── examples/                         # Technology-specific examples
└── README.md                         # Usage guide
```

### Template Features

**Technology Specialization:**
- Framework-specific global rules and patterns
- Technology-appropriate validation loops
- Domain-specific research methodologies
- Framework-specialized documentation references

**Web Research Integration:**
- Extensive web search requirements for technology research
- Official documentation gathering and analysis
- Real-world pattern identification and extraction
- Best practices and gotcha documentation

**Context Engineering Adaptation:**
- PRP framework adapted for specific technologies
- Domain-appropriate success criteria
- Technology-specific implementation blueprints
- Framework-specialized validation gates

## 🔍 Research-Driven Approach

This meta-template emphasizes **extensive web research** as the foundation for creating high-quality templates:

1. **Technology Deep Dive** - Comprehensive research of official docs, patterns, and best practices
2. **Pattern Extraction** - Identification of real-world implementation patterns
3. **Context Integration** - Adaptation of context engineering principles for the technology
4. **Validation Design** - Creation of technology-appropriate testing and validation loops

## 📋 Usage Process

### 1. Define Requirements (PRPs/INITIAL.md)

Be extremely specific about:
- **Target technology/framework**
- **Core features to support**
- **Examples to include**
- **Documentation to research**
- **Development patterns**
- **Security considerations**
- **Common gotchas**
- **Validation requirements**

### 2. Generate Template PRP

```bash
/generate-template-prp PRPs/INITIAL.md
```

This will:
- Conduct extensive web research on your specified technology
- Analyze official documentation and best practices
- Create comprehensive implementation blueprint
- Design technology-specific validation loops

### 3. Execute Template Generation

```bash
/execute-template-prp PRPs/template-{technology-name}.md
```

This will:
- Create complete template package directory structure
- Generate technology-specific CLAUDE.md with global rules
- Create specialized PRP commands for the technology
- Develop domain-specific base PRP template
- Include working examples and comprehensive documentation

## 🎯 Template Quality Standards

Generated templates include:

**Comprehensive Research Foundation:**
- Extensive web research on target technology
- Official documentation analysis and integration
- Real-world pattern identification
- Best practices and gotcha documentation

**Technology Specialization:**
- Framework-specific patterns and conventions
- Domain-appropriate architectural guidance
- Technology-specific validation and testing approaches
- Integration patterns for common use cases

**Context Engineering Integration:**
- Proper adaptation of PRP framework principles
- Technology-appropriate success criteria
- Domain-specific research methodologies
- Specialized validation loops and quality gates

## 🔧 Key Features

### Web Research Emphasis
- **Web search is your best friend** throughout the process
- Comprehensive technology documentation analysis
- Real-world implementation pattern identification
- Community best practices research and integration

### Template Package Completeness
- Complete directory structure with all required files
- Technology-specific global rules and patterns
- Specialized PRP generation and execution commands
- Domain-appropriate base PRP templates
- Working examples and comprehensive documentation

### Quality Validation
- Multiple validation levels for template structure and content
- Technology-specific testing and validation approaches
- Integration testing with base context engineering framework
- Usability validation for immediate developer productivity

## 📚 Examples of Templates You Can Generate

- **Pydantic AI Agents** - AI agent development with tool integration
- **Supabase Applications** - Full-stack apps with real-time features
- **CrewAI Multi-Agents** - Complex multi-agent system development
- **FastAPI Services** - High-performance API development
- **React Applications** - Modern frontend development patterns
- **Any Technology** - The system adapts to any framework or library

## 🚫 Anti-Patterns Avoided

- ❌ Generic templates without technology specialization
- ❌ Shallow research leading to incomplete patterns
- ❌ Missing validation loops and quality gates
- ❌ Ignoring framework-specific best practices
- ❌ Incomplete documentation and examples

## 🔄 Continuous Improvement

Templates generated with this system:
- Are based on comprehensive, current research
- Include real-world patterns and best practices
- Provide immediate developer productivity
- Can be updated as technologies evolve
- Maintain consistency with context engineering principles

## 🎓 Philosophy

This meta-template embodies the principle that **context engineering can be applied to any technology domain** through:

1. **Deep Research** - Understanding the technology thoroughly
2. **Pattern Extraction** - Identifying reusable implementation patterns
3. **Context Integration** - Adapting context engineering principles
4. **Quality Validation** - Ensuring templates work immediately and effectively

The result is a systematic approach to creating high-quality, immediately usable context engineering templates for any technology domain.