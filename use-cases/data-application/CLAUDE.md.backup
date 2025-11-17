# 🏭 Data Persistent Factory System - Global Orchestration Rules

This defines the complete orchestration workflow for the Data Persistent Factory system and the principles that apply to ALL Data Persistent development work. When a user requests to build a data application, follow this systematic process using specialized subagents to transform high-level requirements into simple but complete data applications.

**Core Philosophy**: Transform high-level user requests into fully-functional, tested, and production-ready solutions. User input is required during Phase 0 clarification, then the process runs autonomously.

---

## 🎯 Primary Directive

⚠️ **CRITICAL WORKFLOW TRIGGER**: When ANY user request involves creating, building, or developing a data/persistence application:

1. **IMMEDIATELY** recognize this as a data/persistent factory request (stop everything else)
2. **MUST** follow Phase 0 first - ask clarifying questions
3. **WAIT** for user responses
4. **THEN** check Archon and proceed with workflow

**Factory Workflow Recognition Patterns** (if user says ANY of these):
- "Build a data application..."
- "Create a data-driven system..."
- "Build a database application with API..."
- "Create an application that stores and serves data..."
- "Implement a data service with REST API..."
- "Build a data persistence layer..."
- "Create a persistence layer..."
- "I need data persistence..."
- "Build persistent storage with API..."
- "Create a database layer with endpoints..."
- "Build data storage and retrieval system..."
- Any request mentioning **database/data/persistence + application/system/service/layer**

**If Ambiguous**: Ask user to clarify the domain before proceeding.

**MANDATORY Archon Integration (happens AFTER Phase 0):**
1. After getting user clarifications, run `mcp__archon__health_check`
2. If Archon is available:
   - **CREATE** an Archon project for the agent being built
   - **CREATE** tasks in Archon for each workflow phase:
      - Task 1: "Requirements Analysis" (Phase 1 - data-persistence-planner)
      - Task 2: "Data Persistence Architecture" (Phase 2A - data-persistence-architect)
      - Task 3: "API & Integration Architecture" (Phase 2B - data-api-integration-specialist)
      - Task 4: "Platform & Operations Architecture" (Phase 2C - data-platform-deployment-engineer)
      - Task 5: "Agent Implementation" (Phase 3 - main Claude Code)
      - Task 6: "Application Validation & Testing" (Phase 4 - data-application-validator)
      - Task 7: "Deployment & Documentation" (Phase 5 - main Claude Code)
   - **UPDATE** each task status as you progress:
      - Mark as "doing" when starting the phase
      - Mark as "done" when phase completes successfully
      - Add notes about any issues or deviations
   - **USE** Archon's RAG during implementation for documentation lookup
   - **USE** context7 during implementation for official framework documentation and API references
   - **INSTRUCT** all subagents to reference the Archon project ID
3. If Archon is not available: Proceed without it but use TodoWrite for local tracking

**WORKFLOW ENFORCEMENT**: You MUST:
1. Start with Phase 0 (clarifying questions)
2. Wait for user response before proceeding
3. Then systematically progress through ALL phases
4. Never jump directly to implementation

When you want to use or call upon a subagent, you must invoke the subagent, giving them a prompt and passing control to them.

---

## 🔄 Complete Factory Workflow

### Phase 0: Request Recognition & Clarification
**Trigger Patterns**: (activate factory on any of these):
- "Build a data application..."
- "Create a data-driven system..."
- "Build a database application with API..."
- "Create an application that stores and serves data..."
- "Implement a data service with REST API..."
- "Build a data persistence layer..."
- "Create a persistence layer..."
- "I need data persistence..."
- "Build persistent storage with API..."
- "Create a database layer with endpoints..."
- "Build data storage and retrieval system..."
- Any request mentioning **database/data/persistence + application/system/service/layer**

**Immediate Action**:
````
1. Acknowledge data application creation request
2. Ask 3-4 targeted clarifying questions (BEFORE invoking planner):
   - What type of data will the application manage?
   - Who will use this application and how?
   - What are the performance and scalability requirements?
   - Technology preferences (database type, language, deployment)
   - Integration needs with existing systems
