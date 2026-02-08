# Build with Agent Team

A Claude Code skill for building projects using [Agent Teams](https://www.anthropic.com/news/claude-opus-4-6) — Anthropic's multi-agent collaboration feature where multiple Claude instances work in parallel, communicate with each other, and coordinate autonomously. Give it a plan document describing what you want to build, and it spawns a team of specialized agents in tmux split panes to build it together.

Once set up, it's as simple as:

```bash
/build-with-agent-team [plan-path] [num-agents]
```

## Prerequisites

### 1. Install tmux

Agent teams use tmux for split-pane visualization so you can see all agents working simultaneously.

**macOS:**
```bash
brew install tmux
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install tmux
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install tmux
```

**Windows (WSL required):**

Agent teams require WSL (Windows Subsystem for Linux). Native Windows is not supported.

```powershell
# 1. Install WSL from PowerShell (Admin)
wsl --install

# 2. Restart your computer

# 3. Open WSL and install tmux
sudo apt update && sudo apt install tmux
```

Verify installation:
```bash
tmux -V
```

### 2. Enable Agent Teams

Agent teams are experimental and disabled by default. Enable by adding to `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or export in your shell profile (`~/.bashrc` or `~/.zshrc`):
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

## Installation

Copy the skill to your personal skills directory:

```bash
cp -r build-with-agent-team ~/.claude/skills/
```

Or for project-level use:
```bash
cp -r build-with-agent-team .claude/skills/
```

## Create Your Plan

Write a markdown document describing what you want to build. This works for:

- **Greenfield projects**: A new app, API, or system from scratch
- **Brownfield features**: A new feature in an existing codebase

Your plan should be detailed enough that multiple agents could divide the work. Include:

- What you're building and why
- Tech stack and architecture
- Project structure
- Key components and how they interact
- Data models or API contracts
- Acceptance criteria

See `example-plan/session-manager-plan.md` for an example.

## Usage

```bash
/build-with-agent-team [plan-path] [num-agents]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `plan-path` | Yes | Path to your plan markdown file |
| `num-agents` | No | Number of agents to spawn. If omitted, determined automatically based on the plan's complexity |

**Examples:**

```bash
# Let the skill determine team size
/build-with-agent-team ./plans/my-project.md

# Specify 3 agents
/build-with-agent-team ./plans/my-project.md 3

# Build a feature in existing codebase
/build-with-agent-team ./docs/new-auth-feature.md 2
```

The skill will:
1. Read your plan
2. Analyze it to determine agent roles (frontend, backend, database, etc.)
3. Spawn agents in tmux split panes
4. Coordinate collaboration between agents
5. Ensure agents communicate and challenge each other's work

## Agent Teams vs Subagents

Claude Code has two ways to parallelize work. Choose based on whether your workers need to communicate:

| | Subagents | Agent Teams |
|---|-----------|-------------|
| **Context** | Runs within main session | Each agent has its own session |
| **Communication** | Reports back to main agent only | Agents message each other directly |
| **Coordination** | Main agent manages all work | Shared task list, self-coordination |
| **Visibility** | Results summarized to main context | Each agent visible in tmux pane |
| **Best for** | Quick, focused tasks (research, exploration) | Complex builds requiring collaboration |
| **Token cost** | Lower (results summarized) | Higher (each agent is a separate instance) |

**Use subagents when:**
- Task is quick and isolated
- You only need the result, not the process
- Cost-sensitive

**Use agent teams when:**
- Multiple components need to integrate (frontend + backend + database)
- Agents need to agree on interfaces and contracts
- You want to see parallel progress in real-time
- Building something complex enough to warrant coordination overhead
