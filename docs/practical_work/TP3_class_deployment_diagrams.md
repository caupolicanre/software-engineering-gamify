# Trabajo Práctico 3: Diagrama de clase y diagrama de despliegue

`Carrera:` Licenciatura en Ciencia de Datos

`Cátedra:` Ingeniería de Software II

`Docentes:` Valotto, Victor; Godoy, Cielo

`Alumnos:` Carrozzo, Felipe; Ré, Lautaro Caupolicán

`Año:` 2025

---

# Desarrollo

## 1. Ejercicio de análisis

### ¿Qué comunica cada uno de estos diagramas y qué diferencia hay entre ellos?

#### Diagrama de Clases

Muestra la **estructura estática del sistema**. Es decir, cómo está organizado el código: qué clases existen, qué atributos y métodos tienen, y cómo se relacionan entre sí (asociaciones, herencias, dependencias, composiciones, etc.). 

**Sirve para:**
- Definir la **arquitectura lógica** del sistema.
- Modelar las entidades principales (por ejemplo, `Usuario`, `Tarea`, `Achievement`, `XPService`, etc.).
- Mostrar la **relación entre las clases** (quién usa a quién, quién contiene a quién, herencias, composiciones).
- **Facilitar la implementación** en código orientado a objetos.
- Documentar la estructura de cada componente identificado en el nivel C4.

**Elementos principales:**
- **Clases**: Representan entidades o servicios del sistema.
- **Atributos**: Datos que contiene cada clase.
- **Métodos**: Operaciones que puede realizar cada clase.
- **Relaciones**: Asociación, agregación, composición, herencia, dependencia.

**Ejemplo en nuestro proyecto:**  
En el componente "Achievement Component" del servicio de gamificación, tenemos clases como:
- `AchievementViewSet` (controlador REST)
- `AchievementService` (lógica de negocio)
- `Achievement` (modelo de datos)
- `AchievementEvaluator` (evaluador de criterios)

Cada una con sus atributos, métodos y relaciones claramente definidas.

---

#### Diagrama de Despliegue

Muestra la **estructura física del sistema**, representando dónde se ejecutan los componentes (por ejemplo, en un servidor web, en una base de datos, en el dispositivo del usuario, etc.) y cómo se comunican entre esos nodos a través de la red.

**Sirve para:**
- Mostrar los **nodos físicos o virtuales** (servidores, contenedores Docker, dispositivos móviles, PCs, etc.).
- Indicar **qué componentes o artefactos se ejecutan** en cada nodo.
- Describir las **conexiones de red** entre ellos (por ejemplo, HTTP/REST, AMQP, PostgreSQL Protocol).
- Planificar la **infraestructura de despliegue** (útil en DevOps, testing y mantenimiento).
- Documentar decisiones de escalabilidad, alta disponibilidad y distribución geográfica.

**Elementos principales:**
- **Nodos**: Representan máquinas físicas o virtuales (servidores, VM, contenedores).
- **Artefactos**: Software desplegado en los nodos (aplicaciones, servicios, bases de datos).
- **Conexiones**: Protocolos de comunicación entre nodos (HTTP, AMQP, SQL, Redis Protocol).
- **Estereotipos**: `<<device>>`, `<<execution environment>>`, `<<artifact>>`, `<<database>>`.

**Ejemplo en nuestro proyecto:**  
El diagrama de despliegue muestra:
- **Frontend Web App** ejecutándose en navegadores de usuarios
- **API Gateway** en un servidor Ubuntu con FastAPI
- **Gamification Service** en otro servidor con Django + Celery Workers
- **PostgreSQL** en servidores de base de datos con replicación
- **RabbitMQ** en un servidor de mensajería
- **Redis Cluster** para caché distribuido

---

### Diferencias clave entre ambos diagramas

| Aspecto | Diagrama de Clases | Diagrama de Despliegue |
|---------|-------------------|------------------------|
| **Enfoque** | Lógico / Estructural | Físico / Infraestructura |
| **Qué muestra** | Cómo está organizado el código | Dónde se ejecuta el código |
| **Nivel de abstracción** | Diseño detallado de software | Arquitectura de infraestructura |
| **Elementos** | Clases, atributos, métodos, relaciones | Nodos, servidores, contenedores, comunicación |
| **Pregunta que responde** | "¿Cómo está estructurado el código?" | "¿Dónde y cómo se ejecuta el sistema?" |
| **Fase del desarrollo** | Diseño e implementación | Despliegue y operaciones |
| **Audiencia** | Desarrolladores | DevOps, arquitectos, operaciones |

