# Tier 3: Enterprise Applications

## When to Use This Tier

- **10+ entities** with complex relationships
- **5+ external integrations** (ERP, CRM, payment systems, fiscal printers, etc.)
- **Multi-region/multi-tenant** requirements
- **Regulatory compliance** (GDPR, HIPAA, fiscal regulations)
- **High availability & scalability** requirements
- **Advanced features** (event sourcing, CQRS, message queues, complex workflows)
- **Development time: 90-120 minutes**

## Examples
- Point of Sale (POS) systems with ERP integration
- Healthcare management systems
- Financial trading platforms
- Multi-tenant SaaS platforms
- Supply chain management systems

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  API Gateway + Load Balancer                                │
├─────────────────────────────────────────────────────────────┤
│  REST APIs + GraphQL + WebSocket + Batch Processing         │
├─────────────────────────────────────────────────────────────┤
│  Business Services + Workflow Orchestration                  │
├─────────────────────────────────────────────────────────────┤
│  Integration Layer (Adapters, Clients, Mappers)             │
├───────────────┬──────────────┬──────────────┬───────────────┤
│ Multi-Layer   │ Data Access  │ Event Bus    │ External APIs │
│ Caching       │ (Repository) │ (Kafka/AMQP) │ (10+ systems) │
├───────────────┴──────────────┴──────────────┴───────────────┤
│  Database (RDBMS) + Read Replicas + Partitioning            │
├─────────────────────────────────────────────────────────────┤
│  Monitoring + Distributed Tracing + Audit Logs              │
└─────────────────────────────────────────────────────────────┘
```

## Parallel Architecture Design Approach

For enterprise applications, use **3 parallel design agents** to create comprehensive architecture:

### Agent 1: Data Persistence Architect
**Focus:** Database, caching, performance optimization
- Schema design with normalization and denormalization strategies
- Multi-layer caching (L1: in-memory, L2: Redis, L3: CDN)
- Query optimization and indexing strategies
- Connection pooling and resource management
- Read replicas and partitioning for scale
- Backup and disaster recovery

### Agent 2: API & Integration Specialist
**Focus:** External interfaces, integrations, messaging
- REST API design with versioning
- External system integrations (ERP, CRM, payment gateways, etc.)
- Message queue architecture (Kafka, RabbitMQ, etc.)
- Authentication and authorization across all interfaces
- WebSocket for real-time features
- Webhook handlers for external events
- API rate limiting and circuit breakers

### Agent 3: Platform & Deployment Engineer
**Focus:** Infrastructure, monitoring, operations
- Docker containerization with health checks
- Kubernetes deployment with auto-scaling
- CI/CD pipeline with automated testing
- Infrastructure as code (Terraform/Helm)
- Comprehensive monitoring (Prometheus, Grafana, Jaeger)
- Centralized logging (ELK stack)
- Disaster recovery and high availability

## File Structure

```
enterprise-app/
├── src/main/java/                    # Or your language
│   ├── entity/                       # JPA entities
│   ├── repository/                   # Data repositories
│   ├── service/                      # Business services
│   ├── controller/                   # REST controllers
│   ├── dto/                          # Data transfer objects
│   ├── mapper/                       # Entity-DTO mappers
│   ├── config/                       # Application config
│   ├── security/                     # Auth & authorization
│   ├── cache/                        # Caching services
│   ├── monitoring/                   # Metrics & health
│   ├── integration/                  # External integrations
│   │   ├── adapter/                  # System adapters
│   │   │   ├── ERPAdapter.java
│   │   │   ├── PaymentAdapter.java
│   │   │   └── FiscalPrinterAdapter.java
│   │   ├── client/                   # API clients
│   │   ├── mapper/                   # Data mappers
│   │   ├── processor/                # Event processors
│   │   └── webhook/                  # Webhook handlers
│   ├── messaging/                    # Message queue
│   │   ├── producer/                 # Event publishers
│   │   ├── consumer/                 # Event consumers
│   │   └── event/                    # Event definitions
│   └── batch/                        # Batch jobs
│       ├── job/                      # Job definitions
│       └── step/                     # Job steps
├── src/main/resources/
│   ├── application.yml               # Config
│   ├── application-dev.yml           # Dev config
│   ├── application-prod.yml          # Prod config
│   ├── db/migration/                 # Flyway migrations
│   ├── wsdl/                         # SOAP definitions
│   └── integration/                  # Integration configs
├── src/test/
│   ├── unit/                         # Unit tests
│   ├── integration/                  # Integration tests
│   ├── api/                          # API tests
│   └── resources/
│       ├── wiremock/                 # Mock external APIs
│       └── testdata/                 # Test data
├── deployment/
│   ├── kubernetes/                   # K8s manifests
│   ├── helm/                         # Helm charts
│   └── terraform/                    # Infrastructure
├── docker-compose.yml                # Local dev stack
├── docker-compose.test.yml           # Test environment
├── Dockerfile                        # App container
├── .env.example                      # Environment template
└── docs/
    ├── api/                          # API docs
    ├── integration/                  # Integration guides
    └── deployment/                   # Ops guides
