---
name: "Tier 2 Standard REST API PRP Template"
description: "Template for generating PRPs for standard REST APIs with auth, caching, and integrations (5-10 entities)"
---

## Purpose

Build a production-ready REST API with authentication, caching, external integrations, and comprehensive testing.

**Target**: 5-10 entities, 60-90 minutes implementation time

## Core Principles

1. **Production Ready**: Authentication, security, caching, monitoring
2. **Well Architected**: Clear separation of concerns, maintainable code
3. **External Integration**: Pattern for connecting to 1-3 external services
4. **Performance**: Caching strategy for hot data
5. **Comprehensive Testing**: Unit, integration, and API tests

## Goal

[Detailed description of the application purpose and key functionality]

## Entities

### Core Entities (5-10 total)

#### Entity 1: User
- id (UUID/Integer primary key)
- email (unique, not null)
- password_hash (not null)
- name (not null)
- role (enum: admin, user, etc.)
- created_at, updated_at
- deleted_at (soft delete)

#### Entity 2: [Business Entity]
- id (primary key)
- user_id (foreign key to users)
- [business fields...]
- status (enum)
- created_at, updated_at, deleted_at

[Define 5-10 entities total with relationships]

## Relationships

- User has many [Entity 2]
- [Entity 2] belongs to User
- [Entity 3] has many [Entity 4] through [Join Table]

## Authentication & Authorization

### Authentication
- **Method**: JWT (JSON Web Tokens)
- **Access Token**: Short-lived (15 minutes)
- **Refresh Token**: Long-lived (7 days)
- **Password**: Hashed with bcrypt/argon2

### Authorization
- **Model**: Role-Based Access Control (RBAC)
- **Roles**: admin, manager, user
- **Permissions**: resource:action (e.g., orders:write)

### Protected Endpoints
```
Public:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh

Protected (requires valid JWT):
- All other endpoints
- Authorization by role/permission
```

## External Integrations

### Integration 1: [Payment Gateway / Email Service / etc.]
- **Purpose**: [What it does]
- **API**: [Stripe / SendGrid / etc.]
- **Operations**:
  - Operation 1: [e.g., Create payment intent]
  - Operation 2: [e.g., Confirm payment]
- **Error Handling**: Retry with exponential backoff
- **Testing**: Mock with WireMock/nock

### Integration 2: [Cloud Storage / etc.]
- **Purpose**: [What it does]
- **API**: [AWS S3 / Cloudinary / etc.]
- **Operations**:
  - Upload file
  - Generate signed URL
  - Delete file

[Define 1-3 integrations]

## Caching Strategy

### Cache Layers
- **L1 (In-Memory)**: Hot data, 5-minute TTL
- **L2 (Redis)**: Warm data, 1-hour TTL

### Cached Data
- User profiles (5 min)
- Product catalogs (15 min)
- Category lists (1 hour)
- Static configuration (24 hours)

### Cache Invalidation
- On update: Invalidate specific key
- On delete: Invalidate key and related lists
- On create: Invalidate lists only

## API Endpoints

### Authentication
```
POST   /api/auth/register      - Register new user
POST   /api/auth/login         - Login (returns JWT)
POST   /api/auth/refresh       - Refresh access token
POST   /api/auth/logout        - Logout (invalidate refresh token)
GET    /api/auth/me            - Get current user
```

### Entity Endpoints (CRUD + Advanced)
```
GET    /api/entity?page=1&limit=20&sort=created_at:desc&filter[status]=active
GET    /api/entity/:id
POST   /api/entity
PUT    /api/entity/:id
PATCH  /api/entity/:id
DELETE /api/entity/:id
```

[Define endpoints for all 5-10 entities]

## Technology Stack

**Selected**: [Java/Spring Boot | Node.js/Express | Python/FastAPI | .NET/ASP.NET]

**Database**: PostgreSQL with connection pooling

**Cache**: Redis

**Testing**: [JUnit + MockMvc + TestContainers | Jest + Supertest | pytest | xUnit]

