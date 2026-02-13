# 🚀 Full Guide to Using Claude Code

Everything you need to know to crush building anything with Claude Code! This guide takes you from installation through advanced context engineering, subagents, hooks, and parallel agent workflows.

## 📋 Prerequisites

- Terminal/Command line access
- Node.js installed (for Claude Code installation)
- GitHub account (for GitHub CLI integration)
- Text editor (VS Code recommended)

## 🔧 Installation

**macOS/Linux:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Windows (WSL recommended):**
See detailed instructions in [install_claude_code_windows.md](./install_claude_code_windows.md)

**Verify installation:**
```bash
claude --version
```

---

## ✅ TIP 1: CREATE AND OPTIMIZE CLAUDE.md FILES

Set up context files that Claude automatically pulls into every conversation, containing project-specific information, commands, and guidelines.

```bash
mkdir your-folder-name && cd your-folder-name
claude
```

Use the built-in command:
```
/init
```

Or create your own CLAUDE.md file based on the template in this repository. See `CLAUDE.md` for a Python specific example structure that includes:
- Project awareness and context rules
- Code structure guidelines
- Testing requirements
- Task completion workflow
- Style conventions
- Documentation standards

### Advanced Prompting Techniques

**Power Keywords**: Claude responds to certain keywords with enhanced behavior (information dense keywords):
- **IMPORTANT**: Emphasizes critical instructions that should not be overlooked
- **Proactively**: Encourages Claude to take initiative and suggest improvements
- **Ultra-think**: Can trigger more thorough analysis (use sparingly)

**Essential Prompt Engineering Tips**:
- Avoid prompting for "production-ready" code - this often leads to over-engineering
- Prompt Claude to write scripts to check its work: "After implementing, create a validation script"
- Avoid backward compatibility unless specifically needed - Claude tends to preserve old code unnecessarily
- Focus on clarity and specific requirements rather than vague quality descriptors

### File Placement Strategies

Claude automatically reads CLAUDE.md files from multiple locations:

```bash
# Root of repository (most common)
./CLAUDE.md              # Checked into git, shared with team
./CLAUDE.local.md        # Local only, add to .gitignore

# Parent directories (for monorepos)
root/CLAUDE.md           # General project info
root/frontend/CLAUDE.md  # Frontend-specific context
root/backend/CLAUDE.md   # Backend-specific context

# Reference external files for flexibility
echo "Follow best practices in: ~/company/engineering-standards.md" > CLAUDE.md
```

**Pro Tip**: Many teams keep their CLAUDE.md minimal and reference a shared standards document. This makes it easy to:
- Switch between AI coding assistants
- Update standards without changing every project
- Share best practices across teams

*Note: While Claude Code reads CLAUDE.md automatically, other AI coding assistants can use similar context files (such as .cursorrules for Cursor)*

---

## ✅ TIP 2: SET UP PERMISSION MANAGEMENT

Configure tool allowlists to streamline development while maintaining security for file operations and system commands.

**Method 1: Interactive Allowlist**
When Claude asks for permission, select "Always allow" for common operations.

**Method 2: Use /permissions command**
```
/permissions
```
Then add:
- `Edit` (for file edits)
- `Bash(git commit:*)` (for git commits)
- `Bash(npm:*)` (for npm commands)
- `Read` (for reading files)
- `Write` (for creating files)

**Method 3: Create project settings file**
Create `.claude/settings.local.json`:
```json
{
  "allowedTools": [
    "Edit",
    "Read",
    "Write",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(npm:*)",
    "Bash(python:*)",
    "Bash(pytest:*)"
  ]
}
```

**Security Best Practices**:
- Never allow `Bash(rm -rf:*)` or similar destructive commands
- Use specific command patterns rather than `Bash(*)`
- Review permissions regularly
- Use different permission sets for different projects

*Note: All AI coding assistants have permission management - some built-in, others require manual approval for each action.*

---

## ✅ TIP 3: MASTER CUSTOM SLASH COMMANDS

Slash commands are the key to adding your own workflows into Claude Code. They live in `.claude/commands/` and enable you to create reusable, parameterized workflows.

