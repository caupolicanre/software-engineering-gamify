# Código fuente (Source Code)

Este directorio contiene el código fuente principal del sistema **Gamify**.

## Estructura

```
src/
├── __init__.py                 # Inicialización del paquete principal
├── apps/                       # Aplicaciones Django del sistema
│   ├── achievements/           # Sistema de logros
│   ├── challenges/             # Sistema de desafíos
│   ├── rankings/               # Sistema de rankings y leaderboards
│   ├── rewards/                # Sistema de recompensas
│   ├── streaks/                # Sistema de rachas
│   ├── tasks/                  # Gestión de tareas
│   ├── users/                  # Gestión de usuarios
│   └── xp_management/          # Sistema de experiencia y niveles
├── config/                     # Configuración del proyecto
│   ├── settings/               # Configuraciones por ambiente
│   ├── api_router.py           # Configuración de rutas API
│   ├── celery_app.py           # Configuración de Celery
│   ├── urls.py                 # URLs principales
│   ├── websocket.py            # Configuración WebSocket
│   ├── wsgi.py                 # Punto de entrada WSGI
│   └── asgi.py                 # Punto de entrada ASGI
└── gamify/                     # Módulo principal del sistema
```

## Arquitectura del código

El código sigue una **arquitectura basada en microservicios**, donde cada aplicación (`app`) es un módulo independiente con responsabilidades claras:

- **API Layer**: ViewSets y Serializers (Django REST Framework)
- **Business Logic**: Services y Managers
- **Data Layer**: Models (Django ORM)
- **Event Handling**: Event Handlers y Publishers
- **Utilities**: Validators, Calculators, Helpers

Para más detalles sobre la arquitectura y diseño del código, consulta la [documentación de diseño](../docs/design/design_documentation.md).

## Tecnologías

- **Python 3.13.5** (gestión de dependencias con `uv`)
- **Django 5.2.7** (framework web)
- **Django REST Framework 3.16.1** (API REST)
- **Celery 5.5.3** (procesamiento asíncrono)
- **PostgreSQL** (base de datos)
- **Redis** (caché y message broker)
- **RabbitMQ** (message queue)

## Relación con la documentación

- [Diagrama de clases](../docs/practical_work/TP3_class_deployment_diagrams.md#22-diagramas-de-clases-detallados)
- [Diagrama de despliegue](../docs/practical_work/TP3_class_deployment_diagrams.md#23-diagrama-de-despliegue)
- [Arquitectura C4](../docs/practical_work/TP1_part2_apply_architecture.md#2-vistas-de-arquitectura)