3. ⚠️ CRITICAL: STOP AND WAIT for user responses
   - Wait to proceed to step 4 until user has answered
   - Refrain from making assumptions to "keep the process moving"
   - Avoid creating folders or invoke subagents yet
   - WAIT for explicit user input before continuing
4. Only after user responds: DETERMINE PROJECT FOLDER NAME (snake_case)
5. Create applications/[PROJECT_FOLDER_NAME]/ directory
6. Invoke ALL subagents with the EXACT SAME folder name
7. Tell each subagent: "Output to applications/[PROJECT_FOLDER_NAME]/"
8. Reference PRP template: PRPs/templates/prp_data_application_base.md
````

### Phase 1: Application Requirements Documentation 🎯
**Subagent**: `data-persistence-planner`
**Trigger**: Invoked after Phase 0 clarifications collected
**Mode**: AUTONOMOUS - Works without user interaction
**Philosophy**: COMPREHENSIVE application requirements following PRP template patterns
**Archon**: Update Task 1 to "doing" before invoking subagent

```
Actions:
1. Update Archon Task "Application Requirements Analysis" to status="doing"
2. Follow PRP template structure from PRPs/templates/prp_data_application_base.md
3. Analyze requirements focusing on:
   - Complete application scope (data + API + business logic)
   - User personas and usage patterns
   - Data characteristics and volume
   - API requirements and integration needs
   - Performance and consistency needs
   - Technology stack selection
4. Create comprehensive INITIAL.md following PRP Phase 0 structure
5. Output: applications/[EXACT_FOLDER_NAME]/planning/INITIAL.md
   ⚠️ CRITICAL: Output to planning/ subdirectory
6. Update Archon Task 1 to status="done" after subagent completes
```

**Quality Gate**: INITIAL.md must include:
- ✅ Complete application scope and user requirements
- ✅ Functional requirements
- ✅ Technical requirements
- ✅ External dependencies
- ✅ Success criteria

### Phase 2: Parallel Component Development ⚡
**Execute SIMULTANEOUSLY** (all three consolidated subagents work in parallel):
**Archon**: Update Tasks 2, 3, 4 to "doing" before parallel invocation

**CRITICAL: Use parallel tool invocation:** When invoking multiple subagents, you MUST call all three Task tools in a SINGLE message with multiple tool uses. This ensures true parallel execution.
- ❌ WRONG: Invoke planner, wait for completion, then invoke prompt engineer
- ✅ RIGHT: Single message with three Task tool invocations
- Also update all three Archon tasks (2, 3, 4) to "doing" before the parallel invocation

#### 2A: Data Persistence Architecture
**Subagent**: `data-persistence-architect`
**Philosophy**: INTEGRATED database design with performance optimization built
```
Output: applications/[EXACT_FOLDER_NAME]/planning/persistence_architecture.md
Contents:
- Database schema design with ERDs and integrated performance optimization
- Multi-layer caching strategies aligned with data relationships
- Query optimization and strategic indexing
- Connection pooling and resource management
- Scalability planning with read replicas and partitioning
- Database security and migration strategies
```

#### 2B: API & Integration Architecture
**Subagent**: `data-api-integration-specialist`
**Philosophy**: COMPLETE external interface design with integrated security and messaging
```
Output: applications/[EXACT_FOLDER_NAME]/planning/api-integration.md
Contents:
- REST API endpoint design with OpenAPI documentation
- External system integrations with message queues and webhooks
- Unified authentication and authorization across all interfaces
- Real-time capabilities with WebSocket and streaming
- Error handling and resilience patterns
- API testing and integration validation strategies
```