### Built-in Commands
- `/init` - Generate initial CLAUDE.md
- `/permissions` - Manage tool permissions
- `/clear` - Clear context between tasks
- `/agents` - Manage subagents
- `/help` - Get help with Claude Code

### Custom Command Example

**Repository Analysis**:
```
/primer
```
Performs comprehensive repository analysis to prime Claude Code on your codebase so you can start implemention fixes or new features and it has all the necessary context to do so.

### Creating Your Own Commands

1. Create a markdown file in `.claude/commands/`:
```markdown
# Command: analyze-performance

Analyze the performance of the file specified in $ARGUMENTS.

## Steps:
1. Read the file at path: $ARGUMENTS
2. Identify performance bottlenecks
3. Suggest optimizations
4. Create a benchmark script
```

2. Use the command:
```
/analyze-performance src/heavy-computation.js
```

Commands can use `$ARGUMENTS` to receive parameters and can invoke any of Claude's tools.

*Note: Other AI coding assistants can use these commands as regular prompts - just copy the command content and paste it with your arguments.*

---

## ✅ TIP 4: INTEGRATE MCP SERVERS

Connect Claude Code to Model Context Protocol (MCP) servers for enhanced functionality. Learn more in the [MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp).

**Add Serena MCP Server** - The most powerful coding toolkit:

Make sure you [install uvx](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) first. Here is how you do that in WSL with Windows:
```bash
sudo snap install astral-uv --classic
```

Then add Serena using the command:
```bash
# Install Serena for semantic code analysis and editing
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
```

