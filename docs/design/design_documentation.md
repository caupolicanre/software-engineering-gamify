# Documentación Completa de Diseño - Gamify

---

**Proyecto:** Gamify - Sistema de Gestión de Tareas Gamificado

**Autores:** Caupolicán Ré, Felipe Carrozzo

**Fecha:** Noviembre 2025

**Versión:** 1.0.0

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Fundamentos de Arquitectura de Software](#2-fundamentos-de-arquitectura-de-software)
3. [Atributos de Calidad](#3-atributos-de-calidad)
4. [Arquitectura del Sistema](#4-arquitectura-del-sistema)
5. [Diagramas de Componentes](#5-diagramas-de-componentes)
6. [Diagramas de Clases](#6-diagramas-de-clases)
7. [Diagrama de Despliegue](#7-diagrama-de-despliegue)
8. [Trazabilidad entre Modelos](#8-trazabilidad-entre-modelos)
9. [Aspectos Transversales](#9-aspectos-transversales)
10. [Referencias](#10-referencias)

---

## 1. Introducción

### 1.1. Propósito del documento

Este documento proporciona una descripción completa del diseño arquitectónico del sistema **Gamify**, un sistema de gestión de tareas con mecánicas de gamificación. El documento está dirigido a:

- Arquitectos de software
- Desarrolladores del equipo
- Equipo de operaciones (DevOps)
- Stakeholders técnicos

### 1.2. Alcance

El documento cubre:

- Fundamentos teóricos de arquitectura de software
- Decisiones arquitectónicas tomadas
- Vistas de arquitectura (modelo C4)
- Diagramas de diseño detallado (clases, secuencia, despliegue)
- Trazabilidad entre los diferentes modelos
- Aspectos transversales del sistema

### 1.3. Contexto del proyecto

**Gamify** es una aplicación web y móvil diseñada para ayudar a las personas a organizar sus tareas diarias de manera motivadora, incorporando:

- Sistema de experiencia (XP) y niveles
- Logros desbloqueables
- Recompensas y monedas virtuales
- Rankings sociales
- Rachas de actividad
- Desafíos y competencias

---

## 2. Fundamentos de Arquitectura de Software

### 2.1. Arquitectura vs. Diseño de Software

El **diseño de software** es un concepto abarcativo que engloba diferentes niveles de detalle. Dentro de este, el **diseño de la arquitectura de software** se enfoca en identificar los componentes principales que constituyen la solución desde una visión de alto nivel.

La **arquitectura de software** se centra en:
- Cómo se manejará el sistema a nivel organizativo
- La lógica de negocios
- La estructura general
- El stack de tecnología
- Los escenarios que cubren los requerimientos

### 2.2. Estilos arquitectónicos

Un **estilo arquitectónico** define el diseño del sistema, junto con los componentes y conectores que lo conforman. Es uno de los primeros puntos a cubrir cuando se comienza a planificar un sistema.

Tener el problema y los requerimientos bien definidos es fundamental para elegir la arquitectura que mejor se adecúa a la problemática.

### 2.3. Patrones arquitectónicos

Los **patrones arquitectónicos** son soluciones generales y probadas a problemas recurrentes en el diseño de software a nivel de arquitectura. Se presentan como guías o plantillas que describen cómo estructurar un sistema, considerando el contexto y las restricciones del proyecto.

**Diferencias clave:**
- **Estilos arquitectónicos**: Modelos abstractos que definen vocabulario de componentes y conectores (ej: arquitectura en capas, cliente-servidor)
- **Patrones arquitectónicos**: Soluciones concretas reutilizables para problemas específicos
- **Patrones de diseño**: Enfocados en problemas de implementación a nivel de código

### 2.4. Vistas de arquitectura

Las **vistas de arquitectura** son representaciones de la solución que ayudan a comprender cómo se estructura el sistema. Cada vista modela diferentes partes de la solución con enfoques distintos.

**Modelos principales:**
- **4+1 (Kruchten)**: Vista lógica, de procesos, de desarrollo, física y de escenarios
- **C4**: Contexto, Contenedores, Componentes, Código
- **SEI**: Módulos, Componentes y conectores, Asignación
- **Siemens**: Vista conceptual, de ejecución, de implementación

**Para este proyecto utilizamos el modelo C4** por su claridad y facilidad de comunicación con diferentes stakeholders.

### 2.5. Aspectos transversales

Los **aspectos transversales** son fundamentales para el funcionamiento de un sistema robusto y seguro. Atraviesan todo el sistema, sin limitarse a un único módulo o componente.

Ejemplos:
- **Seguridad**: Autenticación, autorización, encriptación
- **Gestión operativa**: Logging, monitoreo, métricas
- **Comunicación**: Protocolos, serialización, message queues
- **Manejo de errores**: Excepciones, validaciones, recuperación

---

## 3. Atributos de Calidad

### 3.1. Por qué los atributos de calidad definen la arquitectura

Los atributos de calidad definen la arquitectura porque condicionan y guían su desarrollo, asegurando que el sistema no solo haga **qué** debe hacer, sino que lo haga **cómo** se necesita.

Un software que cumple las funciones pero no satisface atributos como rendimiento o confiabilidad probablemente no será útil en la práctica.

### 3.2. Atributos críticos para Gamify

#### 3.2.1. Escalabilidad

**Escenario:**
- **Estímulo**: Duplicación de usuarios activos durante un evento especial
- **Respuesta**: El sistema procesa cada solicitud con un retardo máximo de 3 segundos
- **Medida**: Tiempo de respuesta ≤ 3 segundos para el 95% de las peticiones

**Tácticas aplicadas:**
- Escalado horizontal de servicios
- Caché distribuido (Redis Cluster)
- Load balancing
- Message queue para procesamiento asíncrono

#### 3.2.2. Disponibilidad

**Escenario:**
- **Estímulo**: Usuario ingresa en cualquier momento del día
- **Respuesta**: El sistema permite acceso, visualización y registro sin errores
- **Medida**: Disponibilidad ≥ 99.5% mensual (≤ 4 horas de downtime)

**Tácticas aplicadas:**
- Réplicas de base de datos
- Health checks y auto-recovery
- Backup y disaster recovery
- Monitoreo continuo

### 3.3. Relación: Escenarios → Tácticas → Patrones

1. **Escenarios de calidad**: Describen situaciones concretas donde se ponen a prueba los atributos
2. **Tácticas de diseño**: Ofrecen soluciones a un nivel más concreto (ej: usar caché para mejorar rendimiento)
3. **Patrones de arquitectura**: Soluciones generales que integran múltiples tácticas

**Flujo:** Escenario → Táctica → Patrón

---

## 4. Arquitectura del Sistema

### 4.1. Estilo arquitectónico: Microservicios

Gamify utiliza una **arquitectura de microservicios** donde el sistema se organiza como un conjunto de servicios independientes, cada uno con una funcionalidad específica, que se comunican mediante APIs ligeras.

**Ventajas:**
- Escalabilidad independiente por servicio
- Despliegue independiente
- Flexibilidad tecnológica
- Aislamiento de fallos
- Equipos independientes por servicio

**Desafíos:**
- Complejidad operacional
- Consistencia eventual
- Latencia de red
- Debugging distribuido

### 4.2. Patrón: API Gateway

El sistema implementa un **API Gateway** como punto único de entrada para todos los clientes (web y móvil).

**Responsabilidades:**
- Ruteo de requests
- Autenticación y autorización
- Rate limiting
- Cache de respuestas
- Composición de respuestas
- Traducción de protocolos

### 4.3. Patrón: Event-Driven Architecture

Los microservicios se comunican mediante **eventos de dominio** a través de un message broker (RabbitMQ).

**Eventos principales:**
- `TaskCompleted`: Cuando un usuario completa una tarea
- `LevelUp`: Cuando un usuario sube de nivel
- `AchievementUnlocked`: Cuando se desbloquea un logro
- `StreakMilestone`: Cuando se alcanza un hito de racha

**Ventajas:**
- Desacoplamiento entre servicios
- Procesamiento asíncrono
- Escalabilidad de procesamiento
- Auditoría natural

---

## 5. Diagramas de Componentes

### 5.1. Modelo C4 - Nivel 1: Contexto

El diagrama de contexto muestra el sistema Gamify y sus interacciones con usuarios y sistemas externos.

**Actores:**
- Usuario (Usuario final de la aplicación)
- Sistema de notificaciones externo (Firebase, APNS)
- Servicios de autenticación (Google OAuth, Facebook, Apple)
- Servicios de calendario (Google Calendar, Outlook)

### 5.2. Modelo C4 - Nivel 2: Contenedores

**Contenedores principales:**

1. **Frontend Web App**
   - Tecnología: React + TypeScript + Vite
   - Responsabilidad: Interfaz de usuario web

2. **Mobile App**
   - Tecnología: React Native
   - Responsabilidad: Interfaz de usuario móvil (iOS/Android)

3. **API Gateway**
   - Tecnología: FastAPI + Uvicorn
   - Responsabilidad: Punto de entrada único, ruteo, autenticación

4. **Task Service**
   - Tecnología: FastAPI
   - Responsabilidad: Gestión de tareas, recurrencias

5. **Gamification Service**
   - Tecnología: Django + Celery
   - Responsabilidad: XP, logros, rachas, recompensas, rankings

6. **User Service**
   - Tecnología: FastAPI
   - Responsabilidad: Gestión de usuarios, perfiles

7. **Social Service**
   - Tecnología: FastAPI
   - Responsabilidad: Amistades, interacciones sociales

8. **Notification Service**
   - Tecnología: FastAPI + Celery
   - Responsabilidad: Envío de notificaciones

9. **Message Queue**
   - Tecnología: RabbitMQ
   - Responsabilidad: Comunicación asíncrona entre servicios

10. **Databases**
    - Tecnología: PostgreSQL 15
    - Responsabilidad: Persistencia de datos

11. **Cache**
    - Tecnología: Redis Cluster
    - Responsabilidad: Caché distribuido, rankings

### 5.3. Modelo C4 - Nivel 3: Componentes (Gamification Service)

El **Gamification Service** se descompone en los siguientes componentes:

#### 5.3.1. XP Management Component
- **Responsabilidad**: Gestionar el sistema de experiencia y niveles
- **Clases principales**: `XPViewSet`, `XPService`, `XPTransaction`, `UserLevel`
- **Funciones**: Calcular XP, niveles, multiplicadores

#### 5.3.2. Achievement Component
- **Responsabilidad**: Gestionar el sistema de logros
- **Clases principales**: `AchievementViewSet`, `AchievementService`, `Achievement`, `AchievementEvaluator`
- **Funciones**: Evaluar criterios, desbloquear logros, otorgar recompensas

#### 5.3.3. Streak Component
- **Responsabilidad**: Gestionar rachas diarias
- **Clases principales**: `StreakViewSet`, `StreakService`, `Streak`
- **Funciones**: Tracking de rachas, bonificaciones

#### 5.3.4. Reward Component
- **Responsabilidad**: Gestionar recompensas y monedas virtuales
- **Clases principales**: `RewardViewSet`, `RewardService`, `Reward`
- **Funciones**: Procesar transacciones, gestionar balance

#### 5.3.5. Challenge Component
- **Responsabilidad**: Gestionar desafíos y competencias
- **Clases principales**: `ChallengeViewSet`, `ChallengeService`, `Challenge`
- **Funciones**: Crear, rastrear y completar desafíos

#### 5.3.6. Ranking Component
- **Responsabilidad**: Gestionar leaderboards
- **Clases principales**: `RankingService`, `Ranking`, `CacheManager`
- **Funciones**: Calcular y actualizar rankings

#### 5.3.7. Event Handling Component
- **Responsabilidad**: Procesar eventos de dominio
- **Clases principales**: Event Handlers, Event Publishers
- **Funciones**: Orquestar reacciones a eventos

#### 5.3.8. Core Utilities Component
- **Responsabilidad**: Utilidades compartidas
- **Clases principales**: Validators, Calculators, Config Manager, Logger
- **Funciones**: Funciones auxiliares comunes

---

## 6. Diagramas de Clases

### 6.1. Patrón de diseño: Modelo-Vista-Controlador (MVC)

El sistema utiliza una variación de MVC adaptada a Django REST Framework:

- **Vista (ViewSet)**: Interfaz REST API, interpreta requests HTTP
- **Controlador (Service)**: Lógica de negocio, orquestación
- **Modelo (Model)**: Representación de datos, acceso a BD

### 6.2. Achievement Component - Diseño detallado

#### 6.2.1. API Layer

```
AchievementViewSet
├── Hereda de: viewsets.ModelViewSet
├── Atributos:
│   ├── queryset: QuerySet[Achievement]
│   └── serializer_class: AchievementSerializer
└── Métodos:
    ├── list() -> Response
    ├── retrieve(achievement_id) -> Response
    ├── get_user_achievements(user_id) -> Response
    ├── get_available_achievements() -> Response
    ├── check_progress(user_id) -> Response
    └── unlock_achievement(user_id, achievement_id) -> Response
```

**Relaciones:**
- Usa `AchievementSerializer` para validación
- Delega a `AchievementService` para lógica de negocio

#### 6.2.2. Business Logic Layer

```
AchievementService
├── Atributos:
│   ├── evaluator: AchievementEvaluator
│   ├── reward_service: RewardService
│   └── event_publisher: EventPublisher
└── Métodos:
    ├── check_and_unlock_achievements(user_id, event_type, event_data) -> List[Achievement]
    ├── unlock_achievement(user_id, achievement_id) -> UserAchievement
    ├── get_user_achievements(user_id) -> List[UserAchievement]
    ├── calculate_all_progress(user_id) -> Dict[int, float]
    └── _award_achievement_rewards(user_id, achievement) -> None
```

**Patrón Strategy:**
```
CriteriaValidator (Abstract)
├── Métodos abstractos:
│   ├── validate(user_stats, criteria) -> bool
│   └── calculate_progress(user_stats, criteria) -> float
│
├── TaskCountValidator
│   └── Valida criterios basados en cantidad de tareas
│
├── StreakValidator
│   └── Valida criterios basados en rachas
│
├── LevelValidator
│   └── Valida criterios basados en nivel
│
└── SocialValidator
    └── Valida criterios sociales
```

#### 6.2.3. Data Access Layer

```
Achievement (Model)
├── Campos:
│   ├── id: AutoField (PK)
│   ├── name: CharField(100)
│   ├── description: TextField
│   ├── criteria: JSONField
│   ├── criteria_type: CharField(50)
│   ├── reward_xp: IntegerField
│   ├── reward_coins: IntegerField
│   ├── icon: CharField(100)
│   ├── rarity: CharField(20)
│   └── is_active: BooleanField
├── Manager: AchievementManager
└── Métodos:
    ├── is_unlockable_by(user_id) -> bool
    └── get_rarity_display() -> str
```

```
UserAchievement (Model)
├── Campos:
│   ├── id: AutoField (PK)
│   ├── user: ForeignKey(User)
│   ├── achievement: ForeignKey(Achievement)
│   ├── unlocked_at: DateTimeField
│   ├── progress: FloatField
│   └── is_completed: BooleanField
├── Manager: UserAchievementManager
└── Métodos:
    ├── update_progress(new_progress) -> None
    └── complete() -> None
```

#### 6.2.4. Event Handlers

```
TaskCompletedEventHandler
├── Método:
│   └── handle(event: TaskCompletedEvent) -> None
│       └── Llama a AchievementService.check_and_unlock_achievements()
```

### 6.3. XP Management Component - Diseño detallado

#### 6.3.1. Clases principales

```
XPService
├── Métodos:
│   ├── award_xp(user_id, amount, reason, multiplier) -> XPTransaction
│   ├── get_user_total_xp(user_id) -> int
│   ├── calculate_level(total_xp) -> int
│   └── process_level_up(user_id, old_level, new_level) -> None
```

```
XPTransaction (Model)
├── Campos:
│   ├── user: ForeignKey(User)
│   ├── amount: IntegerField
│   ├── reason: CharField(200)
│   ├── multiplier: FloatField
│   └── timestamp: DateTimeField
```

```
UserLevel (Model)
├── Campos:
│   ├── user: OneToOneField(User)
│   ├── current_level: IntegerField
│   ├── total_xp: IntegerField
│   ├── xp_in_current_level: IntegerField
│   └── last_level_up: DateTimeField
└── Métodos:
    ├── calculate_level() -> int
    └── update_xp(amount) -> bool  # True si hubo level up
```

### 6.4. Task Management Component - Diseño detallado

```
Task (Model)
├── Campos:
│   ├── user: ForeignKey(User)
│   ├── title: CharField(200)
│   ├── description: TextField
│   ├── deadline: DateTimeField
│   ├── priority: CharField(20)  # ENUM: low, medium, high
│   ├── status: CharField(20)  # ENUM: pending, in_progress, completed
│   ├── is_recurring: BooleanField
│   ├── recurrence_pattern: JSONField
│   └── parent_task: ForeignKey(Task, nullable)
└── Métodos:
    ├── mark_as_completed() -> TaskCompletion
    └── generate_next_instance() -> Task
```

---

## 7. Diagrama de Despliegue

### 7.1. Arquitectura de infraestructura

El sistema se despliega en una arquitectura **cloud-native basada en microservicios**.

#### 7.1.1. Capa de Usuario (User Devices)

**Web Browser** (`<< Execution Environment >>`)
- Ejecuta: Frontend Web App (React + TypeScript)
- Servido desde: CDN (Cloudflare / AWS CloudFront)

**Mobile Device** (`<< Execution Environment >>`)
- Ejecuta: Mobile App (React Native)
- Archivos: .apk (Android) / .ipa (iOS)

#### 7.1.2. Capa de Distribución (CDN Layer)

**Cloudflare / AWS CloudFront** (`<< CDN >>`)
- HTTPS, caching, protección DDoS
- Almacenamiento: AWS S3 / MinIO (assets estáticos)

#### 7.1.3. Capa de Balanceo (Load Balancing)

**Application Load Balancer** (`<< Load Balancer >>`)
- Tecnología: NGINX / AWS ALB
- Terminación SSL/TLS
- Health checks
- Distribución de carga

#### 7.1.4. Capa de API Gateway

**API Gateway Server** (`<< Virtual Machine >>`)
- OS: Ubuntu 22.04 LTS
- Recursos: 4 vCPU, 8GB RAM
- Contenedores:
  - API Gateway (FastAPI + Uvicorn, Puerto 8000)
  - Redis Cache (Puerto 6379)

#### 7.1.5. Capa de Microservicios

**Task Service Node** (`<< VM >>`)
- 2 vCPU, 4GB RAM
- Puerto 8001

**Gamification Service Node** (`<< VM >>`)
- 4 vCPU, 8GB RAM
- Contenedores:
  - Gamification Service (Django + Gunicorn, Puerto 8002)
  - Celery Worker
  - Celery Beat

**User Service Node** (`<< VM >>`)
- 2 vCPU, 4GB RAM
- Puerto 8003

**Social Service Node** (`<< VM >>`)
- 2 vCPU, 4GB RAM
- Puerto 8004

**Notification Service Node** (`<< VM >>`)
- 2 vCPU, 4GB RAM
- Puerto 8005
- Celery Worker

#### 7.1.6. Capa de Mensajería

**Message Queue Server** (`<< VM >>`)
- RabbitMQ 3.12
- Puertos: 5672 (AMQP), 15672 (Management)

#### 7.1.7. Capa de Caché

**Redis Cluster Server** (`<< VM >>`)
- 4 vCPU, 8GB RAM
- Redis Cluster: 3 Masters + 3 Replicas
- Puertos: 7000-7005

#### 7.1.8. Capa de Datos

**Primary Database Server** (`<< VM >>`)
- 4 vCPU, 16GB RAM, SSD 100GB
- PostgreSQL 15
  - Main DB (Puerto 5432)
  - Gamification DB (Puerto 5433)

**Replica Database Server** (`<< VM >>`)
- 4 vCPU, 16GB RAM, SSD 100GB
- Réplicas read-only
- Streaming replication

#### 7.1.9. Capa de Monitoreo

**Monitoring Server** (`<< VM >>`)
- Prometheus (Puerto 9090)
- Grafana (Puerto 3000)
- Loki (Puerto 3100)

### 7.2. Protocolos de comunicación

| Origen | Destino | Protocolo | Puerto |
|--------|---------|-----------|--------|
| Browser/Mobile | CDN | HTTPS | 443 |
| Frontend | Load Balancer | HTTPS/REST | 443 |
| LB | API Gateway | HTTP | 8000 |
| Gateway | Microservices | HTTP/REST | 8001-8005 |
| Services | RabbitMQ | AMQP | 5672 |
| Services | PostgreSQL | PostgreSQL Protocol | 5432-5433 |
| Services | Redis | Redis Protocol | 7000-7005 |
| Prometheus | Services | HTTP (metrics) | 9090 |

### 7.3. Decisiones de arquitectura

#### 7.3.1. Alta Disponibilidad
- Load Balancer con múltiples instancias
- Réplicas de BD para lectura
- Redis Cluster

#### 7.3.2. Escalabilidad Horizontal
- Servicios stateless
- Escalado independiente
- Celery Workers escalables

#### 7.3.3. Resiliencia
- Message Queue garantiza entrega
- Health checks y auto-recovery
- Réplicas de BD
- Monitoreo continuo

#### 7.3.4. Seguridad
- SSL/TLS en comunicaciones externas
- API Gateway como firewall
- Servicios backend no expuestos
- Autenticación centralizada

---

## 8. Trazabilidad entre Modelos

### 8.1. Importancia de la trazabilidad

Mantener la trazabilidad entre **C4 → Clases → Despliegue** es fundamental para asegurar la coherencia entre la arquitectura conceptual, el diseño lógico y la implementación física.

**Beneficios:**
1. Verificación de completitud
2. Facilita el mantenimiento
3. Comunicación entre equipos
4. Gestión de dependencias
5. Escalabilidad y evolución

### 8.2. Ejemplo: Achievement Component

#### Nivel C4 - Componentes
```
Gamification Service [Container]
└── Achievement Component [Component]
    - Gestiona el sistema de logros
    - Evalúa criterios y desbloquea logros
```

#### Nivel Clases
```
Achievement Component implementado con:
- API: AchievementViewSet, Serializers
- Lógica: AchievementService, AchievementEvaluator
- Datos: Achievement, UserAchievement (Models)
- Eventos: TaskCompletedEventHandler
```

#### Nivel Despliegue
```
Gamification Service Node [VM: 4 vCPU, 8GB]
├── Django Container (Puerto 8002)
│   └── Ejecuta: ViewSet, Service, Models
├── Celery Worker Container
│   └── Ejecuta: Event Handlers
└── Conexiones:
    ├── PostgreSQL Gamification DB (5433)
    ├── RabbitMQ (5672)
    └── Redis Cluster (7000-7005)
```

### 8.3. Flujo completo: "Desbloquear un logro"

#### Vista C4
1. Frontend → API Gateway
2. Gateway → Task Service
3. Task Service → Message Queue (evento)
4. Gamification Service → Achievement Component

#### Vista Clases
1. `TaskViewSet.complete()` marca tarea
2. `TaskService` publica evento
3. `TaskCompletedEventHandler` recibe
4. `AchievementService.check_and_unlock_achievements()`
5. `AchievementEvaluator` evalúa criterios
6. Se crea `UserAchievement` en BD

#### Vista Despliegue
1. Browser → HTTPS → Load Balancer
2. LB → API Gateway [VM:8000]
3. Gateway → Task Service [VM:8001]
4. Task → RabbitMQ [VM:5672]
5. Celery Worker consume evento
6. Gamification [VM:8002] procesa
7. PostgreSQL [VM:5433] almacena

---

## 9. Aspectos Transversales

### 9.1. Autenticación y Autorización

**Impacto:** Todo el sistema
**Implementación:**
- JWT tokens generados por API Gateway
- Refresh tokens en Redis
- OAuth 2.0 con proveedores externos
- RBAC (Role-Based Access Control)

**Capas afectadas:**
- API Gateway: Validación de tokens
- Servicios: Verificación de permisos
- Base de datos: Protección de información sensible

### 9.2. Gestión de excepciones

**Impacto:** Principalmente capa de servicios
**Implementación:**
- Try-catch en services
- Excepciones custom por dominio
- Logging estructurado
- Respuestas HTTP estandarizadas

**Flujo:**
```
Exception → Service Layer → Log → API Response
```

### 9.3. Interoperabilidad

**Impacto:** Capa de servicios/API
**Implementación:**
- APIs REST estandarizadas (OpenAPI/Swagger)
- Contratos de API versionados
- Serialización JSON estándar
- CORS configurado

### 9.4. Logging y Monitoreo

**Impacto:** Todo el sistema
**Implementación:**
- Logs estructurados (JSON)
- Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Agregación con Loki
- Métricas con Prometheus
- Visualización con Grafana

**Métricas clave:**
- Latencia de requests
- Tasa de errores
- Throughput
- Uso de recursos

### 9.5. Notificaciones

**Impacto:** Capa de servicios
**Implementación:**
- Notification Service dedicado
- Push notifications (Firebase, APNS)
- Emails (SendGrid/SES)
- SMS (Twilio)
- WebSockets para notificaciones en tiempo real

---

## 10. Referencias

### 10.1. Documentación del proyecto

- [Casos de uso](../requirements/casos_uso.xlsx)
- [Atributos de calidad](../requirements/atributos_calidad.xlsx)
- [TP1: Arquitectura](../practical_work/TP1_part1_architecture.md)
- [TP1: Aplicación de arquitectura](../practical_work/TP1_part2_apply_architecture.md)
- [TP2: Diagramas de secuencia](../practical_work/TP2_sequence_diagram.md)
- [TP3: Diagramas de clases y despliegue](../practical_work/TP3_class_deployment_diagrams.md)

### 10.2. Diagramas

- [Diagrama de dominio](./diagrams/images/domain_diagram.png)
- [Diagrama de casos de uso](./diagrams/images/use_cases_diagram.png)
- [Diagrama de secuencia - Nuevo usuario](./diagrams/images/sequence_diagram_new_user.png)
- [Diagrama de secuencia - Completar tarea](./diagrams/images/sequence_diagram_complete_task.png)
- [Diagramas C4](./diagrams/c4/C4.drawio)

### 10.3. Referencias externas

- **Modelo C4**: https://c4model.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **FastAPI**: https://fastapi.tiangolo.com/
- **PostgreSQL Replication**: https://www.postgresql.org/docs/current/warm-standby.html
- **RabbitMQ**: https://www.rabbitmq.com/
- **Celery**: https://docs.celeryproject.org/
- **Redis Cluster**: https://redis.io/docs/manual/scaling/
- **Prometheus**: https://prometheus.io/docs/
- **Grafana**: https://grafana.com/docs/

### 10.4. Libros y artículos

- Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice* (3rd ed.)
- Kruchten, P. (1995). "The 4+1 View Model of Architecture". *IEEE Software*
- Newman, S. (2015). *Building Microservices*. O'Reilly Media
- Richardson, C. (2018). *Microservices Patterns*. Manning Publications

---

## Apéndice A: Glosario

- **API Gateway**: Punto único de entrada para todas las peticiones de clientes
- **AMQP**: Advanced Message Queuing Protocol
- **CDN**: Content Delivery Network
- **CI**: Configuration Item (Elemento de Configuración)
- **CORS**: Cross-Origin Resource Sharing
- **CRUD**: Create, Read, Update, Delete
- **Event-Driven**: Arquitectura basada en eventos
- **JWT**: JSON Web Token
- **Load Balancer**: Balanceador de carga
- **Microservicio**: Servicio pequeño e independiente
- **ORM**: Object-Relational Mapping
- **RBAC**: Role-Based Access Control
- **REST**: Representational State Transfer
- **SLA**: Service Level Agreement
- **VM**: Virtual Machine
- **XP**: Experience Points (Puntos de Experiencia)

---

**Fin del documento**

*Última actualización: Noviembre 2025*
