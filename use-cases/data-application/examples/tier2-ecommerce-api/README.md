# Tier 2 Example: E-commerce API

This is a reference example for a **Tier 2 Standard REST API** application.

## Overview

- **Complexity**: Standard REST API (5-10 entities)
- **Time to Build**: 60-90 minutes
- **Tech Stack**: Node.js + Express + PostgreSQL + Prisma + Redis
- **Agents Used**: 1 (integration-validator for testing)

## What This Example Demonstrates

✅ Authentication & authorization (JWT + RBAC)
✅ External integrations (Stripe, SendGrid, AWS S3)
✅ Redis caching strategy
✅ Complex business logic
✅ Comprehensive testing
✅ Rate limiting
✅ API documentation
✅ Production-ready patterns

## Entities

### User
- id, email, password_hash, name, role (admin/user)
- address fields, phone
- created_at, updated_at

### Product
- id, sku, name, description, price
- category_id, stock_quantity, images[]
- created_at, updated_at

### Category
- id, name, slug, parent_category_id
- created_at, updated_at

### Order
- id, user_id, status (pending/paid/shipped/delivered/cancelled)
- total, subtotal, tax, shipping_cost
- shipping_address, billing_address
- created_at, updated_at

### OrderItem
- id, order_id, product_id
- quantity, price_at_purchase
- created_at

### Cart
- id, user_id, session_id (for guests)
- created_at, updated_at

### CartItem
- id, cart_id, product_id
- quantity, created_at

### Payment
- id, order_id, stripe_payment_id
- amount, status, payment_method
- created_at, updated_at

## External Integrations

### Stripe (Payment Processing)
- Create payment intent
- Confirm payment
- Handle webhooks
- Refund processing

### SendGrid (Email Service)
- Order confirmation emails
- Shipping notification
- Password reset emails

### AWS S3 (Product Images)
- Upload product images
- Generate signed URLs
- Image optimization

## API Endpoints

### Authentication
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout
GET    /api/auth/me
POST   /api/auth/forgot-password
POST   /api/auth/reset-password
```

### Products
```
GET    /api/products?page=1&limit=20&category=electronics&sort=price:desc
GET    /api/products/:id
POST   /api/products (admin only)
PUT    /api/products/:id (admin only)
DELETE /api/products/:id (admin only)
POST   /api/products/:id/images (admin only)
```

### Categories
```
GET    /api/categories
GET    /api/categories/:id
POST   /api/categories (admin only)
PUT    /api/categories/:id (admin only)
DELETE /api/categories/:id (admin only)
```

### Cart
```
GET    /api/cart
POST   /api/cart/items
PUT    /api/cart/items/:id
DELETE /api/cart/items/:id
DELETE /api/cart
```

### Orders
```
GET    /api/orders
GET    /api/orders/:id
POST   /api/orders (create from cart)
PUT    /api/orders/:id/cancel
GET    /api/admin/orders (admin only)
PUT    /api/admin/orders/:id/status (admin only)
```

### Payments
```
POST   /api/payments/create-intent
POST   /api/payments/confirm
POST   /api/payments/webhooks/stripe
```

## File Structure

```
tier2-ecommerce-api/
├── src/
│   ├── models/              # Prisma models
│   ├── repositories/        # Data access (8 repositories)
│   ├── services/            # Business logic
│   │   ├── authService.ts
│   │   ├── productService.ts
│   │   ├── orderService.ts
│   │   ├── cartService.ts
│   │   └── paymentService.ts
│   ├── controllers/         # API endpoints (8 controllers)
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── authorize.ts (RBAC)
│   │   ├── rateLimit.ts
│   │   └── validation.ts
│   ├── integrations/        # External services
│   │   ├── stripe/
│   │   │   ├── stripeClient.ts
│   │   │   └── stripeWebhooks.ts
│   │   ├── sendgrid/
│   │   │   ├── emailClient.ts
│   │   │   └── templates.ts
│   │   └── aws/
│   │       └── s3Client.ts
│   ├── cache/
│   │   ├── redisClient.ts
│   │   └── cacheService.ts
│   ├── validators/          # Zod schemas (10+)
│   ├── routes/              # Route definitions
│   └── index.ts
├── tests/
│   ├── unit/                # Service tests
│   ├── integration/         # API tests with mocks
│   └── fixtures/            # Test data
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

