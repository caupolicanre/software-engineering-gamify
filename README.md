# Gamify - Sistema de Gestión de Tareas Gamificado

<!-- ![Logo del proyecto](resources/images/logo.png) -->


## Descripción
**Gamify** es una aplicación web y móvil diseñada para ayudar a las personas a organizar sus tareas diarias de manera motivadora. Incorpora **niveles, logros, recompensas y ranking social** para hacer más entretenido el seguimiento de actividades.

- [**Github repository**](https://github.com/caupolicanre/gamify/)
<!-- - [**Documentation**](https://caupolicanre.github.io/gamify/) -->


## Contenido principal del repositorio
- [Documentación](./docs/)
- [Código fuente](./src/)
- [Pruebas](./src/apps/achievements/tests/)
- [Recursos](./resources/)
- [Trabajo Práctico Final](./resources/IS2_TP_Final.pdf)

## Equipo
- [Caupolicán Ré](https://github.com/caupolicanre) - Responsable del repositorio
- [Felipe Carrozzo](https://github.com/felipecarrozzo) - Colaborador

---

# Gamify Backend - Achievement System

### 1. Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Django Settings
# ------------------------------------------------------------------------------
SECRET_KEY=super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
# ------------------------------------------------------------------------------
DB_NAME=software_engineering_gamify
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# CORS Settings
# ------------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 2. Migraciones

```bash
# Aplicar migraciones
python manage.py migrate
```

### 3. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 4. Cargar Datos de Ejemplo

```bash
# Crear logros de ejemplo
python manage.py create_sample_achievements

# Crear estadísticas para el usuario creado
python manage.py create_test_user_stats --user-id 1
```

### 5. 🎮 Ejecutar Demo Interactiva (Flask)

Para probar el sistema de logros con una interfaz visual:

```bash
# Terminal 1: Iniciar Django (puerto 8000)
cd src
uv run python manage.py runserver

# Terminal 2: Iniciar Flask Demo (puerto 5000)
cd src/DEMO
uv run python demo_app.py
```

Luego abre en tu navegador: **http://localhost:5000**

📖 **Ver documentación completa de la demo**: [DEMO/README.md](./src/DEMO/README.md)

## 📋 Estructura de Archivos Implementados

```
apps/achievements/
├── api/
│   ├── __init__.py
│   ├── urls.py                     # ✅ Rutas API
│   └── views.py                    # ✅ AchievementViewSet completo
├── events/
│   ├── __init__.py
│   ├── handlers.py                 # ✅ Event Handlers (TaskCompleted, etc.)
│   └── publishers.py               # ✅ EventPublisher
├── management/commands/
│   ├── __init__.py
│   ├── create_sample_achievements.py   # ✅ Comando para datos de prueba
│   ├── create_test_user_stats.py       # ✅ Comando para estadísticas
│   └── simulate_task_completion.py     # ✅ Comando para simular tareas
├── migrations/
│   └── __init__.py
├── models/
│   ├── __init__.py                 # ✅ Achievement, UserAchievement, UserStatistics
│   └── managers.py                 # ✅ Managers personalizados
├── serializers/
│   └── __init__.py                 # ✅ Todos los serializers
├── services/
│   ├── __init__.py
│   ├── achievement_service.py      # ✅ Servicio principal
│   ├── achievement_evaluator.py    # ✅ Evaluador de criterios
│   └── validators/
│       ├── __init__.py
│       ├── base.py                 # ✅ CriteriaValidator (ABC)
│       ├── task_count_validator.py # ✅ Validator de tareas
│       ├── streak_validator.py     # ✅ Validator de rachas
│       └── level_validator.py      # ✅ Validator de niveles
├── utils/
│   ├── __init__.py
│   ├── validators.py               # ✅ AchievementValidator
│   └── notification_sender.py      # ✅ NotificationSender
├── __init__.py
├── admin.py                        # ✅ Admin configurado
└── apps.py
```

## 📡 Endpoints API Disponibles

### Achievements

- `GET /api/v1/achievements/` - Listar todos los logros
- `GET /api/v1/achievements/{id}/` - Detalle de un logro
- `GET /api/v1/achievements/me/` - Logros del usuario autenticado
- `GET /api/v1/achievements/available/` - Logros activos disponibles
- `GET /api/v1/achievements/{id}/progress/` - Progreso de un logro
- `GET /api/v1/achievements/all-progress/` - Progreso de todos los logros
- `POST /api/v1/achievements/unlock/` - Desbloquear logro manualmente

### Filtros y Búsqueda

```bash
# Filtrar por rareza
GET /api/v1/achievements/?rarity=legendary

# Filtrar por tipo de criterio
GET /api/v1/achievements/?criteria_type=streak

# Buscar por nombre
GET /api/v1/achievements/?search=level

# Ordenar
GET /api/v1/achievements/?ordering=-reward_xp
```

## 🔄 Flujo de Desbloqueo de Logros

### Secuencia Completa

1. **Evento Externo** → Una tarea se completa en el Task Service
2. **Message Queue** → Evento `TaskCompleted` publicado a RabbitMQ
3. **Event Handler** → `TaskCompletedEventHandler` consume el evento
4. **Service Layer** → `AchievementService.check_and_unlock_achievements()`
5. **Evaluator** → `AchievementEvaluator` verifica criterios con validators
6. **Validators** → `TaskCountValidator`, `StreakValidator`, etc. evalúan
7. **Si cumple criterios**:
   - Crea/actualiza `UserAchievement` (is_completed=True)
   - Llama a `RewardService` para otorgar XP/monedas
   - Publica evento `AchievementUnlocked`
   - Envía notificación via `NotificationSender`
8. **Si no cumple**:
   - Actualiza progreso en `UserAchievement`
   - Publica evento `ProgressUpdated`

## 🎓 Logros de Ejemplo Creados

### Por Cantidad de Tareas

- **First Steps** (Common) - Completar 1 tarea → 100 XP, 10 monedas
- **Task Master** (Rare) - Completar 10 tareas → 500 XP, 50 monedas
- **Century Club** (Epic) - Completar 100 tareas → 2000 XP, 200 monedas

### Por Rachas

- **Week Warrior** (Rare) - 7 días seguidos → 300 XP, 30 monedas
- **Month Master** (Epic) - 30 días seguidos → 1500 XP, 150 monedas
- **Year Legend** (Legendary) - 365 días seguidos → 10000 XP, 1000 monedas

### Por Nivel

- **Level 10** (Rare) - Alcanzar nivel 10 → 1000 XP, 100 monedas
- **Level 50** (Epic) - Alcanzar nivel 50 → 5000 XP, 500 monedas
- **Level 100** (Legendary) - Alcanzar nivel 100 → 20000 XP, 2000 monedas

## 📝 Logs y Debugging

Los logs se generan automáticamente durante el flujo:

```python
# Ver logs en consola
python manage.py simulate_task_completion --user-id 1 --count 5

# Output esperado:
# INFO: Checking achievements for user 1 after event task_completed
# INFO: Unlocking achievement First Steps for user 1
# INFO: Granted rewards to user 1: {'xp': 100, 'coins': 10}
# INFO: Publishing event to achievement.unlocked: {...}
# INFO: Sending notification: {...}
# INFO: Unlocked 1 achievements for user 1
```

