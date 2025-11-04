# Guía de Despliegue de Documentación - Gamify

Esta guía explica cómo construir, visualizar y desplegar la documentación del proyecto Gamify usando **MkDocs** con el tema **Material**.

---

## Tabla de Contenidos

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalación de dependencias](#2-instalación-de-dependencias)
3. [Visualizar documentación localmente](#3-visualizar-documentación-localmente)
4. [Construir el sitio estático](#4-construir-el-sitio-estático)
5. [Desplegar en GitHub Pages](#5-desplegar-en-github-pages)
6. [Configuración avanzada](#6-configuración-avanzada)
7. [Solución de problemas](#7-solución-de-problemas)

---

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.13.5** (o compatible según `.python-version`)
- **uv** (gestor de paquetes Python) - Recomendado
- **Git** (para control de versiones y despliegue)

### Verificar instalaciones

```cmd
python --version
git --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/).

---

## 2. Instalación de dependencias

### Opción A: Usando uv (Recomendado)

**uv** es un gestor de paquetes Python ultrarrápido que reemplaza a pip.

#### Instalar uv

```cmd
pip install uv
```

#### Instalar dependencias del proyecto

```cmd
cd "d:\College\Licenciatura en Ciencia de Datos\Ingeniería en Software\Ingeniería en Software II\software-engineering"
uv sync
```

Esto instalará todas las dependencias definidas en `pyproject.toml`, incluyendo:
- `mkdocs`
- `mkdocs-material` (tema)
- Extensiones y plugins

### Opción B: Usando pip

Si prefieres usar pip:

```cmd
pip install mkdocs mkdocs-material mkdocstrings mkdocstrings-python pymdown-extensions
```

---

## 3. Visualizar documentación localmente

MkDocs incluye un servidor de desarrollo que recarga automáticamente los cambios.

### Comando básico

```cmd
mkdocs serve
```

### Usando uv

```cmd
uv run mkdocs serve
```

### Resultado esperado

```
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.52 seconds
INFO    -  [12:34:56] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [12:34:56] Serving on http://127.0.0.1:8000/gamify/
```

### Abrir en el navegador

Abre tu navegador y visita:

```
http://127.0.0.1:8000/gamify/
```

O simplemente:

```
http://localhost:8000/gamify/
```

### Características del servidor de desarrollo

- ✅ **Recarga automática**: Los cambios en archivos `.md` o `mkdocs.yml` se reflejan instantáneamente
- ✅ **Preview en tiempo real**: Ve cómo se verá la documentación antes de desplegarla
- ✅ **Navegación completa**: Prueba todos los enlaces y navegación

### Detener el servidor

Presiona `Ctrl + C` en la terminal.

---

## 4. Construir el sitio estático

Para generar los archivos HTML estáticos de la documentación:

### Comando básico

```cmd
mkdocs build
```

### Usando uv

```cmd
uv run mkdocs build
```

### Resultado

Los archivos HTML se generarán en el directorio `site/`:

```
site/
├── index.html
├── README/
├── design/
├── practical_work/
├── requirements/
├── specifications/
├── CI_INVENTORY/
├── DEPLOYMENT_GUIDE/
├── assets/
├── search/
└── ...
```

### Opciones útiles

#### Limpiar antes de construir

```cmd
mkdocs build --clean
```

#### Modo estricto (falla si hay warnings)

```cmd
mkdocs build --strict
```

#### Especificar directorio de salida

```cmd
mkdocs build --site-dir mi_sitio
```

---

## 5. Desplegar en GitHub Pages

GitHub Pages permite alojar sitios estáticos directamente desde un repositorio de GitHub.

### 5.1. Despliegue automático con MkDocs

MkDocs incluye un comando que construye y despliega automáticamente:

```cmd
mkdocs gh-deploy
```

O con uv:

```cmd
uv run mkdocs gh-deploy
```

### ¿Qué hace este comando?

1. Construye la documentación (ejecuta `mkdocs build`)
2. Crea/actualiza la rama `gh-pages`
3. Copia los archivos del directorio `site/` a la rama `gh-pages`
4. Hace commit y push automáticamente

### 5.2. Configurar GitHub Pages

#### Paso 1: Ir a la configuración del repositorio

1. Abre tu repositorio en GitHub: [github.com/caupolicanre/gamify](https://github.com/caupolicanre/gamify)
2. Ve a **Settings** (Configuración)
3. En el menú lateral, selecciona **Pages**

#### Paso 2: Configurar la fuente

- **Source**: Selecciona `Deploy from a branch`
- **Branch**: Selecciona `gh-pages` y carpeta `/ (root)`
- Click en **Save**

#### Paso 3: Esperar el despliegue

GitHub Actions construirá y desplegará el sitio automáticamente. Esto puede tardar 1-3 minutos.

#### Paso 4: Verificar el sitio

Tu documentación estará disponible en:

```
https://caupolicanre.github.io/gamify/
```

### 5.3. Configurar dominio personalizado (Opcional)

Si tienes un dominio propio:

1. Ve a **Settings → Pages**
2. En **Custom domain**, ingresa tu dominio
3. Configura los DNS de tu proveedor:
   - Tipo: `CNAME`
   - Name: `docs` (o el subdominio que prefieras)
   - Value: `caupolicanre.github.io`

---

## 6. Configuración avanzada

### 6.1. Estructura del archivo mkdocs.yml

```yaml
site_name: Gamify
site_url: https://caupolicanre.github.io/gamify
repo_url: https://github.com/caupolicanre/gamify

nav:
  - Home: index.md
  - Documentación:
      - Visión general: README.md
      - Guía de despliegue: DEPLOYMENT_GUIDE.md
  - Diseño:
      - Visión general: design/README.md
      - Documentación completa: design/design_documentation.md
  # ... más secciones

theme:
  name: material
  features:
    - navigation.tabs      # Pestañas de navegación
    - navigation.sections  # Secciones colapsables
    - navigation.top       # Botón "volver arriba"
    - search.suggest       # Sugerencias de búsqueda
    - search.highlight     # Resaltar términos buscados
  language: es
```

### 6.2. Personalizar el tema

#### Colores

```yaml
theme:
  palette:
    - scheme: default
      primary: indigo
      accent: pink
```

#### Logo

```yaml
theme:
  logo: resources/images/logo.png
  favicon: resources/images/favicon.ico
```

#### Fuentes

```yaml
theme:
  font:
    text: Roboto
    code: Roboto Mono
```

### 6.3. Extensiones de Markdown útiles

Ya configuradas en `mkdocs.yml`:

- `pymdownx.highlight`: Resaltado de código
- `pymdownx.superfences`: Bloques de código con pestañas
- `pymdownx.tabbed`: Contenido con pestañas
- `admonition`: Notas, advertencias, tips
- `toc`: Tabla de contenidos

#### Ejemplo de admonitions

```markdown
!!! note "Nota importante"
    Este es un mensaje de nota.

!!! warning "Advertencia"
    Ten cuidado con esto.

!!! tip "Consejo"
    Aquí va un consejo útil.
```

### 6.4. Añadir búsqueda

Ya está configurado con el plugin `search`:

```yaml
plugins:
  - search:
      lang: es
```

---

## 7. Solución de problemas

### Problema 1: "mkdocs: command not found"

**Causa**: MkDocs no está en el PATH o no está instalado.

**Solución**:

```cmd
# Verificar instalación
pip show mkdocs

# Reinstalar si es necesario
uv sync
# o
pip install mkdocs
```

### Problema 2: Errores al ejecutar `mkdocs serve`

**Causa**: Puede haber errores en `mkdocs.yml` o archivos `.md`.

**Solución**:

```cmd
# Modo verbose para ver detalles
mkdocs serve --verbose
```

Revisa el output para identificar el archivo problemático.

### Problema 3: Enlaces rotos en la documentación

**Causa**: Rutas incorrectas en los enlaces.

**Solución**:

```cmd
# Construir en modo estricto
mkdocs build --strict
```

Esto fallará si hay enlaces rotos, mostrando cuáles son.

### Problema 4: Cambios no se reflejan en GitHub Pages

**Causa**: El despliegue no se completó o hay caché.

**Solución**:

1. Verifica que el comando `mkdocs gh-deploy` terminó sin errores
2. Espera 2-3 minutos para que GitHub actualice
3. Fuerza recarga en el navegador: `Ctrl + Shift + R`
4. Revisa la pestaña **Actions** en GitHub para ver el estado del deployment

### Problema 5: Imágenes no se muestran

**Causa**: Rutas incorrectas o archivos no commiteados.

**Solución**:

- Usa rutas relativas: `![Diagrama](./diagrams/images/diagram.png)`
- Asegúrate de que las imágenes estén en `docs/` o subdirectorios
- Verifica que los archivos estén commiteados en Git:

```cmd
git status
git add docs/design/diagrams/images/
git commit -m "Add diagrams"
git push
```

### Problema 6: Python 3.13.5 no disponible

**Causa**: Versión específica de Python no instalada.

**Solución**:

Modifica `.python-version` o usa la versión de Python que tengas:

```cmd
# Ver tu versión de Python
python --version

# Usar esa versión
uv python pin 3.11  # o la que tengas
```

---

## Comandos de referencia rápida

### Desarrollo local

```cmd
# Servidor de desarrollo
mkdocs serve

# Con uv
uv run mkdocs serve
```

### Construcción

```cmd
# Construir sitio
mkdocs build

# Limpiar y construir
mkdocs build --clean

# Modo estricto
mkdocs build --strict
```

### Despliegue

```cmd
# Desplegar a GitHub Pages
mkdocs gh-deploy

# Con mensaje de commit personalizado
mkdocs gh-deploy -m "Update documentation"
```

### Gestión de dependencias

```cmd
# Sincronizar dependencias con uv
uv sync

# Actualizar dependencias
uv sync --upgrade

# Ver dependencias instaladas
uv pip list
```

---

## Estructura de archivos de documentación

```
software-engineering/
├── docs/                           # Directorio de documentación
│   ├── index.md                    # Página principal
│   ├── README.md                   # Visión general
│   ├── DEPLOYMENT_GUIDE.md         # Esta guía
│   ├── CI_INVENTORY.md             # Inventario de CIs
│   ├── design/                     # Documentación de diseño
│   │   ├── README.md
│   │   ├── design_documentation.md
│   │   └── diagrams/
│   │       ├── *.drawio
│   │       ├── c4/
│   │       └── images/
│   ├── practical_work/             # Trabajos prácticos
│   │   ├── TP1_part1_architecture.md
│   │   ├── TP1_part2_apply_architecture.md
│   │   ├── TP2_sequence_diagram.md
│   │   └── TP3_class_deployment_diagrams.md
│   ├── requirements/               # Requerimientos
│   │   ├── README.md
│   │   ├── casos_uso.xlsx
│   │   └── atributos_calidad.xlsx
│   └── specifications/             # Especificaciones
│       ├── README.md
│       └── TP_final_IS_1.docx
├── mkdocs.yml                      # Configuración de MkDocs
├── pyproject.toml                  # Dependencias del proyecto
└── site/                           # Sitio generado (no commitear)
```

---

## Recursos adicionales

### Documentación oficial

- **MkDocs**: [mkdocs.org](https://www.mkdocs.org/)
- **Material for MkDocs**: [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- **GitHub Pages**: [docs.github.com/pages](https://docs.github.com/en/pages)

### Ejemplos de configuración

- [Repositorio de MkDocs Material](https://github.com/squidfunk/mkdocs-material)
- [Ejemplos de temas](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes)

### Extensiones útiles

- [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)
- [MkDocs Plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins)

---

## Flujo de trabajo recomendado

### Para desarrollo diario

1. Inicia el servidor local:
   ```cmd
   uv run mkdocs serve
   ```

2. Edita archivos `.md` en `docs/`

3. Verifica cambios en `http://localhost:8000/gamify/`

4. Cuando estés satisfecho, commitea:
   ```cmd
   git add docs/
   git commit -m "Update documentation"
   git push
   ```

### Para despliegue a producción

1. Asegúrate de que todo está commiteado:
   ```cmd
   git status
   ```

2. Prueba la construcción localmente:
   ```cmd
   uv run mkdocs build --strict
   ```

3. Si no hay errores, despliega:
   ```cmd
   uv run mkdocs gh-deploy
   ```

4. Verifica en: https://caupolicanre.github.io/gamify/

---

## Contacto y soporte

Si tienes problemas o preguntas:

- **Repositorio**: [github.com/caupolicanre/gamify](https://github.com/caupolicanre/gamify)
- **Issues**: [github.com/caupolicanre/gamify/issues](https://github.com/caupolicanre/gamify/issues)
- **Autores**: 
  - Caupolicán Ré - [@caupolicanre](https://github.com/caupolicanre)
  - Felipe Carrozzo - [@felipecarrozzo](https://github.com/felipecarrozzo)

---

**¡Listo!** Ahora tienes todo lo necesario para trabajar con la documentación de Gamify. 🎉
