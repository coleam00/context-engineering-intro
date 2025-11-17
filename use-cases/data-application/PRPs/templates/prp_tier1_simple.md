---
name: "Tier 1 Simple CRUD PRP Template"
description: "Template for generating PRPs for simple CRUD applications (1-5 entities)"
---

## Purpose

Build a simple CRUD application with basic database operations and REST API endpoints.

**Target**: 1-5 entities, 30-45 minutes implementation time

## Core Principles

1. **Keep It Simple**: No over-engineering, basic patterns only
2. **CRUD Focus**: Standard Create, Read, Update, Delete operations
3. **Type Safety**: Use strong typing and validation
4. **Basic Testing**: Unit tests for business logic, integration tests for API
5. **Docker Ready**: Simple docker-compose for local development

## Goal

[Brief 1-2 sentence description of what this application does]

## Entities

### Entity 1: [Name]
- **Fields**:
  - id (primary key)
  - [field_name] (type) - [description]
  - created_at (timestamp)
  - updated_at (timestamp)

### Entity 2: [Name]
- **Fields**:
  - id (primary key)
  - [foreign_key]_id (references Entity 1)
  - [field_name] (type) - [description]

[Repeat for 1-5 entities total]

## Relationships

- [Entity 1] has many [Entity 2]
- [Entity 2] belongs to [Entity 1]

## API Endpoints

### Entity 1 Endpoints
```
GET    /api/entity1           - List all (paginated)
GET    /api/entity1/:id       - Get by ID
POST   /api/entity1           - Create new
PUT    /api/entity1/:id       - Update
DELETE /api/entity1/:id       - Delete
```

### Entity 2 Endpoints
```
GET    /api/entity2           - List all (paginated)
GET    /api/entity2/:id       - Get by ID
POST   /api/entity2           - Create new
PUT    /api/entity2/:id       - Update
DELETE /api/entity2/:id       - Delete
```

## Technology Stack

**Selected**: [Java/Spring Boot | Node.js/Express | Python/FastAPI | .NET/ASP.NET]

**Database**: PostgreSQL (recommended) or MySQL

**Testing**: [JUnit | Jest | pytest | xUnit]

## Implementation Blueprint

### Task 1: Database Schema (5 minutes)
```
1. Create entity models with proper types
2. Define relationships (foreign keys)
3. Add constraints (NOT NULL, UNIQUE)
4. Create migration files
5. Add seed data for development
```

### Task 2: Data Access Layer (5 minutes)
```
1. Create repository for each entity
2. Implement CRUD methods:
   - findAll(pagination)
   - findById(id)
   - create(data)
   - update(id, data)
   - delete(id)
3. Add basic error handling
```

### Task 3: Business Logic (5 minutes)
```
1. Create service for each entity
2. Implement validation logic
3. Add business rules (if any)
4. Handle errors gracefully
```

### Task 4: API Layer (10 minutes)
```
1. Create controller for each entity
2. Implement all CRUD endpoints
3. Add input validation
4. Implement pagination (page, limit)
5. Add proper HTTP status codes
6. Create error response format
```

### Task 5: Testing (5 minutes)
```
1. Write unit tests for services
2. Write integration tests for API endpoints
3. Test validation and error cases
4. Verify pagination works
```

### Task 6: Docker Setup (5 minutes)
```
1. Create Dockerfile
2. Create docker-compose.yml with:
   - Application service
   - Database service
3. Add .env.example with all variables
4. Add health check endpoint
5. Test docker-compose up
```

### Task 7: Documentation (5 minutes)
```
1. Create README with:
   - Project description
   - Setup instructions
   - API endpoint list
   - Environment variables
2. Add inline code comments
3. Create .env.example
```

## Validation Commands

### Linting & Type Checking
```bash
# Node.js
npm run lint
npm run type-check

# Java
mvn checkstyle:check

# Python
ruff check .
mypy .

# .NET
dotnet format --verify-no-changes
```

### Run Tests
```bash
# Node.js
npm test

# Java
mvn test

# Python
pytest

# .NET
dotnet test
```

### Test Docker
```bash
docker-compose up -d
curl http://localhost:3000/health
docker-compose down
```

## Success Criteria

- [ ] All {X} entities created with proper schema
- [ ] All CRUD operations work for each entity
- [ ] Pagination works on list endpoints
- [ ] Input validation working
- [ ] Tests pass (>80% coverage)
- [ ] Docker compose starts successfully
- [ ] Health check responds
- [ ] README complete with setup instructions
- [ ] No hardcoded credentials

## Example Requests

### Create Entity
```bash
POST /api/entity1
Content-Type: application/json

{
  "field_name": "value",
  "another_field": "value"
}

Response: 201 Created
{
  "data": {
    "id": 1,
    "field_name": "value",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

### List Entities (Paginated)
```bash
GET /api/entity1?page=1&limit=20

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

### Update Entity
```bash
PUT /api/entity1/1
Content-Type: application/json

{
  "field_name": "new value"
}

Response: 200 OK
{
  "data": {
    "id": 1,
    "field_name": "new value",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

### Error Response
```bash
POST /api/entity1
Content-Type: application/json

{
  "invalid_field": "value"
}

Response: 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {"field": "field_name", "message": "field_name is required"}
    ]
  }
}
```

## What NOT to Include (Keep It Simple)

❌ **Don't add these unless explicitly required:**
- Authentication/authorization
- External API integrations
- Caching layer
- Message queues
- Advanced monitoring
- Kubernetes deployment
- CI/CD pipeline (basic is fine)

✅ **Keep it focused on:**
- CRUD operations
- Basic validation
- Simple testing
- Docker for local dev
- Clear documentation

## File Structure

```
project/
├── src/
│   ├── models/          # Database entities
│   ├── repositories/    # Data access
│   ├── services/        # Business logic
│   ├── controllers/     # API endpoints
│   └── index.[ext]      # Entry point
├── tests/
│   ├── unit/           # Service tests
│   └── integration/    # API tests
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── package.json / pom.xml / requirements.txt
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application
PORT=3000
NODE_ENV=development
LOG_LEVEL=info
```

## Deployment

**For Tier 1 apps, keep deployment simple:**

1. Use docker-compose for local development
2. Can deploy to simple hosting (Heroku, Railway, Render)
3. Database: Managed PostgreSQL (Railway, Supabase, etc.)

**Don't over-engineer deployment for simple apps!**

---

## Implementation Time Estimate

- Database Schema: 5 min
- Data Access Layer: 5 min
- Business Logic: 5 min
- API Layer: 10 min
- Testing: 5 min
- Docker Setup: 5 min
- Documentation: 5 min

**Total: 40 minutes** (with buffer: 30-45 minutes)

## Confidence Score

Rate the completeness of this PRP: **[1-10]**

A score of 8+ means the implementation should succeed in one pass without additional research.