[Serena](https://github.com/oraios/serena) transforms Claude Code into a fully-featured coding agent with:
- Semantic code retrieval and analysis
- Advanced editing capabilities using Language Server Protocol (LSP)
- Support for Python, TypeScript/JavaScript, PHP, Go, Rust, C/C++, Java
- Free and open-source alternative to subscription-based coding assistants

**Manage MCP servers:**
```bash
# List all configured servers
claude mcp list

# Get details about a specific server
claude mcp get serena

# Remove a server
claude mcp remove serena
```

**Coming Soon**: Archon V2 (HUGE Overhaul) - A comprehensive knowledge and task management backbone for AI coding assistants - enabling true human-AI collaboration on code for the first time.

*Note: MCP is integrated with every major AI coding assistant and the servers are managed in a very similar way.*

---

## ✅ TIP 5: CONTEXT ENGINEERING WITH EXAMPLES

Transform your development workflow from simple prompting to comprehensive context engineering - providing AI with all the information needed for end-to-end implementation.

### Quick Start

The PRP (Product Requirements Prompt) framework is a simple 3-step strategy for context engineering:

```bash
# 1. Define your requirements with examples and context
# Edit INITIAL.md to include example code and patterns

# 2. Generate a comprehensive PRP
/generate-prp INITIAL.md

# 3. Execute the PRP to implement your feature
/execute-prp PRPs/your-feature-name.md
```

### Defining Your Requirements

Your INITIAL.md should always include:

```markdown
## FEATURE
Build a user authentication system

## EXAMPLES
- Authentication flow: `examples/auth-flow.js`
- Similar API endpoint: `src/api/users.js` 
- Database schema pattern: `src/models/base-model.js`
- Validation approach: `src/validators/user-validator.js`

## DOCUMENTATION
- JWT library docs: https://github.com/auth0/node-jsonwebtoken
- Our API standards: `docs/api-guidelines.md`

## OTHER CONSIDERATIONS
- Use existing error handling patterns
- Follow our standard response format
- Include rate limiting
```

### Critical PRP Strategies

**Examples**: The most powerful tool - provide code snippets, similar features, and patterns to follow

**Validation Gates**: Ensure comprehensive testing and iteration until all tests pass

**No Vibe Coding**: Validate PRPs before executing them and the code after execution!

The more specific examples you provide, the better Claude can match your existing patterns and style.

*Note: Context engineering works with any AI coding assistant - the PRP framework and example-driven approach are universal principles.*

---

## ✅ TIP 6: LEVERAGE SUBAGENTS FOR SPECIALIZED TASKS

Subagents are specialized AI assistants that operate in separate context windows with focused expertise. They enable Claude to delegate specific tasks to experts, improving quality and efficiency.

### Understanding Subagents

Each subagent:
- Has its own context window (no pollution from main conversation)
- Operates with specialized system prompts
- Can be limited to specific tools
- Works autonomously on delegated tasks

### Example Subagents in This Repository

**Documentation Manager** (`.claude/agents/documentation-manager.md`):
- Automatically updates docs when code changes
- Ensures README accuracy
- Maintains API documentation
- Creates migration guides

**Validation Gates** (`.claude/agents/validation-gates.md`):
- Runs all tests after changes
- Iterates on fixes until tests pass
- Enforces code quality standards
- Never marks tasks complete with failing tests

### Creating Your Own Subagents

1. Use the `/agents` command or create a file in `.claude/agents/`:

```markdown
---
name: security-auditor
description: "Security specialist. Proactively reviews code for vulnerabilities and suggests improvements."
tools: Read, Grep, Glob
---

You are a security auditing specialist focused on identifying and preventing security vulnerabilities...

## Core Responsibilities
1. Review code for OWASP Top 10 vulnerabilities
2. Check for exposed secrets or credentials
3. Validate input sanitization
4. Ensure proper authentication/authorization
...
```

### Subagent Best Practices

**1. Focused Expertise**: Each subagent should have one clear specialty

**2. Proactive Descriptions**: Use "proactively" in descriptions for automatic invocation:
```yaml
description: "Code reviewer. Proactively reviews all code changes for quality."
```

**3. Tool Limitations**: Only give subagents the tools they need:
```yaml
tools: Read, Grep  # No write access for review-only agents
```

**4. Information Flow Design**: Understand how information flows from primary agent → subagent → primary agent. The subagent description is crucial because it tells your primary Claude Code agent when and how to use it. Include clear instructions in the description for how the primary agent should prompt this subagent.

**5. One-Shot Context**: Subagents don't have full conversation history - they receive a single prompt from your primary agent. Design your subagents with this limitation in mind.

Learn more in the [Subagents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents).

*Note: While other AI assistants don't have formal subagents, you can achieve similar results by creating specialized prompts and switching between different conversation contexts.*

---

## ✅ TIP 7: AUTOMATE WITH HOOKS

Hooks provide deterministic control over Claude Code's behavior through user-defined shell commands that execute at predefined lifecycle events.

### Available Hook Events

Claude Code provides several predefined actions you can hook into:
- **PreToolUse**: Before tool execution (can block operations)
- **PostToolUse**: After successful tool completion  
- **UserPromptSubmit**: When user submits a prompt
- **SubagentStop**: When a subagent completes its task
- **Stop**: When the main agent finishes responding
- **SessionStart**: At session initialization
- **PreCompact**: Before context compaction
- **Notification**: During system notifications

Learn more in the [Hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks).

### Example Hook: Tool Usage Logging

This repository includes a simple hook example in `.claude/hooks/`:

**log-tool-usage.sh** - Logs all tool usage for tracking and debugging:
```bash
#!/bin/bash
# Logs tool usage with timestamps
# Creates .claude/logs/tool-usage.log
# No external dependencies required
```

### Setting Up Hooks

1. **Create hook script** in `.claude/hooks/`
2. **Make it executable**: `chmod +x your-hook.sh`
3. **Add to settings** in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/log-tool-usage.sh"
          }
        ]
      }
    ]
  }
}
```

Hooks ensure certain actions always happen, rather than relying on the AI to remember - perfect for logging, security validations, and build triggers.

*Note: Other AI assistants don't have hooks (though Kiro does!), I can almost guarantee they're coming soon for everyone else.*

---

## ✅ TIP 8: GITHUB CLI INTEGRATION

Set up the GitHub CLI to enable Claude to interact with GitHub for issues, pull requests, and repository management.

```bash
# Install GitHub CLI
# Visit: https://github.com/cli/cli#installation

# Authenticate
gh auth login

