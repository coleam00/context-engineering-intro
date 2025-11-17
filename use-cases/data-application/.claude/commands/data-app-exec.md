# Data Application Execution & Validation

Execute validation and testing based on the tier of the application.

## Prerequisites

- Implementation must be complete
- Project folder must exist with source code
- PLAN.md or planning/ folder must exist

## Validation Workflow by Tier

### Tier 1: Simple CRUD (Inline Validation)

**Duration: 5-10 minutes**

1. **Run Basic Validations**

```bash
# Check project structure
ls -R applications/{project_name}

# Check for required files
test -f applications/{project_name}/package.json || echo "Missing package.json"
test -f applications/{project_name}/docker-compose.yml || echo "Missing docker-compose.yml"
test -f applications/{project_name}/.env.example || echo "Missing .env.example"
```

2. **Run Linting** (if applicable)
```bash
cd applications/{project_name}
npm run lint  # or appropriate command for tech stack
```

3. **Run Unit Tests**
```bash
cd applications/{project_name}
npm test  # or: mvn test, pytest, dotnet test
```

4. **Run Integration Tests**
```bash
cd applications/{project_name}
npm run test:integration  # with test database
```

5. **Test Docker Setup**
```bash
cd applications/{project_name}
docker-compose up -d
docker-compose ps
# Check health
curl http://localhost:3000/health
docker-compose down
```

6. **Generate Report**

```
✅ Validation Complete (Tier 1)

Project Structure: ✅ All required files present
Linting: ✅ No errors
Unit Tests: ✅ {X} tests passed (coverage: {Y}%)
Integration Tests: ✅ {Z} tests passed
Docker: ✅ Containers start successfully
Health Check: ✅ Application responds

📊 Summary:
- Database schema: {X} entities
- API endpoints: {Y} endpoints working
- Test coverage: {Z}%
- Docker: Ready for deployment

🚀 Next Steps:
1. Review the code in applications/{project_name}/
2. Customize .env.example with your actual credentials
3. Run: docker-compose up -d
4. Access API at: http://localhost:3000
5. View API docs at: http://localhost:3000/api-docs

Your application is ready to use!
```

---

### Tier 2: Standard REST API (Agent-Assisted Validation)

**Duration: 15-20 minutes**

1. **Run Static Analysis**
```bash
cd applications/{project_name}
npm run lint
npm run type-check  # TypeScript/Java type checking
```

2. **Run Unit Tests with Coverage**
```bash
cd applications/{project_name}
npm run test:coverage
# Verify >80% coverage threshold
```

3. **Invoke Integration Validator Agent**

```
Use Task tool to invoke: integration-validator

Prompt: "Validate the standard REST API application at applications/{project_name}.

Validation tasks:
1. Test all API endpoints (CRUD operations)
2. Test authentication and authorization flows
3. Test input validation and error handling
4. Test external API integrations (with mocks/stubs)
5. Test Redis caching functionality
6. Test rate limiting
7. Run security checks (SQL injection, XSS prevention)
8. Load test with moderate traffic (100 concurrent users)
9. Verify Docker setup and health checks

Use docker-compose to spin up test environment.

Expected outputs:
- All API endpoints return correct responses
- Authentication works correctly
- All tests pass
- Security vulnerabilities: 0
- Load test: p95 < 200ms, p99 < 500ms
- Error rate < 1%

Generate detailed validation report."
```

4. **Wait for Agent to Complete**

5. **Review Agent Report**

6. **Generate Final Summary**

