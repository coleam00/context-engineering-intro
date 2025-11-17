# Data Application Initialization

Initialize a new data-driven application by gathering requirements and determining the appropriate complexity tier.

## Step 1: Acknowledge Request

Confirm you're starting the data application factory workflow.

## Step 2: Ask Tier Detection Questions

Ask these questions to determine complexity tier:

1. **Entities & Relationships**
   "How many main entities (data models) will your application have? (e.g., users, products, orders)"

2. **External Integrations**
   "Will you need to integrate with external systems? If yes, which ones? (e.g., payment gateways, ERPs, email services, etc.)"

3. **Scale & Complexity**
   "What's the expected scale? (small team project, medium business app, or large enterprise system)"

4. **Special Requirements**
   "Do you have any special requirements? (regulatory compliance, multi-region, real-time features, etc.)"

5. **Technology Preference**
   "Do you have a technology stack preference? (Java/Spring Boot, Node.js/Express, Python/FastAPI, .NET)"

## Step 3: Determine Tier

Based on answers, calculate tier:

```typescript
function determineTier(answers: Answers): Tier {
    let score = 0;

    // Entity count
    if (answers.entities > 10) score += 3;
    else if (answers.entities > 5) score += 1;

    // External integrations
    if (answers.integrations > 5) score += 3;
    else if (answers.integrations > 2) score += 1;

    // Scale
    if (answers.scale === 'enterprise') score += 2;
    else if (answers.scale === 'medium') score += 1;

    // Special requirements
    if (answers.hasCompliance) score += 2;
    if (answers.hasMultiRegion) score += 1;
    if (answers.hasRealTime) score += 1;

    // Determine tier
    if (score >= 7) return 'tier3-enterprise';
    if (score >= 3) return 'tier2-standard';
    return 'tier1-simple';
}
```

## Step 4: Load Appropriate Context

Based on tier, internally load context files (don't show this to user):

**Tier 1 (Simple CRUD):**
```
- context/core-principles.md
- context/tier1-simple-crud.md
- context/modules/database-patterns.md
- context/tech-stacks/{selected_stack}.md
```

**Tier 2 (Standard REST API):**
```
- context/core-principles.md
- context/tier2-standard-app.md
- context/modules/database-patterns.md
- context/modules/api-patterns.md
- context/modules/security-patterns.md
- context/modules/testing-patterns.md
- context/tech-stacks/{selected_stack}.md
```

**Tier 3 (Enterprise Application):**
```
- context/core-principles.md
- context/tier3-enterprise.md
- context/modules/database-patterns.md
- context/modules/api-patterns.md
- context/modules/security-patterns.md
- context/modules/testing-patterns.md
- context/modules/deployment-patterns.md
- context/tech-stacks/{selected_stack}.md
```

## Step 5: Create Project Structure

Determine project folder name (snake_case based on user's description):
```
applications/{project_name}/
```

Create initial directory structure based on tier:

**Tier 1:**
```bash
mkdir -p applications/{project_name}/{src,tests,docs}
```

**Tier 2:**
```bash
mkdir -p applications/{project_name}/{src,tests,deployment,docs}
```

**Tier 3:**
```bash
mkdir -p applications/{project_name}/{src,tests,deployment,docs/api,docs/integration}
mkdir -p applications/{project_name}/planning
```

## Step 6: Check for Archon (Tier 3 only)

For Tier 3, check if Archon is available:
```
Try running mcp__archon__health_check
If available: Create Archon project for tracking
If not available: Use TodoWrite for local tracking
```

## Step 7: Explain Next Steps

Tell the user:

**For Tier 1:**
```
✅ Tier 1 (Simple CRUD) detected
📁 Project structure created at: applications/{project_name}/
🎯 Estimated time: 30-45 minutes

Next steps:
1. Run: /data-app-plan to design your schema and API
2. Then I'll implement everything
3. Run: /data-app-exec to validate and test

Ready to proceed with planning?
```

**For Tier 2:**
```
✅ Tier 2 (Standard REST API) detected
📁 Project structure created at: applications/{project_name}/
🎯 Estimated time: 60-90 minutes

Features: Authentication, caching, external integrations, comprehensive testing

Next steps:
1. Run: /data-app-plan to design architecture
2. Then I'll implement everything
3. Run: /data-app-exec to validate with integration tests

Ready to proceed with planning?
```

**For Tier 3:**
```
✅ Tier 3 (Enterprise Application) detected
📁 Project structure created at: applications/{project_name}/
🎯 Estimated time: 90-120 minutes

This will use parallel architecture agents for:
- Data persistence architecture
- API & integration design
- Platform & deployment configuration

Next steps:
1. Run: /data-app-plan to create comprehensive design
   (This will invoke 3 parallel agents for architecture)
2. Then I'll implement the full application
3. Run: /data-app-exec to run comprehensive validation

Ready to proceed with planning?
```

## Important Notes

- **DO NOT** invoke any agents yet - that happens in /data-app-plan
- **DO NOT** start implementation - that happens after planning
- **WAIT** for user confirmation before proceeding
- Store the tier determination and answers for use by /data-app-plan
