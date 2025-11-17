---
name: "Tier 3 Enterprise Application PRP Template"
description: "Template for generating PRPs for enterprise-grade applications with complex integrations (10+ entities)"
---

## Purpose

Build a production-ready enterprise application with complex business logic, multiple external integrations, message queues, comprehensive monitoring, and full operational readiness.

**Target**: 10+ entities, 90-120 minutes implementation time

**Note**: This template extends `prp_data_application_base.md` with enterprise-specific requirements.

## Core Principles

1. **Enterprise-Grade**: Production-ready with high availability, monitoring, and disaster recovery
2. **Complex Integration**: 5+ external systems with sophisticated integration patterns
3. **Scalability First**: Designed for horizontal scaling, partitioning, and high throughput
4. **Comprehensive Security**: Multi-layered security, compliance (GDPR, HIPAA, etc.)
5. **Full Observability**: Distributed tracing, comprehensive metrics, centralized logging
6. **Operational Excellence**: CI/CD, IaC, automated testing, disaster recovery

## Goal

[Comprehensive description of the enterprise application, business context, and strategic objectives]

## Business Context

### Industry: [Retail / Healthcare / Financial Services / etc.]
### Use Case: [POS System / Patient Management / Trading Platform / etc.]
### Scale:
- Users: [X concurrent users]
- Transactions: [Y per day/hour]
- Data Volume: [Z GB/TB]
- Geographic: [regions/countries]

## Domain Model (10+ Entities)

### Core Business Entities

#### Entity 1: [Primary Business Entity]
- Complex business logic
- Audit trail requirements
- Multi-tenant considerations
- Soft delete + archival strategy

#### Entity 2-10: [Additional Entities]
[Define 10+ entities with rich relationships]

### Aggregate Roots & Bounded Contexts
- **Context 1**: [e.g., Order Management]
  - Entities: Order, OrderItem, OrderStatus
  - Aggregates: Order (root), OrderItem (child)
- **Context 2**: [e.g., Inventory]
  - Entities: Product, Stock, Warehouse
  - Aggregates: Product (root), Stock (child)

[Define 3-5 bounded contexts]

## Complex Relationships

- Multi-level hierarchies
- Many-to-many with metadata
- Temporal relationships
- Cross-context relationships

## Enterprise Architecture

### Layered Architecture
```
┌─────────────────────────────────────────────────────┐
│  API Gateway + Load Balancer                        │
├─────────────────────────────────────────────────────┤
│  REST APIs + GraphQL + WebSocket + Batch           │
├─────────────────────────────────────────────────────┤
│  Business Services + Workflow Orchestration          │
├─────────────────────────────────────────────────────┤
│  Integration Layer (Adapters, Clients, Mappers)     │
├───────────────┬──────────────┬──────────────────────┤
│ Multi-Layer   │ Data Access  │ Event Bus            │
│ Caching       │ (Repository) │ (Kafka/RabbitMQ)     │
├───────────────┴──────────────┴──────────────────────┤
│  Database (RDBMS) + Read Replicas + Partitioning    │
├─────────────────────────────────────────────────────┤
│  Monitoring + Distributed Tracing + Audit Logs      │
└─────────────────────────────────────────────────────┘
```

## External System Integrations (5+)

### Integration 1: ERP System (e.g., Microsoft Dynamics 365)
- **Purpose**: Master data synchronization, financial posting
- **Protocol**: REST API + SOAP (legacy)
- **Patterns**:
  - Adapter: ERPAdapter.java
  - Client: D365ApiClient.java
  - Mapper: ERPDataMapper.java
- **Operations**:
  - Sync customers, products, orders
  - Post financial transactions
  - Real-time inventory updates
- **Resilience**: Circuit breaker, retry with exponential backoff
- **Testing**: WireMock for E2E testing

### Integration 2: Payment Gateway (Stripe/PayPal/etc.)
- **Purpose**: Payment processing
- **Operations**: Create payment intent, confirm payment, refund
- **Security**: PCI-DSS compliance, tokenization
- **Webhook**: Handle payment status events

### Integration 3: Fiscal Compliance (e.g., Fiscal Printer, KSEF)
- **Purpose**: Regulatory compliance for receipts/invoices
- **Protocol**: Custom protocol, REST API
- **Operations**: Issue fiscal receipt, cancel receipt, daily report
- **Requirements**: Sequence integrity, tamper-proof storage

