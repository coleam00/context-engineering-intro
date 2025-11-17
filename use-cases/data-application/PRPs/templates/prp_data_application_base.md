---
name: "Data Application PRP Template"
description: "Template for generating comprehensive PRPs for Data & Persistence Layer development projects"
---

## Purpose

[Brief description of the project to be built and its main purpose]

## Core Principles

1. **Data & Persistence Layer Best Practices**: Deep integration with data & persistent patterns for CRUD operations
2. **Production Ready**: Include security, testing, and monitoring for production deployments
3. **Type Safety First**: Leverage type-safe design and validation throughout
4. **Context Engineering Integration**: Apply proven context engineering workflows to data and persistent development
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation


1. **Data & Persistence Layer Best Practices**:
 - Adopt standardized patterns for CRUD, transactions, caching, and query optimization.
 - Support multiple persistence backends (SQL, NoSQL, object stores, streams) via well-defined abstractions.
 - Ensure consistency & integrity through ACID/BASE alignment depending on context.
2. **Production Readiness**:
- Enforce data security (encryption at rest, in transit, fine-grained access controls, audit logging).
- Provide observability hooks (structured logging, metrics, distributed tracing, anomaly alerts).
- Automate schema migrations and rollbacks with clear versioning.
3. **Type Safety & Schema Validation**:
- Ensure compile-time guarantees (type-safe ORM/DAO, DTO contracts, API schemas).
- Apply runtime validation (e.g., JSON schema, Zod, Pydantic) for untyped inputs.
- Support evolutionary schema design with backward/forward compatibility.
4. **Contextual & Domain-driven Engineering**:
- Align persistence models with Domain-Driven Design (DDD) and bounded contexts.
- Separate read/write concerns (CQRS) where performance/scalability demands it.
- Use event sourcing and audit trails where business traceability is critical.
5. **Comprehensive Testing & Resilience**:
- Provide unit, integration, and contract testing for persistence logic.
- Include fault injection and chaos testing for resilience validation.
- Apply data lifecycle testing: seed, migrate, backup/restore, purge.
6. **Performance & Scalability**:
- Optimize for query efficiency (indexing, partitioning, sharding).
- Enable horizontal scalability with replication and clustering.
- Provide caching strategies (in-memory, distributed) aligned with use cases.
7. **Lifecycle & Governance**:
- Implement data retention, archival, and deletion policies (compliance-driven).
- Support auditability for regulatory environments (GDPR, HIPAA, SOX).
- Ensure versioned APIs and schemas to avoid breaking downstream consumers.

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your implementation focused and practical. Don't build unnecessary complexity.


### What NOT to do in Data & Persistence Layer:
- ❌ **Don't reinvent the wheel** – Avoid building dozens of custom utilities if proven libraries/ORMs/data-access patterns already solve the problem.
- ❌ **Don't over-complicate dependencies** – Keep persistence frameworks and DI layers minimal; prefer lightweight connectors over bloated stacks.
- ❌ **Don't add unnecessary abstractions** – Don't wrap every database call in layers of indirection unless there's a clear business or scaling need.
- ❌ **Don't over-engineer workflows** – Avoid complex CQRS/event sourcing unless justified by domain requirements.
- ❌ **Don't enforce rigid schemas everywhere** – Only apply strict validation where correctness or compliance demands it; otherwise allow flexible data flows.
- ❌ **Don't scatter persistence code** – Centralize schemas, migrations, and DAOs/repositories; avoid "examples/" or ad hoc storage implementations.


### What TO do in Data & Persistence Layer:
- ✅ **Start simple** – Implement a minimal data model and persistence strategy that meets today's needs before optimizing.
- ✅ **Add features incrementally** – Introduce indexing, caching, or sharding only when workloads demand it.
- ✅ **Follow proven reference patterns** – Leverage well-tested approaches (repository pattern, unit of work, schema migration frameworks) instead of inventing new ones.
- ✅ **Use simple defaults** – e.g., default to straightforward CRUD; only introduce advanced result types, event sourcing, or CQRS when required.
- ✅ **Test early and often** – Validate queries, migrations, and schema evolution with unit, integration, and contract tests as you build.
- ✅ **Design for change** – Support forward/backward-compatible schemas, versioning, and migration rollback from day one.

