---
paths:
  - "packages/cli/**/*.ts"
---

# CLI Conventions

## Commands

```bash
# Workflow commands (require git repo)
bun run cli workflow list [--json]
bun run cli workflow run <name> [message] [--branch <branch>] [--from-branch <base>] [--no-worktree] [--resume]
bun run cli workflow status [runId]

# Isolation commands
bun run cli isolation list
bun run cli isolation cleanup [days]           # default: 7 days
bun run cli isolation cleanup --merged         # removes merged branches + remote refs
bun run cli complete <branch-name> [--force]   # full lifecycle: worktree + local/remote branches

# Interactive
bun run cli chat [--cwd <path>]

# Setup
bun run cli setup
bun run cli version
```

## Startup Behavior

1. Deletes `process.env.DATABASE_URL` (prevent target repo's DB from leaking in)
2. Loads `~/.archon/.env` with `override: true`
3. Smart Claude auth default: if no `CLAUDE_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`, sets `CLAUDE_USE_GLOBAL_AUTH=true`
4. Imports all commands AFTER dotenv setup

## WorkflowRunOptions Discriminated Union

```typescript
type WorkflowRunOptions =
  | { branchName?: undefined; noWorktree?: undefined; resume?: boolean }  // No isolation
  | { branchName: string; fromBranch?: string; noWorktree?: boolean; resume?: undefined }; // With branch
```

- `--branch feature-auth` → creates/reuses worktree for that branch
- `--no-worktree` → checks out branch directly without worktree (only with `--branch`)
- `--resume` → resumes last run for this conversation (mutually exclusive with `--branch`)

## Git Repo Requirement

Workflow and isolation commands resolve CWD to the git repo root. Run from within a git repository (subdirectories work). The CLI calls `git rev-parse --show-toplevel` to find the root.

## Conversation ID Format

CLI generates: `cli-{timestamp}-{random6}` (e.g., `cli-1703123456789-a7f3bc`)

## Port Allocation

Worktree-aware: same hash-based algorithm as server (3190–4089 range). Running `bun dev` in a worktree auto-allocates a unique port. Same worktree always gets same port.

## CLIAdapter

The `CLIAdapter` implements `IPlatformAdapter`. It streams output to stdout. `getStreamingMode()` defaults to `'batch'` (configurable via constructor options). No auth needed — CLI is local only.

## Architecture

- `@archon/cli` depends on `@archon/core`, `@archon/workflows`, `@archon/git`, `@archon/isolation`, `@archon/paths`
- Uses `createWorkflowDeps()` from `@archon/core/workflows/store-adapter` to build workflow deps
- Database shared with server (same `~/.archon/archon.db` or `DATABASE_URL`)
- Conversation lifecycle: create → run workflow → persist messages (same DB as web UI)

## Anti-patterns

- Never run CLI commands without being inside a git repository (workflow/isolation commands will fail)
- Never set `DATABASE_URL` in `~/.archon/.env` to point at a target app's database
- Never use `--force` on `complete` unless branch is truly safe to delete (skips uncommitted check)
- Never add interactive prompts inside CLI commands — use flags for all options (non-interactive tool)