#### 2C: Platform & Operations Architecture
**Subagent**: `data-platform-deployment-engineer`
**Philosophy**: PRODUCTION-READY platform with integrated monitoring and observability
```
Output: applications/[EXACT_FOLDER_NAME]/planning/platform-operations.md
Contents:
- Docker containerization with built-in monitoring instrumentation
- Kubernetes deployment with comprehensive observability
- CI/CD pipelines with automated monitoring deployment
- Infrastructure as code with monitoring resources included
- Full-stack monitoring, alerting, and incident response
- Disaster recovery with monitoring validation

🚨 CRITICAL ENVIRONMENT VARIABLE INTEGRATION:
- Create docker-compose.yml with COMPREHENSIVE environment variables
- Include ALL standard Spring Boot application variables:
  - Security: JWT_SECRET, JWT_EXPIRATION, JWT_REFRESH_EXPIRATION
  - Database: HIKARI_MAXIMUM_POOL_SIZE, HIKARI_MINIMUM_IDLE
  - Monitoring: MANAGEMENT_ENDPOINTS_WEB_EXPOSURE_INCLUDE
  - Business: All domain-specific configuration variables (e.g., CACHE_TTL, THRESHOLD values)
- Use ${VARIABLE_NAME} syntax for environment substitution in docker-compose.yml
- Configure Redis with AUTH support when REDIS_PASSWORD is expected
- Mark areas needing business-specific variables with comments:
  # Business-specific environment variables will be added during implementation
- Ensure ALL services (app, redis, postgres) properly reference environment variables
```

**Phase 2 Complete When**: All three subagents report completion

### Phase 3: Data Application Implementation 🔨
**Actor**: Main Claude Code (not a subagent)
**Archon**: Update Task 5 to "doing" before starting implementation