### Key Question:
**"Does this project really need this feature to accomplish its core purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

[Detailed description of what the project should accomplish]

## Why

[Explanation of why this project is needed and what problem it solves]

## What

📌 Data & Persistence Layer Checklist

### Data Layer Classification
- [ ] **Relational Persistence**: SQL databases (e.g., PostgreSQL, MySQL, MSSQL) with strong schema & ACID guarantees
- [ ] **NoSQL Persistence**: Document/Key-Value stores (e.g., MongoDB, Redis, DynamoDB) for flexible or high-throughput needs
- [ ] **Event/Data Streams**: Kafka, Pulsar, or equivalent for real-time event persistence
- [ ] **Hybrid Strategy**: Combination of above, with clear data ownership and boundaries

### Storage & Provider Requirements
- [ ] **Primary Database**: Specify (Postgres, MySQL, MongoDB, etc.)
- [ ] **Migration Framework**: (Flyway, Liquibase, Prisma, Alembic, etc.)
- [ ] **Backup & Recovery**: Scheduled backups, retention, and tested restore procedures
- [ ] **Monitoring & Observability**: Query performance tracking, error logs, slow query alerts
- [ ] **Fallback/Failover Strategy**: Replication, clustering, or container-based DR (disaster recovery)

### External Integrations
- [ ] APIs for Persistence Layer (internal services consuming data)
- [ ] Messaging/Queue Systems (Apache Kafka, RabbitMQ, Apache Pulsar)
- [ ] File Storage (MinIO, local filesystem, NFS)
- [ ] Analytics/BI Tools (Apache Superset, Grafana, or open source warehouse connector)
- [ ] Identity & Access Control (Keycloak, OAuth, RBAC)

### Success Criteria
- [ ] **Correctness**: CRUD, transactions, and migrations work as expected with rollback safety
- [ ] **Security**: Encryption in transit & at rest, secrets stored in Key Vaults, access controls enforced
- [ ] **Scalability**: Query performance within defined SLAs; handles peak throughput & load tests
- [ ] **Resilience**: Automatic failover tested; recovery time and point objectives (RTO/RPO) defined and validated
- [ ] **Governance & Compliance**: Data retention, audit trails, GDPR/PII handling in place
- [ ] **Testing**: Unit, integration, contract, and chaos/fault injection tests executed successfully
- [ ] **Observability**: Logs, metrics, and traces available for operations teams
- [ ] **Evolution**: Schema versioning and compatibility validated for rolling upgrades

## All Needed Context

### Data & Persistence Layer Documentation & Research Path

