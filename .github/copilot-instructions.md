# Copilot Instructions for Gamify

**Project:** Gamify - Sistema de Gestión de Tareas Gamificado  
**Version:** 1.0.0  
**Authors:** Caupolicán Ré, Felipe Carrozzo

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Patterns](#2-architecture-patterns)
3. [Project Structure](#3-project-structure)
4. [Technology Stack](#4-technology-stack)
5. [Development Workflows](#5-development-workflows)
6. [Code Conventions](#6-code-conventions)
7. [Testing Patterns](#7-testing-patterns)
8. [Integration Patterns](#8-integration-patterns)
9. [Known Issues and Gotchas](#9-known-issues-and-gotchas)
10. [Critical Files Reference](#10-critical-files-reference)

---

## 1. Project Overview

### 1.1. What is Gamify?

Gamify is a web and mobile application designed to help people organize their daily tasks in a motivating way by incorporating gamification mechanics:

- **Experience (XP) and Levels**: Users earn XP for completing tasks and level up
- **Achievements**: Unlock achievements based on specific criteria (e.g., complete 10 tasks, maintain a 7-day streak)
- **Rewards**: Earn virtual currency and rewards for accomplishments
- **Rankings**: Social leaderboards to compete with friends
- **Streaks**: Track consecutive days of activity
- **Challenges**: Time-bound competitions between users

### 1.2. Core Business Logic

The system revolves around:
- **Tasks**: Core unit of work, completion triggers XP gain
- **Events**: Task completion, level-ups, and streak milestones trigger events
- **Evaluations**: Achievement criteria are evaluated when relevant events occur
- **Notifications**: Users are notified of achievements, level-ups, and rewards

---

## 2. Architecture Patterns

### 2.1. Microservices Architecture

The system is designed as a **Django monolith** structured as logical microservices:

- `achievements`: Manage unlockable achievements and user progress
- `xp_management`: Handle experience points, levels, and progression
- `streaks`: Track consecutive activity days
- `rewards`: Manage virtual currency and reward distribution
- `challenges`: Time-bound competitions between users
- `rankings`: Leaderboards and social competition
- `tasks`: Core task management
- `users`: User authentication and profile management

Each app is **loosely coupled** and communicates via:
- **Events** (event-driven architecture)
- **Service layer** calls (when synchronous response needed)
- **Shared models** (minimal, avoid tight coupling)

### 2.2. Service Layer Pattern

**CRITICAL**: All business logic lives in the **service layer**, NOT in views or models.

```
Request Flow:
  API ViewSet → Service Layer → Manager/Model → Database
                    ↓
              Event Publisher (async)
```

**Pattern structure:**
```python
# src/apps/{app}/services/{feature}_service.py
class AchievementService:
    """Service layer handles business logic, transactions, and event publishing."""
    
    def __init__(
        self,
        evaluator: AchievementEvaluator,
        validator: AchievementValidator,
        event_publisher: EventPublisher,
        notification_sender: NotificationSender,
    ):
        """Dependencies injected via constructor."""
        self.evaluator = evaluator
        self.validator = validator
        self.event_publisher = event_publisher
        self.notification_sender = notification_sender
    
    @transaction.atomic
    def unlock_achievement(self, user_id: int, achievement_id: int) -> UserAchievement:
        """
        Public method with transaction boundary.
        - Validates input
        - Performs business logic
        - Publishes events
        - Sends notifications
        """
        # Implementation here
        pass
    
    def _grant_achievement_rewards(self, user_achievement: UserAchievement) -> None:
        """Private helper methods prefixed with underscore."""
        pass
```

**Rules:**
- All public service methods use `@transaction.atomic`
- Service layer is **stateless** (no instance state between calls)
- Dependency injection via constructor
- Private helpers prefixed with `_`
- Return domain models, not serializers

### 2.3. Event-Driven Architecture

**How events work:**
1. Service performs action (e.g., complete task)
2. Service publishes event via `EventPublisher` (async, non-blocking)
3. Event handlers in other apps listen and react
4. Handlers call services to perform actions

**Event handler pattern:**
```python
# src/apps/{app}/events/handlers.py
class TaskCompletedEventHandler:
    """Handles task completion events by checking achievements."""
    
    def __init__(self, achievement_service: AchievementService):
        self.achievement_service = achievement_service
    
    def handle(self, event_data: dict) -> None:
        """
        Extract event data → Call service → Log result
        """
        user_id = event_data.get("user_id")
        task_id = event_data.get("task_id")
        
        # Call service to perform business logic
        unlocked = self.achievement_service.check_and_unlock_achievements(
            user_id=user_id,
            event_type="task_completed",
            context={"task_id": task_id},
        )
        
        logger.info(f"Unlocked {len(unlocked)} achievements for user {user_id}")
```

**Event types:**
- `task_completed`: Task marked as done
- `streak_milestone`: User reaches streak milestone (7 days, 30 days, etc.)
- `level_up`: User gains enough XP to level up
- `achievement_unlocked`: Achievement criteria met
- `reward_granted`: Reward given to user

### 2.4. ViewSet → Service Pattern

**ViewSets** are thin wrappers around services:

```python
# src/apps/{app}/api/views.py
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    ViewSet delegates to service layer.
    - Handles HTTP concerns (serialization, pagination, permissions)
    - Minimal business logic
    - Calls services for operations
    """
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    
    @action(detail=False)
    def me(self, request):
        """Custom action example."""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
```

**Rules:**
- Use DRF mixins instead of full `ModelViewSet` (explicit > implicit)
- Custom actions use `@action` decorator
- Serializers handle data validation, not business logic
- Call services for anything beyond CRUD

---

## 3. Project Structure

### 3.1. Directory Layout

```
software-engineering/
├── .env.example              # Environment variable template
├── .github/
│   ├── actions/              # GitHub Actions workflows
│   └── copilot-instructions.md  # This file
├── docs/                     # MkDocs documentation
│   ├── design/               # Architecture diagrams and design docs
│   ├── practical_work/       # Course assignments
│   ├── requirements/         # Requirements specifications
│   └── specifications/       # Technical specifications
├── mkdocs.yml                # Documentation site configuration
├── pyproject.toml            # Project metadata, dependencies, tool configs
├── src/                      # Django application root
│   ├── apps/                 # Django apps (microservices)
│   │   ├── achievements/
│   │   │   ├── api/          # API endpoints (ViewSets, serializers, URLs)
│   │   │   ├── events/       # Event handlers and publishers
│   │   │   ├── managers/     # Custom model managers
│   │   │   ├── models/       # Domain models
│   │   │   ├── services/     # Business logic layer
│   │   │   └── utils/        # Validators, helpers
│   │   ├── xp_management/
│   │   ├── streaks/
│   │   ├── rewards/
│   │   ├── challenges/
│   │   ├── rankings/
│   │   ├── tasks/
│   │   └── users/
│   ├── config/               # Django configuration
│   │   ├── settings/         # Split settings (base, local, test, production)
│   │   ├── api_router.py     # DRF router configuration
│   │   ├── urls.py           # Root URL configuration
│   │   ├── celery_app.py     # Celery configuration
│   │   └── wsgi.py / asgi.py # Server entry points
│   └── manage.py             # Django management command
└── tests/                    # Integration tests
```

### 3.2. App Structure Convention

Each Django app follows this structure:

```
apps/{app_name}/
├── __init__.py
├── apps.py                   # App configuration
├── admin.py                  # Django admin registration
├── api/                      # REST API layer
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # ViewSets
│   └── urls.py               # API URL patterns
├── events/                   # Event-driven components
│   ├── handlers.py           # Event consumers
│   └── publishers.py         # Event producers
├── managers/                 # Custom model managers
│   └── {model}_manager.py
├── models/                   # Domain models
│   ├── __init__.py
│   └── {model}.py            # One file per model
├── services/                 # Business logic layer
│   └── {feature}_service.py
├── utils/                    # Helpers and validators
│   ├── validators.py
│   └── {helper}.py
├── migrations/               # Database migrations
└── tests/                    # Unit tests
    ├── factories.py          # Test data factories
    ├── test_models.py
    ├── test_services.py
    └── api/
        └── test_views.py
```

---

## 4. Technology Stack

### 4.1. Core Technologies

- **Python 3.13.5**: Language (exact version required)
- **Django 5.2.7**: Web framework
- **Django REST Framework 3.16.1**: REST API
- **PostgreSQL**: Primary database
- **Celery 5.5.3**: Asynchronous task processing
- **RabbitMQ**: Message broker (implied from architecture)
- **Redis 7.0.1**: Caching and session storage
- **uv**: Package manager (fast alternative to pip)

### 4.2. Key Dependencies

- **python-decouple 3.8**: Environment variable management
- **django-cors-headers 4.9.0**: CORS support for frontend
- **django-filter 25.2**: Query filtering
- **drf-spectacular 0.29.0**: OpenAPI schema generation
- **pika 1.3.2**: RabbitMQ client
- **psycopg 3.2.12**: PostgreSQL adapter

### 4.3. Development Tools

- **pytest 8.4.2** + **pytest-django 4.11.1**: Testing
- **ruff 0.12.8**: Linting and formatting
- **pre-commit 4.2.0**: Git hooks
- **mkdocs 1.6.1**: Documentation site
- **deptry 0.23.1**: Dependency validation

### 4.4. Settings Structure

**Environment-based settings:**

```
src/config/settings/
├── base.py        # Shared settings (DEBUG, DATABASES, INSTALLED_APPS, etc.)
├── local.py       # Development (DEBUG=True, console email backend)
├── test.py        # Testing (in-memory cache, test database)
└── production.py  # Production (security settings, cloud services)
```

**Activate settings:**
```bash
# Development (default in manage.py)
python manage.py runserver --settings=config.settings.local

# Testing
pytest --ds=config.settings.test

# Production
export DJANGO_SETTINGS_MODULE=config.settings.production
```

**Environment variables (from `.env.example`):**
```bash
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-with-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=software_engineering_gamify
DB_USER=postgres
DB_PASSWORD=your_database_password_here
DB_HOST=localhost
DB_PORT=5432

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 5. Development Workflows

### 5.1. Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/caupolicanre/gamify.git
cd software-engineering

# 2. Install uv (if not installed)
pip install uv

# 3. Create virtual environment and install dependencies
uv venv
uv sync

# 4. Copy environment variables
copy .env.example .env
# Edit .env with your database credentials

# 5. Setup PostgreSQL database
# Create database: software_engineering_gamify
# User: postgres (or your DB_USER from .env)

# 6. Run migrations
uv run python src/manage.py migrate --settings=config.settings.local

# 7. Create superuser
uv run python src/manage.py createsuperuser --settings=config.settings.local

# 8. Run development server
uv run python src/manage.py runserver --settings=config.settings.local
```

### 5.2. Common Django Commands

```bash
# Run development server
uv run python src/manage.py runserver --settings=config.settings.local

# Create new app
cd src/apps
uv run python ../manage.py startapp app_name --settings=config.settings.local

# Make migrations
uv run python src/manage.py makemigrations --settings=config.settings.local

# Run migrations
uv run python src/manage.py migrate --settings=config.settings.local

# Create superuser
uv run python src/manage.py createsuperuser --settings=config.settings.local

# Django shell
uv run python src/manage.py shell --settings=config.settings.local

# Run tests
uv run pytest

# Generate OpenAPI schema
uv run python src/manage.py spectacular --file schema.yml --settings=config.settings.local
```

### 5.3. Testing Workflow

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest src/apps/users/tests/test_views.py

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run tests for specific app
uv run pytest src/apps/achievements/

# Run with verbose output
uv run pytest -v
```

### 5.4. Code Quality Checks

```bash
# Run ruff linter
uv run ruff check src/

# Auto-fix linting issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/

# Check dependency usage
uv run deptry src/

# Run pre-commit hooks manually
uv run pre-commit run --all-files
```

### 5.5. Documentation Workflow

```bash
# Serve documentation locally (auto-reload)
uv run mkdocs serve

# Build static documentation
uv run mkdocs build

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

---

## 6. Code Conventions

### 6.1. Python Style Guide

This project follows **PEP 8** with specific ruff configurations:

- **Indentation**: 4 spaces
- **Line length**: 140 characters
- **Quote style**: Double quotes (`"`)
- **Imports**: Sorted with isort (2 blank lines after imports)

### 6.2. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Classes | PascalCase | `AchievementService`, `UserAchievement` |
| Functions/Methods | snake_case | `unlock_achievement()`, `check_criteria()` |
| Constants | UPPER_SNAKE_CASE | `MAX_LEVEL`, `DEFAULT_XP` |
| Private methods | `_snake_case` | `_grant_rewards()`, `_notify_user()` |
| Django apps | snake_case | `xp_management`, `achievements` |
| Files | snake_case | `achievement_service.py`, `user_achievement.py` |

### 6.3. Import Order

```python
# Standard library
import logging
from typing import Any

# Third-party packages
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action

# Local apps (use relative imports within app)
from ..models import Achievement, UserAchievement
from ..utils.validators import AchievementValidator
from .achievement_evaluator import AchievementEvaluator
```

### 6.4. Docstring Style

```python
def unlock_achievement(self, user_id: int, achievement_id: int) -> UserAchievement:
    """
    Unlock an achievement for a user.
    
    This method validates the achievement exists, checks if already unlocked,
    creates the UserAchievement record, grants rewards, publishes events,
    and sends notifications.
    
    Args:
        user_id: The ID of the user unlocking the achievement
        achievement_id: The ID of the achievement to unlock
    
    Returns:
        UserAchievement: The created user achievement record
    
    Raises:
        ValidationError: If achievement doesn't exist or already unlocked
    """
```

### 6.5. Type Hints

Always use type hints for function signatures:

```python
from typing import Any

def check_and_unlock_achievements(
    self,
    user_id: int,
    event_type: str,
    context: dict[str, Any],
) -> list[UserAchievement]:
    """Type hints improve IDE support and catch errors early."""
    pass
```

### 6.6. Django Model Conventions

```python
from django.db import models

class Achievement(models.Model):
    """Model docstring describes the domain concept."""
    
    # Meta class comes first
    class Meta:
        db_table = "achievements"
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ["-created_at"]
    
    # Fields in logical order (ID, foreign keys, attributes, timestamps)
    name = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.IntegerField(default=0)
    criteria = models.JSONField()  # Store evaluation criteria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom manager
    objects = AchievementManager()
    
    # Methods
    def __str__(self) -> str:
        return self.name
    
    def is_unlocked_by(self, user_id: int) -> bool:
        """Business logic methods."""
        return UserAchievement.objects.filter(
            user_id=user_id,
            achievement_id=self.id,
        ).exists()
```

### 6.7. DRF Serializer Conventions

```python
from rest_framework import serializers
from ..models import Achievement

class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model."""
    
    # Computed fields
    is_unlocked = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = [
            "id",
            "name",
            "description",
            "xp_reward",
            "criteria",
            "is_unlocked",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
    
    def get_is_unlocked(self, obj: Achievement) -> bool:
        """Computed field method."""
        user = self.context.get("request").user
        return obj.is_unlocked_by(user.id) if user.is_authenticated else False
```

---

## 7. Testing Patterns

### 7.1. Test Structure

Tests use **pytest** with **pytest-django**:

```python
import pytest
from django.test import RequestFactory

from gamify.users.models import User
from gamify.users.tests.factories import UserFactory
from gamify.users.views import UserUpdateView


pytestmark = pytest.mark.django_db  # Enable database access for all tests


class TestUserUpdateView:
    """Test class groups related tests."""
    
    def test_get_success_url(self, user: User, rf: RequestFactory):
        """Test method names describe what is being tested."""
        # Arrange
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user
        view.request = request
        
        # Act
        result = view.get_success_url()
        
        # Assert
        assert result == f"/users/{user.username}/"
```

### 7.2. Fixtures and Factories

**Fixtures** (in `conftest.py`):
```python
import pytest
from django.test import RequestFactory

@pytest.fixture
def user(db):
    """Create a test user."""
    from gamify.users.tests.factories import UserFactory
    return UserFactory()

@pytest.fixture
def rf():
    """RequestFactory fixture."""
    return RequestFactory()
```

**Factories** (in `tests/factories.py`):
```python
import factory
from factory.django import DjangoModelFactory

from gamify.users.models import User


class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
```

### 7.3. Test Organization

```
src/apps/{app}/tests/
├── __init__.py
├── conftest.py           # App-specific fixtures
├── factories.py          # Test data factories
├── test_models.py        # Model tests
├── test_services.py      # Service layer tests
├── test_utils.py         # Utility function tests
└── api/
    ├── test_serializers.py
    └── test_views.py     # ViewSet tests
```

### 7.4. Testing Best Practices

- Use `pytest.mark.django_db` for database access
- Use factories for test data creation (not fixtures for data)
- Test one thing per test method
- Use descriptive test names: `test_unlock_achievement_when_already_unlocked_raises_error`
- Mock external dependencies (event publishers, notifications)
- Test happy path AND edge cases
- Use `RequestFactory` instead of Django test client for view tests (faster)

---

## 8. Integration Patterns

### 8.1. Cross-Service Communication

**Synchronous (via service imports):**
```python
# In achievements/services/achievement_service.py
from apps.rewards.services import RewardService

class AchievementService:
    def __init__(self, reward_service: RewardService):
        self.reward_service = reward_service
    
    def _grant_rewards(self, user_achievement: UserAchievement) -> None:
        """Call another service directly when synchronous response needed."""
        self.reward_service.grant_reward(
            user_id=user_achievement.user_id,
            amount=user_achievement.achievement.xp_reward,
        )
```

**Asynchronous (via events):**
```python
# In tasks/services/task_service.py
class TaskService:
    def complete_task(self, task_id: int) -> Task:
        """Complete task and publish event."""
        task = Task.objects.get(id=task_id)
        task.status = "completed"
        task.save()
        
        # Publish event asynchronously
        self.event_publisher.publish(
            event_type="task_completed",
            data={
                "user_id": task.user_id,
                "task_id": task.id,
                "xp_earned": task.xp_value,
            },
        )
        
        return task
```

### 8.2. Database Transactions

**ALWAYS** use `@transaction.atomic` for service methods that modify data:

```python
from django.db import transaction

class AchievementService:
    @transaction.atomic
    def unlock_achievement(self, user_id: int, achievement_id: int) -> UserAchievement:
        """
        Transaction ensures:
        - All database operations succeed together
        - Or all are rolled back on error
        """
        # Create achievement record
        user_achievement = UserAchievement.objects.create(...)
        
        # Grant rewards (if this fails, achievement creation is rolled back)
        self._grant_rewards(user_achievement)
        
        # Publish event (outside transaction)
        transaction.on_commit(lambda: self._publish_event(user_achievement))
        
        return user_achievement
```

### 8.3. Event Publishing Pattern

```python
# events/publishers.py
class EventPublisher:
    """Publishes events to message queue."""
    
    def publish(self, event_type: str, data: dict) -> None:
        """
        Publish event asynchronously via RabbitMQ.
        - Non-blocking (fire and forget)
        - Ensures event is published AFTER transaction commits
        """
        # Send to message queue
        pass
```

### 8.4. Custom Model Managers

```python
# managers/achievement_manager.py
from django.db import models

class AchievementManager(models.Manager):
    """Custom manager for common queries."""
    
    def unlockable_by_criteria(self, criteria_type: str):
        """Filter achievements by criteria type."""
        return self.filter(criteria__type=criteria_type)
    
    def for_user(self, user_id: int):
        """Get achievements unlocked by user."""
        return self.filter(
            userachievement__user_id=user_id,
        ).distinct()
```

---

## 9. Known Issues and Gotchas

### 9.1. Import Path Inconsistency

**ISSUE**: `src/config/api_router.py` imports from `gamify.users` instead of `apps.users`:

```python
# WRONG (current state in api_router.py)
from gamify.users.api.views import UserViewSet

# CORRECT (should be)
from apps.users.api.views import UserViewSet
```

**ACTION**: When modifying routing or imports, use `apps.{app_name}` pattern consistently.

### 9.2. Settings Module Reference

**FIXED**: `src/manage.py` previously referenced non-existent `config.settings.development`. Now correctly uses `config.settings.local`.

**REMINDER**: Settings environments are:
- `config.settings.local` (development)
- `config.settings.test` (testing)
- `config.settings.production` (production)

### 9.3. Database Configuration

**IMPORTANT**: PostgreSQL database must be manually created before running migrations:

```sql
CREATE DATABASE software_engineering_gamify;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE software_engineering_gamify TO postgres;
```

**Environment variables** must match database credentials in `.env`:
```bash
DB_NAME=software_engineering_gamify
DB_USER=postgres
DB_PASSWORD=your_database_password_here
DB_HOST=localhost
DB_PORT=5432
```

### 9.4. Package Management with uv

**ALWAYS** use `uv` commands, NOT `pip`:

```bash
# CORRECT
uv sync                    # Install/update dependencies
uv add django-extensions   # Add new dependency
uv run python manage.py    # Run commands in virtual environment

# WRONG
pip install django-extensions
python manage.py
```

### 9.5. Transaction and Event Publishing

**CRITICAL**: Events should be published AFTER transaction commits:

```python
# CORRECT
@transaction.atomic
def unlock_achievement(self, user_id: int, achievement_id: int) -> UserAchievement:
    user_achievement = UserAchievement.objects.create(...)
    
    # Publish AFTER transaction commits
    transaction.on_commit(lambda: self.event_publisher.publish(...))
    
    return user_achievement

# WRONG (event published even if transaction rolls back)
@transaction.atomic
def unlock_achievement(self, user_id: int, achievement_id: int) -> UserAchievement:
    user_achievement = UserAchievement.objects.create(...)
    self.event_publisher.publish(...)  # Published before commit!
    return user_achievement
```

### 9.6. CORS Configuration

**Frontend URLs** must be added to `CORS_ALLOWED_ORIGINS` in `.env`:

```bash
# Example for React frontend on localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 10. Critical Files Reference

### 10.1. Configuration Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `pyproject.toml` | Project metadata, dependencies, tool configs | Python 3.13.5, Django 5.2.7, DRF 3.16.1, ruff rules |
| `.env.example` | Environment variable template | SECRET_KEY, DEBUG, DB credentials, CORS |
| `src/config/settings/base.py` | Shared Django settings | INSTALLED_APPS, DATABASES, REST_FRAMEWORK, logging |
| `src/config/settings/local.py` | Development settings | DEBUG=True, console email backend |
| `src/config/settings/test.py` | Test settings | In-memory cache, test database |
| `src/config/settings/production.py` | Production settings | Security headers, email backend, admin URL |
| `src/config/api_router.py` | DRF router configuration | API URL patterns, ViewSet registration |
| `src/config/urls.py` | Root URL configuration | Admin, API, static files |
| `mkdocs.yml` | Documentation site config | Navigation, theme, plugins |

### 10.2. Key Application Files

| File | Purpose | Pattern |
|------|---------|---------|
| `src/apps/{app}/services/{feature}_service.py` | Business logic layer | Service pattern with DI |
| `src/apps/{app}/events/handlers.py` | Event consumers | Event-driven handlers |
| `src/apps/{app}/events/publishers.py` | Event producers | Async event publishing |
| `src/apps/{app}/api/views.py` | REST API endpoints | ViewSet with mixins |
| `src/apps/{app}/api/serializers.py` | Data serialization | DRF ModelSerializer |
| `src/apps/{app}/models/{model}.py` | Domain models | Django ORM models |
| `src/apps/{app}/managers/{model}_manager.py` | Custom query logic | Model managers |
| `src/apps/{app}/utils/validators.py` | Input validation | Business rule validators |

### 10.3. Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview | All |
| `docs/design/design_documentation.md` | Architecture and design | Architects, developers |
| `docs/DEPLOYMENT_GUIDE.md` | Documentation deployment | Developers |
| `docs/CI_INVENTORY.md` | Configuration item tracking | Project managers |
| `docs/requirements/README.md` | Requirements specifications | Product owners |
| `docs/specifications/README.md` | Technical specifications | Developers |

---

## Quick Reference Commands

```bash
# Setup
uv sync                                                  # Install dependencies
copy .env.example .env                                   # Create environment file
uv run python src/manage.py migrate                      # Run migrations

# Development
uv run python src/manage.py runserver                    # Start dev server
uv run python src/manage.py shell                        # Django shell
uv run python src/manage.py createsuperuser              # Create admin user

# Testing
uv run pytest                                            # Run all tests
uv run pytest --cov=src --cov-report=html                # With coverage

# Code Quality
uv run ruff check --fix src/                             # Lint and fix
uv run ruff format src/                                  # Format code

# Documentation
uv run mkdocs serve                                      # Preview docs
uv run mkdocs gh-deploy                                  # Deploy to GitHub Pages

# Database
uv run python src/manage.py makemigrations               # Create migrations
uv run python src/manage.py migrate                      # Apply migrations
uv run python src/manage.py showmigrations               # Show migration status
```

---

**This document is maintained by the development team. Last updated: 2025-01-XX**

**For questions or clarifications, contact:**
- Caupolicán Ré (caupolicanre@gmail.com)
- Felipe Carrozzo (felipe.carrozzo@ingenieria.uner.edu.ar)