**External API Mocking**: [WireMock | nock | responses]

## Implementation Blueprint

### Task 1: Database Schema & Migrations (10 minutes)
```
1. Design normalized schema for 5-10 entities
2. Add proper indexes for common queries
3. Create migration files with rollback
4. Add constraints (foreign keys, unique, not null)
5. Implement soft deletes where needed
6. Add audit fields (created_by, updated_by)
7. Create seed data for development
```

### Task 2: Authentication System (15 minutes)
```
1. Create User entity and repository
2. Implement password hashing (bcrypt/argon2)
3. Create JWT service:
   - Generate access token
   - Generate refresh token
   - Verify token
   - Rotate tokens
4. Create authentication middleware
5. Implement registration endpoint
6. Implement login endpoint
7. Implement refresh token endpoint
8. Add role-based authorization middleware
```

### Task 3: Data Access Layer (10 minutes)
```
1. Create repository for each entity
2. Implement CRUD operations
3. Add pagination, filtering, sorting
4. Implement soft delete logic
5. Add transaction support
6. Create database indexes
```

### Task 4: Business Logic Layer (15 minutes)
```
1. Create service for each entity
2. Implement validation logic
3. Add business rules
4. Integrate with external services
5. Implement retry logic for external calls
6. Add comprehensive error handling
7. Implement audit logging
```

### Task 5: External Integrations (15 minutes)
```
1. Create client for each external API
2. Implement adapter pattern
3. Add retry with exponential backoff
4. Implement circuit breaker (optional)
5. Add timeout handling
6. Log all external API calls
7. Create mock implementations for testing
```

### Task 6: Caching Layer (10 minutes)
```
1. Set up Redis connection
2. Implement cache service:
   - get(key)
   - set(key, value, ttl)
   - delete(key)
   - deletePattern(pattern)
3. Add caching to frequently accessed data
4. Implement cache-aside pattern
5. Add cache invalidation on mutations
```

### Task 7: API Controllers (15 minutes)
```
1. Create controller for each entity
2. Implement all CRUD endpoints
3. Add authentication middleware
4. Add authorization checks
5. Implement pagination, filtering, sorting
6. Add rate limiting
7. Add input validation
8. Implement proper error responses
9. Add OpenAPI/Swagger documentation
```

### Task 8: Comprehensive Testing (15 minutes)
```
1. Unit tests for services (mock repositories)
2. Integration tests for repositories (test DB)
3. API tests for all endpoints
4. Authentication/authorization tests
5. External integration tests (with mocks)
6. Cache tests
7. Validation tests
8. Error scenario tests
9. Aim for >80% coverage
```

### Task 9: Docker & Deployment (10 minutes)
```
1. Create Dockerfile with multi-stage build
2. Create docker-compose.yml:
   - Application service
   - PostgreSQL service
   - Redis service
3. Create .env.example with all variables
4. Add health check endpoint
5. Add graceful shutdown
6. Test full stack with docker-compose
```

### Task 10: Documentation & Security (10 minutes)
```
1. Create comprehensive README
2. Document all API endpoints
3. Add setup instructions
4. Document environment variables
5. Add security headers (helmet)
6. Implement CORS properly
7. Add request logging
8. Create API documentation (Swagger)
```

## Validation Commands

### Linting & Type Checking
```bash
npm run lint && npm run type-check  # Node.js
mvn checkstyle:check               # Java
ruff check . && mypy .             # Python
dotnet format --verify-no-changes  # .NET
```

### Unit Tests
```bash
npm run test:unit                  # Node.js
mvn test                           # Java
pytest tests/unit                  # Python
dotnet test --filter Category=Unit # .NET
```

### Integration Tests
```bash
npm run test:integration           # Node.js
mvn verify                         # Java
pytest tests/integration           # Python
dotnet test --filter Category=Integration # .NET
```

