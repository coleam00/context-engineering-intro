# Core Principles for Data Application Development

## Universal Rules

These principles apply to ALL data applications regardless of complexity tier:

### 1. **Simplicity First**
- Start with the simplest solution that meets requirements
- Add complexity only when justified by actual needs
- YAGNI (You Aren't Gonna Need It) - don't build speculative features

### 2. **Type Safety & Validation**
- Use strong typing throughout (TypeScript, Java generics, Python type hints, C# types)
- Validate at boundaries (API inputs, database writes, external integrations)
- Fail fast with clear error messages

### 3. **Security by Default**
- Never hardcode credentials (use environment variables or secret managers)
- Encrypt sensitive data at rest and in transit (TLS/SSL mandatory)
- Apply principle of least privilege for database access
- Implement proper authentication and authorization

### 4. **Data Integrity**
- Use database constraints (foreign keys, unique constraints, not null)
- Implement transactions for multi-step operations
- Validate business rules at application layer

### 5. **Testing Strategy**
- Unit tests for business logic (>80% coverage)
- Integration tests for database operations
- API tests for endpoints
- Test both happy path and error cases

### 6. **Observability**
- Structured logging (JSON format recommended)
- Log errors with context (stack traces, request IDs, user IDs)
- Add health check endpoints
- Monitor key metrics (response times, error rates, database connections)

### 7. **Configuration Management**
- Use environment variables for all configuration
- Create .env.example with all required variables
- Support multiple environments (dev, staging, prod)
- Never commit secrets to version control

### 8. **Code Organization**
- Separate concerns (controllers, services, repositories, models)
- Keep functions small and focused (single responsibility)
- Use consistent naming conventions
- Document non-obvious decisions

### 9. **Error Handling**
- Handle errors gracefully at all layers
- Return appropriate HTTP status codes
- Provide meaningful error messages (dev mode) vs safe messages (prod mode)
- Implement retry logic for transient failures

### 10. **Performance Awareness**
- Index database columns used in WHERE clauses and JOINs
- Implement pagination for list endpoints
- Use connection pooling for databases
- Cache expensive operations when appropriate

## Anti-Patterns to Avoid

- ❌ **God objects** - Services that do everything
- ❌ **Leaky abstractions** - Implementation details exposed in APIs
- ❌ **Magic numbers** - Use named constants
- ❌ **Silent failures** - Always log errors
- ❌ **Premature optimization** - Profile before optimizing
- ❌ **Tight coupling** - Depend on interfaces, not implementations