---

### ¿Por qué es importante mantener la trazabilidad entre C4 → Clases → Despliegue?

Mantener la trazabilidad entre los diagramas **C4**, de **clases** y de **despliegue** es fundamental para asegurar la **coherencia entre la arquitectura conceptual, el diseño lógico y la implementación física** del sistema.

#### Beneficios de la trazabilidad:

1. **Verificación de completitud**: Permite verificar que cada componente definido en C4 tiene:
   - Sus clases correspondientes (diagrama de clases)
   - Un lugar donde ejecutarse (diagrama de despliegue)

2. **Facilita el mantenimiento**: Cuando se necesita hacer un cambio:
   - Se identifica el componente afectado (C4)
   - Se modifican las clases correspondientes (Clases)
   - Se verifica dónde se debe redesplegar (Despliegue)

3. **Comunicación entre equipos**:
   - Los arquitectos trabajan en C4
   - Los desarrolladores implementan las clases
   - Los DevOps configuran el despliegue
   - La trazabilidad asegura que todos trabajen sobre la misma base

4. **Gestión de dependencias**: Permite identificar:
   - Qué clases implementan un componente
   - Qué componentes se comunican entre sí
   - Qué nodos físicos deben estar conectados

5. **Escalabilidad y evolución**: Facilita decisiones como:
   - "Si escalamos el componente X, ¿qué clases se ven afectadas?"
   - "Si agregamos un nuevo servidor, ¿qué componentes pueden aprovechar ese recurso?"

#### Ejemplo en nuestro proyecto:

**C4 - Componentes:**
- Identificamos el "Achievement Component" dentro del "Gamification Service"

**Diagrama de Clases:**
- Detallamos las clases: `AchievementViewSet`, `AchievementService`, `AchievementEvaluator`, `Achievement` (modelo), `UserAchievement` (modelo)
- Mostramos sus relaciones: ViewSet → Service → Models

**Diagrama de Despliegue:**
- El "Gamification Service" se despliega en:
  - Un servidor virtual Ubuntu 22.04 con 4 vCPU y 8GB RAM
  - Contenedor Docker con Django + Gunicorn en puerto 8002
  - Celery Worker para procesamiento asíncrono
  - Conectado a PostgreSQL (Gamification DB) y RabbitMQ

Esta trazabilidad nos permite:
- Saber exactamente qué clases modificar cuando hay un bug en logros
- Identificar qué servidor reiniciar si hay problemas con gamificación
- Planificar el escalado horizontal agregando más instancias del servicio

---

## 2. Aplicación a nuestro proyecto

### 2.1. Revisión C4 - Vista de Componentes

Para el Trabajo Práctico 3, hemos revisado y completado nuestra vista de componentes del modelo C4, enfocándonos especialmente en el **Gamification Service** por ser uno de los componentes críticos del sistema.

#### Gamification Service - Componentes identificados

El servicio de gamificación se compone de los siguientes componentes funcionales:

1. **XP Management Component**
   - Gestiona el sistema de experiencia
   - Incluye: ViewSet, Serializer, Service, Model
   - Funciones: Calcular XP, niveles, multiplicadores

2. **Achievement Component**
   - Gestiona el sistema de logros
   - Incluye: ViewSet, Serializer, Service, Models, Evaluators
   - Funciones: Evaluar criterios, desbloquear logros, otorgar recompensas

3. **Streak Component**
   - Gestiona el sistema de rachas diarias
   - Incluye: ViewSet, Serializer, Service, Model
   - Funciones: Tracking de rachas, bonificaciones

4. **Reward Component**
   - Gestiona recompensas y monedas virtuales
   - Incluye: ViewSet, Serializer, Service, Model
   - Funciones: Procesar transacciones, gestionar balance

5. **Challenge Component**
   - Gestiona desafíos y competencias
   - Incluye: ViewSet, Serializer, Service, Models
   - Funciones: Crear, rastrear y completar desafíos

