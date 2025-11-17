# Python FastAPI Stack

## Tech Stack Components

- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **Database**: SQLAlchemy 2.0 ORM with Alembic migrations
- **Validation**: Pydantic v2
- **Authentication**: python-jose for JWT
- **Testing**: pytest + httpx
- **Documentation**: Auto-generated OpenAPI (built into FastAPI)

## Project Structure

```
project/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas (request/response)
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic
│   ├── routers/          # API endpoints
│   ├── dependencies/     # Dependency injection
│   ├── core/             # Configuration, security
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI app initialization
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── conftest.py       # Pytest fixtures
├── alembic/              # Database migrations
│   ├── versions/
│   └── env.py
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Dependencies (requirements.txt)

```txt
# FastAPI and server
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0  # For async PostgreSQL

# Pydantic
pydantic==2.5.3
pydantic-settings==2.1.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation and utilities
email-validator==2.1.0
python-dotenv==1.0.0

# Redis (if caching)
redis==5.0.1
aioredis==2.0.1

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
faker==22.0.0

# Development
ruff==0.1.13
mypy==1.8.0
black==23.12.1
```

## Example Implementation

### Model (SQLAlchemy)
```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orders = relationship("Order", back_populates="user")
```

### Schema (Pydantic)
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None

class UserInDB(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}

class User(UserInDB):
    """Public user schema (no sensitive data)"""
    pass
```

### Repository
```python
# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from typing import List, Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def get_all(self, skip: int = 0, limit: int = 100) -> tuple[List[User], int]:
        # Get users with pagination
        stmt = select(User).offset(skip).limit(limit)
        users = list(self.db.scalars(stmt))

        # Get total count
        count_stmt = select(func.count()).select_from(User)
        total = self.db.scalar(count_stmt)

        return users, total

    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
```

### Service
```python
# app/services/user_service.py
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, User
from app.core.security import get_password_hash
from fastapi import HTTPException, status
from typing import List

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> User:
        # Check if user exists
        existing = self.repository.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = get_password_hash(user_data.password)

        # Create user
        user_dict = user_data.model_dump()
        user_dict.pop('password')
        user_dict['hashed_password'] = hashed_password

        user = self.repository.create(user_dict)
        return User.model_validate(user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return User.model_validate(user)

    def list_users(self, page: int = 1, limit: int = 20) -> dict:
        skip = (page - 1) * limit
        users, total = self.repository.get_all(skip=skip, limit=limit)

        return {
            "data": [User.model_validate(u) for u in users],
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        }
```

### Router
```python
# app/routers/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import User, UserCreate, UserUpdate
from app.dependencies.auth import get_current_user
from typing import List

router = APIRouter(prefix="/api/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    return service.create_user(user_data)

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    return service.get_user(user_id)

@router.get("/", response_model=dict)
def list_users(
    page: int = 1,
    limit: int = 20,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    """List all users with pagination"""
    return service.list_users(page=page, limit=limit)
```

### Database Configuration
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Authentication
```python
# app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repository = UserRepository(db)
    user = repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
```

### Configuration (Pydantic Settings)
```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "My API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis
    REDIS_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

### Main Application
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import users, auth
from app.core.database import engine, Base

# Create tables (in production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Testing

### Unit Test
```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import Mock
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.models.user import User
from fastapi import HTTPException

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def user_service(mock_repository):
    return UserService(mock_repository)

def test_create_user_success(user_service, mock_repository):
    # Arrange
    user_data = UserCreate(
        email="test@example.com",
        password="password123",
        name="Test User"
    )
    mock_repository.get_by_email.return_value = None
    mock_repository.create.return_value = User(
        id=1,
        email=user_data.email,
        name=user_data.name,
        hashed_password="hashed",
        role="user"
    )

    # Act
    result = user_service.create_user(user_data)

    # Assert
    assert result.email == user_data.email
    mock_repository.create.assert_called_once()

def test_create_user_duplicate_email(user_service, mock_repository):
    # Arrange
    user_data = UserCreate(
        email="existing@example.com",
        password="password123",
        name="Test User"
    )
    mock_repository.get_by_email.return_value = User(id=1, email=user_data.email)

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_data)

    assert exc_info.value.status_code == 409
```

### Integration Test
```python
# tests/integration/test_users_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "name": "Test User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
```

## Alembic Migrations

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users table"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Key Patterns

- Use **Pydantic v2** for request/response validation
- Use **SQLAlchemy 2.0** with modern patterns
- Use **Dependency Injection** via FastAPI Depends
- Use **Repository Pattern** for data access
- Use **Service Layer** for business logic
- Use **Alembic** for database migrations
- Use **pytest** with fixtures for testing
- Use **python-jose** for JWT tokens
- Auto-generated **OpenAPI documentation** at /docs
