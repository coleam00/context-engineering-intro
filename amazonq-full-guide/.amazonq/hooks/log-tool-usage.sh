#!/bin/bash
# PostToolUse hook: Log all tool usage for tracking and debugging
# This hook runs after any tool execution to maintain an audit log

timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Create logs directory if it doesn't exist
mkdir -p .claude/logs

# Log the tool usage
echo "[$timestamp] Claude made an edit " >> .claude/logs/tool-usage.log

# Always return success to avoid blocking tools
echo "{}"