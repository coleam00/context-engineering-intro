# Chapter 13: Troubleshooting

> **"Every Context Engineering failure is a learning opportunity that makes your system more robust."**

This chapter provides a comprehensive guide to diagnosing and fixing common Context Engineering issues. You'll learn systematic troubleshooting approaches and build resilience into your context systems.

## 🎯 Learning Objectives

By the end of this chapter, you will:
- Diagnose common Context Engineering failure modes
- Apply systematic troubleshooting methodologies
- Prevent recurring issues through context improvements
- Build resilience into your Context Engineering systems
- Know when to iterate vs. when to rebuild context

## 🔍 Diagnostic Framework

### **The Context Engineering Failure Spectrum**

Context Engineering failures typically fall into five categories:

```
Low-Level Failures                    High-Level Failures
      ↓                                      ↓
[Syntax] → [Logic] → [Integration] → [Behavior] → [Strategy]
    ↓        ↓           ↓             ↓          ↓
 Quick     Easy to    Moderate      Hard to    Very hard
 fixes     debug      effort        detect     to fix
```

### **The OSCAR Troubleshooting Method**

Use this systematic approach for any Context Engineering issue:

**O - Observe:** What exactly is happening vs. what should happen?  
**S - Scope:** Is this a context issue, implementation issue, or environmental issue?  
**C - Context:** What context was provided? What might be missing?  
**A - Analyze:** What patterns suggest the root cause?  
**R - Resolve:** Fix root cause and validate solution

## 🐛 Common Failure Modes and Solutions

### **Category 1: Context Insufficiency Failures**

#### **Symptom: Generic/Boilerplate Code**

**What You See:**
```python
# AI generates generic code that doesn't match project patterns
class UserService:
    def __init__(self):
        pass
    
    def create_user(self, data):
        # Basic implementation without error handling,
        # validation, or project-specific patterns
        user = User(data)
        return user
```

**Root Cause Analysis:**
- CLAUDE.md lacks specific patterns and examples
- INITIAL.md doesn't reference relevant existing code
- Examples folder is empty or doesn't contain relevant patterns

**Solution:**
```markdown
## Fix Strategy:
1. **Audit missing context**:
   - What patterns exist in the codebase that weren't referenced?
   - What examples would have guided better implementation?

2. **Add specific examples**:
   ```python
   # examples/services/user_service.py
   class UserService:
       def __init__(self, session: AsyncSession, validator: UserValidator):
           self.session = session
           self.validator = validator
       
       async def create_user(self, user_data: UserCreate) -> User:
           # Pattern: Input validation first
           await self.validator.validate_create_data(user_data)
           
           # Pattern: Transaction management
           async with self.session.begin():
               user = User(**user_data.dict())
               self.session.add(user)
               await self.session.flush()
               return user
   ```

3. **Update CLAUDE.md rules**:
   ```markdown
   ### Service Layer Patterns
   - Always use dependency injection for database sessions
   - Include comprehensive input validation
   - Use transaction management for data mutations
   - Follow the pattern in examples/services/user_service.py
   ```

4. **Enhance INITIAL.md references**:
   ```markdown
   ## EXAMPLES:
   - examples/services/user_service.py - Follow this service layer pattern
   - examples/validation/user_validator.py - Use this validation approach
   - examples/database/transaction_manager.py - Follow transaction patterns
   ```
```

#### **Symptom: Inconsistent Code Style**

**What You See:**
```python
# Mix of styles across different implementations
def createUser(userData):  # camelCase
    pass

async def delete_user_account(user_id: int) -> bool:  # snake_case with types
    pass

def UpdateUserProfile(user, data):  # PascalCase without types
    pass
```

**Root Cause:** CLAUDE.md lacks specific style requirements or examples show inconsistent patterns

**Solution:**
```markdown
## Enhanced CLAUDE.md Style Rules:
### Function Naming and Typing
- **Always use snake_case** for function names
- **Always include type hints** for parameters and return values
- **Use async/await** for all database and external API operations
- **Follow the pattern** in examples/api/user_routes.py

### Example:
```python
async def create_user_account(user_data: UserCreate) -> UserResponse:
    """Create new user account with proper validation."""
```

### Anti-Pattern to Avoid:
```python
def createUser(userData):  # Wrong: camelCase, no types, no async
    pass
```
```

### **Category 2: Context Ambiguity Failures**

#### **Symptom: AI Makes Wrong Technology Choices**

**What You See:**
```python
# AI uses different library than project standard
import requests  # Project uses httpx
import sqlite3   # Project uses SQLAlchemy with PostgreSQL
import json      # Project uses Pydantic models
```

**Root Cause:** CLAUDE.md doesn't specify technology stack or examples use inconsistent libraries

