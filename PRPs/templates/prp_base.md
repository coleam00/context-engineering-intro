name: "Enhanced PRP Template v3 - Context-Rich with Validation & Learning"
description: |

## Purpose
Template optimized for AI agents to implement features with comprehensive context, self-validation capabilities, and failure pattern learning to achieve working code through iterative refinement.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Learn from Failures**: Incorporate known failure patterns and solutions
6. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
[What needs to be built - be specific about the end state and desires]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcomes]

## Context Validation Checklist
- [ ] All referenced URLs are accessible
- [ ] All referenced files exist in codebase
- [ ] Environment dependencies are available
- [ ] Similar patterns found in codebase
- [ ] API keys/credentials properly configured
- [ ] Required libraries are installed

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]
  status: [verified/needs_check]
  
- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]
  exists: [true/false]
  
- doc: [Library documentation URL] 
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [PRPs/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]

```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase
```bash

```

### Desired Codebase tree with files to be added and responsibility of file
```bash

```

### Known Gotchas & Failure Patterns
```python
# CRITICAL: [Library name] requires [specific setup]
# FAILURE PATTERN: [Common failure scenario]
# SOLUTION: [How to avoid/fix]

# Example patterns from project history:
# FAILURE: FastAPI + SQLAlchemy async context mixing
# SOLUTION: Always use async session, never sync in async context
# FREQUENCY: High - affects 60% of database integrations

# FAILURE: Pydantic v2 validation breaking changes
# SOLUTION: Use Field() instead of ... for optional fields
# FREQUENCY: Medium - affects 30% of model definitions

# Add project-specific patterns here as they're discovered
```

### Similar Feature Analysis
```yaml
# Patterns found in codebase:
similar_features:
  - file: "src/feature_x.py"
    similarity: "85%"
    reusable_patterns: ["error handling", "async structure"]
    
  - file: "src/feature_y.py" 
    similarity: "70%"
    reusable_patterns: ["validation logic", "response formatting"]

# Recent successful implementations:
recent_successes:
  - prp: "PRPs/auth_system.md"
    success_rate: "100%"
    key_factors: ["comprehensive examples", "OAuth gotchas included"]
    
  - prp: "PRPs/api_integration.md"
    success_rate: "90%"
    key_factors: ["rate limiting handled", "retry logic included"]
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.
```python
Examples: 
 - orm models
 - pydantic models
 - pydantic schemas
 - pydantic validators

```

### Task Breakdown with Dependency Mapping
```yaml
Task 1: [Foundation Task]
DEPENDS_ON: []
CREATES: ["src/models.py", "src/config.py"]
VALIDATES: ["syntax check", "import validation"]
ESTIMATED_TOKENS: ~500
FAILURE_RISK: Low

Task 2: [Core Implementation]
DEPENDS_ON: ["Task 1"]
CREATES: ["src/main_feature.py"]
VALIDATES: ["unit tests", "integration test"]
ESTIMATED_TOKENS: ~1200
FAILURE_RISK: Medium
COMMON_FAILURES: ["async context issues", "validation errors"]

Task 3: [Integration Task]
DEPENDS_ON: ["Task 1", "Task 2"]
CREATES: ["src/api_routes.py", "tests/test_integration.py"]
VALIDATES: ["end-to-end test", "api validation"]
ESTIMATED_TOKENS: ~800
FAILURE_RISK: Medium
ROLLBACK_STRATEGY: "Revert to Task 2 state"

# Add more tasks as needed...
```

### Per Task Implementation Details
```python
# Task 1: Foundation
# PATTERN: Mirror existing config structure
# CRITICAL: Use environment variables for all external dependencies
# GOTCHA: This project uses pydantic-settings v2 syntax

def create_config():
    # ANTI-PATTERN: Don't hardcode values
    # PATTERN: Follow src/config/base.py structure
    pass

# Task 2: Core Implementation  
# PATTERN: Follow async/await throughout
# CRITICAL: Use connection pooling for database operations
# GOTCHA: Library X requires specific initialization order

async def main_feature():
    # FAILURE PATTERN: Mixing sync/async contexts
    # SOLUTION: Always use async variants
    pass
```

### Integration Points & Dependencies
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      # Feature Configuration
      FEATURE_ENABLED=true
      FEATURE_TIMEOUT=30
      FEATURE_API_KEY=your_key_here
      
DATABASE:
  - migration: "Add feature_data table"
  - indexes: ["idx_feature_lookup", "idx_feature_status"]
  - constraints: ["fk_feature_user", "unique_feature_name"]
  
EXTERNAL_APIS:
  - service: "ExternalServiceAPI"
  - rate_limit: "100 req/min"
  - auth_method: "Bearer token"
  - fallback_strategy: "Cache last known good response"
```

## Enhanced Validation Loop

### Level 0: Pre-execution Validation
```bash
# Validate context before starting implementation
echo "Validating PRP context..."

# Check file references
for file in src/example.py src/config.py; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing referenced file: $file"
        exit 1
    fi
done

# Check environment dependencies
python -c "import requests, pydantic, fastapi" 2>/dev/null || {
    echo "❌ Missing required dependencies"
    exit 1
}

