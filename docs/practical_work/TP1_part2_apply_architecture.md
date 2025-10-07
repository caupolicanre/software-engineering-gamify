## Ingeniería de Software II
## Trabajo Práctico 1 Parte 2: Aplicación de la arquitectura al proyecto

`Carrera:` Licenciatura en Ciencia de Datos

`Cátedra:` Ingeniería de Software II

`Docentes:` Valotto, Victor; Godoy, Cielo

`Alumnos:` Carrozzo, Felipe; Ré, Lautaro Caupolicán

`Año:` 2025

**Desarrollo**

**1. Atributos de calidad y escenarios**

- Identificar al menos dos atributos de calidad críticos para su sistema.
- Repasar el escenario de calidad por cada atributo, especificando estímulo, respuesta y medida de la respuesta.

| **Atributo de calidad** | **Escenario** | **Estímulo** | **Respuesta** | **Medida de respuesta** |
|---------------------------|---------------|---------------|----------------|--------------------------|
| **Escalabilidad** | Si el número de usuarios activos se duplica durante un evento especial, el sistema debe seguir funcionando sin degradación significativa en los tiempos de respuesta. | Duplicación de usuarios activos | Procesa cada solicitud con un retardo de 3 segundos como máximo | Tiempo de respuesta ≤ 3 segundos para el 95% de las peticiones globales. |
| **Disponibilidad** | El sistema debe estar disponible al menos el 99.5% del tiempo mensual, permitiendo a los usuarios acceder a su información y registrar tareas en cualquier momento del día, incluyendo fines de semana. | Un usuario ingresa en cualquier momento del día | El sistema permite el acceso, visualización de información y registro de tareas sin errores en al menos el 99.5% mensualmente. | Tiempo total de inactividad mensual menor a 4 horas. |

**2. Vistas de arquitectura**

- Documentar la arquitectura de su proyecto usando el modelo de vistas C4.
- Incluir los diagramas correspondientes al modelo.

**3. Aspectos transversales**

- Identificar qué aspectos transversales deben incluirse en su proyecto (ej. autenticación, gestión de excepciones, interoperabilidad, notificaciones)
- Explicar en qué parte de la arquitectura impactan más y por qué. 

*Autenticación:* Se ubica principalmente en la capa de presentación (control de acceso a la aplicación) y en la capa de servicios/backend. También influye en la capa de datos, ya que es necesario proteger información sensible asociada al usuario.

*Gestión de excepciones:* Afecta principalmente a la capa de servicios/backend, donde se concentran la lógica de negocio y la interacción con datos externos. También se refleja en la infraestructura, ya que los logs se utilizan en el monitoreo del sistema.

*Interoperabilidad:* Recae principalmente en la capa de servicios/API, esta define cómo los diferentes clientes consumen la información. También influye en la infraestructura, cuando se consideran integraciones futuras con servicios externos.

*Mailing y notificaciones:* Se implementa en la capa de servicios, como un módulo de comunicación externa. Requiere coordinación con la infraestructura, ya que depende de proveedores externos.