```
Actions:
1. Update Archon Task 5 "Data Application Implementation" to status="doing"
2. READ the 4 markdown files from planning phase:
   - planning/INITIAL.md (requirements)
   - planning/persistence_architecture.md (unified database and performance design)
   - planning/api-integration.md (unified API and external systems)
   - planning/platform-operations.md (unified deployment and monitoring)
3. Use Archon RAG to search for data persistence patterns and examples
4. Use context7 to look up official Spring Boot, JPA, and framework documentation
5. IMPLEMENT the actual code based on specifications following PRP template
6. Create complete implementation
6.5. 🚨 MANDATORY ENVIRONMENT VARIABLE SYNCHRONIZATION:
   After creating .env.example, IMMEDIATELY:
   a. Read the docker-compose.yml created by data-platform-deployment-engineer
   b. Compare ALL .env.example variables with docker-compose.yml environment section
   c. Add ANY missing environment variables to the app service environment section using ${VARIABLE_NAME} syntax
   d. Ensure Redis authentication configuration matches REDIS_PASSWORD in .env.example
   e. Validate ALL .env.example variables are properly referenced in docker-compose.yml
   f. Test that docker-compose.yml can successfully substitute all environment variables
7. Update Archon task to status="done"
8. Structure final project as a complete application:
   applications/[project_name]/
   ├── src/main/java/           # Complete application source code
   │   ├── entity/             # JPA entities
   │   ├── repository/         # Data repositories
   │   ├── service/           # Business services
   │   ├── controller/        # REST API controllers
   │   ├── dto/               # API data transfer objects
   │   ├── config/           # Application configuration
   │   ├── security/         # Authentication & authorization
   │   ├── cache/           # Caching services
   │   ├── monitoring/       # Metrics and health checks
   │   ├── integration/      # External system integration
   │   │   ├── adapter/      # System-specific adapters
   │   │   │   ├── D365Adapter.java
   │   │   │   ├── HRMAdapter.java  
   │   │   │   ├── ECommerceAdapter.java
   │   │   │   ├── CRMLoyaltyAdapter.java
   │   │   │   └── PostISAdapter.java
   │   │   ├── client/       # External API clients
   │   │   │   ├── D365ApiClient.java
   │   │   │   ├── SOAPClient.java
   │   │   │   └── PostISApiClient.java
   │   │   ├── mapper/       # Data transformation mappers
   │   │   │   ├── D365RequestMapper.java
   │   │   │   └── BusinessDataMapper.java
   │   │   ├── processor/    # Batch and real-time processors
   │   │   │   ├── BatchSyncProcessor.java
   │   │   │   └── RealTimeEventProcessor.java
   │   │   └── webhook/      # Webhook handlers
   │   │       ├── ECommerceWebhookHandler.java
   │   │       └── PostISWebhookHandler.java
   │   ├── messaging/        # Message queue and event processing
   │   │   ├── producer/     # Event publishers
   │   │   ├── consumer/     # Event consumers
   │   │   └── event/       # Event definitions
   │   └── batch/           # Batch processing jobs
   │       ├── job/         # Spring Batch job definitions
   │       ├── step/        # Job steps
   │       └── tasklet/     # Custom tasklets
   ├── src/main/resources/
   │   ├── application.yml    # Application configuration
   │   ├── application-dev.yml # Development configuration
   │   ├── application-prod.yml # Production configuration
   │   ├── db/migration/     # Database migrations (Flyway)
   │   ├── wsdl/            # WSDL files for SOAP services
   │   ├── integration/     # Integration configuration files
   │   │   ├── camel-routes.xml
   │   │   └── spring-integration-context.xml
   │   └── static/          # Static web assets (if needed)
   ├── src/test/              # Comprehensive test suite
   │   ├── unit/             # Unit tests
   │   │   ├── adapter/      # Adapter unit tests
   │   │   ├── service/      # Service unit tests
   │   │   └── controller/   # Controller unit tests
   │   ├── integration/      # Integration tests
   │   │   ├── adapter/      # External system integration tests
   │   │   ├── database/     # Database integration tests
   │   │   └── messaging/    # Message queue integration tests
   │   ├── api/             # API tests
   │   │   ├── rest/        # REST API tests
   │   │   └── webhook/     # Webhook endpoint tests
   │   └── resources/       # Test resources
   │       ├── wiremock/    # WireMock mappings for external systems
   │       └── testdata/    # Test data files
   ├── docker-compose.yml          # Local development stack with external service mocks
   ├── docker-compose.test.yml     # Comprehensive testing environment with:
   │                               # - Application container under test
   │                               # - Test databases (PostgreSQL, Redis)
   │                               # - Message queue infrastructure (RabbitMQ/Kafka)
   │                               # - WireMock containers for external service simulation
   │                               # - Load testing tools (JMeter/Gatling containers)
   ├── Dockerfile                  # Application container
   ├── pom.xml              # Complete application dependencies with integration frameworks
   ├── README.md           # Usage and deployment documentation
   ├── .env.example        # Environment configuration template
   ├── deployment/         # Deployment artifacts
   │   ├── kubernetes/     # K8s deployment manifests
   │   ├── helm/          # Helm charts
   │   └── terraform/     # Infrastructure as code
   └── docs/              # Additional documentation
       ├── api/          # API documentation (OpenAPI/Swagger)
       ├── integration/  # Integration guides for each external system
       └── deployment/   # Deployment and operational guides
```

### Phase 4: Application Validation & Testing ✅
**Subagent**: `data-application-validator`
**Trigger**: Automatic after implementation
**Duration**: 5-10 minutes
**Archon**: Update Task 6 to "doing" before invoking validator

```
Actions:
1. Update Archon Task "Application Validation & Testing" to status="doing"
2. Create comprehensive test suite for complete application
3. Configure Docker-based test environment (docker-compose.test.yml with test containers)
4. Validate against INITIAL.md requirements (API, data, business logic)
4.5. 🚨 ENVIRONMENT CONFIGURATION VALIDATION:
   - Verify ALL .env.example variables are properly used in docker-compose.yml
   - Test docker-compose.yml starts successfully with actual .env file
   - Validate Redis authentication works correctly when REDIS_PASSWORD is set
   - Test all environment variable substitutions work as expected
   - Ensure no hardcoded values that should be environment variables
5. Execute tests using Docker Compose orchestration:
   - Spin up test containers (application, databases, message queues, mock external services)
   - Run Maven/Gradle test suites against containerized environment
   - Execute integration tests with WireMock for external system simulation
   - Perform load testing against realistic infrastructure
   - Generate comprehensive test reports with coverage metrics
   - Tear down test environment and cleanup resources
6. Perform end-to-end application testing in isolated Docker environment
7. Validate performance benchmarks and integration points under load
8. Generate validation report with full application metrics and Docker test execution logs
9. Update Archon task to status="done"
10. Output: Complete application test suite with Docker-based integration testing infrastructure
```

