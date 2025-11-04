# 🎬 Guía Paso a Paso para la Demostración

## 📋 Preparación Previa (Solo una vez)

### 1. Verificar Instalación de Dependencias

```bash
# Desde el directorio raíz del proyecto
uv sync
```

Esto instalará automáticamente Flask y todas las dependencias necesarias.

### 2. Crear Base de Datos y Migraciones

```bash
cd src
uv run python manage.py migrate
```

### 3. Crear Superusuario (si no existe)

```bash
uv run python manage.py createsuperuser
# Username: caupo (o el que prefieras)
# Email: tu@email.com
# Password: (cualquier password seguro)
```

### 4. Cargar Datos de Ejemplo

```bash
# Crear logros de ejemplo
uv run python manage.py create_sample_achievements

# Crear estadísticas iniciales
uv run python manage.py create_test_user_stats --user-id 1
```

## 🚀 Ejecutar la Demo

### Opción A: Ejecución Manual (Recomendado para desarrollo)

**Terminal 1 - Django Backend:**
```bash
cd src
uv run python manage.py runserver
```

Deberías ver:
```
Starting development server at http://127.0.0.1:8000/
```

**Terminal 2 - Verificar que todo está listo:**
```bash
cd src
uv run python check_demo.py
```

Deberías ver todos los checks en verde ✅

**Terminal 3 - Flask Demo:**
```bash
cd src
uv run python demo_app.py
```

Deberías ver:
```
🎮 Gamify Achievement System - Demo App
📍 Demo URL: http://localhost:5000
```

### Opción B: Ejecución Rápida (Windows)

```bash
cd src
start_demo.bat
```

## 🎯 Script de Demostración

### Parte 1: Introducción (2 minutos)

1. **Abrir la demo** en el navegador: `http://localhost:5000`

2. **Explicar la interfaz:**
   - "Aquí tenemos el panel de estadísticas del usuario"
   - "Podemos ver tareas completadas, racha actual, logros y XP"
   - "Esta es la lista de todos los logros disponibles"

3. **Mostrar los logros bloqueados:**
   - "Cada logro tiene su descripción, rareza y recompensas"
   - "La barra de progreso muestra qué tan cerca estamos de desbloquearlo"

### Parte 2: Demostración del Flujo (5 minutos)

#### Paso 1: Estado Inicial
```
📊 Estado:
- Tareas: 0
- Logros desbloqueados: 0
- XP: 0
```

#### Paso 2: Completar Primera Tarea
1. En el campo "Simular Completación de Tareas", ingresa: **1**
2. Click en **"Completar Tareas"**
3. Click en **"Recargar Datos"**

```
✅ Resultado:
- Se desbloquea: "First Steps" (Common)
- Tareas: 1
- Logros: 1
- XP: +100
```

**Explicación:**
> "El sistema detectó que completamos 1 tarea y automáticamente desbloqueó el logro 'First Steps' que requería exactamente 1 tarea completada."

#### Paso 3: Completar 10 Tareas
1. Ingresa: **10**
2. Click en **"Completar Tareas"**
3. Click en **"Recargar Datos"**

```
✅ Resultado:
- Se desbloquea: "Task Master" (Rare)
- Tareas: 11 (1 anterior + 10 nuevas)
- Logros: 2
- XP: +500 (total 600)
```

**Explicación:**
> "Al alcanzar 10 tareas completadas, se desbloqueó automáticamente 'Task Master', un logro de rareza Rare con mayor recompensa."

#### Paso 4: Completar 100 Tareas
1. Ingresa: **100**
2. Click en **"Completar Tareas"**
3. Click en **"Recargar Datos"**

```
✅ Resultado:
- Se desbloquea: "Century Club" (Epic)
- Tareas: 111
- Logros: 3
- XP: +2000 (total 2600)
```

**Explicación:**
> "Con 100 tareas completadas, desbloqueamos 'Century Club', un logro Epic con recompensa significativa de 2000 XP."

### Parte 3: Características Adicionales (3 minutos)

#### Demostrar Filtros
1. Click en **"Desbloqueados"**
   - Muestra solo los 3 logros que acabamos de desbloquear
   
2. Click en **"Bloqueados"**
   - Muestra los logros que aún no hemos conseguido
   - Nota: Las barras de progreso muestran cuánto falta

