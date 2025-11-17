# Data Application Planning

Create a comprehensive implementation plan based on the tier determined in /data-app-init.

## Prerequisites

- User must have run /data-app-init first
- Project folder must exist
- Tier and requirements must be determined

## Planning Workflow by Tier

### Tier 1: Simple CRUD (Direct Planning)

**Duration: 10 minutes**

1. **Read context files loaded in init**

2. **Research similar patterns**
   - Search codebase for similar implementations (if any)
   - Review the tech stack guide for the selected technology

3. **Design schema**
   - Create simple entity definitions (2-5 entities)
   - Define relationships
   - Plan indexes

4. **Design API endpoints**
   - List CRUD endpoints for each entity
   - Define request/response formats
   - Plan pagination

5. **Create lightweight plan**
   - Save to: `applications/{project_name}/PLAN.md`
   - Include:
     - Database schema
     - API endpoints list
     - Technology stack
     - Testing approach
     - Success criteria

6. **Output to user:**
```
📋 Planning Complete (Tier 1)

Schema: {X} entities with relationships
API: {Y} endpoints
Stack: {selected_stack}

Plan saved to: applications/{project_name}/PLAN.md

Ready to implement? I'll now create:
- Database models and migrations
- CRUD operations
- REST API endpoints
- Basic tests
- Docker setup

Shall I proceed with implementation?
```

---

### Tier 2: Standard REST API (Enhanced Planning)

**Duration: 15-20 minutes**

1. **Read context files loaded in init**

2. **Research & Documentation**
   - Search codebase for authentication patterns
   - Research external API integration examples
   - Review caching strategies

3. **Design database architecture**
   - Entity models with validation
   - Relationships and constraints
   - Indexing strategy
   - Migration plan

4. **Design API architecture**
   - REST endpoint design with versioning
   - Authentication & authorization strategy
   - Input validation approach
   - Error handling pattern
   - Rate limiting strategy

5. **Plan external integrations**
   - List each external system
   - Define adapter pattern for each
   - Plan retry and circuit breaker logic

6. **Plan caching strategy**
   - Identify what to cache
   - Define cache layers (in-memory, Redis)
   - Cache invalidation strategy

7. **Create comprehensive plan**
   - Save to: `applications/{project_name}/PLAN.md`
   - Include:
     - Full database schema
     - API endpoint documentation
     - Authentication flow
     - External integrations design
     - Caching architecture
     - Testing strategy
     - Deployment approach

8. **Output to user:**
```
📋 Planning Complete (Tier 2)

Database: {X} entities with {Y} relationships
API: {Z} endpoints with auth
Integrations: {external systems list}
Caching: Redis with {strategy}

Plan saved to: applications/{project_name}/PLAN.md

Ready to implement? I'll create:
- Complete database schema with migrations
- Repository pattern for data access
- Business services with validation
- REST API with authentication
- External integration adapters
- Redis caching layer
- Comprehensive tests
- Docker compose setup

Estimated implementation time: 40-50 minutes

Shall I proceed with implementation?
```

---

### Tier 3: Enterprise Application (Parallel Agent Planning)

**Duration: 30-40 minutes**

1. **Read context files loaded in init**

2. **Create comprehensive requirements document**
   - Save to: `applications/{project_name}/planning/INITIAL.md`
   - Follow PRP template structure from `PRPs/templates/prp_data_application_base.md`
   - Include:
     - Complete application scope
     - Functional requirements
     - Technical requirements
     - External dependencies
     - Success criteria
     - Compliance requirements

3. **Update Archon (if available)**
   - Mark Task 1 "Requirements Analysis" as "doing"
   - Add notes about project scope