**Solution:**
```markdown
## Enhanced Technology Stack Rules:
### Required Libraries
- **HTTP Requests**: Always use `httpx`, never `requests`
- **Database**: Use SQLAlchemy with async sessions, never direct SQL
- **Data Validation**: Use Pydantic models for all data structures
- **Testing**: Use pytest with async support and fixtures

### Examples:
```python
# examples/external_api/http_client.py
import httpx
from typing import Dict, Any

async def fetch_external_data(endpoint: str) -> Dict[str, Any]:
    """Standard pattern for external API calls."""
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, timeout=30.0)
        response.raise_for_status()
        return response.json()
```
```

#### **Symptom: Incorrect Integration Patterns**

**What You See:**
```python
# AI creates direct database connections instead of using existing patterns
import asyncpg

async def get_user(user_id: int):
    conn = await asyncpg.connect("postgresql://...")  # Wrong pattern
    result = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    return result
```

**Root Cause:** Examples don't show integration patterns or INITIAL.md doesn't reference existing integration code

**Solution:**
```markdown
## Add Integration Examples:
```python
# examples/database/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID following established patterns."""
        return await self.session.get(User, user_id)

# Usage in service layer:
# examples/services/user_service.py
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_by_id(user_id)
```

## Update INITIAL.md:
```markdown
## EXAMPLES:
- examples/database/user_repository.py - Use this database access pattern
- examples/services/user_service.py - Follow this service layer integration
- config/database.py - Use existing database session management
```
```

### **Category 3: Validation and Quality Failures**

#### **Symptom: Tests Fail Due to Missing Dependencies**

**What You See:**
```bash
ImportError: No module named 'pytest_asyncio'
AttributeError: 'AsyncMockSession' object has no attribute 'commit'
```

**Root Cause:** Testing examples don't show complete test setup or dependencies

**Solution:**
```markdown
## Enhanced Testing Context:

### Required Test Dependencies (add to requirements-test.txt):
```
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0
httpx>=0.24.0
```

### Complete Test Examples:
```python
# examples/testing/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from ..main import app
from ..database import get_session