```yaml
# MCP servers
- mcp: Archon
  query: "open source data persistence integration streaming real-time kafka microservices security compliance monitoring testing"
  why: Comprehensive exploration of open source data applications including integration, streaming, testing, and compliance patterns

- mcp: context7
  query: "framework documentation API reference implementation examples best practices tutorials"
  why: Access to comprehensive framework documentation, API references, implementation examples, and best practices across all technology stacks used in development

# Research Path
- step: Core Principles & Mindset
  resources:
    - url: https://12factor.net/backing-services
      why: Treat databases as replaceable backing services
      content: Configuration, service binding, portability
    - url: https://martinfowler.com/eaaCatalog/
      why: Foundational persistence and enterprise integration patterns
      content: Repository, Unit of Work, CQRS, Event Sourcing

- step: Schema & Data Management
  resources:
    - url: https://flywaydb.org/documentation/
      why: Schema migration/versioning best practices
      content: Migration scripts, rollback strategies, CI/CD integration
    - url: https://www.postgresql.org/docs/
      why: Relational persistence design and operations
      content: ACID transactions, indexing, partitioning, replication
    - url: https://www.mongodb.com/docs/manual/
      why: NoSQL/document persistence practices
      content: Schema-less design, indexing strategies, aggregation, replication/sharding

- step: Performance & Scalability
  resources:
    - url: https://redis.io/docs/
      why: High-performance caching and ephemeral persistence
      content: Caching patterns, persistence modes (RDB/AOF), clustering, pub/sub
    - url: https://kafka.apache.org/documentation/
      why: Streaming/event persistence patterns
      content: Topics, partitions, replication, exactly-once semantics

- step: Observability & Resilience
  resources:
    - url: https://opentelemetry.io/docs/
      why: Observability for persistence layers
      content: Query metrics, tracing, structured logs
    - url: https://litmuschaos.io/
      why: Chaos engineering for resilience validation
      content: Fault injection, database failure testing, recovery validation

- step: Security & Governance
  resources:
    - url: https://owasp.org/www-project-top-ten/
      why: Security standards for persistence
      content: SQL injection, encryption, secrets management, least privilege
    - url: https://gdpr-info.eu/
      why: Compliance for data protection in the EU
      content: Data retention, deletion, auditability, user consent
    - url: https://www.hhs.gov/hipaa/for-professionals/security/index.html
      why: Compliance for health-related data (if applicable)
      content: Data encryption, access control, audit logging, breach notifications

- step: Open Source Integration Architecture
  resources:
    - url: https://www.enterpriseintegrationpatterns.com/
      why: Message queue, ETL, and integration patterns (vendor-neutral)
      content: Service Bus patterns, Message Routing, Data Transformation, Aggregator patterns
    - url: https://camel.apache.org/manual/
      why: Apache Camel for open source integration routing
      content: Route definitions, data transformation, error handling, connector patterns
    - url: https://spring.io/projects/spring-integration
      why: Spring Integration for open source messaging
      content: Message channels, gateways, service activators, message transformation
    - url: https://www.rabbitmq.com/documentation.html
      why: RabbitMQ open source message broker
      content: Queue management, routing, clustering, high availability
    - url: https://activemq.apache.org/components/artemis/documentation/
      why: Apache ActiveMQ open source messaging
      content: Message persistence, transactions, clustering, bridge configurations

- step: Open Source Testing Strategies
  resources:
    - url: https://pact.io/
      why: Contract testing for microservices integration (open source)
      content: Consumer-driven contracts, provider verification, CI/CD integration
    - url: https://jmeter.apache.org/
      why: Open source performance testing
      content: Load scenarios, performance metrics, CI/CD integration, comprehensive reporting
    - url: https://testcontainers.org/
      why: Integration testing with containerized services
      content: Database containers, message queue testing, service mocking, lifecycle management
    - url: https://wiremock.org/docs/
      why: Open source service mocking
      content: HTTP mocking, request matching, response templating, fault injection
    - url: https://litmuschaos.io/
      why: Open source chaos engineering
      content: Fault injection, network chaos, stress testing, recovery validation

- step: Real-Time Processing & Streaming
  resources:
    - url: https://kafka.apache.org/documentation/streams/
      why: Kafka Streams for real-time data processing
      content: Stream topologies, stateful processing, windowing, exactly-once processing
    - url: https://flink.apache.org/
      why: Apache Flink for complex event processing
      content: Event-driven applications, state management, fault tolerance, windowing
    - url: https://kafka.apache.org/documentation/
      why: Apache Kafka platform patterns
      content: Schema registry, Kafka Streams, connector ecosystem, security
    - url: https://pulsar.apache.org/docs/
      why: Apache Pulsar for enterprise messaging and streaming
      content: Multi-tenancy, geo-replication, tiered storage, functions framework
    - url: https://spark.apache.org/docs/latest/streaming-programming-guide.html
      why: Apache Spark Streaming for batch and stream processing
      content: DStreams, structured streaming, checkpointing, integration patterns

- step: Open Source Security & Compliance
  resources:
    - url: https://oauth.net/2/
      why: OAuth 2.0 for API security (open standard)
      content: Authorization flows, token management, scope definitions, implementation patterns
    - url: https://openid.net/connect/
      why: OpenID Connect for authentication (open standard)
      content: Identity providers, claims, SSO integration, token validation
    - url: https://www.keycloak.org/documentation
      why: Open source identity and access management
      content: User management, SSO, identity brokering, fine-grained authorization
    - url: https://cheatsheetseries.owasp.org/
      why: Open source security best practices
      content: Data protection, secure coding, authentication, authorization patterns
    - url: https://cis-controls.org/
      why: Open security controls framework
      content: Access control, audit logging, data protection, security assessment

- step: Open Source Monitoring & Observability
  resources:
    - url: https://prometheus.io/docs/
      why: Open source metrics collection and alerting
      content: Metrics scraping, alerting rules, service discovery, federation
    - url: https://grafana.com/oss/grafana/
      why: Open source dashboards and visualization
      content: Dashboard design, data source integration, alerting, community plugins
    - url: https://opentelemetry.io/docs/
      why: Open source observability framework
      content: Distributed tracing, metrics, logs, vendor-neutral instrumentation
    - url: https://jaegertracing.io/docs/
      why: Open source distributed tracing
      content: Trace collection, sampling, analysis, performance optimization
    - url: https://micrometer.io/docs/
      why: Open source application metrics
      content: Metrics collection, dimensional metrics, registry integration

- step: Open Source Architecture & Container Patterns
  resources:
    - url: https://microservices.io/patterns/
      why: Microservices patterns for distributed data applications
      content: Data management patterns, saga pattern, API composition, service mesh
    - url: https://kubernetes.io/docs/concepts/
      why: Container orchestration architecture patterns
      content: Data partitioning, service discovery, resilience patterns, scalability
    - url: https://12factor.net/
      why: Twelve-factor methodology for cloud-native applications
      content: Operational excellence, security, reliability, performance, portability
    - url: https://docker.com/resources/what-container
      why: Container architecture patterns
      content: System design, operational excellence, security, reliability
    - url: https://www.martinfowler.com/architecture/
      why: Architecture patterns and practices (vendor-neutral)
      content: Domain-driven design, microservices, data management, evolutionary architecture
```

