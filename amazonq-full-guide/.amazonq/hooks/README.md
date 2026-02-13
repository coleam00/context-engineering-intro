# Claude Code Hooks Examples

This directory contains example hooks for Claude Code that demonstrate how to add deterministic behavior to your AI coding workflow.

## What are Hooks?

Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. They provide control over Claude's behavior, ensuring certain actions always happen rather than relying on the AI to choose to run them.

## Files in this Directory

1. **format-after-edit.sh** - A PostToolUse hook that automatically formats code after file edits
2. **example-hook-config.json** - Example configuration showing how to set up various hooks

## How to Use These Hooks

### Option 1: Copy to Your Settings File

Copy the hooks configuration from `example-hook-config.json` to your Claude Code settings:

**Project-specific** (`.claude/settings.json`):
```bash
# Create settings file if it doesn't exist
touch .claude/settings.json

# Add hooks configuration from example-hook-config.json
```

**User-wide** (`~/.claude/settings.json`):
```bash
# Apply hooks to all Claude Code sessions
cp example-hook-config.json ~/.claude/settings.json
```

### Option 2: Use Individual Hooks

1. Copy the hook script to your project:
```bash
cp format-after-edit.sh /your/project/.claude/hooks/
chmod +x /your/project/.claude/hooks/format-after-edit.sh
```

2. Add to your settings.json:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format-after-edit.sh"
          }
        ]
      }
    ]
  }
}
```

## Available Hook Events

- **PreToolUse**: Before tool execution (can block tools)
- **PostToolUse**: After successful tool completion
- **UserPromptSubmit**: When user submits a prompt
- **SubagentStop**: When a subagent completes
- **Stop**: When main agent finishes responding
- **Notification**: During system notifications
- **PreCompact**: Before context compaction
- **SessionStart**: At session initialization

## Creating Your Own Hooks

1. Write a shell script that:
   - Reads JSON input from stdin
   - Processes the input
   - Returns JSON output (empty `{}` for success)
   - Can return `{"action": "block", "message": "reason"}` to block operations

2. Make it executable:
```bash
chmod +x your-hook.sh
```

3. Add to settings.json with appropriate matcher and event

## Security Considerations

- Hooks execute arbitrary shell commands
- Always validate and sanitize inputs
- Use full paths to avoid PATH manipulation
- Be careful with file operations
- Test hooks thoroughly before deployment

## Debugging Hooks

Run Claude Code with debug flag to see hook execution:
```bash
claude --debug
```

This will show:
- Which hooks are triggered
- Input/output for each hook
- Any errors or issues

## Integration with Subagents

The example configuration includes a hook that integrates with the validation-gates subagent, demonstrating how hooks and subagents can work together for a more robust development workflow.