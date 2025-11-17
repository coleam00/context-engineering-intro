# Node.js Express Stack

## Tech Stack Components

- **Runtime**: Node.js 18+ with TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL with Sequelize or Prisma ORM
- **Validation**: Zod or Joi
- **Authentication**: JWT with jsonwebtoken
- **Testing**: Jest + Supertest
- **Documentation**: Swagger/OpenAPI

## Project Structure

```
project/
├── src/
│   ├── models/           # Database models
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic
│   ├── controllers/      # Route handlers
│   ├── middleware/       # Custom middleware
│   ├── routes/           # Route definitions
│   ├── validators/       # Input validation schemas
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── config/           # Configuration
│   └── index.ts          # Entry point
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # API integration tests
│   └── fixtures/         # Test data
├── prisma/               # If using Prisma
│   ├── schema.prisma
│   └── migrations/
├── package.json
├── tsconfig.json
├── .env.example
└── docker-compose.yml
```

## Dependencies (package.json)

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "dotenv": "^16.3.1",
    "@prisma/client": "^5.7.0",
    "zod": "^3.22.4",
    "jsonwebtoken": "^9.0.2",
    "bcrypt": "^5.1.1",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "express-rate-limit": "^7.1.5",
    "winston": "^3.11.0",
    "ioredis": "^5.3.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^20.10.5",
    "@types/jsonwebtoken": "^9.0.5",
    "@types/bcrypt": "^5.0.2",
    "typescript": "^5.3.3",
    "tsx": "^4.7.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.1",
    "supertest": "^6.3.3",
    "@types/supertest": "^6.0.2",
    "prisma": "^5.7.0"
  }
}
```

## Example Implementation

### Prisma Schema
```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id           Int       @id @default(autoincrement())
  email        String    @unique
  passwordHash String    @map("password_hash")
  name         String
  role         UserRole  @default(USER)
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")
  orders       Order[]

  @@map("users")
}

model Order {
  id        Int      @id @default(autoincrement())
  userId    Int      @map("user_id")
  total     Decimal  @db.Decimal(10, 2)
  status    String
  createdAt DateTime @default(now()) @map("created_at")
  user      User     @relation(fields: [userId], references: [id])
  items     OrderItem[]

  @@map("orders")
}

enum UserRole {
  ADMIN
  USER
}
```

### Repository
```typescript
// src/repositories/user.repository.ts
import { PrismaClient, User } from '@prisma/client';

export class UserRepository {
    constructor(private prisma: PrismaClient) {}

    async findById(id: number): Promise<User | null> {
        return this.prisma.user.findUnique({
            where: { id }
        });
    }

    async findByEmail(email: string): Promise<User | null> {
        return this.prisma.user.findUnique({
            where: { email }
        });
    }

    async create(data: {
        email: string;
        passwordHash: string;
        name: string;
    }): Promise<User> {
        return this.prisma.user.create({
            data
        });
    }

    async findAll(options: {
        skip?: number;
        take?: number;
    }): Promise<{ users: User[]; total: number }> {
        const [users, total] = await Promise.all([
            this.prisma.user.findMany({
                skip: options.skip,
                take: options.take,
                orderBy: { createdAt: 'desc' }
            }),
            this.prisma.user.count()
        ]);

        return { users, total };
    }
}
```

### Service
```typescript
// src/services/user.service.ts
import bcrypt from 'bcrypt';
import { UserRepository } from '../repositories/user.repository';
import { DuplicateEmailError, NotFoundError } from '../utils/errors';

export class UserService {
    constructor(private userRepository: UserRepository) {}

    async createUser(data: {
        email: string;
        password: string;
        name: string;
    }) {
        const existing = await this.userRepository.findByEmail(data.email);
        if (existing) {
            throw new DuplicateEmailError('Email already exists');
        }

        const passwordHash = await bcrypt.hash(data.password, 12);

        const user = await this.userRepository.create({
            email: data.email,
            passwordHash,
            name: data.name
        });

        // Don't return password hash
        const { passwordHash: _, ...userDto } = user;
        return userDto;
    }

    async getUserById(id: number) {
        const user = await this.userRepository.findById(id);
        if (!user) {
            throw new NotFoundError('User not found');
        }

        const { passwordHash: _, ...userDto } = user;
        return userDto;
    }

    async listUsers(page: number = 1, limit: number = 20) {
        const skip = (page - 1) * limit;
        const { users, total } = await this.userRepository.findAll({
            skip,
            take: limit
        });

        return {
            data: users.map(({ passwordHash: _, ...user }) => user),
            meta: {
                page,
                limit,
                total,
                totalPages: Math.ceil(total / limit)
            }
        };
    }
}
```

### Controller
```typescript
// src/controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';
import { CreateUserSchema } from '../validators/user.validator';

export class UserController {
    constructor(private userService: UserService) {}

    create = async (req: Request, res: Response, next: NextFunction) => {
        try {
            const data = CreateUserSchema.parse(req.body);
            const user = await this.userService.createUser(data);
            res.status(201).json({ data: user });
        } catch (error) {
            next(error);
        }
    };

    getById = async (req: Request, res: Response, next: NextFunction) => {
        try {
            const id = parseInt(req.params.id);
            const user = await this.userService.getUserById(id);
            res.json({ data: user });
        } catch (error) {
            next(error);
        }
    };

    list = async (req: Request, res: Response, next: NextFunction) => {
        try {
            const page = parseInt(req.query.page as string) || 1;
            const limit = parseInt(req.query.limit as string) || 20;

            const result = await this.userService.listUsers(page, limit);
            res.json(result);
        } catch (error) {
            next(error);
        }
    };
}
```

### Validation
```typescript
// src/validators/user.validator.ts
import { z } from 'zod';