6. **Ranking Component**
   - Gestiona leaderboards y clasificaciones
   - Incluye: Service, Model, Cache Manager
   - Funciones: Calcular y actualizar rankings

7. **Event Handling Component**
   - Procesa eventos de dominio
   - Incluye: Event Handlers, Event Publishers
   - Funciones: Orquestar reacciones a eventos (TaskCompleted, LevelUp, etc.)

8. **Core Utilities Component**
   - Utilidades compartidas
   - Incluye: Validators, Calculators, Config Manager, Logger
   - Funciones: Funciones auxiliares comunes

**Interacciones entre componentes:**
- Los componentes de API (ViewSets) delegan la lógica a los Services
- Los Services utilizan Models para acceso a datos
- Event Handling Component coordina las reacciones entre componentes
- Core Utilities proporciona funcionalidades transversales

---

### 2.2. Diagramas de Clases Detallados

Hemos desarrollado diagramas de clases detallados para tres componentes críticos:

#### 2.2.1. Achievement Component (Componente de Logros)

Este componente es crítico porque implementa el caso de uso principal: **"Desbloquear un logro"**.

**Capas del componente:**

##### **API Layer (Django REST Framework)**

- **`AchievementViewSet`** (Django ViewSet)
  - Proporciona endpoints REST para gestión de logros
  - Métodos: `list()`, `retrieve()`, `get_user_achievements()`, `get_available_achievements()`, `check_progress()`, `unlock_achievement()`
  - Usa: `AchievementSerializer`, `UserAchievementSerializer`, `AchievementProgressSerializer`

- **`AchievementSerializer`** (Django Serializer)
  - Valida y serializa datos de logros
  - Campos: id, name, description, criteria, reward_xp, reward_coins, icon, rarity
  - Validaciones: `validate_criteria()`, `validate_reward_values()`

- **`UserAchievementSerializer`** (Django Serializer)
  - Serializa logros desbloqueados por usuario
  - Campos: achievement, user, unlocked_at, progress, is_completed
  - Anida `AchievementSerializer`

- **`AchievementProgressSerializer`** (Django Serializer)
  - Calcula y muestra progreso de logros
  - Campos: achievement_id, current_progress, required_progress, percentage

##### **Business Logic Layer**

- **`AchievementService`** (Service Class)
  - Orquesta toda la lógica de logros
  - Métodos principales:
    - `check_and_unlock_achievements(user_id, event_type, event_data)`: Verifica todos los logros tras un evento
    - `unlock_achievement(user_id, achievement_id)`: Desbloquea un logro específico
    - `get_user_achievements(user_id)`: Obtiene logros del usuario
    - `calculate_all_progress(user_id)`: Calcula progreso de todos los logros
  - Colabora con: `AchievementEvaluator`, `RewardService`, `EventPublisher`, `NotificationSender`

- **`AchievementEvaluator`** (Service Class)
  - Evalúa si un usuario cumple criterios de logro
  - Métodos:
    - `evaluate_criteria(user_id, achievement, user_stats)`: Verifica criterios
    - `calculate_progress(user_id, achievement, user_stats)`: Calcula progreso parcial
  - Utiliza validadores específicos por tipo de criterio

- **`CriteriaValidator`** (Abstract Class)
  - Clase base para validadores de criterios
  - Métodos abstractos: `validate()`, `calculate_progress()`

- **`TaskCountValidator`**, **`StreakValidator`**, **`LevelValidator`**
  - Implementaciones concretas de validadores
  - Cada uno valida un tipo específico de criterio

##### **Data Access Layer**

- **`Achievement`** (Django Model)
  - Representa la tabla de logros
  - Campos: id, name, description, criteria (JSON), criteria_type, reward_xp, reward_coins, icon, rarity, is_active
  - Manager: `AchievementManager`
  - Métodos: `is_unlockable_by(user_id)`, `get_rarity_display()`

- **`UserAchievement`** (Django Model)
  - Representa la relación entre usuario y logro
  - Campos: id, user (FK), achievement (FK), unlocked_at, progress, is_completed
  - Manager: `UserAchievementManager`
  - Métodos: `update_progress(new_progress)`, `complete()`