**Success Criteria**:
- All requirements validated
- Core functionality tested
- Error handling verified
- Performance acceptable

### Phase 5: Deployment & Documentation 📦
**Actor**: Main Claude Code
**Archon**: Update Task 7 to "doing" before final documentation
**Final Actions**:

```
Actions:
1. Update Archon Task "Deployment & Documentation" to status="doing"
2. Generate comprehensive README.md
3. Create deployment artifacts
4. Setup monitoring and observability
5. Document API endpoints (if applicable)
6. Provide deployment instructions
7. Update Archon Task 7 to status="done"
8. Add final notes to Archon project about agent capabilities
9. Summary report to user with Archon project link
```

---

## 📋 Archon Task Management Protocol

### Task Creation Flow
When Archon is available, create all workflow tasks immediately after project creation:
```python
# After creating Archon project
tasks = [
    {"title": "Complete Application Requirements Analysis", "assignee": "data-persistence-planner", "description": "Analyze user needs, business processes, and technical requirements for complete data application"},
    {"title": "Unified Data Persistence Architecture", "assignee": "data-persistence-architect", "description": "Design comprehensive database schemas with integrated performance optimization, caching strategies, and scalability planning"},
    {"title": "Unified API & Integration Architecture", "assignee": "data-api-integration-specialist", "description": "Design complete external interfaces including REST APIs, external system integrations, message queues, and authentication"},
    {"title": "Unified Platform & Operations Architecture", "assignee": "data-platform-deployment-engineer", "description": "Design production-ready platform with comprehensive docker-compose.yml environment variable integration, containerization, CI/CD, infrastructure, monitoring, and observability"},
    {"title": "Complete Application Implementation", "assignee": "Claude Code", "description": "Implement complete application with mandatory environment variable synchronization between .env.example and docker-compose.yml"},
    {"title": "Comprehensive Application Validation & Testing", "assignee": "data-application-validator", "description": "Complete testing with environment configuration validation, ensuring docker-compose.yml and .env.example synchronization works correctly"},
    {"title": "Production Deployment & Documentation", "assignee": "Claude Code", "description": "Deploy complete application with integrated monitoring, documentation, and operational procedures"}
]
# Create all tasks with status="todo" initially
```

### Task Status Updates
- Set to "doing" immediately before starting each phase
- Set to "done" immediately after phase completes successfully
- Add notes if phase encounters issues or deviations
- Never have multiple tasks in "doing" status (except during parallel Phase 2)

### Subagent Communication
Always pass the Archon project ID to subagents:
- Include in the prompt: "Use Archon Project ID: [project-id]"
- Subagents should reference this in their output for traceability

## 🎭 Subagent Invocation Rules

### Automatic Invocation
Subagents are invoked AUTOMATICALLY based on workflow phase:
```python
def invoke_workflow(user_request):
    if user_request.contains(data_application_request):
        # Phase 0 - Main Claude Code asks clarifications
        clarifications = ask_data_application_questions()

        # Phase 1 - Invoke planner with context
        invoke("data-persistence-planner", context={
            "user_request": original_request,
            "clarifications": clarifications,
            "prp_template": "PRPs/templates/prp_data_application_base.md"
        })

        # Phase 2 - Parallel automatic
        parallel_invoke([
            "data-persistence-architect",
            "data-api-integration-specialist", 
            "data-platform-deployment-engineer"
        ])

        # Phase 3 - Main Claude Code
        implement_data_application()

        # Phase 4 - Automatic
        invoke("data-application-validator")
```

### Manual Override
Users can explicitly request specific subagents:
- "Use the planner to refine requirements"
- "Have the tool integrator add web search"
- "Run the validator again"

---

## 📁 Output Directory Structure

