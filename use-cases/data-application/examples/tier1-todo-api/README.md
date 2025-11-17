# Tier 1 Example: Simple TODO API

This is a reference example for a **Tier 1 Simple CRUD** application.

## Overview

- **Complexity**: Simple CRUD (1-3 entities)
- **Time to Build**: 30-45 minutes
- **Tech Stack**: Node.js + Express + PostgreSQL + Prisma
- **Agents Used**: 0 (Main Claude only)

## What This Example Demonstrates

✅ Basic CRUD operations
✅ Simple database schema (2 entities)
✅ REST API with pagination
✅ Input validation
✅ Basic testing
✅ Docker setup
✅ Clear documentation

## Entities

### User
- id (integer, primary key)
- email (string, unique)
- password_hash (string)
- name (string)
- created_at (timestamp)

### Todo
- id (integer, primary key)
- user_id (foreign key to users)
- title (string)
- description (text, optional)
- completed (boolean, default false)
- created_at (timestamp)
- updated_at (timestamp)

## API Endpoints

### Authentication
```
POST /api/auth/register - Register new user
POST /api/auth/login    - Login (returns JWT)
```

### Todos
```
GET    /api/todos                - List all todos (paginated)
GET    /api/todos/:id            - Get specific todo
POST   /api/todos                - Create new todo
PUT    /api/todos/:id            - Update todo
DELETE /api/todos/:id            - Delete todo
PATCH  /api/todos/:id/complete   - Mark as complete
```

## File Structure

```
tier1-todo-api/
├── src/
│   ├── models/
│   │   └── index.ts         # Prisma client
│   ├── repositories/
│   │   ├── userRepository.ts
│   │   └── todoRepository.ts
│   ├── services/
│   │   ├── authService.ts
│   │   └── todoService.ts
│   ├── controllers/
│   │   ├── authController.ts
│   │   └── todoController.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   └── validation.ts
│   ├── routes/
│   │   ├── auth.ts
│   │   └── todos.ts
│   └── index.ts             # Entry point
├── prisma/
│   ├── schema.prisma        # Database schema
│   └── migrations/          # Migration files
├── tests/
│   ├── unit/
│   │   ├── todoService.test.ts
│   │   └── authService.test.ts
│   └── integration/
│       ├── todos.test.ts
│       └── auth.test.ts
├── docker-compose.yml
├── Dockerfile
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

## Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
JWT_SECRET=your-secret-key-min-32-characters
PORT=3000
NODE_ENV=development
```

## Setup & Run

```bash
# Install dependencies
npm install

# Run migrations
npx prisma migrate dev

# Start development server
npm run dev

# Run tests
npm test

# Run with Docker
docker-compose up
```

## Example Requests

### Register
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
```

### Create Todo
```bash
curl -X POST http://localhost:3000/api/todos \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

### List Todos
```bash
curl http://localhost:3000/api/todos?page=1&limit=20 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

### Unit Tests
- `todoService.test.ts` - Test business logic
- `authService.test.ts` - Test authentication

### Integration Tests
- `todos.test.ts` - Test TODO API endpoints
- `auth.test.ts` - Test auth endpoints

### Coverage
```bash
npm run test:coverage
# Target: >80%
```

## Key Features

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ Input validation (Zod)
- ✅ Pagination on list endpoints
- ✅ Error handling
- ✅ Docker setup
- ✅ Health check endpoint
- ✅ Auto-generated API docs (Swagger)

## What's NOT Included (Tier 1 Simplicity)

- ❌ External API integrations
- ❌ Caching layer
- ❌ Message queues
- ❌ Advanced monitoring
- ❌ Kubernetes deployment
- ❌ Complex business logic

## Deployment

**Recommended for Tier 1:**
- Railway
- Render
- Heroku
- Any simple cloud platform with PostgreSQL support

## Learning Outcomes

After building this, you'll understand:
1. Basic REST API design
2. CRUD operation patterns
3. JWT authentication
4. Database relationships (1:many)
5. Input validation
6. Testing strategies
7. Docker containerization

## Next Steps

To upgrade to **Tier 2** (Standard REST API), you would add:
- Role-based authorization
- External API integration (e.g., email service)
- Redis caching
- Rate limiting
- More comprehensive testing
- Enhanced monitoring

---

**Note**: This is a reference example. To build your own TODO API, run:
```
/data-app-init
# Answer questions (will detect Tier 1)
/data-app-plan
# Review plan, then implement
```