# Verify setup
gh repo list
```

### Custom GitHub Commands

Use the `/fix-github-issue` command for automated fixes:

```
/fix-github-issue 123
```

This will:
1. Fetch issue details
2. Analyze the problem
3. Search relevant code
4. Implement the fix
5. Run tests
6. Create a PR

*Note: GitHub CLI works with any AI coding assistant - just install it and the AI can use `gh` commands to interact with your repositories.*

---

## ✅ TIP 9: SAFE YOLO MODE WITH DEV CONTAINERS

Allow Claude Code to perform any action while maintaining safety through containerization. This enables rapid development without destructive behavior on your host machine.

**Prerequisites:**
- Install [Docker](https://www.docker.com/) 
- VS Code (or compatible editors)

**Security Features:**
- Network isolation with whitelist
- No access to host filesystem
- Restricted outbound connections
- Safe experimentation environment

**Setup Process:**

1. **Open in VS Code** and press `F1`
2. **Select** "Dev Containers: Reopen in Container"
3. **Wait** for container build
4. **Open terminal** (`Ctrl+J`)
5. **Authenticate** Claude Code in container
6. **Run in YOLO mode**:
   ```bash
   claude --dangerously-skip-permissions
   ```

**Why Use Dev Containers?**
- Test dangerous operations safely
- Experiment with system changes
- Rapid prototyping
- Consistent development environment
- No fear of breaking your system

---

## ✅ TIP 10: PARALLEL DEVELOPMENT WITH GIT WORKTREES

Use Git worktrees to enable multiple Claude instances working on independent tasks simultaneously, or automate parallel implementations of the same feature.

### Manual Worktree Setup

```bash
# Create worktrees for different features
git worktree add ../project-auth feature/auth
git worktree add ../project-api feature/api

# Launch Claude in each worktree
cd ../project-auth && claude  # Terminal 1
cd ../project-api && claude   # Terminal 2
```

### Automated Parallel Agents

AI coding assistants are non-deterministic. Running multiple attempts increases success probability and provides implementation options.

**Setup parallel worktrees:**
```bash
/prep-parallel user-system 3
```

**Execute parallel implementations:**
1. Create a plan file (`plan.md`)
2. Run parallel execution:

```bash
/execute-parallel user-system plan.md 3
```

**Select the best implementation:**
```bash
# Review results
cat trees/user-system-*/RESULTS.md

# Test each implementation
cd trees/user-system-1 && npm test

# Merge the best
git checkout main
git merge user-system-2
```

### Benefits

- **No Conflicts**: Each instance works in isolation
- **Multiple Approaches**: Compare different implementations
- **Quality Gates**: Only consider implementations where tests pass
- **Easy Integration**: Merge the best solution

---

## 🎯 Quick Command Reference

| Command | Purpose |
|---------|---------|
| `/init` | Generate initial CLAUDE.md |
| `/permissions` | Manage tool permissions |
| `/clear` | Clear context between tasks |
| `/agents` | Create and manage subagents |
| `/primer` | Analyze repository structure |
| `ESC` | Interrupt Claude |
| `Shift+Tab` | Enter planning mode |
| `/generate-prp INITIAL.md` | Create implementation blueprint |
| `/execute-prp PRPs/feature.md` | Implement from blueprint |
| `/prep-parallel [feature] [count]` | Setup parallel worktrees |
| `/execute-parallel [feature] [plan] [count]` | Run parallel implementations |
| `/fix-github-issue [number]` | Auto-fix GitHub issues |
| `/prep-parallel [feature] [count]` | Setup parallel worktrees |
| `/execute-parallel [feature] [plan] [count]` | Run parallel implementations |

---

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [MCP Server Library](https://github.com/modelcontextprotocol)

---

## 🚀 Next Steps

1. **Start Simple**: Set up CLAUDE.md and basic permissions
2. **Add Slash Commands**: Create custom commands for your workflow
3. **Install MCP Servers**: Add Serena for enhanced coding capabilities
4. **Implement Subagents**: Add specialists for your tech stack
5. **Configure Hooks**: Automate repetitive tasks
6. **Try Parallel Development**: Experiment with multiple approaches

Remember: Claude Code is most powerful when you provide clear context, specific examples, and comprehensive validation. Happy coding! 🎉