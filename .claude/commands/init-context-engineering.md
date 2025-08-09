---
name: "Initialize Context Engineering Environment"
description: "Initialize context engineering environment in target projects with automatic analysis and setup"
Usage: /init-context-engineering <target-directory>
Example: /init-context-engineering /path/to/target-project
---

# Initialize Context Engineering Environment

## Target Directory: $ARGUMENTS

Initialize context engineering environment in the specified target project by analyzing the project structure and creating all necessary directories, files, and configurations.

## Analysis Process

1. **Project Analysis**
   - Detect project type (Python/TypeScript/Generic)
   - Identify frameworks and dependencies
   - Analyze existing code structure and patterns
   - Determine testing frameworks and conventions

2. **Environment Setup**
   - Create complete directory structure
   - Generate project-specific CLAUDE.md
   - Create customized command templates
   - Set up configuration files

## Directory Structure Created

```
📦 target-project/
├── 📂 .claude/
│   ├── 🎯 settings.local.json
│   └── 📂 commands/
│       ├── 🎯 generate-prp.md
│       └── 🎯 execute-prp.md
├── 📂 context-engineering/
│   ├── 📂 features/
│   │   └── 🎯 INITIAL_EXAMPLE.md
│   ├── 📂 PRPs/
│   │   └── 📂 templates/
│   │       └── 🎯 prp_base.md
│   ├── 📂 examples/
│   └── 🎯 README.md
└── 🎯 CLAUDE.md
```

## Features Created

- **Project Analysis**: Automatic detection of project type, frameworks, and patterns
- **Customized CLAUDE.md**: Project-specific rules and conventions
- **Command Templates**: generate-prp and execute-prp commands tailored to the project
- **Chinese Documentation**: Comprehensive usage guide in Chinese
- **Template System**: PRP templates customized for the project's architecture
- **Example Features**: Ready-to-use feature examples for reference

## Usage Instructions

After initialization, users can:
1. Create feature requirements in `context-engineering/features/`
2. Generate PRPs using `/generate-prp <feature-file>`
3. Execute PRPs using `/execute-prp <prp-file>`
4. Follow the Chinese documentation in `context-engineering/README.md`

## Quality Assurance

- Validates target directory exists
- Analyzes project structure thoroughly
- Creates consistent, project-specific configurations
- Provides comprehensive feedback and next steps
- Includes error handling and validation