@pytest.fixture
async def async_session():
    """Provide async database session for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = sessionmaker(engine, class_=AsyncSession)
    
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(async_session):
    """Provide test client with database override."""
    app.dependency_overrides[get_session] = lambda: async_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# examples/testing/test_user_service.py
import pytest
from ..services import UserService
from ..schemas import UserCreate

class TestUserService:
    async def test_create_user_success(self, async_session):
        """Test user creation with proper async patterns."""
        service = UserService(async_session)
        user_data = UserCreate(username="test", email="test@example.com")
        
        user = await service.create_user(user_data)
        
        assert user.username == "test"
        assert user.id is not None
```
```

#### **Symptom: Performance Issues Not Caught**

**What You See:**
```python
# Code works but has performance problems
async def get_all_user_posts(user_id: int):
    user = await get_user(user_id)  # N+1 query problem
    posts = []
    for post_id in user.post_ids:
        post = await get_post(post_id)  # Separate query for each post
        posts.append(post)
    return posts
```

**Root Cause:** Examples don't show performance patterns or validation doesn't include performance testing

**Solution:**
```markdown
## Add Performance Examples:
```python
# examples/database/efficient_queries.py
from sqlalchemy.orm import selectinload

async def get_user_with_posts(session: AsyncSession, user_id: int) -> User:
    """Efficiently load user with posts in single query."""
    result = await session.execute(
        select(User)
        .options(selectinload(User.posts))  # Eager loading
        .where(User.id == user_id)
    )
    return result.scalar_one()

# Anti-pattern example:
async def get_user_with_posts_slow(session: AsyncSession, user_id: int) -> User:
    """
    DON'T DO THIS: N+1 query problem.
    This loads user first, then queries for each post separately.
    """
    user = await session.get(User, user_id)
    for post in user.posts:  # Triggers separate query for each post
        pass
    return user
```

## Add Performance Validation:
```bash
# Add to validation commands in PRP
python -m pytest tests/performance/ -v  # Performance tests
python -m cProfile -o profile.stats main.py  # Profiling
py-spy record -o profile.svg -- python main.py  # Performance monitoring
```
```

### **Category 4: Complex Integration Failures**

#### **Symptom: External Service Integration Fails**

**What You See:**
```bash
ConnectionError: HTTPSConnectionPool(host='api.external.com', port=443)
TimeoutError: Request timed out after 5 seconds
AuthenticationError: Invalid API key format
```

**Root Cause:** Examples don't show robust external service integration patterns

**Solution:**
```markdown
## Enhanced External Service Examples:
```python
# examples/external_services/robust_client.py
import httpx
import asyncio
from typing import Optional, Dict, Any
from ..config import settings

class ExternalServiceClient:
    """Robust external service client with error handling."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_connections=10),
            headers={"Authorization": f"Bearer {settings.external_api_key}"}
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Make request with comprehensive error handling."""
        
        for attempt in range(3):  # Retry logic
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                
                if response.status_code == 429:  # Rate limited
                    wait_time = int(response.headers.get("Retry-After", 60))
                    await asyncio.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except httpx.TimeoutException:
                if attempt == 2:  # Last attempt
                    raise ExternalServiceError("Service timeout after retries")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code in [401, 403]:
                    raise ExternalServiceError("Authentication failed")
                elif e.response.status_code >= 500:
                    if attempt == 2:
                        raise ExternalServiceError("Service unavailable")
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise ExternalServiceError(f"Request failed: {e}")
        
        return None

# Usage example:
async def fetch_user_profile(user_id: str) -> Dict[str, Any]:
    """Fetch user profile from external service."""
    async with ExternalServiceClient() as client:
        return await client.make_request("GET", f"/users/{user_id}")
```
```

## 🔧 Systematic Troubleshooting Process

### **Step 1: Failure Classification**

Use this decision tree to classify the failure:

```markdown
Is the code syntactically correct?
├─ No → Syntax/Style failure (Level 1)
└─ Yes → Does it run without errors?
    ├─ No → Logic/Runtime failure (Level 2)  
    └─ Yes → Does it produce correct results?
        ├─ No → Integration/Behavior failure (Level 3)
        └─ Yes → Does it meet quality standards?
            ├─ No → Quality/Performance failure (Level 4)
            └─ Yes → Does it solve the business problem?
                ├─ No → Strategy/Design failure (Level 5)
                └─ Yes → Success (investigate if surprising)
```

### **Step 2: Context Audit**

For each failure, audit the context systematically:

```markdown
## Context Audit Checklist:

### CLAUDE.md Analysis:
- [ ] Are the relevant rules specific enough?
- [ ] Do examples exist for this type of implementation?
- [ ] Are there conflicting or ambiguous guidelines?
- [ ] Is the technology stack clearly specified?

### INITIAL.md Analysis:
- [ ] Are requirements clear and complete?
- [ ] Are examples referenced specifically?
- [ ] Are gotchas and constraints documented?
- [ ] Is success criteria measurable?

### PRP Analysis:
- [ ] Was research comprehensive?
- [ ] Are implementation steps clear?
- [ ] Are validation commands correct?
- [ ] Is error handling addressed?

### Environment Analysis:
- [ ] Are dependencies correct and available?
- [ ] Is configuration properly set up?
- [ ] Are external services accessible?
- [ ] Is the development environment consistent?
```

### **Step 3: Root Cause Analysis**

Use the "5 Whys" technique for deeper analysis:

```markdown
## Example Root Cause Analysis:

Problem: AI generated code uses wrong authentication pattern

Why #1: AI didn't follow the existing JWT pattern
└─ Why #2: JWT pattern wasn't referenced in INITIAL.md
    └─ Why #3: examples/auth/ folder doesn't have JWT examples
        └─ Why #4: Authentication examples were never created
            └─ Why #5: No systematic process for creating examples after implementing features

Root Cause: Missing process for extracting and documenting patterns
Solution: Create systematic example extraction process
```

### **Step 4: Solution Implementation**

```markdown
## Solution Priority Matrix:

High Impact, Low Effort (Do First):
- Add missing examples to examples/ folder
- Update CLAUDE.md with specific rules
- Fix validation commands in PRP templates

High Impact, High Effort (Plan and Schedule):
- Restructure examples library organization
- Create comprehensive testing examples
- Build automated context validation

Low Impact, Low Effort (Quick Wins):
- Fix typos in documentation
- Add simple gotchas to INITIAL.md templates
- Improve error messages in validation commands

Low Impact, High Effort (Avoid):
- Perfect documentation for rarely-used features
- Complex tooling for marginal improvements
- Over-engineering simple solutions
```

## 🛡️ Prevention Strategies

### **Proactive Context Maintenance**

#### **Weekly Context Health Checks**

```markdown
## Weekly Review Process:
1. **New Pattern Detection**: What new patterns emerged in recent development?
2. **Example Gap Analysis**: What examples would have prevented recent issues?
3. **Rule Effectiveness**: Which CLAUDE.md rules are being ignored or misunderstood?
4. **Validation Updates**: Do quality gates catch the right issues?
5. **Documentation Sync**: Are examples still current with codebase changes?
```

#### **Continuous Improvement Cycle**

```markdown
## Improvement Cycle:
Failure → Analysis → Context Update → Validation → Documentation
    ↑                                                      ↓
    ←─────────── Monitor for New Failures ←─────────────────
```

### **Resilience Building**

#### **Defensive Context Engineering**

```markdown
## Defensive Strategies:

### Redundant Context:
- Include multiple examples for critical patterns
- Cross-reference patterns across different files
- Provide both positive and negative examples

### Validation in Depth:
- Multiple validation levels (syntax, logic, integration)
- Automated quality checks for common issues  
- Manual validation checklists for complex features

### Graceful Degradation:
- Fallback patterns when primary approach fails
- Alternative implementation strategies in PRPs
- Clear escalation paths for complex issues
```

#### **Context Testing**

```markdown
## Testing Your Context System:

### Regular Context Validation:
1. **Generate PRP for known feature** - Does it produce good guidance?
2. **Execute PRP without human intervention** - Does it work end-to-end?
3. **Compare outputs across team members** - Is behavior consistent?
4. **Test with edge cases** - How does system handle unusual requirements?

### Context Quality Metrics:
- **First-pass success rate**: % features working without iteration
- **Pattern consistency**: How often does generated code match examples?
- **Error reduction**: Fewer errors over time indicates improving context
- **Team velocity**: Faster development indicates effective context
```

## 🚨 Emergency Troubleshooting

### **When Context Engineering Fails Completely**

#### **Emergency Fallback Process**

```markdown
## Emergency Process:
1. **Immediate Fallback**: Disable AI assistance, implement manually
2. **Rapid Diagnosis**: Use OSCAR method to identify root cause
3. **Quick Fix**: Implement minimal context to unblock development
4. **Post-Incident Review**: Comprehensive analysis and prevention
5. **System Hardening**: Update context to prevent recurrence
```

#### **Emergency Context Triage**

```markdown
## Triage Priority:
1. **Critical**: Blocks all development - fix immediately
2. **High**: Causes incorrect implementations - fix within hours
3. **Medium**: Reduces quality or consistency - fix within days
4. **Low**: Minor inconveniences - fix in next maintenance cycle
```

### **Recovery Strategies**

#### **Context Rollback**

```markdown
## When to Rollback Context:
- New context causes widespread failures
- Context changes break established patterns
- Team productivity decreases significantly
- Quality metrics deteriorate rapidly

## Rollback Process:
1. **Identify stable version** of context system
2. **Document current issues** for future resolution
3. **Revert to known-good state**
4. **Gradually reintroduce changes** with validation
```

#### **Incremental Recovery**

```markdown
## Incremental Improvement Process:
1. **Start minimal**: Basic context that works
2. **Add one improvement at a time**
3. **Validate each change thoroughly**
4. **Build confidence gradually**
5. **Monitor metrics continuously**
```

## ✅ Chapter 13 Checklist

Before moving to Chapter 14, ensure you understand:

- [ ] **OSCAR Method**: Systematic approach to diagnosing Context Engineering failures
- [ ] **Failure Categories**: Five types of failures and their root causes
- [ ] **Prevention Strategies**: Proactive maintenance and resilience building
- [ ] **Emergency Procedures**: How to handle complete Context Engineering failures
- [ ] **Recovery Methods**: Rollback and incremental improvement strategies

## 🎯 Key Takeaways

1. **Most failures are context failures** - Fix the context, not just the symptoms
2. **Systematic diagnosis prevents recurring issues** - Use OSCAR method consistently
3. **Prevention is better than fixing** - Proactive context maintenance is essential
4. **Build resilience into your system** - Multiple validation levels and fallback strategies
5. **Learn from every failure** - Each issue makes your context system stronger

## 📚 Next Steps

Ready to learn advanced Context Engineering techniques and optimization strategies?

👉 **[Chapter 14: Best Practices](chapter-14-best-practices.md)**

In Chapter 14, you'll discover advanced techniques, optimization strategies, and expert-level Context Engineering patterns.

---

## 🔬 Troubleshooting Practice Exercise

**Diagnose and fix a Context Engineering issue:**

1. **Create a deliberate failure** - Remove key context from CLAUDE.md or examples
2. **Observe the failure** - Run a PRP and see what goes wrong
3. **Apply OSCAR method** - Systematically diagnose the root cause
4. **Fix the context** - Address the root cause, not just symptoms
5. **Validate the fix** - Ensure the same failure doesn't recur

**Common Practice Scenarios:**
- Remove type hints from examples → See if AI still uses types
- Remove error handling patterns → See if AI handles errors properly
- Remove specific library references → See if AI chooses correct libraries

*This practice will help you build systematic troubleshooting skills.*