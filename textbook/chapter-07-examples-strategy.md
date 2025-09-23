# Chapter 7: Examples Strategy

> **"Examples are the DNA of Context Engineering - they encode the patterns that make AI implementations successful."**

This chapter focuses on building and maintaining your examples library - the most critical component of any Context Engineering system. You'll learn how to create, organize, and evolve examples that consistently guide AI to produce high-quality code.

## 🎯 Learning Objectives

By the end of this chapter, you will:
- Understand why examples are more powerful than documentation
- Know how to identify and extract reusable patterns from your codebase
- Master the art of creating teaching examples that guide AI behavior
- Build a systematic approach to organizing and maintaining examples
- Recognize when and how to evolve your example library

## 🧬 The Power of Examples

### **Why Examples Beat Documentation**

Consider this comparison:

**Documentation Approach:**
```markdown
"Use proper error handling with specific exceptions and helpful messages"
```

**Example Approach:**
```python
# examples/error_handling/api_errors.py
from typing import Optional
from fastapi import HTTPException, status

class ValidationError(HTTPException):
    """Raised when input data fails validation."""
    
    def __init__(self, field: str, value: any, message: str):
        detail = {
            "error_type": "validation_error",
            "field": field,
            "invalid_value": str(value),
            "message": message,
            "suggestion": f"Please provide a valid {field}"
        }
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

# Usage example:
def validate_email(email: str) -> str:
    """Validate email format and return normalized email."""
    if not email or "@" not in email:
        raise ValidationError(
            field="email",
            value=email,
            message="Email must contain @ symbol and domain"
        )
    return email.lower().strip()
```

The example teaches:
- Specific exception structure
- Error message format
- Status code usage
- Helper method patterns
- Input normalization approach

**The AI can copy the exact pattern, not guess at interpretation.**

### **The Learning Science Behind Examples**

**Pattern Recognition:** AI excels at recognizing and reproducing patterns
**Contextual Understanding:** Examples show how patterns apply in real situations
**Constraint Learning:** Examples teach both what to do AND what constraints exist
**Quality Modeling:** Good examples demonstrate quality standards implicitly

### **Examples vs. Other Context Types**

| Context Type | Strength | Limitation |
|--------------|----------|------------|
| **Documentation** | Comprehensive coverage | Requires interpretation |
| **Rules** | Clear constraints | Can be abstract |
| **Examples** | Concrete patterns | Limited scope per example |
| **Anti-Examples** | Show what to avoid | Can be overwhelming if overused |

**The key:** Examples work best when combined with rules and documentation, not as a replacement.

## 🎨 Types of Examples

### **1. Structural Examples** 🏗️
*"How should code be organized and structured?"*

```python
# examples/structure/api_module.py
"""
Example of clean API module organization.
Shows separation of concerns and dependency injection.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..services import UserService
from ..auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Pattern: Dependency injection for services
def get_user_service() -> UserService:
    return UserService()

# Pattern: Clear route definition with types
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Create a new user account.
    
    Pattern: 
    - Input validation via Pydantic model
    - Service layer for business logic
    - Proper HTTP status codes
    - Type hints throughout
    """
    try:
        user = await user_service.create(user_data)
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Pattern: Authentication required routes
@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user's profile."""
    return UserResponse.from_orm(current_user)
```

### **2. Behavioral Examples** ⚡
*"How should code behave in different situations?"*

```python
# examples/behavior/retry_logic.py
"""
Example of robust retry logic with exponential backoff.
Use this pattern for external API calls.
"""

import asyncio
import logging
from typing import TypeVar, Callable, Any
from functools import wraps

T = TypeVar('T')

def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for adding retry logic with exponential backoff.
    
    Pattern:
    - Configurable retry parameters
    - Exponential backoff to avoid overwhelming services
    - Specific exception handling
    - Comprehensive logging
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        logging.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logging.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage example:
@with_retry(max_attempts=3, exceptions=(httpx.HTTPError, asyncio.TimeoutError))
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user data from external API with retry logic."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{user_id}", timeout=10.0)
        response.raise_for_status()
        return response.json()
```

### **3. Integration Examples** 🔌
*"How should different components work together?"*