Every agent factory run creates:
```
applications/
└── [project_name]/
    ├── planning/                    # All planning documents
    ├── src/main/java/              # Complete application source code
    ├── src/test/                   # Comprehensive test suites
    ├── docker-compose.yml          # Development stack
    ├── Dockerfile                  # Application container
    ├── .env.example               # Environment template
    └── README.md                  # Usage documentation
```

---

## 🔧 Implementation Guidelines

### For Simple Data Application/Persistent Requests
Example: "Build persistent storage with API"
```
1. Planner asks minimal questions (2-3)
2. Assumes standard patterns
3. Completes in ~20 minutes total
4. Delivers working project with basic tests
```

### For Complex Data Application/Persistent Requests
Example: "Build a comprehensive data-driven application for an e-commerce system"
```
1. Planner asks comprehensive questions (4-5)
2. Multiple iterations may be needed
3. Delivers simple yet complete system with full test coverage
```

### Error Handling Protocol
If any subagent fails:
```
1. Log error with context
2. Attempt automatic recovery
3. If recovery fails, ask user for guidance
4. Continue with partial implementation if possible
5. Document limitations in README
```

---

## 📝 Main Clarification Guidelines

When a user requests a data application/persistence, the main Claude Code agent should:

### Ask 2-3 Focused Questions
Keep questions simple and targeted:
1. **Core Functionality**: "What specific tasks should this agent handle?"
2. **Integration Needs**: "Will it need to connect to any external services or APIs?"
3. **Output Format**: "Should it return plain text, structured data, or something else?"

### Avoid Over-Questioning
- Don't ask about technical details (the planner will handle those)
- Don't ask about implementation specifics
- Keep questions high-level and user-friendly

### Pass Context to Planner
When invoking the planner, provide:
- Original user request
- User's answers to clarifying questions
- Any additional context from the conversation

## 🚀 Quick Start Examples

### Example 1: Data Persistence Request
**User**: "I need a data application for managing e-commerce orders"

**System Response**:
```
🏗️ Data Application Factory Activated!

I'll help you build a comprehensive data-driven application for your e-commerce system. 
Let me ask a few key questions to understand your specific needs:

1. What types of data will you be storing? (users, products, orders, inventory, etc.)
2. What's your expected scale? (orders per day, concurrent users, product catalog size)
3. Do you have technology preferences? (Java/Spring Boot, .NET, Python, etc.)
4. What are your performance requirements? (response times, availability needs)
5. Will you need integration with external services? (payment processors, inventory systems, etc.)

[STOPS HERE AND WAITS FOR USER TO RESPOND]

[After user responds with their answers]

Perfect! Based on your requirements [summarize their answers], I'll now invoke our requirements planner to create a comprehensive specification for your project.

📋 Creating Requirements Document...
[Invokes data-persistence-planner with context]

[Planner works autonomously and creates INITIAL.md]

⚙️ Building Project Components...
[Parallel invocation of data-api-integration-specialist, data-persistence-architect, data-platform-deployment-engineer]

🔨 Implementing Your Project...
[Main implementation]

✅ Running Validation...
[Invokes data-application-validator]

🎉 Agent Complete!
Your data application Project is ready at: applications/[project_name]
```

---

## 🔍 Monitoring & Debugging

### Progress Tracking
The system provides domain-specific status updates:

**Data Application Factory**:
```

✅ Phase 1: Requirements Complete (Complete application INITIAL.md with PRP structure)
⏳ Phase 2: Designing Application (3 consolidated subagents working...)
  ✅ Data Persistence: Complete (Unified database schemas with integrated performance optimization and caching)
  ✅ API Integration: Complete (Unified REST APIs with external systems, messaging, and authentication)
  ⏳ Platform Operations: In progress (Unified deployment infrastructure with integrated monitoring and observability)...
⏳ Phase 3: Implementation pending...
⏳ Phase 4: Validation pending...  
```

### Debug Mode
Enable with: "Build data application in debug mode"
- Verbose logging from all subagents
- Intermediate outputs preserved
- Step-by-step confirmation mode
- Performance metrics collected

---

## 🛡️ Quality Assurance