- **`UserStatistics`** (Django Model)
  - Almacena estadísticas agregadas del usuario
  - Campos: user (OneToOne), total_tasks_completed, current_streak, longest_streak, total_xp, current_level, friend_count, challenges_won
  - Métodos: `update_stats(stat_name, value)`, `refresh_from_sources()`

##### **Event Handlers**

- **`TaskCompletedEventHandler`**
  - Escucha evento `TaskCompleted` de la cola de mensajes
  - Al recibir evento: verifica y desbloquea logros relacionados con tareas

- **`StreakMilestoneEventHandler`**
  - Escucha evento `StreakMilestone`
  - Al recibir evento: desbloquea logros de racha y otorga bonos

- **`LevelUpEventHandler`**
  - Escucha evento `LevelUp`
  - Al recibir evento: desbloquea logros de nivel y otorga recompensas

##### **Utilities**

- **`EventPublisher`**
  - Publica eventos de dominio a la cola de mensajes
  - Métodos: `publish_achievement_unlocked()`, `publish_progress_updated()`

- **`NotificationSender`**
  - Envía notificaciones al Notification Service
  - Métodos: `send_achievement_notification()`, `send_progress_notification()`

- **`AchievementValidator`**
  - Validaciones de negocio
  - Métodos: `validate_achievement_exists()`, `validate_not_already_unlocked()`, `validate_criteria_format()`

##### **Servicios Externos**

- **`RewardService`**
  - Interfaz con el servicio de recompensas
  - Métodos: `award_coins()`, `award_xp()`

**Relaciones clave:**
- `AchievementViewSet` → `AchievementService` (delegación)
- `AchievementService` → `AchievementEvaluator` (evaluación)
- `AchievementService` → `Achievement`, `UserAchievement` (persistencia)
- `AchievementEvaluator` → `CriteriaValidator` (estrategia)
- `TaskCompletedEventHandler` → `AchievementService` (trigger)

---

#### 2.2.2. XP Management Component

Este componente gestiona todo el sistema de experiencia y niveles.

**Clases principales:**

##### **API Layer**

- **`XPViewSet`** (Django ViewSet)
  - Endpoints: `/xp/`, `/xp/leaderboard/`, `/xp/user/{id}/`
  - Métodos: `list()`, `award_xp()`, `get_leaderboard()`, `get_user_xp()`

- **`XPSerializer`** (Django Serializer)
  - Serializa transacciones de XP
  - Campos: user, amount, reason, multiplier, timestamp

- **`XPHistorySerializer`** (Django Serializer)
  - Serializa historial completo de XP del usuario
  - Campos: transactions[], total_xp, current_level, next_level_xp

##### **Business Logic**

- **`XPService`** (Service Class)
  - Lógica central de XP
  - Métodos:
    - `award_xp(user_id, amount, reason, multiplier)`: Otorga XP
    - `get_user_total_xp(user_id)`: Consulta XP total
    - `calculate_level(total_xp)`: Calcula nivel según XP
    - `process_level_up(user_id, old_level, new_level)`: Procesa subida de nivel

- **`LevelCalculator`** (Utility Class)
  - Cálculos matemáticos de niveles
  - Métodos:
    - `calculate_level_from_xp(total_xp)`: XP → Nivel
    - `calculate_xp_required(level)`: Nivel → XP requerido
    - `get_level_rewards(level)`: Obtiene recompensas de nivel

- **`XPCalculator`** (Utility Class)
  - Cálculos de XP según contexto
  - Métodos:
    - `calculate_base_xp(task_difficulty)`: XP base por dificultad
    - `apply_streak_multiplier()`: Aplica multiplicador de racha
    - `apply_challenge_multiplier()`: Aplica multiplicador de desafío

##### **Data Access**

- **`XPTransaction`** (Django Model)
  - Tabla: `xp_transactions`
  - Campos: id, user (FK), amount, reason, multiplier, timestamp
  - Manager: `XPTransactionManager` con métodos como `get_user_total_xp()`

- **`UserLevel`** (Django Model)
  - Tabla: `user_levels`
  - Campos: user (OneToOne), current_level, total_xp, xp_in_current_level, last_level_up
  - Métodos: `calculate_level()`, `update_xp(amount)`

