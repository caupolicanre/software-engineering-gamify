# Trabajo Práctico 3: Diagrama de clase y diagrama de despliegue

`Carrera:` Licenciatura en Ciencia de Datos

`Cátedra:` Ingeniería de Software II

`Docentes:` Valotto, Victor; Godoy, Cielo

`Alumnos:` Carrozzo, Felipe; Ré, Lautaro Caupolicán

`Año:` 2025

---

# Desarrollo

## 1. Ejercicio de análisis

> Explicar qué comunica cada uno de estos diagramas y qué diferencia hay entre ellos.

  - *Diagrama de clases:* muestra la estructura estática del sistema. Es decir, cómo está organizado el código: qué clases existen, qué atributos y métodos tienen, y cómo se relacionan entre sí (asociaciones, herencias, dependencias, composiciones, etc.). Sirve para:

    - Definir la **arquitectura lógica** del sistema.
    - Modelar las entidades principales (por ejemplo, Usuario, Tarea, Perfil, GestorDeUsuarios, etc.).
    - Mostrar la **relación entre las clases** (quién usa a quién, quién contiene a quién, etc.).
    - **Facilitar la implementación** en código orientado a objetos.

  - *Diagrama de despliegue:* muestra la estructura física del sistema, representando dónde se ejecutan los componentes (por ejemplo, en un servidor web, en una base de datos, en el celular del usuario, etc.) y cómo se comunican entre esos nodos. Sirve para:

    - Mostrar los **nodos físicos** (servidores, dispositivos móviles, PCs, etc.).
    - Indicar **qué componentes** o aplicaciones **se ejecutan** en cada nodo.
    - Describir las **conexiones de red** entre ellos (por ejemplo, HTTP, API REST, conexión a base de datos).
    - Planificar la **infraestructura de despliegue** (útil en DevOps, testing y mantenimiento).

> Justificar por qué es importante mantener la trazabilidad entre C4 → Clases → Despliegue.

  - Mantener la trazabilidad entre los diagramas **C4**, de **clases** y de **despliegue** es fundamental para asegurar la coherencia entre la arquitectura conceptual, el diseño lógico y la implementación física del sistema. Esto permite verificar que cada componente definido se encuentre correctamente representado en el código y desplegado en la infraestructura, facilitando además el mantenimiento y la gestión de cambios.
