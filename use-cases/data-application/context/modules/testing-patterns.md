# Testing Patterns

## Testing Pyramid

```
        /\
       /  \      E2E Tests (5-10%)
      /____\
     /      \    Integration Tests (20-30%)
    /________\
   /          \  Unit Tests (60-70%)
  /____________\
```

## Unit Testing

### Test Structure (AAA Pattern)
```typescript
describe('UserService', () => {
    describe('createUser', () => {
        it('should create a user with valid data', async () => {
            // Arrange
            const userData = {
                email: 'test@example.com',
                password: 'SecurePass123!',
                name: 'Test User'
            };
            const mockRepo = {
                create: jest.fn().mockResolvedValue({ id: 1, ...userData })
            };
            const service = new UserService(mockRepo);

            // Act
            const result = await service.createUser(userData);

            // Assert
            expect(result).toHaveProperty('id');
            expect(result.email).toBe(userData.email);
            expect(mockRepo.create).toHaveBeenCalledWith(
                expect.objectContaining({
                    email: userData.email,
                    passwordHash: expect.any(String)
                })
            );
        });

        it('should throw error for duplicate email', async () => {
            // Arrange
            const userData = { email: 'existing@example.com', password: 'pass' };
            const mockRepo = {
                create: jest.fn().mockRejectedValue(
                    new Error('UNIQUE constraint failed')
                )
            };
            const service = new UserService(mockRepo);

            // Act & Assert
            await expect(service.createUser(userData))
                .rejects
                .toThrow('Email already exists');
        });
    });
});
```

### Mocking Dependencies
```typescript
import { jest } from '@jest/globals';

// Mock external module
jest.mock('stripe', () => ({
    Stripe: jest.fn().mockImplementation(() => ({
        paymentIntents: {
            create: jest.fn().mockResolvedValue({ id: 'pi_123', status: 'succeeded' })
        }
    }))
}));

// Mock database
const mockDb = {
    query: jest.fn(),
    connect: jest.fn(),
    release: jest.fn()
};

// Spy on methods
const emailService = new EmailService();
const sendSpy = jest.spyOn(emailService, 'send');

await userService.register(userData);

expect(sendSpy).toHaveBeenCalledWith(
    userData.email,
    'Welcome Email',
    expect.any(String)
);
```

### Test Coverage
```bash
# Run tests with coverage
npm test -- --coverage

# Coverage thresholds in package.json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Integration Testing

### Database Integration Tests
```typescript
import { Pool } from 'pg';

describe('UserRepository Integration Tests', () => {
    let pool: Pool;
    let repository: UserRepository;

    beforeAll(async () => {
        // Use test database
        pool = new Pool({
            connectionString: process.env.TEST_DATABASE_URL
        });
        repository = new UserRepository(pool);

        // Run migrations
        await runMigrations(pool);
    });

    beforeEach(async () => {
        // Clean database before each test
        await pool.query('TRUNCATE users CASCADE');
    });

    afterAll(async () => {
        await pool.end();
    });

    it('should create and retrieve user', async () => {
        // Create user
        const user = await repository.create({
            email: 'test@example.com',
            passwordHash: 'hashed'
        });

        expect(user.id).toBeDefined();

        // Retrieve user
        const found = await repository.findById(user.id);

        expect(found).toEqual(user);
    });
});
```

### API Integration Tests
```typescript
import request from 'supertest';
import { app } from '../app';