export const CreateUserSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
    name: z.string().min(2).max(100)
});

export const UpdateUserSchema = z.object({
    name: z.string().min(2).max(100).optional(),
    email: z.string().email().optional()
});
```

### Routes
```typescript
// src/routes/user.routes.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { CreateUserSchema } from '../validators/user.validator';

export function createUserRoutes(userController: UserController) {
    const router = Router();

    router.post('/', validate(CreateUserSchema), userController.create);
    router.get('/', authenticate, userController.list);
    router.get('/:id', authenticate, userController.getById);

    return router;
}
```

### Middleware
```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { UnauthorizedError } from '../utils/errors';

export interface AuthRequest extends Request {
    user?: {
        id: number;
        email: string;
        role: string;
    };
}

export const authenticate = (
    req: AuthRequest,
    res: Response,
    next: NextFunction
) => {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
        throw new UnauthorizedError('No token provided');
    }

    const token = authHeader.substring(7);

    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET!) as any;
        req.user = payload;
        next();
    } catch (error) {
        throw new UnauthorizedError('Invalid token');
    }
};

// src/middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';
import { ValidationError } from '../utils/errors';

export const validate = (schema: ZodSchema) => {
    return (req: Request, res: Response, next: NextFunction) => {
        try {
            req.body = schema.parse(req.body);
            next();
        } catch (error: any) {
            next(new ValidationError('Validation failed', error.errors));
        }
    };
};
```

### Error Handling
```typescript
// src/middleware/error-handler.ts
import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';
import logger from '../utils/logger';

export class AppError extends Error {
    constructor(
        public statusCode: number,
        public code: string,
        message: string,
        public details?: any
    ) {
        super(message);
        this.name = this.constructor.name;
    }
}

export class NotFoundError extends AppError {
    constructor(message: string = 'Resource not found') {
        super(404, 'NOT_FOUND', message);
    }
}

export class ValidationError extends AppError {
    constructor(message: string, details?: any) {
        super(400, 'VALIDATION_ERROR', message, details);
    }
}

export const errorHandler = (
    err: Error,
    req: Request,
    res: Response,
    next: NextFunction
) => {
    logger.error({
        error: err.message,
        stack: err.stack,
        url: req.url,
        method: req.method
    });

    if (err instanceof AppError) {
        return res.status(err.statusCode).json({
            error: {
                code: err.code,
                message: err.message,
                details: err.details
            }
        });
    }

    if (err instanceof ZodError) {
        return res.status(400).json({
            error: {
                code: 'VALIDATION_ERROR',
                message: 'Invalid input',
                details: err.errors
            }
        });
    }

    res.status(500).json({
        error: {
            code: 'INTERNAL_ERROR',
            message: process.env.NODE_ENV === 'production'
                ? 'An unexpected error occurred'
                : err.message
        }
    });
};
```

### Main Application
```typescript
// src/index.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { PrismaClient } from '@prisma/client';
import { errorHandler } from './middleware/error-handler';
import { createUserRoutes } from './routes/user.routes';
import { UserRepository } from './repositories/user.repository';
import { UserService } from './services/user.service';
import { UserController } from './controllers/user.controller';

const app = express();
const prisma = new PrismaClient();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Dependency injection
const userRepository = new UserRepository(prisma);
const userService = new UserService(userRepository);
const userController = new UserController(userService);

// Routes
app.use('/api/users', createUserRoutes(userController));

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

// Error handler
app.use(errorHandler);

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

## Testing

### Unit Test
```typescript
// tests/unit/user.service.test.ts
import { UserService } from '../../src/services/user.service';
import { UserRepository } from '../../src/repositories/user.repository';

describe('UserService', () => {
    let userService: UserService;
    let userRepository: jest.Mocked<UserRepository>;

    beforeEach(() => {
        userRepository = {
            findByEmail: jest.fn(),
            create: jest.fn(),
            findById: jest.fn()
        } as any;

        userService = new UserService(userRepository);
    });

    describe('createUser', () => {
        it('should create user with valid data', async () => {
            userRepository.findByEmail.mockResolvedValue(null);
            userRepository.create.mockResolvedValue({
                id: 1,
                email: 'test@example.com',
                name: 'Test User',
                passwordHash: 'hashed',
                role: 'USER',
                createdAt: new Date(),
                updatedAt: new Date()
            });

            const result = await userService.createUser({
                email: 'test@example.com',
                password: 'password',
                name: 'Test User'
            });

            expect(result).toHaveProperty('id');
            expect(result.email).toBe('test@example.com');
            expect(result).not.toHaveProperty('passwordHash');
        });
    });
});
```

### Integration Test
```typescript
// tests/integration/user.api.test.ts
import request from 'supertest';
import { app } from '../../src/index';
import { prisma } from '../../src/utils/prisma';

describe('POST /api/users', () => {
    beforeEach(async () => {
        await prisma.user.deleteMany();
    });

    it('should create user with valid data', async () => {
        const response = await request(app)
            .post('/api/users')
            .send({
                email: 'test@example.com',
                password: 'SecurePass123!',
                name: 'Test User'
            })
            .expect(201);

        expect(response.body.data).toHaveProperty('id');
        expect(response.body.data.email).toBe('test@example.com');
    });

    it('should return 400 for invalid email', async () => {
        const response = await request(app)
            .post('/api/users')
            .send({
                email: 'invalid-email',
                password: 'password'
            })
            .expect(400);

        expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
});
```

## Key Patterns

- Use **TypeScript** for type safety
- Use **Zod** for runtime validation
- Use **Prisma** for type-safe database access
- Use **Dependency Injection** for testability
- Use **Repository Pattern** for data access
- Use **Middleware** for cross-cutting concerns
- Use **Jest** for testing
- Use **Prisma Migrate** for database migrations