## Environment Variables

```bash
# Application
PORT=3000
NODE_ENV=production
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key-min-32-characters
JWT_EXPIRATION=900
JWT_REFRESH_SECRET=your-refresh-secret-key
JWT_REFRESH_EXPIRATION=604800

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# SendGrid
SENDGRID_API_KEY=SG...
FROM_EMAIL=noreply@example.com

# AWS S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_BUCKET_NAME=product-images

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

## Caching Strategy

### L1: In-Memory (Node-cache)
- Active cart data: 5 min TTL
- Current user session: 10 min TTL

### L2: Redis
- Product details: 15 min TTL
- Category tree: 1 hour TTL
- Product listings: 5 min TTL

### Cache Invalidation
- Product update → Invalidate product cache + listings
- Category change → Invalidate category tree
- Order placed → Invalidate cart + stock count

## Testing

### Unit Tests (>80% coverage)
```bash
npm run test:unit
```
- All service methods
- Business logic
- Validation logic

### Integration Tests
```bash
npm run test:integration
```
- All API endpoints
- Authentication flows
- External API mocks (WireMock/nock)
- Redis caching

### API Tests
```bash
npm run test:api
```
- End-to-end flows:
  - User registration → Login → Browse → Add to cart → Checkout → Payment

## Key Features

### Authentication & Authorization
- ✅ JWT with refresh tokens
- ✅ Role-based access control (admin, user)
- ✅ Password reset flow
- ✅ Email verification (optional)

### Payment Processing
- ✅ Stripe integration
- ✅ Payment intent creation
- ✅ Webhook handling
- ✅ Refund support

### Email Notifications
- ✅ Order confirmation
- ✅ Shipping updates
- ✅ Password reset
- ✅ Template-based emails

### Product Management
- ✅ Image upload to S3
- ✅ Stock management
- ✅ Category hierarchy
- ✅ Search and filtering

### Performance
- ✅ Redis caching
- ✅ Database indexing
- ✅ Query optimization
- ✅ Rate limiting

### Security
- ✅ Password hashing (bcrypt)
- ✅ SQL injection protection
- ✅ XSS prevention
- ✅ CORS configuration
- ✅ Security headers (helmet)
- ✅ Rate limiting

## Example Business Flows

### Checkout Flow
```
1. User adds products to cart
2. User proceeds to checkout
3. System creates order from cart
4. System creates Stripe payment intent
5. User confirms payment
6. System updates order status
7. System sends confirmation email
8. System clears cart
```

### Admin Order Management
```
1. Admin views all orders
2. Admin updates order status (shipped)
3. System sends shipping notification email
4. Customer receives tracking info
```

## Deployment

**Recommended for Tier 2:**
- AWS ECS or App Runner
- Google Cloud Run
- Heroku with add-ons
- DigitalOcean App Platform

**Required Add-ons:**
- PostgreSQL database (managed)
- Redis instance
- File storage (S3 or equivalent)

## Performance Requirements

- **Response Time**: p95 < 200ms
- **Throughput**: > 100 req/s
- **Cache Hit Ratio**: > 70%
- **Error Rate**: < 1%

## Security Checklist

- [x] HTTPS only in production
- [x] Environment variables for secrets
- [x] SQL injection protected
- [x] XSS prevention
- [x] CSRF protection
- [x] Rate limiting
- [x] Security headers
- [x] Password strength requirements
- [x] PCI-DSS compliant (Stripe handles cards)

## Learning Outcomes

After building this, you'll understand:
1. Complex REST API design
2. Authentication & authorization patterns
3. External API integration
4. Payment processing
5. Caching strategies
6. Email service integration
7. File upload to cloud storage
8. Comprehensive testing
9. Production deployment

## Upgrading to Tier 3

To upgrade to **Tier 3** (Enterprise), you would add:
- Message queue (RabbitMQ/Kafka)
- Microservices architecture
- Advanced monitoring (Prometheus, Grafana)
- Distributed tracing (Jaeger)
- Kubernetes deployment
- Multi-region support
- Complex integrations (ERP, CRM)
- CQRS/Event Sourcing
- Advanced analytics

---

**Note**: This is a reference example. To build your own e-commerce API, run:
```
/data-app-init
# Answer questions (will detect Tier 2)
/data-app-plan
# Review plan, then implement
```
