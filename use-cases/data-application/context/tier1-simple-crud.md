# Tier 1: Simple CRUD Applications

## When to Use This Tier

- **1-5 entities** with simple relationships
- **No external integrations** (or just 1 simple API)
- **Basic CRUD operations** (Create, Read, Update, Delete)
- **Single database** (no caching, no message queues)
- **Development time: 30-45 minutes**

## Examples
- TODO list API
- Simple blog (posts, comments)
- Contact manager
- Bookmark collection
- Note-taking app

## Architecture Pattern

```
┌─────────────────────────────────────┐
│  REST API (Express/FastAPI/Spring)  │
├─────────────────────────────────────┤
│  Business Logic (Services)          │
├─────────────────────────────────────┤
│  Data Access (Repository/ORM)       │
├─────────────────────────────────────┤
│  Database (PostgreSQL/MySQL/SQLite) │
└─────────────────────────────────────┘
```

## File Structure

```
project/
├── src/
│   ├── models/          # Database models/entities
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic
│   ├── controllers/     # API endpoints
│   ├── middleware/      # Auth, logging, error handling
│   ├── config/          # Configuration
│   └── index.js/main.py # Entry point
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # API tests
├── .env.example        # Environment template
├── docker-compose.yml  # Local development
├── Dockerfile          # Container definition
├── README.md           # Documentation
└── package.json/requirements.txt # Dependencies
```

## Implementation Checklist

### 1. Database Schema (10 min)
- [ ] Define entities with relationships
- [ ] Add constraints (primary keys, foreign keys, unique)
- [ ] Create migration files
- [ ] Add seed data for development

### 2. Data Access Layer (5 min)
- [ ] Implement repository pattern or use ORM
- [ ] Create CRUD methods for each entity
- [ ] Add basic error handling

### 3. Business Logic (5 min)
- [ ] Create service layer for business rules
- [ ] Implement validation logic
- [ ] Add simple error handling

### 4. API Layer (10 min)
- [ ] Define REST endpoints (GET, POST, PUT, DELETE)
- [ ] Add request validation
- [ ] Implement pagination for list endpoints
- [ ] Add basic error responses

### 5. Testing (5 min)
- [ ] Write unit tests for services
- [ ] Write integration tests for API endpoints
- [ ] Test error cases

### 6. Documentation (5 min)
- [ ] Add API documentation (OpenAPI/Swagger)
- [ ] Create README with setup instructions
- [ ] Document environment variables

## API Endpoint Pattern

For each entity, implement:

```
GET    /api/entities          - List all (with pagination)
GET    /api/entities/:id      - Get one by ID
POST   /api/entities          - Create new
PUT    /api/entities/:id      - Update existing
DELETE /api/entities/:id      - Delete by ID
```

## Database Design Guidelines

### Keep It Simple
- Use auto-incrementing IDs or UUIDs
- Standard timestamps (created_at, updated_at)
- Soft deletes optional (deleted_at)

### Example Entity
```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Validation Strategy

### Request Validation
- Validate required fields
- Check field types and formats
- Enforce length limits
- Sanitize inputs

### Business Validation
- Check entity exists before update/delete
- Validate relationships (foreign keys)
- Enforce business rules (e.g., can't complete deleted todo)

## Error Handling

### HTTP Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request (validation errors)
- **401** - Unauthorized
- **404** - Not Found
- **500** - Internal Server Error

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {"field": "title", "message": "Title is required"}
    ]
  }
}
```

## Testing Requirements

### Unit Tests (>80% coverage)
- Test service methods in isolation
- Mock database calls
- Test both success and error cases

### Integration Tests
- Test full API endpoints
- Use test database
- Test authentication/authorization
- Test error responses

## Deployment

### Docker Setup
- Single container with application
- Link to database container
- Use docker-compose for local development

### Environment Variables
```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
PORT=3000
NODE_ENV=development
LOG_LEVEL=info
```

## Success Criteria

- ✅ All CRUD operations work
- ✅ Tests pass (>80% coverage)
- ✅ API documented
- ✅ Runs in Docker
- ✅ README with clear setup instructions
- ✅ No hardcoded credentials
