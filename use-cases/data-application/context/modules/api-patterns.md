# API Design Patterns

## RESTful API Design

### HTTP Methods
- **GET** - Retrieve resources (idempotent, cacheable)
- **POST** - Create resources (not idempotent)
- **PUT** - Update/replace entire resource (idempotent)
- **PATCH** - Partial update (not necessarily idempotent)
- **DELETE** - Remove resource (idempotent)

### URL Naming Conventions
```
# Good
GET    /api/users                  - List users
GET    /api/users/:id              - Get specific user
POST   /api/users                  - Create user
PUT    /api/users/:id              - Update user
DELETE /api/users/:id              - Delete user
GET    /api/users/:id/posts        - List user's posts

# Bad
GET    /api/getUsers
POST   /api/user/create
GET    /api/user/:id/getPosts
```

## Request/Response Patterns

### Request Validation
```typescript
// Using validation library (e.g., Zod, Joi, class-validator)
const CreateUserSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
    name: z.string().min(2).max(100)
});

app.post('/api/users', async (req, res) => {
    try {
        const data = CreateUserSchema.parse(req.body);
        const user = await userService.create(data);
        res.status(201).json({ data: user });
    } catch (error) {
        if (error instanceof ZodError) {
            return res.status(400).json({
                error: {
                    code: 'VALIDATION_ERROR',
                    message: 'Invalid input',
                    details: error.errors
                }
            });
        }
        throw error;
    }
});
```

### Response Format
```json
// Success Response
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// List Response with Pagination
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  },
  "links": {
    "self": "/api/users?page=1",
    "next": "/api/users?page=2",
    "prev": null,
    "first": "/api/users?page=1",
    "last": "/api/users?page=8"
  }
}

// Error Response
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "details": {
      "userId": 123
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

## Status Codes

### Common Status Codes
- **200 OK** - Success (GET, PUT, PATCH)
- **201 Created** - Resource created (POST)
- **204 No Content** - Success with no response body (DELETE)
- **400 Bad Request** - Validation error
- **401 Unauthorized** - Not authenticated
- **403 Forbidden** - Not authorized
- **404 Not Found** - Resource doesn't exist
- **409 Conflict** - Duplicate resource
- **422 Unprocessable Entity** - Business logic error
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error
- **502 Bad Gateway** - External service error
- **503 Service Unavailable** - Server overloaded

## Pagination, Filtering, Sorting

### Query Parameters
```
# Pagination
GET /api/products?page=2&limit=20

# Filtering
GET /api/products?category=electronics&minPrice=100&maxPrice=500

# Sorting
GET /api/products?sort=price:desc,name:asc

# Search
GET /api/products?q=laptop

# Combined
GET /api/products?category=electronics&sort=price:desc&page=1&limit=20
```

### Implementation
```typescript
app.get('/api/products', async (req, res) => {
    const {
        page = 1,
        limit = 20,
        sort = 'created_at:desc',
        category,
        minPrice,
        maxPrice,
        q
    } = req.query;

    const filters = {
        category,
        minPrice: minPrice ? parseFloat(minPrice) : undefined,
        maxPrice: maxPrice ? parseFloat(maxPrice) : undefined,
        search: q
    };

    const [products, total] = await productService.findAll({
        page: parseInt(page),
        limit: parseInt(limit),
        sort: parseSort(sort),
        filters
    });

    res.json({
        data: products,
        meta: {
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            totalPages: Math.ceil(total / limit)
        }
    });
});
```

## API Versioning

### URL Versioning (Recommended)
```
GET /api/v1/users
GET /api/v2/users
```

### Header Versioning
```
GET /api/users
Headers: {
  "API-Version": "2"
}
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 100,                   // Max 100 requests per window
    message: 'Too many requests, please try again later',
    standardHeaders: true,
    legacyHeaders: false,
});

app.use('/api/', limiter);

// Different limits for different endpoints
const strictLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5  // Only 5 login attempts per 15 minutes
});

app.post('/api/auth/login', strictLimiter, loginHandler);
```

## CORS Configuration

```typescript
import cors from 'cors';

app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400  // 24 hours
}));
```

## API Documentation (OpenAPI/Swagger)

```typescript
/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: List all users
 *     tags: [Users]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *     responses:
 *       200:
 *         description: List of users
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 */
app.get('/api/users', userController.list);
```

## Error Handling Middleware

```typescript
// Error types
class AppError extends Error {
    constructor(
        public statusCode: number,
        public code: string,
        message: string,
        public details?: any
    ) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends AppError {
    constructor(message: string, details?: any) {
        super(400, 'VALIDATION_ERROR', message, details);
    }
}

class NotFoundError extends AppError {
    constructor(resource: string) {
        super(404, 'NOT_FOUND', `${resource} not found`);
    }
}

// Error handler middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    // Log error
    logger.error({
        error: err.message,
        stack: err.stack,
        requestId: req.id,
        url: req.url,
        method: req.method
    });

    // Handle known errors
    if (err instanceof AppError) {
        return res.status(err.statusCode).json({
            error: {
                code: err.code,
                message: err.message,
                details: err.details,
                requestId: req.id
            }
        });
    }

    // Handle unknown errors (don't leak details in production)
    res.status(500).json({
        error: {
            code: 'INTERNAL_ERROR',
            message: process.env.NODE_ENV === 'production'
                ? 'An unexpected error occurred'
                : err.message,
            requestId: req.id
        }
    });
});
```

## Request Logging

```typescript
import morgan from 'morgan';
import { v4 as uuidv4 } from 'uuid';

// Add request ID
app.use((req, res, next) => {
    req.id = uuidv4();
    res.setHeader('X-Request-Id', req.id);
    next();
});

// Structured logging
app.use((req, res, next) => {
    const start = Date.now();

    res.on('finish', () => {
        const duration = Date.now() - start;
        logger.info({
            requestId: req.id,
            method: req.method,
            url: req.url,
            status: res.statusCode,
            duration,
            userAgent: req.get('user-agent'),
            ip: req.ip
        });
    });

    next();
});
```

## Content Negotiation

```typescript
app.get('/api/users/:id', async (req, res) => {
    const user = await userService.findById(req.params.id);

    res.format({
        'application/json': () => {
            res.json({ data: user });
        },
        'application/xml': () => {
            res.send(toXML(user));
        },
        'text/html': () => {
            res.send(`<h1>${user.name}</h1>`);
        },
        'default': () => {
            res.status(406).send('Not Acceptable');
        }
    });
});
```

## Health Check Endpoint

```typescript
app.get('/health', async (req, res) => {
    const checks = await Promise.all([
        checkDatabase(),
        checkRedis(),
        checkExternalAPI()
    ]);

    const isHealthy = checks.every(check => check.status === 'up');

    res.status(isHealthy ? 200 : 503).json({
        status: isHealthy ? 'healthy' : 'unhealthy',
        timestamp: new Date().toISOString(),
        checks: {
            database: checks[0],
            redis: checks[1],
            externalAPI: checks[2]
        }
    });
});
```
