# Security Patterns

## Authentication

### JWT (JSON Web Tokens)
```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

// Login
async function login(email: string, password: string) {
    const user = await userRepository.findByEmail(email);
    if (!user) {
        throw new UnauthorizedError('Invalid credentials');
    }

    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) {
        throw new UnauthorizedError('Invalid credentials');
    }

    const accessToken = jwt.sign(
        { userId: user.id, email: user.email, role: user.role },
        process.env.JWT_SECRET!,
        { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
        { userId: user.id },
        process.env.JWT_REFRESH_SECRET!,
        { expiresIn: '7d' }
    );

    return { accessToken, refreshToken, user };
}

// Authentication middleware
function authenticateJWT(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.substring(7);

    try {
        const payload = jwt.verify(token, process.env.JWT_SECRET!);
        req.user = payload;
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
    }
}
```

### Password Hashing
```typescript
import bcrypt from 'bcrypt';
import argon2 from 'argon2';

// bcrypt (good for most applications)
const saltRounds = 12;
const hash = await bcrypt.hash(password, saltRounds);
const isValid = await bcrypt.compare(password, hash);

// argon2 (recommended for high-security applications)
const hash = await argon2.hash(password);
const isValid = await argon2.verify(hash, password);
```

## Authorization

### Role-Based Access Control (RBAC)
```typescript
enum Role {
    ADMIN = 'admin',
    MANAGER = 'manager',
    USER = 'user'
}

function requireRole(allowedRoles: Role[]) {
    return (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}

// Usage
app.delete('/api/users/:id',
    authenticateJWT,
    requireRole([Role.ADMIN]),
    deleteUser
);
```

### Permission-Based Access Control
```typescript
enum Permission {
    READ_USERS = 'users:read',
    WRITE_USERS = 'users:write',
    DELETE_USERS = 'users:delete',
    READ_ORDERS = 'orders:read',
    WRITE_ORDERS = 'orders:write'
}

const rolePermissions: Record<Role, Permission[]> = {
    [Role.ADMIN]: [
        Permission.READ_USERS,
        Permission.WRITE_USERS,
        Permission.DELETE_USERS,
        Permission.READ_ORDERS,
        Permission.WRITE_ORDERS
    ],
    [Role.MANAGER]: [
        Permission.READ_USERS,
        Permission.WRITE_USERS,
        Permission.READ_ORDERS,
        Permission.WRITE_ORDERS
    ],
    [Role.USER]: [
        Permission.READ_ORDERS
    ]
};

function requirePermission(permission: Permission) {
    return (req: Request, res: Response, next: NextFunction) => {
        const userPermissions = rolePermissions[req.user.role] || [];

        if (!userPermissions.includes(permission)) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}
```

## Input Validation & Sanitization

### SQL Injection Prevention
```typescript
// BAD: String concatenation (SQL injection vulnerability)
const query = `SELECT * FROM users WHERE email = '${email}'`;

// GOOD: Parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
const result = await pool.query(query, [email]);

// GOOD: ORM (Sequelize, TypeORM, Prisma)
const user = await User.findOne({ where: { email } });
```

### XSS Prevention
```typescript
import validator from 'validator';
import DOMPurify from 'isomorphic-dompurify';

// Sanitize HTML input
const cleanHtml = DOMPurify.sanitize(userInput);

// Escape output in templates
// React/Vue automatically escape by default
// In Express: use template engine with auto-escaping

// Validate and sanitize
const sanitizedEmail = validator.normalizeEmail(email);
const sanitizedUrl = validator.isURL(url) ? url : null;
```

### CSRF Protection
```typescript
import csrf from 'csurf';

// Add CSRF protection
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
    res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/form', csrfProtection, (req, res) => {
    // Process form
});
```

## Data Encryption

### Encryption at Rest
```typescript
import crypto from 'crypto';

// Encrypt sensitive data before storing
function encrypt(text: string, key: string): string {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', Buffer.from(key, 'hex'), iv);

    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag().toString('hex');
    return `${iv.toString('hex')}:${authTag}:${encrypted}`;
}

function decrypt(encryptedData: string, key: string): string {
    const [ivHex, authTagHex, encrypted] = encryptedData.split(':');
    const decipher = crypto.createDecipheriv(
        'aes-256-gcm',
        Buffer.from(key, 'hex'),
        Buffer.from(ivHex, 'hex')
    );

    decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}
```