```python
# examples/integration/database_service.py
"""
Example of service layer with database integration.
Shows transaction management, error handling, and testing patterns.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
from typing import Optional, List
from ..database import get_session
from ..models import User
from ..schemas import UserCreate

class UserService:
    """
    Service layer for user operations.
    
    Pattern:
    - Dependency injection for database session
    - Transaction management with context managers
    - Specific exception handling and conversion
    - Clear separation from API layer
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        try:
            yield self.session
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with proper error handling."""
        async with self.transaction():
            user = User(**user_data.dict())
            self.session.add(user)
            
            try:
                await self.session.flush()  # Get ID before commit
                await self.session.refresh(user)  # Load relationships
                return user
            except IntegrityError as e:
                if "email" in str(e):
                    raise ValueError("Email address already exists")
                elif "username" in str(e):
                    raise ValueError("Username already taken")
                else:
                    raise ValueError("User creation failed due to data conflict")
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID with relationship loading."""
        result = await self.session.get(User, user_id)
        return result
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination."""
        result = await self.session.execute(
            select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
        )
        return result.scalars().all()

# Usage in API layer:
async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """API endpoint showing service integration."""
    service = UserService(session)
    try:
        user = await service.create_user(user_data)
        return UserResponse.from_orm(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### **4. Testing Examples** 🧪
*"How should different types of testing be implemented?"*

```python
# examples/testing/test_user_service.py
"""
Example of comprehensive service testing.
Shows unit tests, integration tests, and mocking patterns.
"""

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from ..services import UserService
from ..models import User
from ..schemas import UserCreate

class TestUserService:
    """
    Test class showing testing patterns.
    
    Pattern:
    - Class-based organization
    - Setup and teardown with fixtures
    - Mocking external dependencies
    - Clear test naming
    - Comprehensive coverage
    """
    
    @pytest.fixture
    async def mock_session(self):
        """Mock database session for testing."""
        session = AsyncMock(spec=AsyncSession)
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.add = AsyncMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        return session
    
    @pytest.fixture
    def user_service(self, mock_session):
        """Create UserService with mocked dependencies."""
        return UserService(mock_session)
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return UserCreate(
            username="testuser",
            email="test@example.com",
            password="secure_password123"
        )
    
    async def test_create_user_success(self, user_service, sample_user_data, mock_session):
        """Test successful user creation."""
        # Arrange
        expected_user = User(id=1, **sample_user_data.dict())
        mock_session.flush.return_value = None
        mock_session.refresh.side_effect = lambda user: setattr(user, 'id', 1)
        
        # Act
        result = await user_service.create_user(sample_user_data)
        
        # Assert
        assert result.username == sample_user_data.username
        assert result.email == sample_user_data.email
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    async def test_create_user_duplicate_email(self, user_service, sample_user_data, mock_session):
        """Test error handling for duplicate email."""
        # Arrange
        from sqlalchemy.exc import IntegrityError
        mock_session.flush.side_effect = IntegrityError("email", "email", "UNIQUE constraint failed")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email address already exists"):
            await user_service.create_user(sample_user_data)
        
        mock_session.rollback.assert_called_once()
    
    @pytest.mark.integration
    async def test_create_user_integration(self, real_db_session, sample_user_data):
        """Integration test with real database."""
        service = UserService(real_db_session)
        
        user = await service.create_user(sample_user_data)
        
        assert user.id is not None
        assert user.username == sample_user_data.username
        
        # Cleanup
        await real_db_session.delete(user)
        await real_db_session.commit()
```

### **5. Configuration Examples** ⚙️
*"How should configuration and setup be handled?"*

```python
# examples/config/settings.py
"""
Example of comprehensive application configuration.
Shows environment-based config, validation, and secrets management.
"""

from pydantic import BaseSettings, validator, SecretStr
from typing import Optional, List
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings with validation and environment support.
    
    Pattern:
    - Pydantic for validation and type conversion
    - Environment variable support with defaults
    - Secret handling for sensitive data
    - Validation for configuration consistency
    """
    
    # Application
    app_name: str = "My Application"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str
    database_pool_size: int = 10
    database_pool_timeout: int = 30
    
    # Authentication
    secret_key: SecretStr
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # External Services
    redis_url: Optional[str] = None
    email_service_api_key: Optional[SecretStr] = None
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    @validator("secret_key")
    def secret_key_must_be_long(cls, v):
        """Ensure secret key is sufficiently long."""
        if len(v.get_secret_value()) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    @validator("database_url")
    def database_url_must_be_valid(cls, v):
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "sqlite://", "mysql://")):
            raise ValueError("Database URL must use supported driver")
        return v
    
    @validator("allowed_origins")
    def origins_must_be_valid(cls, v):
        """Validate CORS origins."""
        for origin in v:
            if not origin.startswith(("http://", "https://")):
                raise ValueError(f"Invalid origin format: {origin}")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Pattern:
    - Caching for performance
    - Factory function for dependency injection
    - Environment-specific loading
    """
    return Settings()