describe('POST /api/users', () => {
    beforeEach(async () => {
        await clearDatabase();
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

    it('should require authentication for protected endpoints', async () => {
        await request(app)
            .get('/api/users/1')
            .expect(401);
    });

    it('should allow access with valid token', async () => {
        const token = await getAuthToken('user@example.com');

        await request(app)
            .get('/api/users/1')
            .set('Authorization', `Bearer ${token}`)
            .expect(200);
    });
});
```

### Test Containers (Docker)
```typescript
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('Integration Tests with TestContainers', () => {
    let postgresContainer: StartedTestContainer;
    let redisContainer: StartedTestContainer;

    beforeAll(async () => {
        // Start PostgreSQL container
        postgresContainer = await new GenericContainer('postgres:15')
            .withEnvironment({
                POSTGRES_USER: 'test',
                POSTGRES_PASSWORD: 'test',
                POSTGRES_DB: 'testdb'
            })
            .withExposedPorts(5432)
            .start();

        // Start Redis container
        redisContainer = await new GenericContainer('redis:7-alpine')
            .withExposedPorts(6379)
            .start();

        // Update connection strings
        process.env.DATABASE_URL = `postgresql://test:test@${postgresContainer.getHost()}:${postgresContainer.getMappedPort(5432)}/testdb`;
        process.env.REDIS_URL = `redis://${redisContainer.getHost()}:${redisContainer.getMappedPort(6379)}`;
    }, 60000);  // Longer timeout for container startup

    afterAll(async () => {
        await postgresContainer.stop();
        await redisContainer.stop();
    });

    // Your integration tests here...
});
```

## Mocking External APIs

### Using nock (Node.js)
```typescript
import nock from 'nock';

describe('PaymentService', () => {
    afterEach(() => {
        nock.cleanAll();
    });

    it('should process payment successfully', async () => {
        // Mock external payment API
        nock('https://api.stripe.com')
            .post('/v1/payment_intents')
            .reply(200, {
                id: 'pi_123',
                status: 'succeeded',
                amount: 1000
            });

        const service = new PaymentService();
        const result = await service.processPayment({
            amount: 1000,
            currency: 'usd'
        });

        expect(result.status).toBe('succeeded');
    });

    it('should handle API errors', async () => {
        nock('https://api.stripe.com')
            .post('/v1/payment_intents')
            .reply(402, {
                error: {
                    message: 'Insufficient funds'
                }
            });

        const service = new PaymentService();

        await expect(
            service.processPayment({ amount: 1000, currency: 'usd' })
        ).rejects.toThrow('Payment failed');
    });

    it('should retry on network errors', async () => {
        // First attempt fails
        nock('https://api.stripe.com')
            .post('/v1/payment_intents')
            .replyWithError('Network error');

        // Second attempt succeeds
        nock('https://api.stripe.com')
            .post('/v1/payment_intents')
            .reply(200, { id: 'pi_123', status: 'succeeded' });

        const service = new PaymentService();
        const result = await service.processPayment({ amount: 1000, currency: 'usd' });

        expect(result.status).toBe('succeeded');
    });
});
```

### Using WireMock (Java)
```java
@SpringBootTest
@AutoConfigureWireMock(port = 8089)
class PaymentServiceTest {

    @Autowired
    private PaymentService paymentService;

    @Test
    void shouldProcessPaymentSuccessfully() {
        // Setup WireMock stub
        stubFor(post(urlEqualTo("/v1/payment_intents"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("""
                    {
                        "id": "pi_123",
                        "status": "succeeded",
                        "amount": 1000
                    }
                    """)));

        PaymentResult result = paymentService.processPayment(
            new PaymentRequest(1000, "usd")
        );

        assertEquals("succeeded", result.getStatus());
    }
}
```

## Load Testing

### Using k6
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '30s', target: 20 },   // Ramp up to 20 users
        { duration: '1m', target: 20 },    // Stay at 20 users
        { duration: '30s', target: 50 },   // Ramp up to 50 users
        { duration: '1m', target: 50 },    // Stay at 50 users
        { duration: '30s', target: 0 },    // Ramp down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<200', 'p(99)<500'],  // 95% < 200ms, 99% < 500ms
        http_req_failed: ['rate<0.01'],                  // Error rate < 1%
    },
};

export default function () {
    const response = http.get('http://localhost:3000/api/products');

    check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 200ms': (r) => r.timings.duration < 200,
    });

    sleep(1);
}
```

### Run Load Test
```bash
# Install k6
brew install k6  # macOS
# or download from k6.io

# Run test
k6 run load-test.js

# Run with custom options
k6 run --vus 10 --duration 30s load-test.js
```

## Test Data Management

### Factories
```typescript
import { faker } from '@faker-js/faker';

class UserFactory {
    static build(overrides?: Partial<User>): User {
        return {
            id: faker.number.int(),
            email: faker.internet.email(),
            name: faker.person.fullName(),
            createdAt: faker.date.past(),
            ...overrides
        };
    }

    static buildMany(count: number): User[] {
        return Array.from({ length: count }, () => this.build());
    }
}

// Usage in tests
const user = UserFactory.build({ email: 'specific@example.com' });
const users = UserFactory.buildMany(10);
```

### Fixtures
```typescript
// fixtures/users.json
[
    {
        "id": 1,
        "email": "admin@example.com",
        "role": "admin"
    },
    {
        "id": 2,
        "email": "user@example.com",
        "role": "user"
    }
]

// Load fixtures in tests
import usersFixture from './fixtures/users.json';

beforeEach(async () => {
    await User.bulkCreate(usersFixture);
});
```

## E2E Testing

### Using Playwright
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
    test('should register new user successfully', async ({ page }) => {
        await page.goto('http://localhost:3000/register');

        // Fill form
        await page.fill('input[name="email"]', 'test@example.com');
        await page.fill('input[name="password"]', 'SecurePass123!');
        await page.fill('input[name="name"]', 'Test User');

        // Submit
        await page.click('button[type="submit"]');

        // Check redirect
        await expect(page).toHaveURL(/.*\/dashboard/);

        // Check welcome message
        await expect(page.locator('h1')).toContainText('Welcome, Test User');
    });

    test('should show validation errors', async ({ page }) => {
        await page.goto('http://localhost:3000/register');

        await page.click('button[type="submit"]');

        await expect(page.locator('.error')).toContainText('Email is required');
    });
});
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@postgres:5432/testdb
          REDIS_URL: redis://redis:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Testing Checklist

- [ ] Unit tests for all business logic (>80% coverage)
- [ ] Integration tests for database operations
- [ ] API integration tests for all endpoints
- [ ] Authentication/authorization tests
- [ ] Error handling tests
- [ ] External API mocking (WireMock/nock)
- [ ] Load/performance tests
- [ ] Security tests (SQL injection, XSS)
- [ ] E2E tests for critical flows
- [ ] Tests run in CI/CD
