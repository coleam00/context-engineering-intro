---
description: Comprehensive validation for this codebase
---

# Validate Codebase

> **Example generated validation command** for a React + FastAPI + PostgreSQL app

## Phase 1: Linting
!`cd frontend && npm run lint`
!`cd backend && ruff check src/`

## Phase 2: Type Checking
!`cd frontend && npx tsc --noEmit`
!`cd backend && mypy src/`

## Phase 3: Style Checking
!`cd frontend && npm run format:check`
!`cd backend && black --check src/`

## Phase 4: Unit Testing
!`cd frontend && npm test -- --coverage`
!`cd backend && pytest tests/unit -v --cov=src`

## Phase 5: End-to-End Testing

### Setup
!`docker-compose up -d`
!`timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'`

### Frontend E2E (Playwright)
!`cd frontend && npx playwright test`

**Tests:**
- User registration → email verification → login
- Create item → edit item → delete item
- Search and filter functionality
- Error handling and validation
- All main user workflows

### Backend E2E (API + Database)

**Test all API endpoints:**
!`curl -X POST http://localhost:8000/api/auth/register -d '{"email":"test@test.com","password":"Test123!"}'`
!`TOKEN=$(curl -X POST http://localhost:8000/api/auth/login -d '{"email":"test@test.com","password":"Test123!"}' | jq -r '.token')`
!`curl http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN"`
!`curl -X POST http://localhost:8000/api/items -H "Authorization: Bearer $TOKEN" -d '{"name":"Test"}'`

**Verify database:**
!`docker exec postgres psql -U user -d db -c "SELECT COUNT(*) FROM users;"`
!`docker exec postgres psql -U user -d db -c "SELECT * FROM items WHERE name='Test';"`

**Test error handling:**
!`curl -w "%{http_code}" http://localhost:8000/api/items/invalid-id` # Should be 404
!`curl -w "%{http_code}" http://localhost:8000/api/admin -H "Authorization: Bearer $TOKEN"` # Should be 403

### Cleanup
!`docker-compose down -v`

## Summary
All validation passed! Ready for deployment.
