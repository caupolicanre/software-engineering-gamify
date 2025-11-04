# Trabajo Práctico 4: Diseño de Casos de Prueba

`Carrera:` Licenciatura en Ciencia de Datos

`Cátedra:` Ingeniería de Software II

`Docentes:` Valotto, Victor; Godoy, Cielo

`Alumnos:` Carrozzo, Felipe; Ré, Lautaro Caupolicán

`Año:` 2025

---

## Tabla de Contenidos

1. [Revisión Teórica](#1-revisión-teórica)
   - 1.1. [¿Por qué los casos de uso son una buena base para diseñar pruebas funcionales?](#11-por-qué-los-casos-de-uso-son-una-buena-base-para-diseñar-pruebas-funcionales)
   - 1.2. [Técnicas de diseño de pruebas aplicadas](#12-técnicas-de-diseño-de-pruebas-aplicadas)
   - 1.3. [Niveles de prueba implementados](#13-niveles-de-prueba-implementados)
2. [Casos de Uso Seleccionados](#2-casos-de-uso-seleccionados)
   - 2.1. [Caso de Uso 1: Desbloquear un Logro](#21-caso-de-uso-1-desbloquear-un-logro)
   - 2.2. [Caso de Uso 2: Consultar Progreso de Logros](#22-caso-de-uso-2-consultar-progreso-de-logros)
3. [Diseño de Casos de Prueba](#3-diseño-de-casos-de-prueba)
   - 3.1. [Casos de Prueba para "Desbloquear un Logro"](#31-casos-de-prueba-para-desbloquear-un-logro)
   - 3.2. [Casos de Prueba para "Consultar Progreso de Logros"](#32-casos-de-prueba-para-consultar-progreso-de-logros)
   - 3.3. [Casos de Prueba para API (Integración)](#33-casos-de-prueba-para-api-integración)
4. [Clases de Equivalencia y Valores Límite](#4-clases-de-equivalencia-y-valores-límite)
   - 4.1. [Campo: progress (Decimal, rango 0-100)](#41-campo-progress-decimal-rango-0-100)
   - 4.2. [Campo: count (Integer, rango 1-100 en simulación)](#42-campo-count-integer-rango-1-100-en-simulación)
   - 4.3. [Campo: reward_xp y reward_coins (Integer, ≥ 0)](#43-campo-reward_xp-y-reward_coins-integer--0)
   - 4.4. [Campo: criteria (JSONField)](#44-campo-criteria-jsonfield)
5. [Implementación de Pruebas](#5-implementación-de-pruebas)
   - 5.1. [Estructura de Tests](#51-estructura-de-tests)
6. [Análisis de Resultados](#6-análisis-de-resultados)
   - 6.1. [Sobre el Diseño de Pruebas](#61-sobre-el-diseño-de-pruebas)
   - 6.2. [Sobre los Casos de Uso](#62-sobre-los-casos-de-uso)
   - 6.3. [Conclusiones Finales](#63-conclusiones-finales)

---

# Desarrollo

## 1. Revisión Teórica

### 1.1. ¿Por qué los casos de uso son una buena base para diseñar pruebas funcionales?

Los casos de uso describen cómo interactúan los usuarios con el sistema para cumplir un objetivo específico, mostrando los flujos de acciones, entradas y resultados esperados.
Por eso, son una excelente base para diseñar pruebas funcionales, porque:

**Reflejan los requerimientos funcionales reales:** Cada caso de uso representa una funcionalidad que el sistema debe cumplir; por lo tanto, probarlos **permite verificar que el sistema hace lo que el usuario necesita.**

**Permiten derivar escenarios de prueba completos:** A partir de los flujos principales y alternativos del caso de uso, se pueden definir distintos casos de prueba (por ejemplo, camino feliz, errores de validación, condiciones excepcionales).

**Facilitan la trazabilidad entre requisitos y pruebas:** Cada prueba puede vincularse directamente con un caso de uso, lo que ayuda a garantizar que todas las funciones del sistema están cubiertas y validadas.

**Usan un lenguaje comprensible:** Los casos de uso se escriben en un lenguaje que entienden tanto desarrolladores como usuarios o testers, lo que facilita la comunicación dentro del equipo.

### 1.2. Técnicas de diseño de pruebas aplicadas

En este trabajo práctico aplicamos las siguientes técnicas de caja negra:

#### 1.2.1. Partición de Clases de Equivalencia

Dividimos el dominio de entrada en clases de equivalencia donde todos los valores de una clase deben comportarse de manera similar. Por ejemplo:
- Para el campo `progress` en `UserAchievement`: [0-100] es válido, <0 o >100 son inválidos
- Para `count` en simulación de tareas: [1-100] es válido, <1 o >100 son inválidos

#### 1.2.2. Análisis de Valores Límite

Probamos los valores en los bordes de las clases de equivalencia:
- Para `progress`: 0, 1, 99, 100, 101, -1
- Para `count`: 0, 1, 50, 100, 101

#### 1.2.3. Pruebas de Flujo Normal y Alternativo

- **Flujo normal:** Usuario desbloquea un logro cumpliendo criterios
- **Flujo alternativo:** Usuario intenta desbloquear un logro ya desbloqueado
- **Flujo de excepción:** Usuario intenta desbloquear un logro inexistente

### 1.3. Niveles de prueba implementados

#### Pruebas Unitarias
- Prueban componentes individuales (modelos, serializers, validators)
- Se ejecutan de forma aislada
- Usan mocks para dependencias externas

#### Pruebas de Integración
- Prueban la interacción entre múltiples componentes
- Incluyen pruebas de servicios que coordinan múltiples modelos
- Prueban la API completa (ViewSets con servicios y modelos)

#### Pruebas de Sistema
- Simulan flujos de usuario completos
- Ejemplo: Simular completación de tareas → verificar progreso de logros → verificar desbloqueo

---

## 2. Casos de Uso Seleccionados

Para este trabajo práctico, seleccionamos dos casos de uso críticos del sistema Gamify relacionados con el módulo de **Achievements (Logros)**:

### 2.1. Caso de Uso 1: Desbloquear un Logro

**Actor Principal:** Sistema (automatizado) / Usuario

**Precondiciones:**
- El usuario debe estar autenticado
- Debe existir al menos un logro activo en el sistema
- El usuario debe tener estadísticas registradas

**Flujo Principal:**
1. El sistema detecta que el usuario ha completado una acción (ej: completar una tarea)
2. El sistema evalúa los criterios de todos los logros activos
3. Si se cumplen los criterios de un logro, el sistema:
   - Crea un registro `UserAchievement` con progreso 100%
   - Marca el logro como completado
   - Registra la fecha de desbloqueo
   - Otorga las recompensas asociadas (XP y monedas)
   - Publica un evento de logro desbloqueado
   - Envía una notificación al usuario
4. El sistema retorna la información del logro desbloqueado

**Flujos Alternativos:**

**FA1:** El usuario no cumple los criterios
- El sistema actualiza el progreso del logro
- No se desbloquea el logro
- Se retorna el progreso actual

**FA2:** El logro ya fue desbloqueado previamente
- El sistema detecta que el logro ya existe y está completado
- No se crea un nuevo registro
- Se retorna un error indicando que ya fue desbloqueado

**FA3:** El logro no existe o está inactivo
- El sistema no encuentra el logro solicitado
- Se retorna un error 404

**Postcondiciones:**
- El logro queda registrado como desbloqueado para el usuario
- Las recompensas son otorgadas
- Se envía notificación al usuario

### 2.2. Caso de Uso 2: Consultar Progreso de Logros

**Actor Principal:** Usuario autenticado

**Precondiciones:**
- El usuario debe estar autenticado
- Deben existir logros activos en el sistema

**Flujo Principal:**
1. El usuario solicita ver su progreso en todos los logros
2. El sistema obtiene las estadísticas del usuario
3. El sistema obtiene todos los logros activos
4. Para cada logro, el sistema:
   - Calcula el progreso basándose en las estadísticas del usuario
   - Determina si el logro está desbloqueado, en progreso o bloqueado
   - Calcula el porcentaje de completitud
5. El sistema retorna la lista de logros con su progreso

**Flujos Alternativos:**

**FA1:** Usuario sin estadísticas
- El sistema crea estadísticas predeterminadas con valores en 0
- Todos los logros muestran 0% de progreso

**FA2:** Filtrar solo logros desbloqueados
- El usuario solicita ver solo los logros desbloqueados
- El sistema retorna solo los registros con `is_completed=True`

**FA3:** Consultar progreso de un logro específico
- El usuario solicita el progreso de un logro en particular
- El sistema calcula y retorna el progreso solo de ese logro

**Postcondiciones:**
- El usuario visualiza su progreso actualizado en los logros

---

## 3. Diseño de Casos de Prueba

### 3.1. Casos de Prueba para "Desbloquear un Logro"

#### CP-DL-001: Desbloqueo exitoso cuando se cumplen criterios

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-001 |
| **Descripción** | Verificar que un logro se desbloquea cuando el usuario cumple los criterios |
| **Precondiciones** | - Usuario autenticado<br>- Logro "Task Master" existe (requiere 10 tareas)<br>- Usuario tiene 10 tareas completadas |
| **Datos de entrada** | `user_id=1`, `achievement_id="task-master-uuid"` |
| **Pasos** | 1. Llamar a `unlock_achievement(user_id, achievement_id)`<br>2. Verificar creación de UserAchievement<br>3. Verificar `is_completed=True`<br>4. Verificar `progress=100.0` |
| **Resultado esperado** | - UserAchievement creado<br>- `is_completed=True`<br>- `unlocked_at` no es NULL<br>- Recompensas otorgadas<br>- Evento publicado |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_success` |

#### CP-DL-002: Error al desbloquear logro ya desbloqueado

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-002 |
| **Descripción** | Verificar que se rechaza el desbloqueo de un logro ya desbloqueado |
| **Precondiciones** | - Usuario autenticado<br>- Logro ya desbloqueado previamente |
| **Datos de entrada** | `user_id=1`, `achievement_id="already-unlocked-uuid"` |
| **Pasos** | 1. Intentar desbloquear logro ya desbloqueado<br>2. Capturar excepción |
| **Resultado esperado** | - Se lanza `ValueError` con mensaje "already unlocked"<br>- No se crea nuevo registro |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_raises_error_if_already_unlocked` |

#### CP-DL-003: Error al desbloquear logro inexistente

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-003 |
| **Descripción** | Verificar que se rechaza el desbloqueo de un logro que no existe |
| **Precondiciones** | - Usuario autenticado |
| **Datos de entrada** | `user_id=1`, `achievement_id="fake-uuid-12345"` |
| **Pasos** | 1. Intentar desbloquear logro inexistente<br>2. Capturar excepción |
| **Resultado esperado** | - Se lanza `ValueError` con mensaje "Achievement .* does not exist" |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_raises_error_for_nonexistent_achievement` |

#### CP-DL-004: Error al desbloquear con usuario inexistente

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-004 |
| **Descripción** | Verificar que se rechaza el desbloqueo si el usuario no existe |
| **Precondiciones** | - Logro válido existe |
| **Datos de entrada** | `user_id=99999`, `achievement_id="valid-uuid"` |
| **Pasos** | 1. Intentar desbloquear con usuario inexistente<br>2. Capturar excepción |
| **Resultado esperado** | - Se lanza `ValueError` con mensaje "User .* does not exist" |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_raises_error_for_nonexistent_user` |

#### CP-DL-005: Actualización de progreso cuando no se cumplen criterios

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-005 |
| **Descripción** | Verificar que se actualiza el progreso cuando no se cumplen los criterios completos |
| **Precondiciones** | - Usuario con 10 tareas completadas<br>- Logro requiere 20 tareas |
| **Datos de entrada** | `user_id=1`, `event_type="task_completed"` |
| **Pasos** | 1. Ejecutar `check_and_unlock_achievements`<br>2. Verificar que no se desbloquea<br>3. Verificar actualización de progreso |
| **Resultado esperado** | - No se desbloquea el logro<br>- `progress=50.0` (10/20)<br>- `is_completed=False` |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_check_and_unlock_achievements_updates_progress` |

#### CP-DL-006: Transaccionalidad en desbloqueo

| Campo | Valor |
|-------|-------|
| **ID** | CP-DL-006 |
| **Descripción** | Verificar que el desbloqueo usa transacciones atómicas |
| **Precondiciones** | - Usuario y logro válidos |
| **Datos de entrada** | `user_id=1`, `achievement_id="valid-uuid"` |
| **Pasos** | 1. Simular error en publicación de evento<br>2. Verificar que el UserAchievement fue guardado |
| **Resultado esperado** | - A pesar del error en el evento, el logro queda guardado<br>- Transacción commit antes de evento |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_uses_transaction` |

### 3.2. Casos de Prueba para "Consultar Progreso de Logros"

#### CP-CP-001: Obtener progreso de todos los logros

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-001 |
| **Descripción** | Verificar que se obtiene el progreso de todos los logros activos |
| **Precondiciones** | - Usuario autenticado con estadísticas<br>- Al menos 2 logros activos |
| **Datos de entrada** | `user_id=1` |
| **Pasos** | 1. Llamar a `calculate_all_progress(user_id)`<br>2. Verificar estructura de respuesta |
| **Resultado esperado** | - Lista con al menos 2 logros<br>- Cada elemento contiene: id, name, description, progress, progress_percentage, is_unlocked |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_calculate_all_progress` |

#### CP-CP-002: Obtener progreso con usuario sin estadísticas

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-002 |
| **Descripción** | Verificar que se crean estadísticas si no existen |
| **Precondiciones** | - Usuario sin registro de UserStatistics |
| **Datos de entrada** | `user_id=1` |
| **Pasos** | 1. Eliminar estadísticas del usuario<br>2. Llamar a `calculate_all_progress`<br>3. Verificar creación de estadísticas |
| **Resultado esperado** | - Se crea registro UserStatistics con valores por defecto<br>- Se retorna lista de progreso<br>- Todos los progresos en 0% |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_calculate_all_progress_creates_stats_if_missing` |

#### CP-CP-003: Obtener progreso de logro específico

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-003 |
| **Descripción** | Verificar consulta de progreso de un logro en particular |
| **Precondiciones** | - Usuario con logro en progreso (50%) |
| **Datos de entrada** | `user_id=1`, `achievement_id="in-progress-uuid"` |
| **Pasos** | 1. Llamar a `get_achievement_progress`<br>2. Verificar datos del progreso |
| **Resultado esperado** | - `achievement_id` correcto<br>- `current_progress=50.0`<br>- `percentage=50.0`<br>- `is_unlocked=False` |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_achievement_progress` |

#### CP-CP-004: Obtener progreso de logro no iniciado

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-004 |
| **Descripción** | Verificar progreso de logro sin UserAchievement |
| **Precondiciones** | - Usuario existe<br>- Logro existe pero usuario no ha iniciado |
| **Datos de entrada** | `user_id=1`, `achievement_id="not-started-uuid"` |
| **Pasos** | 1. Llamar a `get_achievement_progress`<br>2. Verificar valores iniciales |
| **Resultado esperado** | - `current_progress=0.0`<br>- `percentage=0.0`<br>- `is_unlocked=False` |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_achievement_progress_not_started` |

#### CP-CP-005: Filtrar solo logros desbloqueados

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-005 |
| **Descripción** | Verificar filtro de logros desbloqueados |
| **Precondiciones** | - Usuario con 1 logro desbloqueado y 1 en progreso |
| **Datos de entrada** | `user_id=1`, `include_locked=False` |
| **Pasos** | 1. Llamar a `get_user_achievements` con filtro<br>2. Verificar solo logros desbloqueados |
| **Resultado esperado** | - Lista con 1 elemento<br>- `is_unlocked=True` para todos |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_user_achievements_unlocked_only` |

#### CP-CP-006: Incluir todos los logros (bloqueados y desbloqueados)

| Campo | Valor |
|-------|-------|
| **ID** | CP-CP-006 |
| **Descripción** | Verificar inclusión de logros bloqueados |
| **Precondiciones** | - Usuario con logros en diferentes estados |
| **Datos de entrada** | `user_id=1`, `include_locked=True` |
| **Pasos** | 1. Llamar a `get_user_achievements` con include_locked<br>2. Verificar todos los logros activos |
| **Resultado esperado** | - Lista con al menos 2 elementos<br>- Mezcla de `is_unlocked=True` y `is_unlocked=False` |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_user_achievements_include_locked` |

### 3.3. Casos de Prueba para API (Integración)

#### CP-API-001: Listar logros disponibles

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-001 |
| **Descripción** | Verificar endpoint GET /achievements/ |
| **Precondiciones** | - Al menos 1 logro activo existe |
| **Datos de entrada** | GET /api/v1/achievements/ |
| **Pasos** | 1. Hacer petición GET<br>2. Verificar código de respuesta<br>3. Verificar estructura de datos |
| **Resultado esperado** | - Status 200 OK<br>- `results` con lista de logros<br>- Paginación presente |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_list_achievements` |

#### CP-API-002: Obtener detalle de logro

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-002 |
| **Descripción** | Verificar endpoint GET /achievements/{id}/ |
| **Precondiciones** | - Logro con nombre "Task Master" existe |
| **Datos de entrada** | GET /api/v1/achievements/{id}/ |
| **Pasos** | 1. Hacer petición GET con ID válido<br>2. Verificar datos del logro |
| **Resultado esperado** | - Status 200 OK<br>- `name="Task Master"`<br>- Todos los campos presentes |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_retrieve_achievement` |

#### CP-API-003: Desbloquear logro manualmente (POST)

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-003 |
| **Descripción** | Verificar endpoint POST /achievements/unlock/ |
| **Precondiciones** | - Usuario autenticado<br>- Logro no desbloqueado |
| **Datos de entrada** | POST /api/v1/achievements/unlock/<br>`{"achievement_id": "valid-uuid"}` |
| **Pasos** | 1. Hacer petición POST<br>2. Verificar respuesta<br>3. Verificar registro en BD |
| **Resultado esperado** | - Status 201 CREATED<br>- `is_completed=True` en respuesta<br>- UserAchievement creado |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement` |

#### CP-API-004: Error al desbloquear logro ya desbloqueado (POST)

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-004 |
| **Descripción** | Verificar rechazo de desbloqueo duplicado |
| **Precondiciones** | - Usuario con logro ya desbloqueado |
| **Datos de entrada** | POST /api/v1/achievements/unlock/<br>`{"achievement_id": "unlocked-uuid"}` |
| **Pasos** | 1. Hacer petición POST<br>2. Verificar error |
| **Resultado esperado** | - Status 400 BAD REQUEST<br>- Mensaje "already unlocked" en respuesta |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_unlock_achievement_already_unlocked` |

#### CP-API-005: Obtener logros del usuario autenticado

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-005 |
| **Descripción** | Verificar endpoint GET /achievements/me/ |
| **Precondiciones** | - Usuario autenticado<br>- Usuario tiene al menos 1 logro |
| **Datos de entrada** | GET /api/v1/achievements/me/ |
| **Pasos** | 1. Hacer petición GET autenticada<br>2. Verificar logros del usuario |
| **Resultado esperado** | - Status 200 OK<br>- Lista con al menos 1 logro |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_user_achievements` |

#### CP-API-006: Incluir logros bloqueados

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-006 |
| **Descripción** | Verificar parámetro include_locked |
| **Precondiciones** | - Usuario con logros desbloqueados y bloqueados |
| **Datos de entrada** | GET /api/v1/achievements/me/?include_locked=true |
| **Pasos** | 1. Hacer petición con parámetro<br>2. Verificar inclusión de todos |
| **Resultado esperado** | - Status 200 OK<br>- Lista incluye logros bloqueados y desbloqueados |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_user_achievements_include_locked` |

#### CP-API-007: Obtener progreso de todos los logros

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-007 |
| **Descripción** | Verificar endpoint GET /achievements/all-progress/ |
| **Precondiciones** | - Usuario autenticado<br>- Estadísticas existen |
| **Datos de entrada** | GET /api/v1/achievements/all-progress/ |
| **Pasos** | 1. Hacer petición GET<br>2. Verificar estructura de progreso |
| **Resultado esperado** | - Status 200 OK<br>- Cada elemento contiene: id, name, progress_percentage, is_unlocked |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_all_progress` |

#### CP-API-008: Rechazar acceso sin autenticación

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-008 |
| **Descripción** | Verificar protección de endpoints privados |
| **Precondiciones** | - Sin token de autenticación |
| **Datos de entrada** | GET /api/v1/achievements/all-progress/ |
| **Pasos** | 1. Hacer petición sin autenticación<br>2. Verificar rechazo |
| **Resultado esperado** | - Status 401 UNAUTHORIZED |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_get_all_progress_unauthenticated_without_user_id` |

#### CP-API-009: Filtrar logros por rareza

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-009 |
| **Descripción** | Verificar filtro de rareza |
| **Precondiciones** | - Logros con diferentes rarezas existen |
| **Datos de entrada** | GET /api/v1/achievements/?rarity=common |
| **Pasos** | 1. Hacer petición con filtro<br>2. Verificar solo logros comunes |
| **Resultado esperado** | - Status 200 OK<br>- Todos los resultados tienen `rarity="common"` |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_filter_by_rarity` |

#### CP-API-010: Buscar logros por nombre

| Campo | Valor |
|-------|-------|
| **ID** | CP-API-010 |
| **Descripción** | Verificar búsqueda de logros |
| **Precondiciones** | - Logro con "Task" en el nombre existe |
| **Datos de entrada** | GET /api/v1/achievements/?search=Task |
| **Pasos** | 1. Hacer petición con parámetro search<br>2. Verificar resultados |
| **Resultado esperado** | - Status 200 OK<br>- Al menos 1 resultado con "Task" en nombre |
| **Resultado obtenido** | ✅ PASS |
| **Test implementado** | `test_search_achievements` |

---

## 4. Clases de Equivalencia y Valores Límite

### 4.1. Campo: progress (Decimal, rango 0-100)

#### Clases de Equivalencia

| Clase | Descripción | Rango | Válida |
|-------|-------------|-------|--------|
| CE1 | Valores negativos | progress < 0 | ❌ Inválida |
| CE2 | Valor mínimo válido | progress = 0 | ✅ Válida |
| CE3 | Valores intermedios válidos | 0 < progress < 100 | ✅ Válida |
| CE4 | Valor máximo válido | progress = 100 | ✅ Válida |
| CE5 | Valores superiores al máximo | progress > 100 | ❌ Inválida |

#### Valores Límite

| Valor | Clase | Esperado |
|-------|-------|----------|
| -10.00 | CE1 | Se ajusta a 0.00 |
| -0.01 | CE1 | Se ajusta a 0.00 |
| 0.00 | CE2 | Aceptado |
| 0.01 | CE3 | Aceptado |
| 50.00 | CE3 | Aceptado |
| 99.99 | CE3 | Aceptado |
| 100.00 | CE4 | Aceptado |
| 100.01 | CE5 | Se ajusta a 100.00 |
| 150.00 | CE5 | Se ajusta a 100.00 |

**Tests implementados:**
- `test_update_progress_max_100`: Verifica ajuste a 100
- `test_update_progress_min_0`: Verifica ajuste a 0
- `test_update_progress`: Verifica actualización normal

### 4.2. Campo: count (Integer, rango 1-100 en simulación)

#### Clases de Equivalencia

| Clase | Descripción | Rango | Válida |
|-------|-------------|-------|--------|
| CE1 | Valores no positivos | count ≤ 0 | ❌ Inválida |
| CE2 | Valores válidos bajos | 1 ≤ count < 50 | ✅ Válida |
| CE3 | Valores válidos medios | count = 50 | ✅ Válida |
| CE4 | Valores válidos altos | 50 < count ≤ 100 | ✅ Válida |
| CE5 | Valores superiores al límite | count > 100 | ❌ Inválida |

#### Valores Límite

| Valor | Clase | Esperado |
|-------|-------|----------|
| 0 | CE1 | Error de validación |
| 1 | CE2 | Aceptado |
| 2 | CE2 | Aceptado |
| 50 | CE3 | Aceptado |
| 99 | CE4 | Aceptado |
| 100 | CE4 | Aceptado |
| 101 | CE5 | Error de validación |
| 150 | CE5 | Error de validación |

**Tests implementados:**
- `test_simulate_task_completions`: Verifica conteo válido
- `test_simulate_task_completions_invalid_count`: Verifica rechazo de count > 100
- `test_validate_count_minimum`: Verifica rechazo de count < 1
- `test_validate_count_maximum`: Verifica rechazo de count > 100

### 4.3. Campo: reward_xp y reward_coins (Integer, ≥ 0)

#### Clases de Equivalencia

| Clase | Descripción | Rango | Válida |
|-------|-------------|-------|--------|
| CE1 | Valores negativos | reward < 0 | ❌ Inválida |
| CE2 | Valor cero | reward = 0 | ✅ Válida |
| CE3 | Valores positivos | reward > 0 | ✅ Válida |

#### Valores Límite

| Valor XP | Valor Coins | Esperado |
|----------|-------------|----------|
| -100 | 50 | Error de validación |
| 100 | -50 | Error de validación |
| -100 | -50 | Error de validación |
| 0 | 0 | Aceptado |
| 0 | 50 | Aceptado |
| 100 | 0 | Aceptado |
| 100 | 50 | Aceptado |

**Tests implementados:**
- `test_validate_reward_xp_rejects_negative`: Verifica rechazo XP negativo
- `test_validate_reward_coins_rejects_negative`: Verifica rechazo coins negativo
- `test_validate_reward_values_valid`: Verifica aceptación de valores positivos
- `test_validate_reward_values_zero`: Verifica aceptación de valores en 0

### 4.4. Campo: criteria (JSONField)

#### Clases de Equivalencia

| Clase | Descripción | Ejemplo | Válida |
|-------|-------------|---------|--------|
| CE1 | Criterio válido task_count | `{"required_count": 10}` | ✅ Válida |
| CE2 | Criterio válido streak | `{"required_days": 7}` | ✅ Válida |
| CE3 | Criterio válido level | `{"required_level": 5}` | ✅ Válida |
| CE4 | Criterio vacío | `{}` | ✅ Válida |
| CE5 | No es diccionario | `"not a dict"` | ❌ Inválida |
| CE6 | Null | `null` | ❌ Inválida |

**Tests implementados:**
- `test_validate_criteria_rejects_non_dict`: Verifica rechazo de no-dict
- `test_validate_criteria_format_valid_dict`: Verifica aceptación de dict válido
- `test_validate_criteria_format_empty_dict`: Verifica aceptación de dict vacío

---

## 5. Implementación de Pruebas

### 5.1. Estructura de Tests

El proyecto implementa pruebas siguiendo la estructura de pytest-django:

```
src/apps/achievements/tests/
├── __init__.py
├── conftest.py                 # Fixtures compartidos
├── test_models.py              # Pruebas de modelos
├── test_serializers.py         # Pruebas de serializers
├── test_validators.py          # Pruebas de validators
├── test_managers.py            # Pruebas de managers
├── test_evaluator.py           # Pruebas de evaluador
├── test_services.py            # Pruebas de servicios
└── test_views.py               # Pruebas de API
```

---

## 6. Análisis de Resultados

**Observación:** La cantidad de tests implementados supera ampliamente los casos de prueba diseñados, cubriendo escenarios adicionales y casos límite no contemplados inicialmente.

### 6.1. Sobre el Diseño de Pruebas

**✅ Puntos Positivos:**
1. **Partición por clases de equivalencia** permitió identificar casos límite tempranamente
2. **Fixtures reutilizables** aceleraron significativamente el desarrollo de tests

**⚠️ Desafíos encontrados:**
1. **Tests asíncronos complejos** para event handlers requieren más infraestructura
2. **Mocking de dependencias externas** puede ser complicado
3. **Balance entre tests unitarios e integración** requiere decisiones conscientes

### 6.2. Sobre los Casos de Uso

**Relación Use Cases → Tests:**
- Los casos de uso proveen el **QUÉ** probar (funcionalidad esperada)
- Los tests implementan el **CÓMO** verificarlo (aserciones específicas)
- Los flujos alternativos son críticos para cobertura completa

**Importancia de documentar flujos alternativos:**
- Cada flujo alternativo → mínimo 1 test
- Flujos de excepción → tests de manejo de errores
- Precondiciones → fixtures y setup de tests

**Ventajas del patrón:**
- Claridad en la estructura del test
- Fácil identificación de qué se está probando
- Mantenibilidad a largo plazo


### 6.3. Conclusiones Finales

#### Sobre el Proceso de Testing

1. **Los casos de uso son fundamentales** para diseñar pruebas funcionales completas. Cada flujo (principal y alternativos) debe tener tests correspondientes.

2. **Las técnicas de caja negra (partición de equivalencia, valores límite)** son efectivas para identificar casos de prueba no obvios y encontrar bugs en los bordes.

3. **La cobertura de código es útil pero no suficiente**. Un 90% de cobertura no garantiza calidad si no se prueban escenarios críticos de negocio.

4. **Los tests de integración encuentran diferentes bugs que los unitarios**. Ambos niveles son necesarios para una suite de pruebas robusta.

#### Sobre la Calidad del Código

1. **Escribir tests primero (TDD) o junto con el código** resulta en mejor diseño. Los componentes testeables son inherentemente más modulares.

2. **Fixtures bien diseñados reducen significativamente el boilerplate**. El tiempo invertido en fixtures se recupera multiplicado en tests más simples.

3. **Los tests sirven como documentación viva**. Un desarrollador nuevo puede entender el comportamiento esperado leyendo los tests.

#### Sobre los Casos de Uso del Proyecto

1. **"Desbloquear un logro"** es un caso de uso complejo que involucra:
   - Validación de criterios
   - Transacciones de base de datos
   - Eventos asíncronos
   - Otorgamiento de recompensas
   - Notificaciones
   
   Requiere pruebas exhaustivas en todos los niveles.

2. **"Consultar progreso de logros"** es un caso de uso de consulta que requiere:
   - Cálculos correctos de porcentajes
   - Manejo de datos faltantes
   - Filtrado y paginación
   - Rendimiento optimizado

3. **La arquitectura event-driven** del sistema añade complejidad al testing pero mejora la escalabilidad. Los tests deben verificar tanto el comportamiento síncrono como la correcta publicación de eventos.

---

## Referencias

### Código Fuente

- [Achievement Tests](../../src/apps/achievements/tests/)
- [Achievement Models](../../src/apps/achievements/models/)
- [Achievement Services](../../src/apps/achievements/services/)
- [Achievement API](../../src/apps/achievements/api/)