### Data & Persistence Architecture Patterns (follow main_reference)
```yaml
persistence_structure:
  configuration:
    - central_config: "Centralized configuration for all persistence settings (environment-driven)"
    - provider_abstraction: "Abstraction layer for different database backends (Postgres, MongoDB, Redis, etc.)"
    - environment_variables: "Use environment variables or secret manager for connection strings, credentials, and pooling"
    - no_hardcoding: "Never hardcode DB credentials, URIs, or sensitive configs"
  
  data_model_definition:
    - default_crud: "Implement simple CRUD operations by default; avoid unnecessary complexity"
    - schema_evolution: "Use migration frameworks for versioned schema evolution and rollback"
    - schema_centralization: "Keep schema definitions and migrations in a centralized, tracked location"
    - domain_alignment: "Align entities with domain models and bounded contexts (DDD principles)"
  
  integration_patterns:
    - repository_or_dao: "Encapsulate database access via Repository/DAO pattern"
    - unit_of_work: "Manage transactional boundaries consistently across operations"
    - advanced_patterns: "Optional CQRS or Event Sourcing for complex domains"
    - error_handling: "Consistent error handling, retries, and logging for all persistence operations"
  
  testing_strategy:
    - unit_tests: "Validate individual queries, repositories, and transaction logic"
    - integration_tests: "Test against ephemeral or staging databases (Docker, Testcontainers, etc.)"
    - contract_tests: "Verify schema version compatibility between services"
    - resilience_tests: "Fault-injection, failover, and latency testing to ensure robustness"
```