**Flujo típico:**
1. Usuario completa tarea
2. `XPService.award_xp()` calcula XP con multiplicadores
3. Se crea `XPTransaction` en BD
4. Se actualiza `UserLevel`
5. Si hay subida de nivel → `process_level_up()` → publica evento `LevelUp`

---

#### 2.2.3. Task Management Component

Este componente gestiona tareas, sus estados y recurrencias.

**Clases principales:**

##### **API Layer**

- **`TaskViewSet`** (Django ViewSet)
  - Endpoints CRUD para tareas
  - Métodos: `create()`, `update()`, `complete()`, `delete()`, `list()`

- **`TaskSerializer`** (Django Serializer)
  - Campos: id, user, title, description, deadline, priority, status, is_recurring, recurrence_pattern
  - Validaciones: `validate_deadline()`, `validate_recurrence_pattern()`

- **`TaskCompletionSerializer`** (Django Serializer)
  - Maneja la completación de tareas
  - Campos: task_id, completion_time, notes

##### **Business Logic**

- **`TaskService`** (Service Class)
  - Métodos:
    - `create_task(user_id, task_data)`: Crea tarea
    - `complete_task(user_id, task_id)`: Marca como completada
    - `generate_recurring_task(task)`: Genera próxima instancia recurrente
    - `calculate_xp_reward(task)`: Calcula XP según dificultad

- **`RecurrenceManager`** (Service Class)
  - Gestiona lógica de tareas recurrentes
  - Métodos:
    - `calculate_next_occurrence(pattern, last_date)`: Calcula próxima fecha
    - `validate_recurrence_pattern(pattern)`: Valida patrón (daily, weekly, monthly)

##### **Data Access**

- **`Task`** (Django Model)
  - Tabla: `tasks`
  - Campos: id, user (FK), title, description, deadline, priority (enum), status (enum), is_recurring, recurrence_pattern (JSON), parent_task (FK, nullable)
  - Manager: `TaskManager` con métodos como `get_overdue()`, `get_upcoming()`
  - Métodos: `mark_as_completed()`, `generate_next_instance()`

- **`TaskCompletion`** (Django Model)
  - Tabla: `task_completions`
  - Registro de completaciones (útil para estadísticas)
  - Campos: task (FK), user (FK), completed_at, xp_earned, notes

**Flujo de completación de tarea:**
1. Usuario hace clic en "Completar tarea"
2. Frontend → API Gateway → Task Service
3. `TaskService.complete_task()`:
   - Valida que la tarea pertenezca al usuario
   - Actualiza status en BD
   - Calcula XP ganado
   - Si es recurrente → genera próxima instancia
   - Publica evento `TaskCompleted` a RabbitMQ
4. Gamification Service escucha evento y procesa logros

---

### 2.3. Diagrama de Despliegue

El diagrama de despliegue muestra la infraestructura física/virtual donde se ejecutan todos los componentes del sistema Gamify App.

#### Arquitectura general

La arquitectura sigue un modelo **cloud-native basado en microservicios**, desplegado en proveedores cloud (AWS / Digital Ocean / Render).

#### Nodos principales

##### **1. User Devices (Dispositivos de Usuario)**

- **Web Browser** (`<< Execution Environment >>`)
  - Chrome, Firefox, Safari, Edge
  - Ejecuta: **Frontend Web App**
    - React + TypeScript
    - Bundled con Vite
    - Servido desde CDN

- **Mobile Device** (`<< Execution Environment >>`)
  - iOS/Android
  - Ejecuta: **Mobile App**
    - React Native
    - Archivos .apk / .ipa

##### **2. CDN Layer (Capa de Distribución de Contenido)**

- **Cloudflare / AWS CloudFront** (`<< CDN >>`)
  - Distribución global de assets estáticos
  - HTTPS, caching, protección DDoS
  - Conectado a: **AWS S3 / MinIO**
    - Almacenamiento de archivos estáticos
    - Avatares, attachments, imágenes

##### **3. Load Balancing Zone (Balanceo de Carga)**

- **Application Load Balancer** (`<< Load Balancer >>`)
  - NGINX / AWS ALB
  - Terminación SSL/TLS
  - Health checks
  - Distribuye tráfico a API Gateway

##### **4. API Gateway Cluster**

