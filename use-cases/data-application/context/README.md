# Data Application Context Modules

This directory contains modular, composable context files that are loaded dynamically based on application complexity tier.

## Philosophy

Instead of one massive context file, we use **progressive disclosure**:
- Load only what you need
- Compose modules for specific features
- Swap tech stacks without rewriting everything

## Structure

```
context/
├── README.md (this file)
├── core-principles.md          # Always loaded (50 lines)
├── tier1-simple-crud.md        # For simple apps (150 lines)
├── tier2-standard-app.md       # For standard apps (200 lines)
├── tier3-enterprise.md         # For enterprise apps (250 lines)
├── modules/                    # Feature-specific modules
│   ├── database-patterns.md    # DB design, indexing, migrations
│   ├── api-patterns.md         # REST API, pagination, error handling
│   ├── security-patterns.md    # Auth, encryption, security
│   ├── testing-patterns.md     # Unit, integration, load tests
│   └── deployment-patterns.md  # Docker, K8s, CI/CD
└── tech-stacks/                # Technology-specific implementations
    ├── java-spring.md          # Spring Boot specifics
    ├── nodejs-express.md       # Express.js specifics
    ├── python-fastapi.md       # FastAPI specifics (TODO)
    └── dotnet-aspnet.md        # ASP.NET Core specifics (TODO)
```

## Loading Strategy

### Tier 1: Simple CRUD (1-5 entities, 30-45 min)

```
Loaded Context:
- core-principles.md
- tier1-simple-crud.md
- modules/database-patterns.md
- tech-stacks/{selected}.md

Total: ~400 lines
```

### Tier 2: Standard REST API (5-10 entities, 60-90 min)

```
Loaded Context:
- core-principles.md
- tier2-standard-app.md
- modules/database-patterns.md
- modules/api-patterns.md
- modules/security-patterns.md
- modules/testing-patterns.md
- tech-stacks/{selected}.md

Total: ~750 lines
```

### Tier 3: Enterprise Application (10+ entities, 90-120 min)

```
Loaded Context:
- core-principles.md
- tier3-enterprise.md
- modules/database-patterns.md
- modules/api-patterns.md
- modules/security-patterns.md
- modules/testing-patterns.md
- modules/deployment-patterns.md
- tech-stacks/{selected}.md

Total: ~1100 lines
```

## Core Principles (Always Loaded)

Universal rules that apply to ALL data applications:

1. **Simplicity First** - YAGNI, start simple
2. **Type Safety & Validation** - Strong typing, validate at boundaries
3. **Security by Default** - No hardcoded secrets, encrypt sensitive data
4. **Data Integrity** - Use constraints, transactions, validation
5. **Testing Strategy** - Unit, integration, API tests
6. **Observability** - Structured logging, metrics, health checks
7. **Configuration Management** - Environment variables, no secrets in code
8. **Code Organization** - Separation of concerns, consistent naming
9. **Error Handling** - Graceful errors, appropriate status codes
10. **Performance Awareness** - Indexing, pagination, connection pooling

## Tier Guides

### tier1-simple-crud.md

**For**: Basic CRUD APIs (TODO app, simple blog, bookmark manager)

**Covers**:
- Simple 3-layer architecture (API → Service → Repository → DB)
- Basic entity design with relationships
- CRUD endpoint patterns
- Pagination and filtering
- Basic testing strategy
- Docker setup

### tier2-standard-app.md

**For**: Business applications (e-commerce, booking systems, CMS)

**Covers**:
- Authentication & authorization (JWT, RBAC)
- External API integrations (payment, email, storage)
- Caching strategy (Redis)
- Rate limiting
- Comprehensive testing
- Security best practices

### tier3-enterprise.md

**For**: Large-scale systems (POS, ERP, healthcare, financial platforms)

**Covers**:
- Complex architecture with message queues
- Multi-layer caching (L1: in-memory, L2: Redis)
- Multiple external integrations with adapters
- Advanced patterns (CQRS, event sourcing)
- Comprehensive monitoring & observability
- High availability & disaster recovery
- Multi-region deployment

## Feature Modules