### Integration 4: Email/SMS Service (SendGrid, Twilio)
- **Purpose**: Customer notifications
- **Operations**: Transactional emails, SMS notifications
- **Patterns**: Template management, queue-based sending

### Integration 5: Cloud Storage (AWS S3, Azure Blob)
- **Purpose**: Document storage, media files
- **Operations**: Upload, download, generate signed URLs, lifecycle policies

[Define 5-10 integrations with detailed patterns]

## Message Queue Architecture

### Event Bus (Kafka / RabbitMQ)

#### Topics/Queues
- **orders.events**: Order lifecycle events
- **inventory.events**: Stock changes, restock alerts
- **customer.events**: Customer profile changes
- **payment.events**: Payment status updates

#### Producers
- OrderEventProducer: Publishes order events
- InventoryEventProducer: Publishes inventory events

#### Consumers
- InventoryConsumer: Listens to orders, reserves stock
- NotificationConsumer: Sends emails/SMS on events
- AnalyticsConsumer: Streams to data warehouse

#### Patterns
- Event Sourcing (where applicable)
- CQRS for read/write separation
- Saga pattern for distributed transactions

## Multi-Layer Caching Strategy

### L1: In-Memory Cache (Caffeine / Local)
- **TTL**: 10-30 seconds
- **Data**: Hot user sessions, active cart data
- **Size**: Limited per instance

### L2: Distributed Cache (Redis)
- **TTL**: 5-60 minutes
- **Data**: User profiles, product catalogs, session data
- **Patterns**: Cache-aside, write-through

### L3: CDN (CloudFlare / AWS CloudFront)
- **TTL**: Hours to days
- **Data**: Static assets, product images, public content

### Cache Invalidation
- **On Update**: Invalidate all cache layers
- **On Delete**: Invalidate key and related data
- **Pattern**: Cache stampede prevention with locks

## Authentication & Authorization

### Multi-Tenant Authentication
- **JWT**: With tenant_id claim
- **SSO**: Integration with corporate identity provider (OAuth2, SAML)
- **MFA**: Two-factor authentication for sensitive operations

### Fine-Grained Authorization
- **RBAC**: Role-based access control
- **ABAC**: Attribute-based (tenant, region, department)
- **Permission Matrix**: By role, resource, and action
- **Row-Level Security**: Database-level tenant isolation

## Security & Compliance

### Data Protection
- **Encryption at Rest**: Database encryption, file storage encryption
- **Encryption in Transit**: TLS 1.3, certificate management
- **PII/PHI Handling**: Tokenization, masking, audit trails

### Compliance Requirements
- **GDPR**: Data export, right to be forgotten, consent management
- **HIPAA** (if applicable): Access controls, audit logging, encryption
- **PCI-DSS** (if payments): Tokenization, no card data storage
- **SOX** (if financial): Audit trails, segregation of duties

### Audit Logging
- **What**: All data changes, access attempts, admin actions
- **Where**: Dedicated audit database, immutable logs
- **Retention**: 7 years (regulatory requirement)

## Monitoring & Observability

### Metrics (Prometheus + Grafana)
- **Application**: Request rate, response time, error rate
- **Business**: Orders/hour, revenue, active users
- **Infrastructure**: CPU, memory, disk, network
- **Cache**: Hit/miss ratio, evictions
- **Database**: Connection pool, slow queries, replication lag
- **External**: API call latency, success/failure rates

### Distributed Tracing (Jaeger / Zipkin)
- **Trace All**: User requests through all services
- **Span Tags**: user_id, tenant_id, order_id, etc.
- **Performance**: Identify bottlenecks across services

### Centralized Logging (ELK Stack / Loki)
- **Structured JSON**: All logs in consistent format
- **Correlation IDs**: Trace requests across services
- **Log Levels**: Debug, info, warn, error
- **Retention**: 90 days hot, 1 year cold storage

### Alerting
- **Critical**: Payment failures, database down, API errors > 1%
- **Warning**: High latency, cache miss rate, disk space
- **Info**: Deployment events, scaling events

## Deployment Architecture

### Containerization (Docker)
- Multi-stage builds for optimization
- Health checks, liveness, readiness probes
- Resource limits (CPU, memory)
- Non-root user for security