3. Click en **"Todos"**
   - Vista completa de todos los logros

#### Demostrar Desbloqueo Manual (Testing)
1. Busca un logro bloqueado (ej: "Week Warrior")
2. Click en el botón **"Desbloquear"**
3. Confirma la acción

```
💡 Explicación:
"Esta función de desbloqueo manual es útil para testing y debugging. En producción, los logros solo se desbloquean cuando se cumplen los criterios automáticamente."
```

### Parte 4: Arquitectura y Tecnología (2 minutos)

**Explicar el stack:**

```
Frontend (Flask Demo):
├── HTML5 + Bootstrap 5
├── JavaScript (Fetch API)
└── Interfaz responsive

Backend (Django REST):
├── Django 5.2.7
├── Django REST Framework
├── PostgreSQL
└── API RESTful

Comunicación:
└── HTTP/JSON (localhost:8000 ↔ localhost:5000)
```

**Flujo de datos:**
```
1. Usuario → Simula tarea
2. Flask → POST a Django API
3. Django → Evalúa criterios de logros
4. Django → Desbloquea logro si cumple
5. Django → Retorna estado actualizado
6. Flask → Actualiza interfaz
7. Usuario → Ve logro desbloqueado
```

## 📊 Casos de Uso Demostrados

### ✅ Caso 1: Desbloqueo Automático por Tareas
- **Criterio**: Completar N tareas
- **Ejemplo**: First Steps (1), Task Master (10), Century Club (100)

### ✅ Caso 2: Sistema de Rareza
- **Common**: Logros básicos, bajo XP
- **Rare**: Logros moderados, XP medio
- **Epic**: Logros difíciles, alto XP
- **Legendary**: Logros muy difíciles, XP máximo

### ✅ Caso 3: Sistema de Progreso
- Barras de progreso muestran avance
- Contador visual (ej: 50/100)
- Porcentaje de completitud

### ✅ Caso 4: Recompensas
- XP acumulativo
- Monedas virtuales
- Visualización de recompensas en cada logro

## 🎤 Preguntas Frecuentes en la Demo

**P: ¿Los logros se guardan en la base de datos?**
R: Sí, todos los logros y el progreso del usuario se persisten en PostgreSQL.

**P: ¿Qué pasa si completo más tareas de las necesarias?**
R: El sistema registra el total acumulado. Si completaste 150 tareas, ya tienes desbloqueados todos los logros de tareas (1, 10, 100).

**P: ¿Cómo funciona el desbloqueo automático?**
R: Django tiene event handlers que escuchan eventos (tareas completadas, rachas, etc.) y evalúan automáticamente los criterios de cada logro.

**P: ¿Se puede integrar con aplicaciones reales?**
R: Sí, la API REST puede consumirse desde cualquier frontend (React, Vue, móvil, etc.).

## 🐛 Solución Rápida de Problemas

### Error: "Cannot connect to Django"
```bash
# Solución: Asegurate de que Django esté corriendo
cd src
uv run python manage.py runserver
```

### Error: "No achievements found"
```bash
# Solución: Crea los logros de ejemplo
cd src
uv run python manage.py create_sample_achievements
```

### Error: Puerto 5000 en uso
```python
# Edita demo_app.py, línea final:
app.run(debug=True, port=5001)  # Cambia a otro puerto
```

## 🎓 Conclusión de la Demo

**Resumen de lo demostrado:**
1. ✅ Sistema de logros funcional
2. ✅ Desbloqueo automático basado en criterios
3. ✅ Sistema de rareza y recompensas
4. ✅ Tracking de progreso en tiempo real
5. ✅ API REST completa y funcional
6. ✅ Interfaz moderna y responsive

**Próximos pasos posibles:**
- Integración con frontend real (React/Vue)
- Sistema de notificaciones en tiempo real
- Logros por rachas y niveles
- Ranking y competición entre usuarios
- Logros secretos y eventos especiales

---

**Duración total recomendada:** 10-15 minutos

**Archivos importantes:**
- `demo_app.py` - Aplicación Flask
- `templates/index.html` - Interfaz web
- `check_demo.py` - Script de verificación
- `DEMO_README.md` - Documentación completa
