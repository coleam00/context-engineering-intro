# Tier 2: Standard REST API Applications

## When to Use This Tier

- **5-10 entities** with moderate relationships
- **1-3 external integrations** (payment APIs, email services, cloud storage)
- **Authentication & authorization** required
- **Caching layer** for performance
- **Background jobs** (optional)
- **Development time: 60-90 minutes**

## Examples
- E-commerce API (products, orders, customers, payments)
- Project management tool (projects, tasks, users, teams)
- Booking system (reservations, availability, customers)
- Content management system (posts, media, users, comments)

## Architecture Pattern

```
┌──────────────────────────────────────────────┐
│  REST API + Authentication                   │
├──────────────────────────────────────────────┤
│  Business Services + External Integrations   │
├──────────────────────────────────────────────┤
│  Data Access Layer (Repository Pattern)      │
├──────────────────────────────────────────────┤
│  Cache Layer (Redis)    │  Database (RDBMS)  │
├──────────────────────────────────────────────┤
│  Message Queue (Optional - RabbitMQ/Redis)   │
└──────────────────────────────────────────────┘
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
│   │   ├── payment/        # Payment gateway
│   │   ├── email/          # Email service
│   │   └── storage/        # Cloud storage
│   ├── cache/              # Caching logic
│   ├── jobs/               # Background jobs
│   ├── validators/         # Input validation
│   ├── config/             # Configuration
│   └── index.js            # Entry point
├── tests/
│   ├── unit/               # Service tests
│   ├── integration/        # API tests
│   └── fixtures/           # Test data
├── migrations/             # Database migrations
├── seeds/                  # Seed data
├── docker-compose.yml      # Multi-container setup
├── Dockerfile              # Application container
├── .env.example           # Environment template
└── README.md              # Documentation
```

## Implementation Checklist

### 1. Authentication & Authorization (15 min)
- [ ] Implement JWT or session-based auth
- [ ] Create user registration and login endpoints
- [ ] Add role-based access control (RBAC)
- [ ] Implement password hashing (bcrypt/argon2)
- [ ] Add refresh token mechanism

### 2. Database Design (15 min)
- [ ] Design normalized schema with relationships
- [ ] Add indexes for query performance
- [ ] Create migration files with rollback support
- [ ] Implement soft deletes where needed
- [ ] Add audit fields (created_by, updated_by)

### 3. Caching Layer (10 min)
- [ ] Set up Redis connection
- [ ] Cache frequently accessed data
- [ ] Implement cache invalidation strategy
- [ ] Add cache warming for critical data

### 4. External Integrations (15 min)
- [ ] Create client wrappers for external APIs
- [ ] Implement retry logic with exponential backoff
- [ ] Add timeout handling
- [ ] Log all external API calls
- [ ] Mock external services in tests

### 5. API Development (15 min)
- [ ] Implement RESTful endpoints
- [ ] Add input validation middleware
- [ ] Implement pagination, filtering, sorting
- [ ] Add rate limiting
- [ ] Generate OpenAPI/Swagger documentation

### 6. Testing & Quality (15 min)
- [ ] Unit tests for services (>80% coverage)
- [ ] Integration tests for API endpoints
- [ ] Test authentication flows
- [ ] Mock external API calls
- [ ] Test error scenarios

### 7. Documentation & Deployment (10 min)
- [ ] Create comprehensive README
- [ ] Document all API endpoints
- [ ] Add deployment instructions
- [ ] Create docker-compose setup
- [ ] Document environment variables

## Authentication Pattern

### JWT Implementation
```javascript
// Login endpoint returns JWT
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}

// Protected endpoints require Authorization header
GET /api/orders
Headers: {
  "Authorization": "Bearer eyJhbGc..."
}
```

### Role-Based Access Control
```javascript
// Middleware checks user role
requireRole(['admin', 'manager'])

// Or check permissions
requirePermission('orders:write')
```

## External Integration Pattern

### Payment Gateway Example
```javascript
// integrations/payment/stripe-client.js
class StripeClient {
  async createPayment(amount, currency, metadata) {
    try {
      const result = await this.retryWithBackoff(() =>
        stripe.paymentIntents.create({
          amount,
          currency,
          metadata
        })
      );

      this.logSuccess('payment_created', result.id);
      return result;
    } catch (error) {
      this.logError('payment_failed', error);
      throw new PaymentError(error.message);
    }
  }

  async retryWithBackoff(fn, maxRetries = 3) {
    // Exponential backoff: 1s, 2s, 4s
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await this.sleep(Math.pow(2, i) * 1000);
      }
    }
  }
}
```

## Caching Strategy

### Cache Layers
1. **Hot Data** - Cache for 5-15 minutes (user profiles, product details)
2. **Warm Data** - Cache for 1 hour (categories, settings)
3. **Cold Data** - Cache for 24 hours (static content)

### Cache Invalidation
```javascript
// Invalidate on update
async updateProduct(id, data) {
  const product = await productRepo.update(id, data);
  await cache.delete(`product:${id}`);
  await cache.delete('products:list:*'); // Invalidate lists
  return product;
}

// Cache-aside pattern
async getProduct(id) {
  const cached = await cache.get(`product:${id}`);
  if (cached) return cached;

  const product = await productRepo.findById(id);
  await cache.set(`product:${id}`, product, 600); // 10 min TTL
  return product;
}
```

## API Design Guidelines

### Pagination
```
GET /api/products?page=1&limit=20&sort=price:desc
```

### Filtering
```
GET /api/products?category=electronics&minPrice=100&maxPrice=500
```

### Sorting
```
GET /api/products?sort=name:asc,price:desc
```

### Response Format
```json
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

## Error Handling

### HTTP Status Codes
- **200** - Success
- **201** - Created
- **204** - No Content (successful delete)
- **400** - Bad Request (validation)
- **401** - Unauthorized (not authenticated)
- **403** - Forbidden (not authorized)
- **404** - Not Found
- **409** - Conflict (duplicate)
- **429** - Too Many Requests (rate limit)
- **500** - Internal Server Error
- **502** - Bad Gateway (external service error)
- **503** - Service Unavailable

### Error Response
```json
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "Unable to process payment",
    "details": {
      "provider": "stripe",
      "reason": "insufficient_funds"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

## Testing Strategy

### Unit Tests
- Mock database and external APIs
- Test service logic in isolation
- Test validation rules
- Test error handling

### Integration Tests
- Use test database (with test containers)
- Test full request/response cycle
- Test authentication/authorization
- Mock external APIs (use WireMock or nock)
- Test rate limiting

### Example Integration Test
```javascript
describe('POST /api/orders', () => {
  it('should create order with valid data', async () => {
    const token = await getAuthToken('user@example.com');
    const response = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${token}`)
      .send({
        items: [{ productId: 1, quantity: 2 }],
        shippingAddress: {...}
      });

    expect(response.status).toBe(201);
    expect(response.body.data).toHaveProperty('id');
  });
});
```

## Deployment Configuration

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}

  redis:
    image: redis:7-alpine
```

### Environment Variables
```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
JWT_EXPIRATION=3600
STRIPE_API_KEY=sk_test_...
SENDGRID_API_KEY=SG...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
PORT=3000
NODE_ENV=development
```

## Success Criteria

- ✅ Authentication & authorization working
- ✅ All CRUD operations functional
- ✅ External integrations tested
- ✅ Caching implemented
- ✅ Tests pass (>80% coverage)
- ✅ API documentation complete
- ✅ Docker setup working
- ✅ Error handling robust
- ✅ Rate limiting implemented