# Usage example:
from fastapi import Depends

async def get_database_url(settings: Settings = Depends(get_settings)) -> str:
    """Get database URL for dependency injection."""
    return settings.database_url
```

## 📚 Building Your Example Library

### **Step 1: Pattern Discovery**

#### **Identifying Patterns in Existing Code**

```bash
# Find patterns in your codebase
grep -r "class.*Service" src/  # Service layer patterns
grep -r "@router\." src/       # API route patterns  
grep -r "def test_" tests/     # Testing patterns
grep -r "async def" src/       # Async function patterns
```

#### **Pattern Extraction Questions**

For each pattern you find, ask:
- **What makes this good?** Why is this approach better than alternatives?
- **What's the context?** When should this pattern be used vs. not used?
- **What are the variations?** How does this pattern adapt to different situations?
- **What are the gotchas?** What commonly goes wrong with this pattern?

### **Step 2: Example Creation Process**

#### **The Example Lifecycle**

```markdown
1. **Identify Need** - Where do AI implementations consistently fail?
2. **Extract Pattern** - Find the best implementation of this pattern in your codebase
3. **Create Teaching Example** - Simplify and document the essential pattern
4. **Add Context** - Explain when, why, and how to use the pattern
5. **Test with AI** - Verify the example guides AI to correct implementations
6. **Iterate** - Refine based on AI behavior and results
```

#### **Example Creation Template**

```python
# examples/[category]/[pattern_name].py
"""
[Brief description of what this example demonstrates]

Use this pattern when:
- [Specific use case 1]
- [Specific use case 2]

Avoid this pattern when:
- [Situation where it's not appropriate]

Key principles:
- [Important principle 1]
- [Important principle 2]
"""

# Imports with comments about choices
from typing import List, Optional  # Always use type hints
from pydantic import BaseModel     # For data validation
from fastapi import HTTPException  # For proper error handling

class ExampleClass:
    """
    Example class showing [specific pattern].
    
    This demonstrates:
    - [Key feature 1 with explanation]
    - [Key feature 2 with explanation]
    - [Key feature 3 with explanation]
    """
    
    def __init__(self, dependency: SomeType):
        """Initialize with dependency injection pattern."""
        self.dependency = dependency
    
    def example_method(self, param: str) -> str:
        """
        Example method showing [specific behavior].
        
        Args:
            param: [Explanation of parameter]
            
        Returns:
            [Explanation of return value]
            
        Raises:
            HTTPException: [When and why this exception occurs]
        """
        # Pattern: Input validation
        if not param or not param.strip():
            raise HTTPException(
                status_code=400,
                detail="Parameter cannot be empty"
            )
        
        # Pattern: Use dependency for external operations
        try:
            result = self.dependency.process(param)
            return f"Processed: {result}"
        except Exception as e:
            # Pattern: Convert internal exceptions to API exceptions
            raise HTTPException(
                status_code=500,
                detail=f"Processing failed: {str(e)}"
            )

# Usage example showing how to apply the pattern
def create_example_instance():
    """Show how to instantiate and use the example class."""
    dependency = SomeDependency()
    instance = ExampleClass(dependency)
    
    try:
        result = instance.example_method("test input")
        print(f"Success: {result}")
    except HTTPException as e:
        print(f"Error: {e.detail}")

# Anti-pattern example (what NOT to do)
class BadExample:
    """
    This shows what NOT to do.
    
    Problems with this approach:
    - [Problem 1 with explanation]
    - [Problem 2 with explanation]
    """
    
    def bad_method(self, param):  # Missing type hints
        return param.process()    # No error handling, missing validation
```

### **Step 3: Organization Strategy**

#### **Directory Structure**

```
examples/
├── README.md                    # Overview and navigation
├── api/                        # API-related patterns
│   ├── routes.py               # Route definition patterns
│   ├── middleware.py           # Middleware patterns
│   └── error_handling.py       # Error handling patterns
├── database/                   # Database patterns
│   ├── models.py               # Model definition patterns
│   ├── repositories.py         # Repository pattern
│   └── migrations.py           # Migration patterns
├── services/                   # Business logic patterns
│   ├── user_service.py         # Service layer patterns
│   └── external_api.py         # External service integration
├── testing/                    # Testing patterns
│   ├── unit_tests.py           # Unit testing patterns
│   ├── integration_tests.py    # Integration testing patterns
│   └── fixtures.py             # Test fixture patterns
├── config/                     # Configuration patterns
│   ├── settings.py             # Application settings
│   └── environment.py          # Environment management
└── utils/                      # Utility patterns
    ├── validation.py           # Input validation patterns
    └── formatting.py           # Data formatting patterns