### TLS/SSL Configuration
```typescript
import https from 'https';
import fs from 'fs';

const options = {
    key: fs.readFileSync('private-key.pem'),
    cert: fs.readFileSync('certificate.pem'),
    minVersion: 'TLSv1.2',  // Minimum TLS version
    ciphers: 'HIGH:!aNULL:!MD5'  // Strong ciphers only
};

const server = https.createServer(options, app);
```

## Secrets Management

### Environment Variables
```bash
# .env (never commit to git!)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-secret-key-min-32-characters-long
JWT_REFRESH_SECRET=another-secret-key-min-32-chars
ENCRYPTION_KEY=64-char-hex-string
API_KEY=external-api-key
```

### Loading Secrets
```typescript
import dotenv from 'dotenv';

// Load from .env file
dotenv.config();

// Validate required secrets exist
const requiredEnvVars = [
    'DATABASE_URL',
    'JWT_SECRET',
    'JWT_REFRESH_SECRET',
    'ENCRYPTION_KEY'
];

for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
        throw new Error(`Missing required environment variable: ${envVar}`);
    }
}
```

### Secret Rotation
```typescript
// Support multiple JWT secrets for rotation
const JWT_SECRETS = [
    process.env.JWT_SECRET,          // Current
    process.env.JWT_SECRET_PREVIOUS  // Previous (during rotation)
].filter(Boolean);

function verifyToken(token: string) {
    for (const secret of JWT_SECRETS) {
        try {
            return jwt.verify(token, secret!);
        } catch (error) {
            // Try next secret
            continue;
        }
    }
    throw new Error('Invalid token');
}
```

## Rate Limiting & DDoS Protection

### API Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

const limiter = rateLimit({
    store: new RedisStore({
        client: redis,
        prefix: 'rl:'
    }),
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 100,                   // Max 100 requests
    standardHeaders: true,
    legacyHeaders: false,
    message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);
```

### Brute Force Protection
```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,  // Max 5 login attempts
    skipSuccessfulRequests: true  // Don't count successful logins
});

app.post('/api/auth/login', loginLimiter, loginHandler);
```

## Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet());  // Enables multiple security headers

// Or configure individually
app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:']
    }
}));

app.use(helmet.hsts({
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
}));
```

## Audit Logging

```typescript
interface AuditLog {
    userId: number;
    action: string;
    resource: string;
    resourceId?: string;
    changes?: any;
    ipAddress: string;
    userAgent: string;
    timestamp: Date;
}

async function logAudit(log: AuditLog) {
    await db.query(
        `INSERT INTO audit_logs (
            user_id, action, resource, resource_id,
            changes, ip_address, user_agent, timestamp
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
        [
            log.userId,
            log.action,
            log.resource,
            log.resourceId,
            JSON.stringify(log.changes),
            log.ipAddress,
            log.userAgent,
            log.timestamp
        ]
    );
}

// Usage in controller
async function updateUser(req: Request, res: Response) {
    const oldUser = await userRepository.findById(req.params.id);
    const updatedUser = await userRepository.update(req.params.id, req.body);

    await logAudit({
        userId: req.user.id,
        action: 'UPDATE',
        resource: 'user',
        resourceId: req.params.id,
        changes: { before: oldUser, after: updatedUser },
        ipAddress: req.ip,
        userAgent: req.get('user-agent') || '',
        timestamp: new Date()
    });

    res.json({ data: updatedUser });
}
```

## Security Checklist

### Before Production
- [ ] All secrets in environment variables (not hardcoded)
- [ ] HTTPS/TLS enabled
- [ ] Strong password hashing (bcrypt/argon2)
- [ ] JWT tokens with short expiration
- [ ] CORS properly configured
- [ ] SQL injection protection (parameterized queries)
- [ ] XSS protection (input sanitization, output escaping)
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Security headers enabled (helmet)
- [ ] Audit logging implemented
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies regularly updated
- [ ] Security scanning in CI/CD
