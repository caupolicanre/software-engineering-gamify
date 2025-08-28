# Módulo de Inventario

Este módulo centraliza el **inventario de activos (Configuration Items, CIs)** que forman parte del proyecto.

---

## Tabla de activos

| ID | Nombre del CI | Formato | Categoría | Versión | Ubicación | Responsable | Criticidad | Justificación |
|------|---------|---------|-----------|---------|-----------|-------------|------------|---------------|
| **CI-001** | [Diagrama de contexto]() | `.drawio` | Documentación | 1.0.0 | [`/docs/design`](../design) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Representa el sistema y sus interacciones con actores externos. |
| **CI-002** | [Diagrama de dominio]() | `.drawio` | Diseño | 1.0.0 | [`/docs/design`](../design) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Representa gráficamente la interacción entre actores y funcionalidades del sistema. |
| **CI-003** | [Diagrama de casos de uso]() | `.drawio` | Diseño | 1.0.0 | [`/docs/design`](../design) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Media** | Describe las entidades principales del negocio y sus relaciones. |
| **CI-004** | [Casos de uso]() | `.xlsx` | Documentación | 1.0.0 | [`/docs/specifications`](../specifications) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Media** | Define el alcance funcional del sistema. |
| **CI-005** | [Atributos de calidad]() | `.xlsx` | Documentación | 1.0.0 | [`/docs/specifications`](../specifications) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Documento de soporte al diseño y validación de la arquitectura. |
| **CI-006** | [Documento de desarrollo de contenidos]() | `.docx` | Documentación | 1.0.0 | [`/resources`](../resources) | [@caupolicanre](https://github.com/caupolicanre) | **Baja** | Permite rastrear decisiones previas tomadas en el desarrollo. |

---

## Notas

- Todos los archivos identificados como **CIs** son controlados bajo versionado en Git.
- Las rutas son relativas al repositorio raíz.
- El nombre de cada **CI** en la columna **Archivo** incluye un hipervínculo directo al archivo correspondiente en la estructura del repositorio.
- Los formatos indicados corresponden a la versión actual de cada activo.