### Data Application Quality Gates
1. **Comprehensive tests** for all application layers (API, business logic, data)
2. **Docker-based integration testing** with realistic infrastructure simulation
3. **Performance benchmarks** and load testing in containerized environment
4. **Security measures** for complete application protection
5. **WireMock external system simulation** for reliable integration testing
6. **Monitoring and observability** setup with containerized monitoring stack
7. **Environment template** (.env.example)
8. **>90% test coverage** for all application components

#### **Docker Testing Infrastructure Requirements**
- **Test Environment Isolation**: Each test run uses fresh containerized infrastructure
- **External Service Mocking**: WireMock containers simulate all external dependencies
- **Database State Management**: Containerized databases with test data initialization and cleanup
- **Performance Testing**: Load testing tools (JMeter/Gatling) running in containers
- **Integration Test Orchestration**: Docker Compose manages complete test environment lifecycle
- **Realistic Infrastructure**: Test containers mirror production configuration
- **Parallel Test Execution**: Multiple isolated test environments for concurrent testing
- **Resource Cleanup**: Automated container teardown and resource cleanup after tests

### Validation Checklist
Before delivery, confirm:
- [ ] All requirements from INITIAL.md implemented
- [ ] Tests passing with >90% coverage
- [ ] Error scenarios handled
- [ ] Documentation complete
- [ ] Usage examples provided

---

## 🎨 Customization Points

### User Preferences
Users can specify:
- Output format (string, structured, streaming)
- Testing depth (basic, comprehensive, exhaustive)
- Documentation style (minimal, standard, detailed)

### Advanced Features
For power users:
- Custom subagent configurations
- Alternative workflow sequences
- Integration with existing codebases
- CI/CD pipeline generation

---

## 📊 Success Metrics

### Data Application Factory (Optimized)
- **Time to Completion**: Target <35 minutes for standard applications (25% improvement)
- **Test Coverage**: Minimum 90% for all application layers
- **Performance Validation**: 100% of SLAs tested
- **User Intervention**: Minimize to initial requirements only

---

## 🔄 Continuous Improvement

### Feedback Loop
After each data application creation:
1. Analyze what worked well
2. Identify bottlenecks
3. Update subagent if needed
4. Refine workflow based on patterns

### Pattern Library
Build a library of common data application patterns:
- Simple CRUD applications
- Multi-entity data systems
- API-first data services
- Event-driven data flows
- External system integrations

---

## 🚨 Important Rules

### ALWAYS:
- ✅ **Recognize domain correctly** from user request
- ✅ **Follow appropriate workflow** (AI vs Data Persistence)
- ✅ **Use Archon integration** for task management
- ✅ **Create comprehensive tests** for chosen domain
- ✅ **Document everything** appropriately
- ✅ **Validate against requirements**

### Anti-patterns to ALWAYS avoid:
- ❌ **Mix domains** - Don't use AI agent patterns for data persistence
- ❌ **Skip domain recognition** - Always determine the correct factory
- ❌ **Ignore specialized requirements** - Each domain has specific needs
- ❌ **Create overly complex solutions** - Match complexity to requirements
- ❌ **Forget security considerations** for either domain

---

## 🎯 Final Checklist

Before considering ANY solution complete:
- [ ] Domain correctly identified and appropriate factory used
- [ ] Requirements captured in appropriate format (INITIAL.md)
- [ ] All components generated by domain-specific subagents
- [ ] Implementation complete and functional
- [ ] Tests written and passing with domain-appropriate coverage
- [ ] Documentation comprehensive and clear
- [ ] Security measures in place for the domain
- [ ] User provided with clear next steps

---

## 🔄 Domain-Specific Principles

### Data Application Core Principles  
- **Enterprise-grade** - Comprehensive, production-ready applications
- **PRP template integration** - Follow enterprise patterns
- **Performance-first** - Optimize for scale and reliability
- **Comprehensive testing** - Unit, integration, API, and performance tests
- **Operational excellence** - Monitoring, alerting, and observability

This factory system provides the best of both worlds: simple data persistence layers when needed, and comprehensive, enterprise-grade data persistence layers when required, all with consistent Archon integration and quality assurance.