### Data & Persistence Security Patterns (research required)
```yaml
security_requirements:
  secrets_management:
    environment_variables: ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
    secure_storage: "Never commit secrets to version control; use Key Vaults/Secret Managers"
    rotation_strategy: "Plan for credential rotation and secret expiry"
  
  access_control:
    principle_of_least_privilege: "Separate accounts for read/write/admin"
    role_based_access: "Use RBAC/ABAC at database and service layer"
    audit_logging: "Track access and modifications for compliance"
  
  data_protection:
    encryption: "Encrypt data in transit (TLS) and at rest (native DB or KMS)"
    masking: "Apply masking or tokenization for sensitive fields (PII/PHI)"
    backups: "Automated, encrypted, and tested restore procedures"
  
  observability:
    logging: "Query logs and error logs with sensitive data redaction"
    metrics: "Track query latency, slow queries, cache hits/misses"
    tracing: "Distributed tracing for persistence calls (OpenTelemetry or equivalent)"
```

### Data & Persistence Performance Patterns (research required)
```yaml
performance_and_scalability:
  query_optimization:
    indexing: "Design indexes for high-read queries; use composite indexes where needed"
    query_plans: "Analyze query execution plans and optimize joins, filters, and aggregations"
    caching: "Use caching layers (in-memory or distributed) for frequent read patterns"
  
  scaling_strategies:
    vertical_scaling: "Scale compute/memory of database nodes for increased load"
    horizontal_scaling: "Partition/shard data across multiple nodes for throughput"
    replication: "Implement replication for high availability and read scaling"
  
  data_partitioning:
    sharding: "Distribute large datasets across nodes based on business keys"
    table_partitioning: "Partition large tables to improve query performance and maintenance"
  
  concurrency_control:
    transactions: "Use ACID transactions where needed; optimize isolation levels"
    optimistic_locking: "For high-concurrency workloads to prevent conflicts"
    connection_pooling: "Maintain efficient DB connection pools to handle load spikes"
  
  monitoring_and_alerting:
    metrics: "Track query latency, throughput, cache hit/miss, replication lag"
    alerts: "Set up thresholds and automated alerts for performance degradation"
    dashboards: "Provide visibility to operations teams for proactive tuning"
  
  resilience_under_load:
    failover_testing: "Simulate node failures to validate automatic failover"
    stress_testing: "Load testing for peak queries and transaction bursts"
    chaos_testing: "Inject latency, network errors, and partial outages to validate system robustness"
```

## Implementation Blueprint

### Technology Research Phase

**RESEARCH REQUIRED - Complete before implementation:**

