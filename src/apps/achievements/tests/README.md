# Achievement Tests

Este directorio contiene todos los tests para la aplicación de `achievements`.

## Estructura de Tests

Los tests están organizados en diferentes archivos según la funcionalidad que prueban:

### 1. **conftest.py**
Contiene todas las fixtures de pytest que son compartidas entre los diferentes tests:
- Fixtures de usuarios (`user`, `another_user`)
- Fixtures de modelos (`task_count_achievement`, `streak_achievement`, `level_achievement`, etc.)
- Fixtures de servicios (`achievement_service`, `achievement_evaluator`, `achievement_validator`)
- Fixtures de clientes API (`api_client`, `authenticated_client`)

### 2. **test_models.py**
Tests para los modelos de Django:
- `TestAchievementModel`: Tests para el modelo `Achievement`
- `TestUserAchievementModel`: Tests para el modelo `UserAchievement`
- `TestUserStatisticsModel`: Tests para el modelo `UserStatistics`
- `TestAchievementChoices`: Tests para los choices del modelo

### 3. **test_managers.py**
Tests para los custom managers:
- `TestAchievementManager`: Tests para `AchievementManager` 
- `TestUserAchievementManager`: Tests para `UserAchievementManager`

### 4. **test_validators.py**
Tests para los validadores de negocio:
- `TestAchievementValidator`: Tests para `AchievementValidator`

### 5. **test_evaluator.py**
Tests para el evaluador de logros:
- `TestAchievementEvaluator`: Tests para `AchievementEvaluator`

### 6. **test_services.py**
Tests para la capa de servicios:
- `TestAchievementService`: Tests para `AchievementService`

### 7. **test_serializers.py**
Tests para los serializers de Django REST Framework:
- `TestAchievementSerializer`
- `TestUserAchievementSerializer`
- `TestAchievementProgressSerializer`
- `TestUserAchievementListSerializer`
- `TestAchievementUnlockRequestSerializer`
- `TestSimulateTaskCompletionSerializer`
- `TestTaskSimulationResultSerializer`

### 8. **test_views.py**
Tests para las vistas API (ViewSets):
- `TestAchievementViewSet`: Tests para los endpoints principales
- `TestAchievementViewSetOrdering`: Tests para ordering y filtering
- `TestAchievementViewSetPagination`: Tests para paginación

## Ejecutar los Tests

### Ejecutar todos los tests de achievements

```bash
# Desde la raíz del proyecto
uv run pytest src/apps/achievements/tests/

# Con verbose output
uv run pytest -v src/apps/achievements/tests/

# Con coverage
uv run pytest --cov=src/apps/achievements src/apps/achievements/tests/
```

### Ejecutar un archivo específico de tests

```bash
# Tests de modelos
uv run pytest src/apps/achievements/tests/test_models.py

# Tests de servicios
uv run pytest src/apps/achievements/tests/test_services.py

# Tests de API views
uv run pytest src/apps/achievements/tests/test_views.py
```

### Ejecutar una clase específica de tests

```bash
# Solo tests del modelo Achievement
uv run pytest src/apps/achievements/tests/test_models.py::TestAchievementModel

# Solo tests del AchievementService
uv run pytest src/apps/achievements/tests/test_services.py::TestAchievementService
```

### Ejecutar un test específico

```bash
# Test específico
uv run pytest src/apps/achievements/tests/test_models.py::TestAchievementModel::test_create_achievement

# Con output detallado
uv run pytest -vv src/apps/achievements/tests/test_models.py::TestAchievementModel::test_create_achievement
```

### Ejecutar tests con diferentes opciones

```bash
# Detener en el primer error
uv run pytest -x src/apps/achievements/tests/

# Mostrar print statements
uv run pytest -s src/apps/achievements/tests/

# Ejecutar solo tests que fallaron la última vez
uv run pytest --lf src/apps/achievements/tests/

# Mostrar los 10 tests más lentos
uv run pytest --durations=10 src/apps/achievements/tests/

# Generar reporte HTML de coverage
uv run pytest --cov=src/apps/achievements --cov-report=html src/apps/achievements/tests/
# El reporte estará en htmlcov/index.html
```

## Cobertura de Tests

Los tests cubren:

✅ **Modelos**: Creación, validación, métodos personalizados, relaciones  
✅ **Managers**: Queries personalizadas, filtros, búsquedas  
✅ **Validadores**: Validación de reglas de negocio  
✅ **Evaluadores**: Evaluación de criterios, cálculo de progreso  
✅ **Servicios**: Lógica de negocio, transacciones, eventos  
✅ **Serializers**: Serialización, validación de datos de entrada  
✅ **Views**: Endpoints API, permisos, filtros, paginación  

## Fixtures Disponibles

### Usuarios
- `user`: Usuario de prueba básico
- `another_user`: Segundo usuario para tests que requieren múltiples usuarios

### Achievements
- `task_count_achievement`: Achievement tipo "task_count" (10 tareas)
- `streak_achievement`: Achievement tipo "streak" (7 días)
- `level_achievement`: Achievement tipo "level" (nivel 5)
- `inactive_achievement`: Achievement inactivo
- `legendary_achievement`: Achievement legendario (1000 tareas)

### User Achievements
- `unlocked_user_achievement`: Achievement desbloqueado (100% progreso)
- `in_progress_user_achievement`: Achievement en progreso (50% progreso)

### Estadísticas
- `user_stats`: Estadísticas de usuario con valores de prueba

### Servicios
- `achievement_service`: Instancia de `AchievementService`
- `achievement_evaluator`: Instancia de `AchievementEvaluator`
- `achievement_validator`: Instancia de `AchievementValidator`

### API Clients
- `api_client`: Cliente API sin autenticación
- `authenticated_client`: Cliente API autenticado con `user`

## Convenciones de Nomenclatura

Los tests siguen estas convenciones:

- **Archivos**: `test_*.py`
- **Clases**: `Test<ComponentName>`
- **Métodos**: `test_<what_is_being_tested>_<expected_result>`

Ejemplos:
```python
def test_create_achievement()  # Test básico de creación
def test_unlock_achievement_already_unlocked()  # Test de caso específico
def test_validate_reward_values_negative_xp()  # Test de validación específica
```

## Markers de Pytest

Todos los tests usan el marker `@pytest.mark.django_db` para acceder a la base de datos.

## Notas Importantes

1. **Base de datos**: Los tests usan una base de datos de prueba en memoria
2. **Transacciones**: Cada test se ejecuta en una transacción que se revierte automáticamente
3. **Fixtures**: Las fixtures se crean automáticamente y se limpian después de cada test
4. **Mocking**: Se utilizan mocks para componentes externos (event publishers, notification senders)
