---
description: Generate comprehensive validation command for this codebase
---

# Generate Ultimate Validation Command

Analyze this codebase deeply and create `.claude/commands/validate.md` that comprehensively validates everything.

## Step 0: Discover Real User Workflows

**Before analyzing tooling, understand what users ACTUALLY do:**

1. Read workflow documentation:
   - README.md - Look for "Usage", "Quickstart", "Examples" sections
   - CLAUDE.md/AGENTS.md or similar - Look for workflow patterns
   - docs/ folder - User guides, tutorials

2. Identify external integrations:
   - What CLIs does the app use? (Check Dockerfile for installed tools)
   - What external APIs does it call? (Telegram, Slack, GitHub, etc.)
   - What services does it interact with?

3. Extract complete user journeys from docs:
   - Find examples like "Fix Issue (GitHub):" or "User does X → then Y → then Z"
   - Each workflow becomes an E2E test scenario

**Critical: Your E2E tests should mirror actual workflows from docs, not just test internal APIs.**

## Step 1: Deep Codebase Analysis

Explore the codebase to understand:

**What validation tools already exist:**
- Linting config: `.eslintrc*`, `.pylintrc`, `ruff.toml`, etc.
- Type checking: `tsconfig.json`, `mypy.ini`, etc.
- Style/formatting: `.prettierrc*`, `black`, `.editorconfig`
- Unit tests: `jest.config.*`, `pytest.ini`, test directories
- Package manager scripts: `package.json` scripts, `Makefile`, `pyproject.toml` tools

**What the application does:**
- Frontend: Routes, pages, components, user flows
- Backend: API endpoints, authentication, database operations
- Database: Schema, migrations, models
- Infrastructure: Docker services, dependencies

**How things are currently tested:**
- Existing test files and patterns
- CI/CD workflows (`.github/workflows/`, etc.)
- Test commands in package.json or scripts

## Step 2: Generate validate.md

Create `.claude/commands/validate.md` with these phases (ONLY include phases that exist in the codebase):

### Phase 1: Linting
Run the actual linter commands found in the project (e.g., `npm run lint`, `ruff check`, etc.)

### Phase 2: Type Checking
Run the actual type checker commands found (e.g., `tsc --noEmit`, `mypy .`, etc.)

### Phase 3: Style Checking
Run the actual formatter check commands found (e.g., `prettier --check`, `black --check`, etc.)

### Phase 4: Unit Testing
Run the actual test commands found (e.g., `npm test`, `pytest`, etc.)

### Phase 5: End-to-End Testing (BE CREATIVE AND COMPREHENSIVE)

Test COMPLETE user workflows from documentation, not just internal APIs.

**The Three Levels of E2E Testing:**

1. **Internal APIs** (what you might naturally test):
   - Test adapter endpoints work
   - Database queries succeed
   - Commands execute

2. **External Integrations** (what you MUST test):
   - CLI operations (GitHub CLI create issue/PR, etc.)
   - Platform APIs (send Telegram message, post Slack message)
   - Any external services the app depends on

3. **Complete User Journeys** (what gives 100% confidence):
   - Follow workflows from docs start-to-finish
   - Example: "User asks bot to fix GitHub issue" → Bot clones repo → Makes changes → Creates PR → Comments on issue
   - Test like a user would actually use the application in production

**Examples of good vs. bad E2E tests:**
- ❌ Bad: Tests that `/clone` command stores data in database
- ✅ Good: Clone repo → Load commands → Execute command → Verify git commit created
- ✅ Great: Create GitHub issue → Bot receives webhook → Analyzes issue → Creates PR → Comments on issue with PR link

**Approach:**
- Use Docker for isolated, reproducible testing
- Create test data/repos/issues as needed
- Verify outcomes in external systems (GitHub, database, file system)
- Clean up after tests

## Critical: Don't Stop Until Everything is Validated

**Your job is to create a validation command that leaves NO STONE UNTURNED.**

- Every user workflow from docs should be tested end-to-end
- Every external integration should be exercised (GitHub CLI, APIs, etc.)
- Every API endpoint should be hit
- Every error case should be verified
- Database integrity should be confirmed
- The validation should be so thorough that manual testing is completely unnecessary

If /validate passes, the user should have 100% confidence their application works correctly in production. Don't settle for partial coverage - make it comprehensive, creative, and complete.

## Output

Write the generated validation command to `.claude/commands/validate.md`

The command should be executable, practical, and give complete confidence in the codebase.