4. **Invoke 3 Parallel Architecture Agents**

   **CRITICAL: Use parallel tool invocation - single message with 3 Task tool uses**

   **Agent 1: data-persistence-architect**
   ```
   Prompt: "Design comprehensive data persistence architecture for {project_name}.

   Context:
   - Project folder: applications/{project_name}
   - Requirements: {summary from INITIAL.md}
   - Expected entities: {X}
   - Expected scale: {Y}

   Create detailed architecture covering:
   - Database schema design with ERDs
   - Multi-layer caching strategies (L1: in-memory, L2: Redis)
   - Query optimization and indexing
   - Connection pooling configuration
   - Read replicas and partitioning for scale
   - Database security and backup strategies
   - Migration framework setup

   Output to: applications/{project_name}/planning/persistence_architecture.md

   Use context from:
   - context/modules/database-patterns.md
   - context/tech-stacks/{stack}.md"
   ```

   **Agent 2: data-api-integration-specialist**
   ```
   Prompt: "Design API and integration architecture for {project_name}.

   Context:
   - Project folder: applications/{project_name}
   - Requirements: {summary from INITIAL.md}
   - External systems: {list}

   Create detailed architecture covering:
   - REST API endpoint design with OpenAPI spec
   - External system integrations (adapters, clients, mappers)
   - Message queue architecture (Kafka/RabbitMQ)
   - Authentication and authorization (JWT, RBAC)
   - WebSocket for real-time features (if needed)
   - Webhook handlers for external events
   - API rate limiting and circuit breakers
   - Error handling and resilience patterns

   Output to: applications/{project_name}/planning/api-integration.md

   Use context from:
   - context/modules/api-patterns.md
   - context/modules/security-patterns.md"
   ```

   **Agent 3: data-platform-deployment-engineer**
   ```
   Prompt: "Design platform and operations architecture for {project_name}.

   Context:
   - Project folder: applications/{project_name}
   - Requirements: {summary from INITIAL.md}
   - Deployment target: {Kubernetes/Docker/etc}

   Create detailed architecture covering:
   - Docker containerization with health checks
   - Kubernetes deployment manifests (if needed)
   - CI/CD pipeline with automated testing
   - Infrastructure as code (Terraform/Helm)
   - Comprehensive monitoring (Prometheus, Grafana, Jaeger)
   - Centralized logging (structured JSON logs)
   - Disaster recovery and high availability
   - Environment variable management
   - CRITICAL: Create docker-compose.yml with COMPREHENSIVE environment variables

   Output to: applications/{project_name}/planning/platform-operations.md

   Use context from:
   - context/modules/deployment-patterns.md
   - context/modules/testing-patterns.md"
   ```

5. **Wait for all 3 agents to complete**

6. **Update Archon (if available)**
   - Mark Tasks 2, 3, 4 as "done"
   - Add summary notes from each agent

7. **Synthesize and validate**
   - Read all 3 architecture documents
   - Check for consistency and completeness
   - Verify all requirements are addressed

8. **Output to user:**
```
📋 Planning Complete (Tier 3 - Enterprise)

✅ Requirements documented: applications/{project_name}/planning/INITIAL.md
✅ Data Persistence Architecture: applications/{project_name}/planning/persistence_architecture.md
   - {X} entities with optimized schema
   - Multi-layer caching strategy
   - Performance optimization plan

✅ API & Integration Architecture: applications/{project_name}/planning/api-integration.md
   - {Y} REST endpoints
   - {Z} external system integrations
   - Message queue architecture
   - Comprehensive security

✅ Platform & Operations: applications/{project_name}/planning/platform-operations.md
   - Docker + Kubernetes deployment
   - CI/CD pipeline
   - Full observability stack
   - Disaster recovery plan

All planning documents are in: applications/{project_name}/planning/

Ready to implement? This will create a production-ready enterprise application with:
- Complete database layer with performance optimization
- Full REST API with authentication and authorization
- All external system integrations
- Message queue event processing
- Comprehensive monitoring and logging
- Docker and Kubernetes deployment
- Complete test suite (unit, integration, API, performance)

Estimated implementation time: 50-70 minutes

Shall I proceed with implementation?
```

## Error Handling

If tier not determined:
```
❌ Error: Please run /data-app-init first to determine the appropriate tier and project structure.
```

If project folder doesn't exist:
```
❌ Error: Project folder not found. Please run /data-app-init first.
```

If agents fail (Tier 3):
```
⚠️  Warning: One or more architecture agents failed.
Falling back to direct planning by main Claude.
This may take longer but will still produce a complete plan.
```

## Next Step

After planning is complete and user confirms, they should run the implementation (you as main Claude) or tell them to confirm to start implementation directly.