- **API Gateway Server** (`<< Virtual Machine >>`)
  - Ubuntu 22.04 LTS
  - 4 vCPU, 8GB RAM
  - Contenedores:
    - **API Gateway** (FastAPI + Uvicorn, Python 3.11 con uv, Puerto 8000)
    - **Redis Cache** (Redis 7.x, Puerto 6379)

##### **5. Microservices Cluster**

###### **Task Service Node** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
- Contenedor: **Task Management Service**
  - FastAPI + Uvicorn
  - Python 3.11 (uv)
  - Puerto 8001

###### **Gamification Service Node** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 4 vCPU, 8GB RAM
- Contenedores:
  - **Gamification Service** (Django + Gunicorn, Puerto 8002)
  - **Celery Worker** (Procesamiento de eventos)
  - **Celery Beat** (Tareas programadas)
- Todos con Python 3.11 (uv)

###### **User Service Node** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
- Contenedor: **User Management Service**
  - FastAPI + Uvicorn
  - Python 3.11 (uv)
  - Puerto 8003

###### **Social Service Node** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
- Contenedor: **Social Service**
  - FastAPI + Uvicorn
  - Python 3.11 (uv)
  - Puerto 8004

###### **Notification Service Node** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
- Contenedores:
  - **Notification Service** (FastAPI + Celery, Puerto 8005)
  - **Celery Worker** (Procesamiento de notificaciones)

##### **6. Messaging Infrastructure (Infraestructura de Mensajería)**

- **Message Queue Server** (`<< Virtual Machine >>`)
  - Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
  - Contenedor: **RabbitMQ 3.12**
    - AMQP Broker
    - Puertos: 5672 (AMQP), 15672 (Management UI)
    - Gestiona eventos asincrónicos entre servicios

##### **7. Caching Infrastructure (Infraestructura de Caché)**

- **Redis Cluster Server** (`<< Virtual Machine >>`)
  - Ubuntu 22.04 LTS, 4 vCPU, 8GB RAM
  - Contenedor: **Redis Cluster**
    - Redis 7.x en modo cluster
    - 3 Masters + 3 Replicas
    - Puertos: 7000-7005
    - Cachea rankings, leaderboards, datos frecuentes

##### **8. Database Infrastructure (Infraestructura de Base de Datos)**

###### **Primary Database Server** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 4 vCPU, 16GB RAM, SSD 100GB
- Bases de datos:
  - **Main Database** (PostgreSQL 15, Puerto 5432)
    - Usuarios, tareas, relaciones sociales
  - **Gamification Database** (PostgreSQL 15, Puerto 5433)
    - XP, logros, rachas, recompensas

###### **Replica Database Server** (`<< Virtual Machine >>`)
- Ubuntu 22.04 LTS, 4 vCPU, 16GB RAM, SSD 100GB
- Réplicas read-only:
  - **Main DB Replica** (PostgreSQL 15, Puerto 5432)
  - **Gamification DB Replica** (PostgreSQL 15, Puerto 5433)
- Streaming replication desde primarios

##### **9. Monitoring & Observability (Monitoreo y Observabilidad)**

- **Monitoring Server** (`<< Virtual Machine >>`)
  - Ubuntu 22.04 LTS, 2 vCPU, 4GB RAM
  - Contenedores:
    - **Prometheus** (Recolección de métricas, Puerto 9090)
    - **Grafana** (Visualización, Puerto 3000)
    - **Loki** (Agregación de logs, Puerto 3100)

##### **10. External Services (Servicios Externos)**

- **Authentication Services**: Google OAuth, Facebook, Apple Sign In
- **Push Notification Provider**: Firebase Cloud Messaging, APNS
- **Email Service**: SendGrid / AWS SES
- **SMS Service**: Twilio / WhatsApp Business API
- **Calendar Services**: Google Calendar API, Microsoft Outlook API

---

#### Protocolos de comunicación