```

## Implementation Checklist

### 1. Requirements & Planning (15 min)
- [ ] Gather comprehensive requirements
- [ ] Identify all external systems
- [ ] Map compliance requirements
- [ ] Define SLAs and performance targets
- [ ] Create comprehensive INITIAL.md

### 2. Parallel Architecture Design (30 min)
**Run these 3 agents in parallel:**
- [ ] **Persistence Architect** → Database schema, caching, performance
- [ ] **API Integration Specialist** → REST APIs, external systems, messaging
- [ ] **Platform Engineer** → Docker, K8s, monitoring, CI/CD

### 3. Core Implementation (30 min)
- [ ] Implement domain entities and repositories
- [ ] Build business service layer
- [ ] Create REST API controllers
- [ ] Implement authentication/authorization
- [ ] Add caching layer
- [ ] Build integration adapters for external systems

### 4. Integration Development (15 min)
- [ ] Create clients for external APIs
- [ ] Implement message queue producers/consumers
- [ ] Build webhook handlers
- [ ] Add retry and circuit breaker patterns
- [ ] Implement data transformation mappers

### 5. Testing & Quality (20 min)
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests with WireMock
- [ ] API tests with realistic data
- [ ] Performance/load tests
- [ ] Security scanning

### 6. Operations & Deployment (10 min)
- [ ] Configure monitoring and alerting
- [ ] Set up distributed tracing
- [ ] Create deployment manifests
- [ ] Document runbooks
- [ ] Test disaster recovery

## External Integration Patterns

### Adapter Pattern for External Systems
```java
// integration/adapter/ERPAdapter.java
@Component
public class ERPAdapter {
    private final ERPApiClient client;
    private final CircuitBreaker circuitBreaker;
    private final RetryTemplate retryTemplate;

    public OrderResponse syncOrder(Order order) {
        return circuitBreaker.execute(() ->
            retryTemplate.execute(ctx -> {
                log.info("Syncing order {} to ERP (attempt {})",
                    order.getId(), ctx.getRetryCount());

                ERPOrderRequest request = mapper.toERPRequest(order);
                ERPOrderResponse response = client.createOrder(request);

                log.info("Order {} synced successfully to ERP", order.getId());
                return mapper.fromERPResponse(response);
            })
        );
    }
}
```

### Message Queue Pattern
```java
// messaging/producer/OrderEventProducer.java
@Component
public class OrderEventProducer {
    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        OrderEvent event = OrderEvent.builder()
            .eventId(UUID.randomUUID())
            .eventType("ORDER_CREATED")
            .aggregateId(order.getId())
            .timestamp(Instant.now())
            .payload(mapper.toEventPayload(order))
            .build();

        kafkaTemplate.send("orders.events", order.getId().toString(), event);
    }
}

// messaging/consumer/OrderEventConsumer.java
@Component
public class OrderEventConsumer {
    @KafkaListener(topics = "orders.events", groupId = "inventory-service")
    public void handleOrderEvent(OrderEvent event) {
        switch (event.getEventType()) {
            case "ORDER_CREATED":
                inventoryService.reserveStock(event.getPayload());
                break;
            case "ORDER_CANCELLED":
                inventoryService.releaseStock(event.getPayload());
                break;
        }
    }
}
```

### Webhook Handler Pattern
```java
// integration/webhook/PaymentWebhookHandler.java
@RestController
@RequestMapping("/webhooks")
public class PaymentWebhookHandler {
    @PostMapping("/payments/stripe")
    public ResponseEntity<Void> handleStripeWebhook(
            @RequestBody String payload,
            @RequestHeader("Stripe-Signature") String signature) {

        // Verify webhook signature
        if (!webhookVerifier.verify(payload, signature)) {
            return ResponseEntity.status(401).build();
        }

        // Process event asynchronously
        StripeEvent event = parser.parse(payload);
        eventPublisher.publish(event);

        return ResponseEntity.ok().build();
    }
}
```

## Multi-Layer Caching Strategy

### Cache Layers
```java
// cache/CacheService.java
@Service
public class CacheService {
    // L1: In-memory (Caffeine) - 10 seconds
    @Cacheable(value = "products", cacheManager = "l1CacheManager")
    public Product getProductL1(Long id) {
        return getProductL2(id);
    }

    // L2: Redis - 5 minutes
    @Cacheable(value = "products", cacheManager = "l2CacheManager")
    public Product getProductL2(Long id) {
        return productRepository.findById(id);
    }