# Check API connectivity (if applicable)
curl -s --head "https://api.example.com/health" > /dev/null || {
    echo "⚠️  API connectivity issue - proceeding with mocked responses"
}

echo "✅ Context validation passed"
```

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check . --fix              # Auto-fix style issues
mypy .                          # Type checking
bandit -r . -f json            # Security check

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests with Failure Analysis
```python
# CREATE comprehensive test suite with failure pattern coverage
import pytest
from unittest.mock import Mock, patch

def test_happy_path():
    """Basic functionality works"""
    result = feature_function("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError - common failure pattern"""
    with pytest.raises(ValidationError):
        feature_function("")

def test_external_api_timeout():
    """Handles timeouts gracefully - learned from past failures"""
    with patch('external_api.call', side_effect=TimeoutError):
        result = feature_function("valid")
        assert result.status == "error"
        assert "timeout" in result.message.lower()

def test_rate_limit_handling():
    """Handles rate limiting - common failure in API integrations"""
    with patch('external_api.call', side_effect=RateLimitError):
        result = feature_function("valid")
        assert result.status == "retry_later"

def test_database_connection_loss():
    """Handles database disconnection - infrastructure failure pattern"""
    with patch('database.connection', side_effect=ConnectionError):
        result = feature_function("valid")
        assert result.status == "error"
        assert "database" in result.message.lower()

# Edge cases discovered from similar features:
def test_concurrent_access():
    """Multiple simultaneous requests - learned from feature_x.py"""
    import asyncio
    
    async def concurrent_test():
        tasks = [feature_function(f"input_{i}") for i in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        assert all(not isinstance(r, Exception) for r in results)
    
    asyncio.run(concurrent_test())
```

### Level 3: Integration Test with Real Dependencies
```bash
# Start services in test mode
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be ready
./scripts/wait-for-services.sh

# Run integration tests
pytest tests/integration/ -v --tb=short

# Test the actual endpoints/CLI
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}' | jq .

# Expected: {"status": "success", "data": {...}}
# If error: Check logs and service health
```

### Level 4: Performance & Load Testing
```bash
# Basic performance validation
python -m pytest tests/performance/ -v

# Load testing (if applicable)
ab -n 100 -c 10 http://localhost:8000/feature/

# Memory usage check
python -c "
import psutil
import gc
from src.feature import feature_function

process = psutil.Process()
initial_memory = process.memory_info().rss

# Run feature multiple times
for i in range(100):
    result = feature_function(f'test_{i}')
    if i % 10 == 0:
        gc.collect()

final_memory = process.memory_info().rss
memory_increase = final_memory - initial_memory

print(f'Memory increase: {memory_increase / 1024 / 1024:.2f} MB')
assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase
"
```

## Success Metrics & Monitoring

### Implementation Metrics
```yaml
estimated_metrics:
  token_usage: ~3000 tokens
  implementation_time: ~45 minutes
  confidence_score: 8/10
  similar_feature_success_rate: 85%
  
risk_factors:
  - external_api_dependency: medium
  - database_migration: low
  - authentication_complexity: high
  
success_indicators:
  - all_tests_pass: required
  - performance_benchmarks_met: required
  - security_scan_clean: required
  - documentation_complete: required
```

### Failure Recovery Strategy
```yaml
rollback_plan:
  level_1: "Revert to last working commit"
  level_2: "Disable feature flag, use fallback implementation"
  level_3: "Restore from backup, investigate offline"
  
monitoring:
  - error_rate: "< 1% over 24h"
  - response_time: "< 500ms p95"
  - availability: "> 99.9%"
  
alerts:
  - error_spike: "Slack #alerts"
  - performance_degradation: "Email ops team"
  - external_api_failures: "Auto-retry with exponential backoff"
```

## Final Enhanced Validation Checklist
- [ ] All tests pass: `pytest tests/ -v --cov=src --cov-report=term-missing`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy .`
- [ ] No security issues: `bandit -r . -f json`
- [ ] Performance benchmarks met: `pytest tests/performance/ -v`
- [ ] Integration tests successful: `pytest tests/integration/ -v`
- [ ] Documentation complete and accurate
- [ ] Environment variables documented in .env.example
- [ ] Database migrations (if any) are reversible
- [ ] Monitoring and alerting configured
- [ ] Rollback plan tested and documented

## Post-Implementation Analysis
```yaml
# To be completed after implementation
actual_metrics:
  token_usage: [actual]
  implementation_time: [actual]
  iterations_required: [actual]
  test_failures: [list]
  
lessons_learned:
  - what_worked_well: []
  - what_could_improve: []
  - new_gotchas_discovered: []
  - patterns_to_reuse: []
  
template_improvements:
  - context_gaps_found: []
  - validation_gaps_found: []
  - missing_documentation: []
  - suggested_template_updates: []
```

---

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't skip context validation steps
- ❌ Don't ignore known failure patterns
- ❌ Don't proceed without rollback strategy

## Confidence Score: [X/10]
[Reasoning for confidence score based on context completeness, similar feature success rate, and risk factors]