These are mixed and matched based on requirements:

### database-patterns.md

- Schema design and normalization
- Indexing strategies
- Query optimization
- Connection pooling
- Migration best practices
- Repository pattern

### api-patterns.md

- RESTful design principles
- Request/response formats
- HTTP status codes
- Pagination, filtering, sorting
- API versioning
- Rate limiting
- Error handling
- OpenAPI documentation

### security-patterns.md

- Authentication (JWT, sessions)
- Authorization (RBAC, ABAC)
- Password hashing (bcrypt, argon2)
- SQL injection prevention
- XSS/CSRF protection
- Data encryption
- Secrets management
- Security headers

### testing-patterns.md

- Unit testing patterns
- Integration testing
- API testing
- Test containers (Docker)
- Mocking external APIs
- Load testing (k6, JMeter)
- Test data factories
- CI/CD integration

### deployment-patterns.md

- Docker containerization
- Docker Compose for local dev
- Kubernetes deployment
- Environment management
- CI/CD pipelines
- Monitoring & logging
- Database migrations
- Zero-downtime deployment
- Backup & disaster recovery

## Tech Stack Guides

These provide language/framework-specific implementation details:

### java-spring.md

- Spring Boot 3.x patterns
- JPA/Hibernate entities
- Spring Data repositories
- Spring Security
- Maven/Gradle setup
- Testing with JUnit 5 & TestContainers

### nodejs-express.md

- Express.js with TypeScript
- Prisma ORM
- Zod validation
- JWT authentication
- Testing with Jest & Supertest
- Dependency injection patterns

### python-fastapi.md (TODO)

- FastAPI patterns
- SQLAlchemy ORM
- Pydantic validation
- Testing with pytest

### dotnet-aspnet.md (TODO)

- ASP.NET Core patterns
- Entity Framework Core
- Data annotations
- Testing with xUnit

## Usage in Commands

### /data-app-init

Determines tier and loads appropriate context:

```typescript
if (tier === 'tier1') {
    load('context/core-principles.md');
    load('context/tier1-simple-crud.md');
    load('context/modules/database-patterns.md');
    load(`context/tech-stacks/${stack}.md`);
}
```

### /data-app-plan

Uses loaded context to create plan:
- Tier 1: Main Claude plans directly using context
- Tier 2: Main Claude plans with enhanced features
- Tier 3: Passes context to 3 parallel design agents

### Implementation

Main Claude uses all loaded context modules to guide implementation.

## Adding New Modules

To add a new module:

1. Create the module file (80-100 lines recommended)
2. Focus on one specific aspect
3. Include code examples
4. Add to appropriate tier loading logic
5. Update this README

Example:

```bash
# Create new module
touch context/modules/graphql-patterns.md

# Add content (80-100 lines)
# - GraphQL schema design
# - Resolvers
# - DataLoader pattern
# - Testing GraphQL APIs

# Update tier loading to include when needed
```

## Adding New Tech Stacks

To add a new tech stack guide:

1. Create tech stack file (200-250 lines)
2. Include project structure
3. Show key patterns with examples
4. Include testing examples
5. Update README

Example:

```bash
# Create new tech stack
touch context/tech-stacks/ruby-rails.md

# Add content:
# - Project structure
# - ActiveRecord patterns
# - Controller patterns
# - Testing with RSpec
# - Deployment
```

## Benefits of Modular Context

✅ **Progressive Disclosure** - Load only what you need

✅ **Maintainability** - Update one module, affects all tiers using it

✅ **Reusability** - Mix and match modules

✅ **Technology Flexibility** - Swap tech stacks easily

✅ **Scalability** - Add new modules without refactoring existing ones

✅ **Clarity** - Each file has a single, focused purpose

## Context Size Comparison

### Old System
- Single CLAUDE.md: 696 lines
- Loaded for every request
- Tech-specific content mixed with general patterns

### New System
- **Tier 1**: ~400 lines (43% less)
- **Tier 2**: ~750 lines (similar, but better organized)
- **Tier 3**: ~1100 lines (58% more, but appropriate for complexity)

The key difference: Context matches complexity!