### Security Scan
```bash
npm audit                          # Node.js
mvn dependency-check:check         # Java
safety check                       # Python
dotnet list package --vulnerable   # .NET
```

### Test with Docker
```bash
docker-compose up -d
# Wait for services to be ready
sleep 10
# Run health check
curl http://localhost:3000/health
# Run API tests against Docker stack
npm run test:api
# Cleanup
docker-compose down
```

## Success Criteria

- [ ] All {X} entities implemented with proper schema
- [ ] Authentication working (register, login, refresh, logout)
- [ ] Authorization enforced (RBAC)
- [ ] All CRUD operations working
- [ ] External integrations tested (with mocks)
- [ ] Caching implemented and working
- [ ] Pagination, filtering, sorting working
- [ ] Rate limiting configured
- [ ] Tests passing (>80% coverage)
- [ ] Security scan clean (no vulnerabilities)
- [ ] Docker compose works
- [ ] API documented (Swagger/OpenAPI)
- [ ] README complete
- [ ] No hardcoded secrets

## API Examples

### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

Response: 201 Created
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  },
  "tokens": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  },
  "tokens": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

### Protected Endpoint
```bash
GET /api/entity?page=1&limit=20&sort=created_at:desc
Authorization: Bearer eyJhbGc...

Response: 200 OK
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

### Unauthorized Error
```bash
GET /api/entity
# No Authorization header

Response: 401 Unauthorized
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "No token provided"
  }
}
```

### Forbidden Error
```bash
DELETE /api/users/123
Authorization: Bearer eyJhbGc...  # user role, not admin

Response: 403 Forbidden
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions"
  }
}
```

## File Structure

```
project/
├── src/
│   ├── models/              # Database entities
│   ├── repositories/        # Data access
│   ├── services/            # Business logic
│   ├── controllers/         # API endpoints
│   ├── middleware/          # Auth, validation, logging
│   ├── integrations/        # External API clients
│   │   ├── payment/
│   │   ├── email/
│   │   └── storage/
│   ├── cache/              # Caching logic
│   ├── validators/         # Input validation
│   ├── types/              # TypeScript types
│   └── index.[ext]         # Entry point
├── tests/
│   ├── unit/               # Service tests
│   ├── integration/        # DB tests
│   ├── api/               # API endpoint tests
│   └── fixtures/          # Test data
├── migrations/             # Database migrations
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── package.json / pom.xml / requirements.txt
```

## Environment Variables

```bash
# Application
PORT=3000
NODE_ENV=production
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# JWT
JWT_SECRET=your-secret-key-min-32-characters
JWT_EXPIRATION=900
JWT_REFRESH_SECRET=your-refresh-secret-key
JWT_REFRESH_EXPIRATION=604800

# External Services
STRIPE_API_KEY=sk_test_...
SENDGRID_API_KEY=SG...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

## Performance Requirements

- **Response Time**: p95 < 200ms, p99 < 500ms
- **Throughput**: > 100 requests/second
- **Error Rate**: < 1%
- **Cache Hit Ratio**: > 70% for hot data

## Security Requirements

- [ ] HTTPS only in production
- [ ] Strong password hashing (bcrypt rounds >= 12)
- [ ] JWT tokens with short expiration
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection (input sanitization, output escaping)
- [ ] CSRF protection
- [ ] Rate limiting configured
- [ ] Security headers (helmet)
- [ ] CORS properly configured
- [ ] No secrets in code or version control

---

## Implementation Time Estimate

- Database Schema: 10 min
- Authentication System: 15 min
- Data Access Layer: 10 min
- Business Logic: 15 min
- External Integrations: 15 min
- Caching Layer: 10 min
- API Controllers: 15 min
- Testing: 15 min
- Docker & Deployment: 10 min
- Documentation: 10 min

**Total: 125 minutes** (with buffer: 60-90 minutes with parallel work)

## Confidence Score

Rate the completeness of this PRP: **[1-10]**

A score of 8+ means the implementation should succeed in one pass without additional research.