### Orchestration (Kubernetes)
- **Deployments**: Rolling updates, rollback capability
- **Services**: ClusterIP, Load Balancer
- **ConfigMaps**: Application configuration
- **Secrets**: Sensitive credentials
- **HPA**: Horizontal Pod Autoscaler (CPU/memory based)
- **PDB**: Pod Disruption Budgets for availability

### Infrastructure as Code
- **Terraform**: Cloud resources (AWS/Azure/GCP)
- **Helm**: Kubernetes package management
- **ArgoCD**: GitOps deployment

### CI/CD Pipeline
- **Build**: Compile, lint, security scan
- **Test**: Unit, integration, E2E
- **Deploy**: Dev → Staging → Production
- **Rollback**: Automated rollback on failures
- **Blue-Green**: Zero-downtime deployments

## High Availability & Disaster Recovery

### Database
- **Primary-Replica**: Read replicas for scaling
- **Automated Backups**: Daily full, hourly incremental
- **Point-in-Time Recovery**: 7-day retention
- **Cross-Region Replication**: For disaster recovery

### Application
- **Multiple Replicas**: Minimum 3 pods per service
- **Auto-Scaling**: Based on CPU/memory/custom metrics
- **Circuit Breakers**: Prevent cascade failures
- **Rate Limiting**: Protect from DDoS, API abuse

### Recovery Objectives
- **RTO** (Recovery Time Objective): < 1 hour
- **RPO** (Recovery Point Objective): < 15 minutes

## Testing Strategy

### Unit Tests (>80% coverage)
- All business logic
- All service methods
- Validation logic
- Mocked dependencies

### Integration Tests
- Database operations with TestContainers
- Message queue processing
- Cache operations
- API integration (with WireMock)

### API Tests
- All endpoints (happy path + error cases)
- Authentication/authorization
- Pagination, filtering, sorting
- Rate limiting

### Performance Tests (JMeter / Gatling / k6)
- **Load Test**: Sustained load (100-500 concurrent users)
- **Stress Test**: Find breaking point (gradual increase to 1000+)
- **Spike Test**: Sudden traffic surge
- **Endurance Test**: Extended period (24 hours)

### Security Tests
- **OWASP Top 10**: SQL injection, XSS, CSRF, etc.
- **Penetration Testing**: External security audit
- **Dependency Scanning**: npm audit, OWASP Dependency-Check

## Implementation Blueprint

### Phase 1: Core Infrastructure (15 min)
- Database schema with all entities
- Migration framework setup
- Docker and docker-compose configuration
- Basic CI/CD pipeline

### Phase 2: Data & Business Layer (20 min)
- All entities and repositories
- All business services
- Transaction management
- Audit logging

### Phase 3: Integration Layer (25 min)
- Adapters for all 5+ external systems
- API clients with retry logic
- Circuit breaker implementation
- Message queue producers/consumers
- Integration testing with WireMock

### Phase 4: API Layer (15 min)
- All REST endpoints
- Authentication & authorization
- Input validation
- API documentation (OpenAPI)
- Rate limiting

### Phase 5: Caching & Performance (10 min)
- Multi-layer cache setup
- Cache warming strategies
- Cache invalidation logic
- Performance tuning

### Phase 6: Monitoring & Operations (15 min)
- Prometheus metrics
- Distributed tracing
- Centralized logging
- Health checks and readiness probes
- Alerting rules

### Phase 7: Testing (20 min)
- Unit tests (all services)
- Integration tests (all integrations)
- API tests (all endpoints)
- Performance tests
- Security scans

### Phase 8: Deployment & Documentation (10 min)
- Kubernetes manifests
- Helm charts
- Infrastructure as code
- Comprehensive README
- API documentation
- Runbooks

## Validation Commands

### Build & Lint
```bash
mvn clean verify
npm run lint && npm run type-check
```

### Unit Tests
```bash
mvn test
npm run test:unit
```

### Integration Tests
```bash
mvn verify -P integration-tests
npm run test:integration
```

### Performance Tests
```bash
k6 run tests/load/scenario.js
mvn gatling:test
```

### Security Scan
```bash
mvn org.owasp:dependency-check-maven:check
npm audit
```

### Docker Build & Test
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Success Criteria

### Functional
- [ ] All 10+ entities implemented
- [ ] All business logic working
- [ ] All 5+ integrations tested
- [ ] Message queue processing functional
- [ ] Authentication & authorization complete
- [ ] Multi-tenant isolation working