| Origen | Destino | Protocolo | Descripción |
|--------|---------|-----------|-------------|
| Web Browser | CDN | HTTPS | Descarga de assets estáticos |
| Mobile App | CDN | HTTPS | Descarga de assets estáticos |
| Frontend | Load Balancer | HTTPS/REST | Requests API |
| Load Balancer | API Gateway | HTTP | Distribución de carga |
| API Gateway | Microservices | HTTP/REST | Ruteo de requests |
| API Gateway | Redis Gateway | Redis Protocol | Operaciones de caché |
| Microservices | RabbitMQ | AMQP | Publicación/suscripción de eventos |
| Celery Workers | RabbitMQ | AMQP | Consumo de tareas |
| Services | PostgreSQL | PostgreSQL Protocol | Lectura/escritura en BD |
| Services | Redis Cluster | Redis Protocol | Operaciones de caché distribuido |
| Services | S3 | S3 API | Upload/download de archivos |
| Notification Service | External APIs | HTTPS/SMTP | Envío de notificaciones |
| PostgreSQL Primary | Replicas | Streaming Replication | Replicación de datos |
| Prometheus | Services | HTTP | Scraping de métricas |

---

#### Decisiones de arquitectura

##### **Alta Disponibilidad**
- Load Balancer distribuye tráfico entre múltiples instancias
- Réplicas de base de datos para queries de lectura
- Redis Cluster con múltiples nodos

##### **Escalabilidad Horizontal**
- Cada microservicio puede escalar independientemente
- Celery Workers pueden agregarse según carga
- API Gateway stateless, escalable fácilmente

##### **Separación de Responsabilidades**
- Frontend separado del backend
- Microservicios independientes por dominio
- Bases de datos separadas para diferentes contextos

##### **Resiliencia**
- Message Queue garantiza entrega de eventos
- Réplicas de BD previenen pérdida de datos
- Health checks en Load Balancer detectan servicios caídos
- Monitoreo continuo con Prometheus + Grafana

##### **Seguridad**
- SSL/TLS en todas las comunicaciones externas
- API Gateway como punto único de entrada
- Servicios backend no expuestos directamente
- Autenticación centralizada

##### **Gestión de Dependencias Python**
- Uso de **uv** para gestión de paquetes Python
  - Más rápido que pip
  - Lock files reproducibles
  - Mejor gestión de dependencias

---

## 3. Relación entre modelos

### 3.1. Trazabilidad C4 → Clases → Despliegue

Para ilustrar la trazabilidad completa, tomemos como ejemplo el **Achievement Component**:

#### **Nivel C4 - Componentes**
```
Gamification Service [Container]
└── Achievement Component [Component]
    - Gestiona el sistema de logros
    - Evalúa criterios y desbloquea logros
    - Otorga recompensas
```

#### **Nivel Clases**
```
Achievement Component se implementa mediante:

API Layer:
├── AchievementViewSet (controlador REST)
├── AchievementSerializer (validación/serialización)
└── UserAchievementSerializer

Business Logic:
├── AchievementService (orquestación)
├── AchievementEvaluator (evaluación de criterios)
├── TaskCountValidator, StreakValidator, LevelValidator
└── EventPublisher, NotificationSender

Data Access:
├── Achievement (modelo)
├── UserAchievement (modelo)
└── UserStatistics (modelo)

Event Handlers:
├── TaskCompletedEventHandler
├── StreakMilestoneEventHandler
└── LevelUpEventHandler
```

#### **Nivel Despliegue**
```
Achievement Component se despliega en:

Gamification Service Node [VM: Ubuntu 22.04, 4 vCPU, 8GB RAM]
├── Gamification Service Container
│   ├── Django + Gunicorn (puerto 8002)
│   ├── Ejecuta: AchievementViewSet, AchievementService, etc.
│   └── Python 3.11 con uv
│
├── Celery Worker Container
│   ├── Ejecuta: TaskCompletedEventHandler, etc.
│   └── Consume eventos de RabbitMQ
│
└── Conexiones:
    ├── PostgreSQL (Gamification DB) - puerto 5433
    ├── RabbitMQ - puerto 5672 (eventos)
    ├── Redis Cluster - puertos 7000-7005 (caché)
    └── Notification Service - puerto 8005 (HTTP)
```

---

### 3.2. Ejemplo completo de flujo: "Desbloquear un logro"

#### **Vista C4**
1. Usuario interactúa con **Frontend Web App** [Container]
2. Request va al **API Gateway** [Container]
3. Gateway rutea a **Task Service** [Container]
4. Task Service publica evento a **Message Queue** [Container]
5. **Gamification Service** [Container] → **Achievement Component** [Component] procesa evento
6. Achievement Component verifica criterios y desbloquea logro

