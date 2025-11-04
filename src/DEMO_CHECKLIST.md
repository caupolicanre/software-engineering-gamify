# ✅ Checklist Pre-Demo

## 🔍 Antes de Comenzar

### 1. Verificar Entorno
```bash
# ¿Python 3.13.5 instalado?
python --version

# ¿UV instalado?
uv --version

# ¿Dependencias sincronizadas?
uv sync
```

- [ ] Python 3.13.5 ✓
- [ ] UV package manager ✓
- [ ] Todas las dependencias instaladas ✓

### 2. Verificar Base de Datos
```bash
cd src
uv run python manage.py showmigrations
```

- [ ] Migraciones aplicadas ✓
- [ ] Superusuario creado (ID=1) ✓

### 3. Verificar Datos de Prueba
```bash
cd src
uv run python check_demo.py
```

Debe mostrar:
- [ ] ✅ Flask instalado ✓
- [ ] ✅ API Django funcionando ✓
- [ ] ✅ Logros creados (mínimo 9) ✓

### 4. Iniciar Servicios

**Terminal 1 - Django:**
```bash
cd src
uv run python manage.py runserver
```
- [ ] Django corriendo en http://localhost:8000 ✓
- [ ] API responde en http://localhost:8000/api/v1/achievements/ ✓

**Terminal 2 - Flask:**
```bash
cd src
uv run python demo_app.py
```
- [ ] Flask corriendo en http://localhost:5000 ✓
- [ ] Página de demo carga correctamente ✓

### 5. Prueba Rápida

Abre: http://localhost:5000

- [ ] Página carga sin errores ✓
- [ ] Panel de estadísticas visible ✓
- [ ] Logros se muestran en cards ✓
- [ ] Todos los valores en 0 (estado inicial) ✓

## 🎬 Durante la Demo

### Preparar la Pantalla
- [ ] Navegador en pantalla completa (F11)
- [ ] Zoom al 100% (Ctrl+0)
- [ ] DevTools cerradas (F12)
- [ ] Pestañas innecesarias cerradas
- [ ] Notificaciones del sistema desactivadas

### Tener Abiertas
- [ ] Tab 1: Demo Flask (http://localhost:5000)
- [ ] Tab 2: Django Admin (http://localhost:8000/admin) - opcional
- [ ] Tab 3: API JSON (http://localhost:8000/api/v1/achievements/) - opcional

### Script de Demostración

#### Paso 1: Introducción (1 min)
- [ ] Explicar qué es Gamify
- [ ] Mostrar panel de estadísticas
- [ ] Mostrar lista de logros

#### Paso 2: Primera Tarea (2 min)
- [ ] Completar 1 tarea
- [ ] Ver "First Steps" desbloqueado
- [ ] Mostrar aumento de XP

#### Paso 3: Múltiples Tareas (2 min)
- [ ] Completar 10 tareas
- [ ] Ver "Task Master" desbloqueado
- [ ] Mostrar progreso acumulativo

#### Paso 4: Logro Epic (2 min)
- [ ] Completar 100 tareas
- [ ] Ver "Century Club" desbloqueado
- [ ] Mostrar recompensas altas

#### Paso 5: Filtros (1 min)
- [ ] Demostrar filtro "Desbloqueados"
- [ ] Demostrar filtro "Bloqueados"
- [ ] Mostrar barras de progreso

#### Paso 6: Desbloqueo Manual (1 min)
- [ ] Seleccionar logro bloqueado
- [ ] Desbloquear manualmente
- [ ] Explicar uso para testing

#### Paso 7: Recarga de Datos (1 min)
- [ ] Click en "Recargar Datos"
- [ ] Verificar actualización
- [ ] Mostrar estadísticas finales

#### Paso 8: Q&A (Resto del tiempo)
- [ ] Responder preguntas
- [ ] Mostrar código si es necesario
- [ ] Explicar arquitectura

## 🐛 Plan de Contingencia

### Problema: Django no responde
```bash
# Solución: Reiniciar servidor
Ctrl+C
uv run python manage.py runserver
```

### Problema: Flask no carga datos
```bash
# Verificar conectividad
curl http://localhost:8000/api/v1/achievements/

# Recargar página
F5 o Ctrl+R
```

### Problema: No hay logros
```bash
# Recrear logros
cd src
uv run python manage.py create_sample_achievements
```

### Problema: Puerto ocupado
```python
# Cambiar puerto en demo_app.py
app.run(debug=True, port=5001)  # Usar otro puerto
```

## 📝 Notas para Recordar

### Puntos Clave a Mencionar
- ✅ Sistema de logros gamificado
- ✅ Desbloqueo automático basado en criterios
- ✅ Sistema de rareza y recompensas
- ✅ API REST completa
- ✅ Tracking de progreso en tiempo real
- ✅ Arquitectura desacoplada (Django + Flask)

### Datos Importantes
- Usuario demo: Superuser (ID: 1)
- Sin autenticación para simplificar demo
- PostgreSQL como base de datos
- Bootstrap 5 para UI moderna
- Comunicación HTTP/JSON entre servicios

## 🎯 Métricas de Éxito

Al final de la demo, debes poder mostrar:
- [ ] Mínimo 3 logros desbloqueados
- [ ] Estadísticas actualizadas (tareas, XP)
- [ ] Barras de progreso funcionando
- [ ] Filtros operativos
- [ ] Notificaciones Toast visibles
- [ ] UI responsive y fluida

## ⏰ Timeboxing

| Sección | Tiempo | Acumulado |
|---------|--------|-----------|
| Setup y verificación | 5 min | 5 min |
| Introducción | 1 min | 6 min |
| Demo interactiva | 7 min | 13 min |
| Q&A | 2 min | 15 min |

**Total recomendado: 15 minutos**

## 🚨 Último Check (30 segundos antes)

```bash
# Terminal 1
cd src
uv run python manage.py runserver
# ✅ Verificar que esté corriendo

# Terminal 2
cd src
uv run python demo_app.py
# ✅ Verificar que esté corriendo

# Navegador
http://localhost:5000
# ✅ Verificar que cargue

# Reload para estado fresco
Ctrl+R o F5
```

---

## ✅ Demo Lista

Si todos los checks están marcados, ¡estás listo para la demostración!

**¡Éxitos! 🎉**