### Performance
- [ ] Load test passed (p95 < 200ms, p99 < 500ms)
- [ ] Throughput > 1000 req/s
- [ ] Cache hit ratio > 70%
- [ ] External API calls < 5% of total latency

### Security
- [ ] Security scan clean (0 high/critical vulnerabilities)
- [ ] All secrets in vault/env vars
- [ ] Encryption at rest and in transit
- [ ] Audit logging complete
- [ ] Compliance requirements met

### Operations
- [ ] All services containerized
- [ ] Kubernetes manifests ready
- [ ] Monitoring dashboards configured
- [ ] Alerts defined and tested
- [ ] Disaster recovery tested
- [ ] Documentation complete

### Testing
- [ ] Unit test coverage > 80%
- [ ] All integration tests passing
- [ ] API tests passing
- [ ] Performance tests meeting SLAs
- [ ] Security tests clean

## File Structure

```
enterprise-app/
├── src/main/java/
│   ├── entity/              # 10+ JPA entities
│   ├── repository/          # Data repositories
│   ├── service/             # Business services
│   ├── controller/          # REST controllers
│   ├── dto/                 # Data transfer objects
│   ├── mapper/              # Entity-DTO mappers
│   ├── config/              # App configuration
│   ├── security/            # Auth & authorization
│   ├── cache/               # Multi-layer caching
│   ├── monitoring/          # Metrics & health
│   ├── integration/         # External integrations
│   │   ├── adapter/         # System adapters (5+)
│   │   ├── client/          # API clients
│   │   ├── mapper/          # Data mappers
│   │   ├── processor/       # Event processors
│   │   └── webhook/         # Webhook handlers
│   ├── messaging/           # Message queue
│   │   ├── producer/        # Event publishers
│   │   ├── consumer/        # Event consumers
│   │   └── event/          # Event definitions
│   └── batch/              # Batch jobs
│       ├── job/            # Job definitions
│       └── step/           # Job steps
├── src/test/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   ├── api/               # API tests
│   ├── performance/       # Load tests
│   └── resources/
│       ├── wiremock/      # External API mocks
│       └── testdata/      # Test fixtures
├── deployment/
│   ├── kubernetes/        # K8s manifests
│   ├── helm/             # Helm charts
│   └── terraform/        # Infrastructure as code
├── docker-compose.yml            # Local dev
├── docker-compose.test.yml       # Test environment
├── Dockerfile
├── .env.example
└── docs/
    ├── api/              # OpenAPI specs
    ├── integration/      # Integration guides
    ├── deployment/       # Deployment guides
    └── runbooks/        # Operational runbooks
```

## Environment Variables (Comprehensive)

```bash
# Application
PORT=8080
NODE_ENV=production
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
HIKARI_MAXIMUM_POOL_SIZE=20
HIKARI_MINIMUM_IDLE=5

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
CACHE_TTL_L1=30
CACHE_TTL_L2=1800

# JWT
JWT_SECRET=your-secret-key-min-32-characters
JWT_EXPIRATION=900
JWT_REFRESH_SECRET=your-refresh-secret-key
JWT_REFRESH_EXPIRATION=604800

# External Systems (5+)
ERP_API_URL=https://erp.example.com/api
ERP_API_KEY=
PAYMENT_GATEWAY_URL=
PAYMENT_GATEWAY_KEY=
FISCAL_PRINTER_HOST=
EMAIL_SERVICE_API_KEY=
STORAGE_BUCKET_NAME=

# Message Queue
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672

# Monitoring
PROMETHEUS_ENABLED=true
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831
SENTRY_DSN=

# Compliance
TENANT_ID=
GDPR_ENABLED=true
AUDIT_LOG_RETENTION_DAYS=2555
```

---

## Implementation Time Estimate

- Core Infrastructure: 15 min
- Data & Business Layer: 20 min
- Integration Layer: 25 min
- API Layer: 15 min
- Caching & Performance: 10 min
- Monitoring & Operations: 15 min
- Testing: 20 min
- Deployment & Documentation: 10 min

**Total: 130 minutes** (with buffer and parallel work: 90-120 minutes)

## Confidence Score

Rate the completeness of this PRP: **[1-10]**

For enterprise apps, a score of 9+ is needed for successful one-pass implementation.
Score should account for:
- Completeness of requirements
- Clarity of integration patterns
- Testing strategy comprehensiveness
- Operational readiness
- Security and compliance coverage