```

#### **Example Naming Conventions**

```markdown
### File Naming:
- `[noun]_[pattern].py` - e.g., `user_service.py`, `auth_middleware.py`
- `test_[component].py` - e.g., `test_user_service.py`
- `[domain]_[function].py` - e.g., `email_notifications.py`

### Class Naming:
- Pattern classes: `[Domain][Pattern]` - e.g., `UserService`, `AuthMiddleware`
- Example classes: `Example[Pattern]` - e.g., `ExampleValidator`
- Anti-pattern classes: `Bad[Pattern]` - e.g., `BadErrorHandling`

### Function Naming:
- Pattern functions: `[verb]_[noun]` - e.g., `validate_email`, `format_response`
- Example functions: `example_[pattern]` - e.g., `example_retry_logic`
```

## 🔄 Maintaining and Evolving Examples

### **Example Lifecycle Management**

#### **Regular Review Process**

```markdown
### Monthly Review Checklist:
- [ ] Are examples still relevant to current codebase?
- [ ] Do examples reflect current best practices?
- [ ] Are there new patterns that need examples?
- [ ] Are there examples that are never referenced?

### Quarterly Deep Review:
- [ ] Reorganize examples based on usage patterns
- [ ] Update examples with new library versions
- [ ] Add examples for new domains or technologies
- [ ] Remove obsolete or confusing examples
```

#### **Version Control for Examples**

```markdown
### Example Versioning Strategy:
1. **Tag major changes** - When fundamental patterns change
2. **Document migrations** - How to update from old to new patterns
3. **Maintain compatibility** - Keep old examples until full migration
4. **Clear deprecation** - Mark outdated examples clearly
```

### **Feedback-Driven Improvement**

#### **Tracking Example Effectiveness**

```markdown
### Metrics to Track:
- **Usage frequency** - Which examples are referenced most in PRPs?
- **Success rate** - Do features using specific examples work on first try?
- **AI behavior** - Does AI follow the example patterns correctly?
- **Team feedback** - Which examples are most/least helpful?

### Improvement Signals:
- **High failure rate** - Example might be unclear or missing context
- **Frequent questions** - Example might need more explanation
- **Inconsistent AI behavior** - Example might be ambiguous
- **Never referenced** - Example might not address real needs
```

#### **Community Contribution Pattern**

```markdown
### Example Contribution Process:
1. **Identify Gap** - Notice missing or poor examples during development
2. **Create Example** - Follow the example creation template
3. **Test with AI** - Verify the example guides correct behavior
4. **Document Context** - Add clear usage guidance and constraints
5. **Team Review** - Get feedback on clarity and usefulness
6. **Integrate** - Add to examples library with proper organization
```

## ✅ Chapter 7 Checklist

Before moving to Chapter 8, ensure you understand:

- [ ] **Example Power**: Why examples are more effective than documentation for AI guidance
- [ ] **Example Types**: Structural, behavioral, integration, testing, and configuration examples
- [ ] **Creation Process**: How to identify, extract, and document effective patterns
- [ ] **Organization Strategy**: How to structure and maintain an example library
- [ ] **Evolution Approach**: How to keep examples current and useful over time

## 🎯 Key Takeaways

1. **Examples encode patterns more effectively than text** - AI learns better from concrete code than abstract descriptions
2. **Good examples teach constraints implicitly** - They show not just what to do, but how to do it well
3. **Organization enables discovery** - Well-structured examples are easier to find and reference
4. **Examples require maintenance** - They must evolve with your codebase and practices
5. **Quality over quantity** - A few excellent examples beat many mediocre ones

## 📚 Next Steps

Ready to learn how to execute PRPs and turn comprehensive context into working code?

👉 **[Chapter 9: PRP Execution](chapter-09-prp-execution.md)**

In Chapter 9, you'll master the `/execute-prp` command and learn how to systematically implement features from your comprehensive PRPs.

---

## 🔬 Example Library Building Exercise

**Start building your example library:**

1. **Audit your codebase** - Find 3 patterns that appear multiple times
2. **Extract one example** - Choose the best implementation of one pattern
3. **Create a teaching example** - Follow the template from this chapter
4. **Document context** - Add clear usage guidance and constraints
5. **Test with AI** - Use the example in an INITIAL.md and see how AI responds

**Quality Questions:**
- Does the example show the complete pattern, not just a fragment?
- Is it clear when this pattern should and shouldn't be used?
- Would a new team member understand how to apply this pattern?

*This hands-on practice will help you create examples that truly guide AI behavior.*