    // Cache invalidation
    @CacheEvict(value = "products", allEntries = true,
        cacheManager = {"l1CacheManager", "l2CacheManager"})
    public void invalidateProductCache() {
        // Evicts from both cache layers
    }
}
```

## Security & Compliance

### Multi-Tenant Data Isolation
```java
@Entity
@Table(name = "orders")
@FilterDef(name = "tenantFilter",
    parameters = @ParamDef(name = "tenantId", type = "long"))
@Filter(name = "tenantFilter", condition = "tenant_id = :tenantId")
public class Order {
    @Id
    private Long id;

    @Column(name = "tenant_id", nullable = false)
    private Long tenantId;

    // Other fields...
}
```

### Audit Logging
```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Order {
    @CreatedBy
    private String createdBy;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedBy
    private String modifiedBy;

    @LastModifiedDate
    private Instant modifiedAt;
}
```

### GDPR Compliance
```java
// service/DataPrivacyService.java
@Service
public class DataPrivacyService {
    public void exportUserData(Long userId) {
        // Export all user data in machine-readable format
        UserDataExport export = aggregateUserData(userId);
        generateExportFile(export);
    }

    public void deleteUserData(Long userId) {
        // Hard delete or anonymize based on retention policy
        userRepository.anonymizeUser(userId);
        auditLog.logDeletion(userId, "GDPR_REQUEST");
    }
}
```

## Monitoring & Observability

### Metrics
```java
@Timed(value = "order.processing.time")
@Counted(value = "order.processing.count")
public Order processOrder(OrderRequest request) {
    // Business logic
    metricsRegistry.counter("orders.created",
        "region", request.getRegion()).increment();
    return order;
}
```

### Distributed Tracing
```java
@NewSpan("process-payment")
public PaymentResult processPayment(Payment payment) {
    Span span = tracer.currentSpan();
    span.tag("payment.amount", payment.getAmount().toString());
    span.tag("payment.currency", payment.getCurrency());

    try {
        PaymentResult result = paymentGateway.process(payment);
        span.tag("payment.status", result.getStatus());
        return result;
    } catch (Exception e) {
        span.tag("error", "true");
        span.tag("error.message", e.getMessage());
        throw e;
    }
}
```

### Health Checks
```java
@Component
public class ExternalSystemsHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        Map<String, Status> systems = new HashMap<>();

        systems.put("erp", checkERP());
        systems.put("payment", checkPaymentGateway());
        systems.put("database", checkDatabase());

        boolean allUp = systems.values().stream()
            .allMatch(s -> s == Status.UP);

        return allUp ? Health.up().withDetails(systems).build()
                    : Health.down().withDetails(systems).build();
    }
}
```

## Testing Strategy

### Integration Testing with Docker
```yaml
# docker-compose.test.yml
version: '3.8'
services:
  app:
    build: .
    depends_on:
      - postgres
      - redis
      - wiremock
    environment:
      - DATABASE_URL=postgresql://postgres:5432/testdb
      - REDIS_URL=redis://redis:6379
      - ERP_API_URL=http://wiremock:8080/erp

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: testdb

  redis:
    image: redis:7-alpine

  wiremock:
    image: wiremock/wiremock
    volumes:
      - ./src/test/resources/wiremock:/home/wiremock
```

### Load Testing
```bash
# Run JMeter tests
jmeter -n -t tests/load/order-flow.jmx \
  -l results.jtl \
  -e -o report/

# Performance SLAs
# - p95 response time < 200ms
# - p99 response time < 500ms
# - Throughput > 1000 req/s
# - Error rate < 0.1%
```

## Deployment Configuration

### Environment Variables (Comprehensive)
```bash
# .env.example

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
HIKARI_MAXIMUM_POOL_SIZE=20
HIKARI_MINIMUM_IDLE=5

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
CACHE_TTL=300

# Security
JWT_SECRET=your-secret-key-min-32-chars
JWT_EXPIRATION=3600
JWT_REFRESH_EXPIRATION=604800

# External Integrations
ERP_API_URL=https://erp.example.com/api
ERP_API_KEY=
PAYMENT_GATEWAY_URL=
PAYMENT_GATEWAY_KEY=
FISCAL_PRINTER_HOST=

# Messaging
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672

# Monitoring
PROMETHEUS_ENABLED=true
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831

# Application
PORT=8080
NODE_ENV=production
LOG_LEVEL=info
```

## Success Criteria

- ✅ All business requirements implemented
- ✅ External integrations tested with WireMock
- ✅ Multi-layer caching working
- ✅ Message queue processing functional
- ✅ Authentication & authorization complete
- ✅ Tests pass (>80% coverage)
- ✅ Load tests meet SLAs
- ✅ Security scan clean
- ✅ Monitoring dashboards configured
- ✅ Distributed tracing working
- ✅ High availability tested
- ✅ Disaster recovery documented
- ✅ Compliance requirements met
- ✅ API documentation complete
- ✅ Deployment automation working
