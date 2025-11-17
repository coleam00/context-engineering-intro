# Database Design Patterns

## Schema Design

### Entity Design Checklist
- [ ] Primary key (auto-increment ID or UUID)
- [ ] Foreign keys with proper constraints
- [ ] Unique constraints where needed
- [ ] Not null constraints for required fields
- [ ] Default values for optional fields
- [ ] Timestamps (created_at, updated_at)
- [ ] Soft deletes (deleted_at) if needed
- [ ] Audit fields (created_by, updated_by) if needed

### Relationships
```sql
-- One-to-Many
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL
);

-- Many-to-Many
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

## Indexing Strategy

### When to Add Indexes
- Columns used in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY
- Columns with high cardinality (many unique values)

### Index Types
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Unique index
CREATE UNIQUE INDEX idx_products_sku ON products(sku);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- Full-text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || content));
```

## Query Optimization

### N+1 Query Problem
```javascript
// BAD: N+1 queries
const users = await User.findAll();
for (const user of users) {
    user.posts = await Post.findAll({ where: { userId: user.id } });
}

// GOOD: Single query with eager loading
const users = await User.findAll({
    include: [{ model: Post }]
});
```

### Pagination
```sql
-- Use LIMIT and OFFSET
SELECT * FROM products
ORDER BY id
LIMIT 20 OFFSET 40;  -- Page 3 (20 items per page)

-- Better: Use cursor-based pagination for large datasets
SELECT * FROM products
WHERE id > 1000  -- Last ID from previous page
ORDER BY id
LIMIT 20;
```

## Migration Best Practices

### Migration Structure
```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users_rollback.sql
DROP TABLE IF EXISTS users;
```

### Safe Migration Practices
- Always provide rollback scripts
- Test migrations on staging first
- Avoid blocking operations on large tables
- Use transactions where supported
- Add indexes after data insertion (for large datasets)

## Connection Pooling

### Configuration
```javascript
// Node.js (pg)
const pool = new Pool({
    host: 'localhost',
    database: 'mydb',
    max: 20,                    // Maximum connections
    idleTimeoutMillis: 30000,   // Close idle connections after 30s
    connectionTimeoutMillis: 2000  // Timeout after 2s
});

// Java (HikariCP)
HikariConfig config = new HikariConfig();
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(2000);
config.setIdleTimeout(300000);
```

## Transaction Management

### ACID Properties
```javascript
// Node.js example
async function transferMoney(fromId, toId, amount) {
    const client = await pool.connect();
    try {
        await client.query('BEGIN');

        // Debit from account
        await client.query(
            'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
            [amount, fromId]
        );

        // Credit to account
        await client.query(
            'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
            [amount, toId]
        );

        await client.query('COMMIT');
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release();
    }
}
```

## Repository Pattern

```typescript
// TypeScript example
interface Repository<T> {
    findById(id: number): Promise<T | null>;
    findAll(filters?: any): Promise<T[]>;
    create(data: Partial<T>): Promise<T>;
    update(id: number, data: Partial<T>): Promise<T>;
    delete(id: number): Promise<boolean>;
}

class UserRepository implements Repository<User> {
    async findById(id: number): Promise<User | null> {
        const result = await pool.query(
            'SELECT * FROM users WHERE id = $1',
            [id]
        );
        return result.rows[0] || null;
    }

    async findAll(filters?: { email?: string }): Promise<User[]> {
        let query = 'SELECT * FROM users WHERE deleted_at IS NULL';
        const params: any[] = [];

        if (filters?.email) {
            query += ' AND email = $1';
            params.push(filters.email);
        }

        const result = await pool.query(query, params);
        return result.rows;
    }

    // ... other methods
}
```

## Performance Monitoring

### Slow Query Logging
```sql
-- PostgreSQL: Enable slow query log
ALTER DATABASE mydb SET log_min_duration_statement = 1000;  -- Log queries > 1s

-- Analyze query performance
EXPLAIN ANALYZE
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id, u.name;
```

### Key Metrics to Monitor
- Query execution time (p95, p99)
- Connection pool utilization
- Cache hit ratio
- Number of slow queries
- Dead tuple count (PostgreSQL)
- Index usage statistics