```
✅ Validation Complete (Tier 2)

Static Analysis: ✅ No errors or warnings
Unit Tests: ✅ {X} tests passed (coverage: {Y}%)
Integration Tests: ✅ {Z} tests passed

🤖 Integration Validator Agent Results:
  ✅ All {N} API endpoints working
  ✅ Authentication & authorization verified
  ✅ Input validation working correctly
  ✅ External integrations tested (with mocks)
  ✅ Redis caching functional
  ✅ Rate limiting operational
  ✅ Security scan: 0 vulnerabilities
  ✅ Load test passed:
     - p95 latency: {X}ms
     - p99 latency: {Y}ms
     - Error rate: {Z}%
  ✅ Docker health checks passing

📊 Summary:
- Database: {X} entities with proper indexes
- API: {Y} endpoints with authentication
- Integrations: {Z} external systems tested
- Security: All checks passed
- Performance: Meets SLAs
- Test coverage: {W}%

🚀 Next Steps:
1. Review the code in applications/{project_name}/
2. Configure .env with real API keys
3. Run: docker-compose up -d
4. Access API at: http://localhost:3000
5. View API docs at: http://localhost:3000/api-docs
6. Review integration guide in docs/

Your application is production-ready!
```

---

### Tier 3: Enterprise Application (Multi-Agent Validation)

**Duration: 20-30 minutes**

1. **Update Archon** (if available)
   - Mark Task 6 "Validation & Testing" as "doing"

2. **Run Static Analysis & Unit Tests**
```bash
cd applications/{project_name}
# Java: mvn clean verify
# Node: npm run lint && npm run test:coverage
# Check coverage >80%
```

3. **Invoke Integration Validator Agent**

```
Use Task tool to invoke: integration-validator

Prompt: "Validate the enterprise application at applications/{project_name}.

This is a Tier 3 enterprise application with:
- Complex database schema with {X} entities
- {Y} REST API endpoints
- {Z} external system integrations
- Message queue processing
- Multi-layer caching
- Comprehensive security

Validation tasks:
1. Database Integration
   - Test all CRUD operations
   - Verify transactions and rollbacks
   - Test connection pooling
   - Verify database migrations
   - Check index usage

2. API Testing
   - Test all REST endpoints
   - Verify authentication (JWT)
   - Test role-based authorization
   - Verify API versioning
   - Test pagination, filtering, sorting

3. External Integrations (CRITICAL)
   - Test all {Z} external system integrations
   - Use WireMock for mocking external APIs
   - Test retry and circuit breaker logic
   - Verify error handling
   - Test webhook handlers

4. Message Queue
   - Test event producers
   - Test event consumers
   - Verify message ordering
   - Test error handling and dead letter queues

5. Caching
   - Verify L1 (in-memory) cache
   - Verify L2 (Redis) cache
   - Test cache invalidation
   - Measure cache hit ratios

6. Security
   - SQL injection testing
   - XSS prevention testing
   - CSRF protection testing
   - Authentication bypass attempts
   - Authorization boundary testing

7. Docker Environment Testing
   - Use docker-compose.test.yml
   - Spin up full test environment
   - Run all integration tests
   - Verify monitoring endpoints
   - Test health checks

8. Environment Configuration
   - Verify all .env.example variables used in docker-compose.yml
   - Test Redis authentication with REDIS_PASSWORD
   - Verify database connection with env vars
   - Test all environment variable substitutions

Generate comprehensive validation report with:
- Test results summary
- Performance metrics
- Security scan results
- Coverage statistics
- Recommendations for improvements"
```

4. **In Parallel, Invoke Performance Tester Agent** (Optional but recommended)

```
Use Task tool to invoke: performance-tester

Prompt: "Run performance tests on the enterprise application at applications/{project_name}.

Load Test Scenarios:
1. Normal Load (100 concurrent users, 5 minutes)
2. Peak Load (500 concurrent users, 5 minutes)
3. Stress Test (gradually increase to 1000 users)
4. Spike Test (sudden increase to 1000 users)

Test these endpoints:
- {list critical endpoints}

Performance SLAs:
- p95 response time < 200ms
- p99 response time < 500ms
- Error rate < 0.1%
- Throughput > 1000 req/s

Use k6 or JMeter for load testing.

Generate report with:
- Response time percentiles
- Throughput metrics
- Error rates
- Resource utilization
- Bottleneck identification
- Optimization recommendations"
```

5. **Wait for Both Agents to Complete**

