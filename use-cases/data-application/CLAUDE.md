# Data Application Factory - Adaptive Hybrid Orchestration

## Overview

This factory creates data-driven applications using an **adaptive hybrid approach** that automatically scales complexity based on requirements:

- **Tier 1 (Simple CRUD)**: Slash commands + Main Claude (30-45 min)
- **Tier 2 (Standard REST API)**: Slash commands + Main Claude + 1 validation agent (60-90 min)
- **Tier 3 (Enterprise)**: Slash commands + 3 parallel design agents + Main Claude + 2 validation agents (90-120 min)

## Workflow Trigger

When a user request matches ANY of these patterns, activate the data application factory:

**Primary Triggers:**
- "Build a data application..."
- "Create a data-driven system..."
- "Build a database application with API..."
- "Create an application that stores and serves data..."
- "I need data persistence..."
- "Build a [system] with database and API..."
- Any request mentioning **database/data/persistence + application/system/service**

**Action:** Immediately invoke: `/data-app-init`

## Three-Phase Workflow

### Phase 1: Initialization (`/data-app-init`)

**What it does:**
1. Asks 5 targeted questions to understand requirements
2. Calculates complexity tier based on answers
3. Loads appropriate context modules
4. Creates project structure
5. Explains next steps to user

**Tier Detection Logic:**
```
Score = 0
+ Entity count (>10: +3, >5: +1)
+ Integrations (>5: +3, >2: +1)
+ Scale (enterprise: +2, medium: +1)
+ Compliance requirements (+2)
+ Multi-region (+1)
+ Real-time features (+1)

If score >= 7: Tier 3 (Enterprise)
If score >= 3: Tier 2 (Standard)
Else: Tier 1 (Simple)
```

**Context Loading:**
- **Tier 1**: core-principles + tier1 + database + tech-stack
- **Tier 2**: core-principles + tier2 + database + api + security + testing + tech-stack
- **Tier 3**: core-principles + tier3 + all modules + tech-stack

### Phase 2: Planning (`/data-app-plan`)

**Tier 1 Approach:**
- Main Claude creates lightweight plan directly
- Research similar patterns
- Design schema and API
- Save to `PLAN.md`
- Duration: 10 minutes

**Tier 2 Approach:**
- Main Claude creates enhanced plan
- Research patterns and integrations
- Design database, API, caching, integrations
- Save to `PLAN.md`
- Duration: 15-20 minutes

**Tier 3 Approach:**
- Main Claude creates comprehensive `INITIAL.md`
- **Invoke 3 parallel agents** (single message, 3 Task tool calls):
  1. `data-persistence-architect` → persistence_architecture.md
  2. `data-api-integration-specialist` → api-integration.md
  3. `data-platform-deployment-engineer` → platform-operations.md
- Wait for all agents to complete
- Synthesize results
- Duration: 30-40 minutes

**Archon Integration (Tier 3 only):**
- Check `mcp__archon__health_check`
- If available: Create project, track tasks
- If not: Use TodoWrite for local tracking

### Phase 3: Implementation & Validation

**Implementation (Main Claude):**
- Read all planning documents
- Implement based on tier requirements
- For Tier 1: Simple CRUD + basic tests
- For Tier 2: Full REST API + auth + integrations + tests
- For Tier 3: Enterprise application + all features

**Validation (`/data-app-exec`):**
- **Tier 1**: Inline validation (tests, Docker, health checks)
- **Tier 2**: Invoke `integration-validator` agent for comprehensive testing
- **Tier 3**: Invoke `integration-validator` + `performance-tester` agents in parallel

## Specialized Agents

**Design Agents (Tier 3 only):**
- `data-persistence-architect` - Database, caching, performance
- `data-api-integration-specialist` - APIs, integrations, messaging
- `data-platform-deployment-engineer` - Docker, K8s, monitoring

**Validation Agents:**
- `integration-validator` - Integration tests, security scans (Tier 2 & 3)
- `performance-tester` - Load testing, performance validation (Tier 3 optional)

**CRITICAL: Always invoke parallel agents in a SINGLE message with multiple Task tool calls.**

## Context Structure

All context is modular and composable:

```
context/
├── core-principles.md          # Universal rules (all tiers)
├── tier1-simple-crud.md        # Simple CRUD patterns
├── tier2-standard-app.md       # Standard REST API patterns
├── tier3-enterprise.md         # Enterprise patterns
├── modules/                    # Mix-and-match modules
│   ├── database-patterns.md
│   ├── api-patterns.md
│   ├── security-patterns.md
│   ├── testing-patterns.md
│   └── deployment-patterns.md
└── tech-stacks/                # Technology-specific guides
    ├── java-spring.md
    ├── nodejs-express.md
    ├── python-fastapi.md
    └── dotnet-aspnet.md
```

## Quick Reference

| Aspect | Tier 1 | Tier 2 | Tier 3 |
|--------|--------|--------|--------|
| **Entities** | 1-5 | 5-10 | 10+ |
| **Integrations** | 0-1 | 1-3 | 5+ |
| **Time** | 30-45 min | 60-90 min | 90-120 min |
| **Agents** | 0 | 1 (validation) | 5-6 (3 design + 2 validation) |
| **Orchestration** | Slash commands | Slash commands | Slash commands + agents |
| **Implementation** | Main Claude | Main Claude | Main Claude |
| **Features** | CRUD, tests | + Auth, cache, integrations | + Message queues, monitoring, K8s |

## User Experience

**Simple Request:**
```
User: "Build a TODO API"
→ /data-app-init detects Tier 1
→ /data-app-plan creates simple plan (10 min)
→ Main Claude implements (20 min)
→ /data-app-exec validates inline (5 min)
✅ Done in 35 minutes
```

**Standard Request:**
```
User: "Build an e-commerce API with Stripe integration"
→ /data-app-init detects Tier 2
→ /data-app-plan creates enhanced plan (15 min)
→ Main Claude implements with auth and integrations (45 min)
→ /data-app-exec validates with agent (15 min)
✅ Done in 75 minutes
```

**Enterprise Request:**
```
User: "Build a POS system with ERP integration and fiscal compliance"
→ /data-app-init detects Tier 3
→ /data-app-plan invokes 3 parallel design agents (35 min)
→ Main Claude implements enterprise features (60 min)
→ /data-app-exec validates with 2 agents (25 min)
✅ Done in 120 minutes
```

## Key Principles

1. **User stays in control** - Slash commands provide visibility and checkpoints
2. **Main Claude implements** - Keeps context continuity
3. **Agents for specialized tasks** - Long-running, isolated work
4. **Progressive complexity** - Start simple, add only what's needed
5. **Modular context** - Load only what you need
6. **Parallel execution** - Multiple agents work simultaneously (Tier 3)

## Migration from Old System

**Old system (all requests):**
- Always used 5+ agents
- Always took 90+ minutes
- Always enterprise complexity
- 696-line monolithic CLAUDE.md

**New system (adaptive):**
- 0-6 agents based on need
- 30-120 minutes based on complexity
- Complexity matches requirements
- 150-line orchestration + modular context

## Success Criteria

**All Tiers:**
- Tests pass (>80% coverage)
- Docker works
- README complete
- No hardcoded secrets

**Tier 2+:**
- Security scan clean
- Integration tests pass
- API documented

**Tier 3:**
- Load tests pass
- All integrations tested
- Monitoring configured
- K8s manifests ready

## Commands

- **`/data-app-init`** - Initialize and determine tier
- **`/data-app-plan`** - Create implementation plan
- **`/data-app-exec`** - Validate and test

Start every data application request with `/data-app-init`.
