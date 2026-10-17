# Sistema de Gestión y Reserva de Espacios Físicos - API REST

**Cátedra I - Introducción al Desarrollo Web / Móvil**  
*Universidad Católica del Norte - Departamento de Ingeniería de Sistemas y Computación*

---

## 1. Descripción del Proyecto
Este backend resuelve la problemática de gestión de reservas de espacios físicos dentro de una institución, eliminando los errores comunes asociados a la coordinación manual (reservas duplicadas, falta de historial y desconocimiento de la disponibilidad en tiempo real). 

Proporciona una **API REST** desarrollada con **FastAPI**, **SQLAlchemy** y **Pydantic**, implementando separación de responsabilidades a través del **Repository Pattern** y una **Capa de Servicios** donde se ejecutan las reglas de negocio principales (como la prevención de solapamiento de horarios).

---

## 2. Requisitos Previos e Instalación

### Requisitos:
- Python 3.10 o superior.
- Git.

### Pasos de instalación:
1. Clonar o situarse en la raíz del repositorio:
   ```bash
   cd D:\Prueba1WM
   ```

2. Crear y activar el entorno virtual:
   ```bash
   # En PowerShell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Base de Datos y Migraciones (Alembic)

La estructura de la base de datos se gestiona con **Alembic**, permitiendo la evolución controlada del esquema sin pérdida de datos.

1. **Ejecutar las migraciones pendientes:**
   ```bash
   alembic upgrade head
   ```

2. **Historial de migraciones incluidas:**
   - `6e35895b32b6_creacion_inicial_tablas.py`: Creación inicial de las tablas `usuarios`, `espacios` y `reservas`.
   - `6608ebd63841_agregar_descripcion_a_espacios.py`: Modificación incremental que agrega el atributo opcional `descripcion` a la entidad `espacios`.

---

## 4. Carga de Datos Iniciales (Seed)

Para facilitar la evaluación y pruebas inmediatas, se incluye un script reproducible que carga automáticamente **5 usuarios, 10 espacios y 15 reservas** no solapadas:

```bash
python seed.py
```

---

## 5. Ejecución del Proyecto

Para iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

- Servidor disponible en: `http://127.0.0.1:8000`
- **Documentación Interactiva Swagger (OpenAPI):** `http://127.0.0.1:8000/docs`


---

## 6. Arquitectura del Software

El proyecto sigue una arquitectura en capas basada en **Clean Architecture**, dividida en los siguientes conceptos:

- **Router (`app/routers/`):** Controladores HTTP responsables de recibir las peticiones, validar parámetros con FastAPI, llamar a la capa de servicio y devolver códigos de estado HTTP apropiados (`200`, `201`, `204`, etc.). No realizan consultas directas a la base de datos.
- **Service (`app/services/`):** Contiene la lógica de negocio y las validaciones de dominio (por ejemplo, comprobar que la hora de inicio sea menor a la de fin y validar que no exista superposición de horarios entre reservas).
- **Repository (`app/repositories/`):** Capa encargada exclusivamente del acceso a datos y persistencia mediante consultas de SQLAlchemy.
- **DTO / Schemas (`app/schemas/`):** Modelos de Pydantic que definen la estructura y validaciones de entrada  y salida, asegurando que nunca se expongan directamente los modelos de persistencia.
- **Models (`app/models/`):** Entidades de base de datos declaradas con el estilo moderno de SQLAlchemy 2.0 (`Mapped` y `mapped_column`) con sus respectivas claves foráneas y relaciones bidireccionales.
- **Database (`app/database.py`):** Configuración del motor SQLite (`engine`), creador de sesiones (`SessionLocal`) y generador de dependencia (`get_db`).
- **Middleware (`app/middlewares/timing.py`):** Funcionalidad transversal que intercepta cada petición HTTP para calcular su tiempo exacto de procesamiento, registrando un log en consola y agregando la cabecera `X-Process-Time`.
- **Dependencies (`app/routers/`):** Funciones proveedoras de dependencias que utilizan el sistema `Depends` de FastAPI para instanciar repositorios y servicios inyectando la sesión activa de base de datos.
- **Endpoints:** Puntos de acceso expuestos bajo el protocolo HTTP siguiendo convenciones RESTful con sustantivos en plural (`/api/usuarios`, `/api/espacios`, `/api/reservas`).

---

## 7. Justificación de Principios SOLID

En el proyecto se aplican los siguientes principios SOLID:

1. **Principio de Responsabilidad Única:**
   - Se separó cada operación en capas: `routers/` solo atiende HTTP, `services/` solo procesa reglas de negocio y `repositories/` solo ejecuta operaciones SQL. Un cambio en la base de datos solo afecta al repositorio, no al router.
2. **Principio de Inversión de Dependencias:**
   - Los servicios y routers no crean conexiones directas a la base de datos por su cuenta, sino que reciben sus dependencias inyectadas desde afuera mediante el contenedor de dependencias de FastAPI (`Depends(get_db)` y `Depends(get_..._service)`).
3. **Principio Abierto/Cerrado:**
   - Los esquemas DTO de Pydantic extienden clases base (por ejemplo, `RespuestaEspacio(CrearEspacio)`), permitiendo agregar nuevos campos y respuestas sin modificar ni romper el comportamiento de los esquemas de entrada base.

---

## 8. Tabla de Endpoints de la API REST

### Usuarios (`/api/usuarios`)
| Método | Ruta | Descripción | Código Éxito |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/usuarios` | Listar usuarios con paginación (`?pagina=1&limite=10`) | `200 OK` |
| `GET` | `/api/usuarios/{id_usuario}` | Obtener el detalle de un usuario por su ID | `200 OK` |
| `POST` | `/api/usuarios` | Crear un nuevo usuario en el sistema | `201 Created` |
| `PUT` | `/api/usuarios/{id_usuario}` | Actualización completa de datos del usuario | `200 OK` |
| `DELETE` | `/api/usuarios/{id_usuario}` | Eliminar un usuario del sistema | `204 No Content` |

### Espacios (`/api/espacios`)
| Método | Ruta | Descripción | Código Éxito |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/espacios` | Listar espacios con paginación y filtros (`?capacidad=30&disponibilidad=true`) | `200 OK` |
| `GET` | `/api/espacios/{id_espacio}` | Obtener el detalle de un espacio específico | `200 OK` |
| `POST` | `/api/espacios` | Registrar un nuevo espacio físico | `201 Created` |
| `PUT` | `/api/espacios/{id_espacio}` | Actualizar atributos de un espacio | `200 OK` |
| `DELETE` | `/api/espacios/{id_espacio}` | Eliminar un espacio físico | `204 No Content` |

### Reservas (`/api/reservas`)
| Método | Ruta | Descripción | Código Éxito |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/reservas` | Consultar reservas con filtros (`usuario_id`, `espacio_id`, `fecha`, `estado`) y paginación | `200 OK` |
| `GET` | `/api/reservas/{id_reserva}` | Obtener detalle de una reserva por su ID | `200 OK` |
| `POST` | `/api/reservas` | Crear una reserva validando solapamiento de horario | `201 Created` |
| `PATCH` | `/api/reservas/{id_reserva}` | Actualización parcial de una reserva (fechas, horarios o estado) | `200 OK` |
| `DELETE` | `/api/reservas/{id_reserva}` | Cancelar/eliminar una reserva | `204 No Content` |