6. **Update Archon** (if available)
   - Mark Task 6 as "done"
   - Add validation results summary

7. **Synthesize Results and Generate Final Report**

```
✅ Validation Complete (Tier 3 - Enterprise)

Static Analysis: ✅ No errors or warnings
Unit Tests: ✅ {X} tests passed (coverage: {Y}%)

🤖 Integration Validator Results:
  ✅ Database: All operations working, migrations verified
  ✅ API: All {N} endpoints tested and working
  ✅ Authentication: JWT working, role-based auth verified
  ✅ External Integrations: All {Z} systems tested with WireMock
     - {List each system}: ✅
  ✅ Message Queue: Event processing working correctly
  ✅ Caching: Multi-layer cache operational
     - L1 cache hit ratio: {X}%
     - L2 cache hit ratio: {Y}%
  ✅ Security: All checks passed, 0 vulnerabilities
  ✅ Docker Environment: Full stack tested successfully
  ✅ Environment Config: All variables properly configured

🚀 Performance Test Results:
  ✅ Normal Load (100 users):
     - p95: {X}ms, p99: {Y}ms ✅
     - Throughput: {Z} req/s ✅
  ✅ Peak Load (500 users):
     - p95: {X}ms, p99: {Y}ms ✅
     - Throughput: {Z} req/s ✅
  ✅ Stress Test: System handles up to {X} concurrent users
  ✅ Error Rate: {Y}% (well below 0.1% threshold)

📊 Enterprise Application Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Database:
  - {X} entities with optimized schema
  - Multi-layer caching working
  - Connection pooling configured

APIs & Integration:
  - {Y} REST endpoints (all tested)
  - {Z} external system integrations
  - Message queue processing operational

Security:
  - JWT authentication ✅
  - Role-based authorization ✅
  - Input validation ✅
  - Audit logging ✅
  - All security scans passed ✅

Performance:
  - Response times meet SLAs ✅
  - Handles expected load ✅
  - Auto-scaling configured ✅

Deployment:
  - Docker containerization ✅
  - Kubernetes manifests ready ✅
  - CI/CD pipeline configured ✅
  - Monitoring and logging ✅

Test Coverage: {W}% (exceeds 80% requirement)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Production Deployment Ready!

Next Steps:
1. Review all code in applications/{project_name}/
2. Review architecture docs in applications/{project_name}/planning/
3. Configure production .env with real credentials
4. Review deployment guide in docs/deployment/
5. Deploy to staging first:
   - Update image tags in deployment/kubernetes/
   - Apply manifests: kubectl apply -f deployment/kubernetes/
6. Run smoke tests in staging
7. Deploy to production with monitoring

📚 Documentation:
- API Documentation: applications/{project_name}/docs/api/
- Integration Guides: applications/{project_name}/docs/integration/
- Deployment Guide: applications/{project_name}/docs/deployment/
- README: applications/{project_name}/README.md

{If Archon available:}
📊 Archon Project: {project_link}
   All tasks completed successfully!

Your enterprise application is production-ready! 🎉
```

## Error Handling

If implementation not found:
```
❌ Error: No implementation found at applications/{project_name}/
Please complete the implementation first.
```

If tests fail:
```
⚠️  Tests Failed!

Failed tests:
{list failures}

I'll now attempt to fix the failing tests...
{attempt fixes}

Re-running tests...
{show results}
```

If agents fail:
```
⚠️  Warning: Validation agent failed. Running manual validation...
{fallback to inline validation}
```

## Success Criteria by Tier

**Tier 1:**
- All unit tests pass
- Integration tests pass
- Docker starts successfully
- Health check responds

**Tier 2:**
- All above, plus:
- >80% test coverage
- Security scan clean
- Load test meets SLAs
- External integrations tested

**Tier 3:**
- All above, plus:
- All external systems integrated and tested
- Message queue processing verified
- Multi-layer caching working
- Performance tests pass under load
- Kubernetes manifests validated
- Full observability working