✅ **Persistence Framework Deep Dive:**
- [ ] Evaluate database options (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- [ ] Study migration/versioning frameworks (Flyway, Alembic, Liquibase, Prisma)
- [ ] Analyze abstraction patterns (Repository, DAO, Unit of Work, CQRS/Event Sourcing)
- [ ] Review connection management, pooling, and type-safe data access patterns
- [ ] Assess testing strategies (unit, integration, contract, resilience/chaos tests)

✅ **Data & Persistence Architecture Investigation:**
- [ ] Define project structure conventions (config/connection modules, migrations/, repositories/)
- [ ] Model design and domain alignment (entities, bounded contexts, DDD principles)
- [ ] Schema evolution and versioning strategies (backward/forward compatibility)
- [ ] Performance patterns: indexing, caching, partitioning, replication
- [ ] Error handling, retry mechanisms, and transactional consistency

✅ **Security and Production Patterns:**
- [ ] Secrets and credentials management (env vars, secret managers, rotation policies)
- [ ] Access control and audit logging (RBAC/ABAC, activity tracking)
- [ ] Data protection (encryption at rest/in transit, masking, PII/PHI handling)
- [ ] Observability: logging, metrics, distributed tracing for persistence operations
- [ ] Deployment, scaling, and resilience considerations (failover, load testing, disaster recovery)

### Data & Persistence Layer Implementation Plan
```yaml
Implementation Task 1 - Persistence Architecture Setup (Follow main_reference):
  CREATE project structure:
    - central_config: Centralized configuration for all persistence settings (env-driven)
    - provider_abstraction: Abstraction layer for different database backends
    - repositories/: Repository or DAO modules for each domain entity
    - migrations/: Versioned schema definitions and migration scripts
    - tests/: Comprehensive test suite
    - docs/: Documentation for schema, data flows, and operational patterns

Implementation Task 2 - Core Data Model Development:
  IMPLEMENT domain entities and repositories:
    - Define entities aligned with bounded contexts (DDD)
    - Implement CRUD operations in repository/DAO pattern
    - Apply Unit of Work or transactional boundaries where needed
    - Error handling, logging, and retries for persistence operations
    - Use schema validation (type-safe models or validators)

Implementation Task 3 - Migration & Schema Evolution:
  DEVELOP migrations/ scripts:
    - Versioned migration files for schema changes
    - Rollback strategies and backward/forward compatibility
    - Automated migration execution in CI/CD pipelines
    - Testing migrations against ephemeral or staging DBs
    - Documentation of schema evolution for developers and operations

Implementation Task 4 - Integration & External Dependencies:
  INTEGRATE with external systems:
    - Connect to queues, messaging systems, and storage backends
    - Implement caching layers (Redis, in-memory, or distributed)
    - Secure connections (TLS, credentials via secrets manager)
    - Dependency injection or service abstraction for external integrations
    - Parameter validation and consistency checks

Implementation Task 5 - Comprehensive Testing:
  IMPLEMENT testing suite:
    - Unit tests for repositories, queries, and transactions
    - Integration tests with ephemeral/staging DBs
    - Contract tests for schema version compatibility
    - Resilience/fault-injection tests (failover, latency, disconnections)
    - Performance/load testing of queries and persistence operations

Implementation Task 6 - Security and Production Readiness:
  SETUP security patterns:
    - Manage credentials via env vars or secret managers
    - Access control and audit logging implementation
    - Data encryption (in transit and at rest)
    - Masking/tokenization for sensitive fields (PII/PHI)
    - Observability: metrics, logs, tracing
    - Production deployment configuration, scaling, and failover strategies
```

## Validation Loop

### Level 1: Project Structure Validation
```bash
# Verify complete project structure
find persistence_project -type f | sort
test -d persistence_project/repositories && echo "Repositories folder present"
test -d persistence_project/migrations && echo "Migrations folder present"
test -d persistence_project/tests && echo "Tests folder present"
test -d persistence_project/config && echo "Configuration folder present"
test -d persistence_project/docs && echo "Documentation folder present"

# Verify presence of central configuration and provider abstraction
grep -q "central_config" persistence_project/config/
grep -q "provider_abstraction" persistence_project/config/

# Expected: All required directories and config abstractions exist
# If missing: Generate missing folders/files with correct patterns
```

### Level 2: Project Functionality Validation
```bash
# Verify database connectivity and configuration
cd persistence_project && npm run test:connection 2>&1 | grep -E "(Connected|Connection successful)"
# OR for Java projects: ./mvnw test -Dtest=DatabaseConnectionTest
# OR for .NET projects: dotnet test --filter="Category=Connection"

# Verify CRUD operations functionality
cd persistence_project && npm run test:crud 2>&1 | grep -E "(PASS|✓)"
# OR: ./mvnw test -Dtest=*CrudTest*
# OR: dotnet test --filter="Category=CRUD"

# Verify migration system is working
cd persistence_project && npm run migrate:up && npm run migrate:status | grep -E "(up|applied|success)"
# OR: ./mvnw flyway:migrate && ./mvnw flyway:info
# OR: dotnet ef migrations list

# Test rollback capability
cd persistence_project && npm run migrate:down && npm run migrate:up
# OR: ./mvnw flyway:undo && ./mvnw flyway:migrate
# OR: dotnet ef database update [previous-migration] && dotnet ef database update

# Verify repository/DAO pattern implementation
grep -r "class.*Repository\|interface.*Repository" persistence_project/repositories/
grep -r "class.*DAO\|interface.*DAO" persistence_project/repositories/

# Verify transaction management
grep -r "@Transactional\|beginTransaction\|commit\|rollback" persistence_project/

# Expected: All CRUD operations pass, migrations work bidirectionally, repositories follow patterns
# If failing: Fix database configuration, update connection strings, implement missing methods
```

### Level 3: Comprehensive Testing Validation
```bash
# Run full test suite with coverage reporting
cd persistence_project && npm run test:coverage -- --reporter=text-summary
# OR: ./mvnw test jacoco:report && cat target/site/jacoco/index.html
# OR: dotnet test --collect:"XPlat Code Coverage" --settings coverlet.runsettings

# Verify test coverage meets minimum threshold (>80% for persistence layer)
cd persistence_project && npm run test:coverage:check
# OR: ./mvnw jacoco:check
# OR: dotnet tool install -g dotnet-reportgenerator-globaltool && reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coverage

# Run integration tests with test containers/ephemeral databases
cd persistence_project && npm run test:integration
# OR: ./mvnw test -Dtest=*IntegrationTest* -Dtestcontainers.reuse.enable=true
# OR: dotnet test --filter="Category=Integration"

# Execute contract tests for schema compatibility
cd persistence_project && npm run test:contract
# OR: ./mvnw test -Dtest=*ContractTest*
# OR: dotnet test --filter="Category=Contract"

# Run performance tests for query optimization
cd persistence_project && npm run test:performance 2>&1 | grep -E "Query.*ms|Response time"
# OR: ./mvnw test -Dtest=*PerformanceTest* -Djmh.runner.jmhOutputFormat=text
# OR: dotnet test --filter="Category=Performance" --logger:console;verbosity=detailed

# Execute resilience/chaos testing
cd persistence_project && npm run test:resilience
# OR: ./mvnw test -Dtest=*ResilienceTest*
# OR: dotnet test --filter="Category=Resilience"

# Verify connection pool behavior under load
cd persistence_project && npm run test:connection-pool
# OR: ./mvnw test -Dtest=ConnectionPoolTest
# OR: dotnet test --filter="Category=ConnectionPool"

# Expected: >80% test coverage, all integration tests pass, performance within SLAs
# If failing: Increase test coverage, fix failing integration tests, optimize slow queries
```

### Level 4: Production Readiness Validation
```bash
# Verify security configurations
cd persistence_project && npm run security:audit
# OR: ./mvnw org.owasp:dependency-check-maven:check
# OR: dotnet list package --vulnerable --include-transitive

# Check for hardcoded secrets/credentials
grep -r -i "password\|secret\|key" --include="*.js" --include="*.java" --include="*.cs" persistence_project/ | grep -v "process.env\|System.getenv\|Configuration\|\${" || echo "No hardcoded secrets found"

# Verify encryption at rest and in transit
grep -r -i "encrypt\|tls\|ssl" persistence_project/config/
grep -r "sslMode\|ssl.*true\|TLS" persistence_project/

# Test backup and restore procedures
cd persistence_project && npm run backup:create && npm run backup:restore:test
# OR: ./mvnw exec:exec -Dexec.executable="pg_dump" && ./mvnw exec:exec -Dexec.executable="pg_restore"
# OR: dotnet run --project Scripts -- backup && dotnet run --project Scripts -- restore-test

# Verify observability and monitoring
grep -r -i "logger\|metrics\|trace\|monitor" persistence_project/
curl -s http://localhost:8080/actuator/health | jq .status
# OR: curl -s http://localhost:5000/health | grep -E "Healthy|200"

# Test failover and disaster recovery
cd persistence_project && npm run test:failover
# OR: ./mvnw test -Dtest=FailoverTest -Dchaos.enabled=true
# OR: dotnet test --filter="Category=FailoverTest"

# Verify production deployment readiness
cd persistence_project && npm run build:production && npm run deploy:staging
# OR: ./mvnw clean package -Pprod && docker build -t persistence-app .
# OR: dotnet publish -c Release && docker build -t persistence-app .

# Load testing for production capacity
cd persistence_project && npm run test:load -- --duration=300 --users=100
# OR: ./mvnw gatling:test -Dgatling.simulationClass=LoadTest
# OR: dotnet run --project LoadTests -- --duration=300 --concurrent-users=100

# Verify compliance and audit logging
grep -r -i "audit\|gdpr\|hipaa\|compliance" persistence_project/
cd persistence_project && npm run audit:compliance:check
# OR: ./mvnw verify -Pcompliance-check
# OR: dotnet test --filter="Category=Compliance"

# Expected: No security vulnerabilities, encryption enabled, backups tested, monitoring active
# If failing: Fix security issues, enable encryption, configure monitoring, test disaster recovery
```

## 🔍 Final Validation Checklist — Data & Persistence

### Data Model Completeness
- [ ] Entities / schemas are fully defined with clear typing
  - Java → JPA entities / Hibernate validators
  - .NET → EF Core entities + DataAnnotations
  - Node.js → Mongoose schemas / Sequelize models / Prisma schema
- [ ] Relationships, indexes, and constraints are implemented correctly
- [ ] Versioned schema migrations exist
  - Java → Liquibase / Flyway
  - .NET → EF Migrations
  - Node.js → Prisma Migrate / Sequelize Migrations / Knex
- [ ] Test datasets prepared for integration and E2E testing

### Validation & Type Safety
- [ ] Input validation before persistence layer
  - Java → Bean Validation (JSR 380)
  - .NET → FluentValidation / DataAnnotations
  - Node.js → Zod / Joi / class-validator
- [ ] Strong typing between DTOs and persistence entities
- [ ] Nullability, defaults, and constraints checked against DB schema

### Security & Compliance
- [ ] Sensitive fields encrypted at rest (passwords, tokens, PII)
- [ ] Proper hashing for credentials (bcrypt, Argon2, PBKDF2)
- [ ] Secrets (DB credentials, encryption keys) injected via env or vaults (never hardcoded)
- [ ] Data access control implemented (role-based, row/column-level if needed)
- [ ] Compliance rules enforced (GDPR/CCPA retention, audit logging)

### Reliability & Error Handling
- [ ] Transaction management tested
  - Java → Spring @Transactional / JTA
  - .NET → TransactionScope
  - Node.js → ORM transaction API (Sequelize, Prisma, TypeORM)
- [ ] Retry policies for transient DB failures in place
- [ ] Connection pool configurations validated under load
- [ ] Backup & restore documented and tested

### Performance & Scalability
- [ ] Indexes reviewed for frequent queries
- [ ] Query plans analyzed for heavy joins/aggregations
- [ ] Connection pooling tuned (HikariCP, EF Core pool, pg-pool/mysql2 in Node.js)
- [ ] Caching strategies applied (e.g., Redis for hot data)

## 🚫 Anti-Patterns to Avoid (Data & Persistence)

- ❌ Hardcoding DB credentials (must use env vars or secret manager)
- ❌ Skipping migrations in favor of manual schema changes
- ❌ Overloading ORM models with business logic
- ❌ Ignoring validation at persistence layer ("garbage in, garbage stored")
- ❌ Forgetting to close/release connections → leaks & pool exhaustion
- ❌ Using production DB for dev/test without isolation

RESEARCH STATUS: [TO BE COMPLETED]
– Collect concrete persistence best practices for Java, .NET, and Node.js implementations before coding begins.