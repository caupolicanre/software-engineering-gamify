# Módulo de Inventario

Este módulo centraliza el **inventario de activos (Configuration Items, CIs)** que forman parte del proyecto.

## Resumen
- **Total de CIs:** 19
- **Versión del inventario:** 2.3.0
- **Fecha de inventario:** 2025-11-04
- **Responsable:** Equipo Gamify ([Caupolicán Ré](https://github.com/caupolicanre) - [Felipe Carrozzo](https://github.com/felipecarrozzo))

---

## Tabla de activos

| ID | Nombre del CI | Formato | Categoría | Versión | Ubicación | Responsable | Criticidad | Justificación | Última Modificación |
|------|---------|---------|-----------|---------|-----------|-------------|------------|---------------|---------------------|
| **CI-001** | [Diagrama de dominio (fuente)](./design/diagrams/domain_diagram.drawio) | `.drawio` | Diseño | 1.0.0 | [`/docs/design/diagrams`](./design/diagrams/) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Describe las entidades principales del negocio y sus relaciones. | 2025-11-03 |
| **CI-002** | [Diagrama de dominio (imagen)](./design/diagrams/images/domain_diagram.png) | `.png` | Diseño | 1.0.0 | [`/docs/design/diagrams/images`](./design/diagrams/images/) | [@caupolicanre](https://github.com/caupolicanre) | **Media** | Exportación visual del diagrama de dominio. | 2025-11-03 |
| **CI-003** | [Diagrama de casos de uso (fuente)](./design/diagrams/use_cases_diagram.drawio) | `.drawio` | Diseño | 1.0.0 | [`/docs/design/diagrams`](./design/diagrams/) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Representa gráficamente la interacción entre actores y funcionalidades del sistema. | 2025-11-03 |
| **CI-004** | [Diagrama de casos de uso (imagen)](./design/diagrams/images/use_cases_diagram.png) | `.png` | Diseño | 1.0.0 | [`/docs/design/diagrams/images`](./design/diagrams/images/) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Media** | Exportación visual del diagrama de casos de uso. | 2025-11-03 |
| **CI-005** | [Diagrama de casos de uso foco (imagen)](./design/diagrams/images/use_cases_diagram_foco.png) | `.png` | Diseño | 1.0.0 | [`/docs/design/diagrams/images`](./design/diagrams/images/) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Media** | Vista focalizada del diagrama de casos de uso. | 2025-11-03 |
| **CI-006** | [Diagrama de secuencia (fuente)](./design/diagrams/sequence_diagram.drawio) | `.drawio` | Diseño | 1.0.0 | [`/docs/design/diagrams`](./design/diagrams/) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Detalla las interacciones temporales entre objetos del sistema. | 2025-11-03 |
| **CI-007** | [Diagrama de secuencia - Nuevo usuario](./design/diagrams/images/sequence_diagram_new_user.png) | `.png` | Diseño | 1.0.0 | [`/docs/design/diagrams/images`](./design/diagrams/images/) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Flujo de registro de nuevo usuario. | 2025-11-03 |
| **CI-008** | [Diagrama de secuencia - Completar tarea](./design/diagrams/images/sequence_diagram_complete_task.png) | `.png` | Diseño | 1.0.0 | [`/docs/design/diagrams/images`](./design/diagrams/images/) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Flujo de completación de tarea. | 2025-11-03 |
| **CI-009** | [Diagramas C4 (fuente)](./design/diagrams/c4/C4.drawio) | `.drawio` | Diseño | 1.0.0 | [`/docs/design/diagrams/c4`](./design/diagrams/c4/) | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Modelo de arquitectura C4 (Contexto, Contenedores, Componentes, Código). | 2025-11-03 |
| **CI-010** | [Casos de uso](./requirements/casos_uso.xlsx) | `.xlsx` | Documentación | 1.0.0 | [`/docs/requirements`](./requirements/) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Define el alcance funcional del sistema. | 2025-08-28 |
| **CI-011** | [Atributos de calidad](./requirements/atributos_calidad.xlsx) | `.xlsx` | Documentación | 1.0.0 | [`/docs/requirements`](./requirements/) | [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Documento de soporte al diseño y validación de la arquitectura. | 2025-08-28 |
| **CI-012** | [TP1 Parte 1: Arquitectura](./practical_work/TP1_part1_architecture.md) | `.md` | Documentación | 1.0.0 | [`/docs/practical_work`](./practical_work/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Trabajo práctico sobre conceptos de arquitectura de software. | 2025-11-03 |
| **CI-013** | [TP1 Parte 2: Aplicación arquitectura](./practical_work/TP1_part2_apply_architecture.md) | `.md` | Documentación | 1.0.0 | [`/docs/practical_work`](./practical_work/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Aplicación de arquitectura al proyecto, modelo C4 y aspectos transversales. | 2025-11-03 |
| **CI-014** | [TP2: Diagramas de secuencia](./practical_work/TP2_sequence_diagram.md) | `.md` | Documentación | 1.0.0 | [`/docs/practical_work`](./practical_work/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Trabajo práctico sobre diagramas de secuencia y casos de uso. | 2025-11-03 |
| **CI-015** | [TP3: Diagramas de clases y despliegue](./practical_work/TP3_class_deployment_diagrams.md) | `.md` | Documentación | 1.0.0 | [`/docs/practical_work`](./practical_work/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Diagramas de clases detallados, diagrama de despliegue y trazabilidad. | 2025-11-03 |
| **CI-016** | [TP4: Diseño de casos de prueba](./practical_work/TP4_test_cases_design.md) | `.md` | Documentación | 1.0.0 | [`/docs/practical_work`](./practical_work/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Diseño de casos de prueba basados en casos de uso, clases de equivalencia y valores límite. 192 tests implementados. | 2025-11-04 |
| **CI-017** | [Documentación de desarrollo de contenidos](./specifications/TP_final_IS_1.pdf) | `.pdf` | Documentación | 1.0.0 | [`/docs/specifications`](./specifications/) | [@caupolicanre](https://github.com/caupolicanre) | **Baja** | Permite rastrear recursos auxiliares del proyecto. | 2025-11-03 |
| **CI-018** | [Configuración del proyecto](../pyproject.toml) | `.toml` | Configuración | 1.0.0 | Raíz del proyecto | [@caupolicanre](https://github.com/caupolicanre) | **Alta** | Configuración de dependencias y herramientas del proyecto. | 2025-11-03 |
| **CI-019** | [Trabajo Práctico Final IS2](../resources/IS2_TP_Final.pdf) | `.pdf` | Documentación | 1.0.0 | [`/resources`](../resources/) | [@caupolicanre](https://github.com/caupolicanre) [@felipecarrozzo](https://github.com/felipecarrozzo) | **Alta** | Trabajo práctico final de Ingeniería de Software 2 con todas las entregas consolidadas. | 2025-11-04 |

---

## Estadísticas por Categoría
- **Diseño:** 9 CIs
- **Documentación:** 9 CIs
- **Configuración:** 1 CI

---

## Estadísticas por Criticidad
- **Criticidad Alta:** 15 CIs
- **Criticidad Media:** 3 CIs
- **Criticidad Baja:** 1 CI

---

## Información Adicional
- **Formatos de archivo:** `.drawio`, `.png`, `.xlsx`, `.pdf`, `.md`, `.toml`
- **Control de versiones:** Todos los CIs están bajo control de versiones con Git
- **Repositorio:** [github.com/caupolicanre/gamify](https://github.com/caupolicanre/gamify)

---

## Notas

- Todos los **nombres de CIs** en la columna "Nombre del CI" incluyen hipervínculos directos a los archivos correspondientes en el repositorio.
- Los formatos indicados corresponden a la versión actual de cada activo.
- Todos los archivos identificados como **CIs** son controlados bajo versionado en Git.
- Las rutas son relativas al directorio `docs/` salvo que se indique lo contrario.
- El inventario se enfoca en **artefactos de diseño y documentación** que definen la arquitectura y el alcance del sistema.
- El código fuente y las pruebas se gestionan de manera independiente en el directorio `src/`.