#### **Vista Clases**
1. `TaskViewSet.complete()` marca tarea como completada
2. `TaskService.complete_task()` calcula XP y publica evento `TaskCompleted`
3. `TaskCompletedEventHandler` recibe evento de RabbitMQ
4. `AchievementService.check_and_unlock_achievements()` inicia verificación
5. `AchievementEvaluator.evaluate_criteria()` evalúa cada logro
6. `TaskCountValidator.validate()` verifica si criterios se cumplen
7. `AchievementService.unlock_achievement()` crea `UserAchievement`
8. `RewardService.award_xp()` y `award_coins()` otorgan recompensas
9. `EventPublisher.publish_achievement_unlocked()` publica evento
10. `NotificationSender.send_achievement_notification()` envía notificación

#### **Vista Despliegue**
1. **Web Browser** [Device] envía HTTPS request
2. **Application Load Balancer** [Infrastructure] recibe y distribuye
3. **API Gateway** [VM + Container: puerto 8000] valida y rutea
4. **Task Service** [VM + Container: puerto 8001] procesa tarea
5. **RabbitMQ** [VM + Container: puerto 5672] recibe evento `TaskCompleted`
6. **Celery Worker** [Container en Gamification Node] consume evento
7. **Gamification Service** [VM + Container: puerto 8002] procesa logros
8. **PostgreSQL Gamification DB** [VM + DB: puerto 5433] almacena desbloqueo
9. **Redis Cluster** [VM + Container: puertos 7000-7005] actualiza caché
10. **Notification Service** [VM + Container: puerto 8005] envía push notification
11. **Firebase / APNS** [External Service] entrega notificación al dispositivo

---

### 3.3. Matriz de trazabilidad

| Componente C4 | Clases principales | Nodo de despliegue |
|---------------|-------------------|-------------------|
| **Achievement Component** | AchievementViewSet, AchievementService, Achievement (Model) | Gamification Service Node (VM), Puerto 8002 |
| **XP Management Component** | XPViewSet, XPService, XPTransaction (Model) | Gamification Service Node (VM), Puerto 8002 |
| **Task Component** | TaskViewSet, TaskService, Task (Model) | Task Service Node (VM), Puerto 8001 |
| **Event Handling Component** | TaskCompletedEventHandler, EventPublisher | Celery Worker Container (Gamification Node) |
| **Notification Component** | NotificationService, NotificationSender | Notification Service Node (VM), Puerto 8005 |

---

## 4. Conclusiones

### 4.1. Aprendizajes del TP3

1. **Integración de vistas arquitectónicas**: Comprendimos cómo las diferentes vistas (C4, clases, despliegue) se complementan para dar una visión completa del sistema.

2. **Importancia del diseño detallado**: El diagrama de clases nos permitió identificar responsabilidades claras y evitar código acoplado.

3. **Planificación de infraestructura**: El diagrama de despliegue nos ayudó a anticipar necesidades de recursos, puntos de fallo y estrategias de escalado.

4. **Trazabilidad como herramienta de calidad**: Mantener la coherencia entre niveles nos permitió detectar componentes faltantes y redundancias.

### 4.2. Próximos pasos

1. **Implementación**: Con los diagramas de clases detallados, el equipo de desarrollo puede comenzar la codificación.

2. **Configuración de infraestructura**: Con el diagrama de despliegue, el equipo DevOps puede provisionar servidores y configurar redes.

3. **Testing**: Los diagramas de secuencia servirán como base para diseñar casos de prueba.

4. **Documentación continua**: A medida que el sistema evolucione, los diagramas deberán actualizarse para mantener la trazabilidad.

---

## 5. Referencias

- Modelo C4: https://c4model.com/
- Django REST Framework: https://www.django-rest-framework.org/
- FastAPI: https://fastapi.tiangolo.com/
- PostgreSQL Replication: https://www.postgresql.org/docs/current/warm-standby.html
- RabbitMQ: https://www.rabbitmq.com/
- Celery: https://docs.celeryproject.org/
- uv (Python package manager): https://github.com/astral-sh/uv
