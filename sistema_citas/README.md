# 🏥 Sistema de Gestión de Citas — FastAPI

## Estructura del proyecto

```
sistema_citas/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py      # Conexión SQLAlchemy + get_db
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # Modelos ORM (tablas)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py         # Esquemas Pydantic (validación)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── especialidad.py
│   │   ├── medico.py
│   │   ├── paciente.py
│   │   ├── consultorio.py
│   │   └── cita.py
│   ├── __init__.py
│   └── main.py                # Entry point
├── .env.example
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.11+
- PostgreSQL corriendo localmente (o en Docker)

## Instalación

```bash
# 1. Clonar o copiar el proyecto
cd sistema_citas

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

## Configuración de base de datos

Edita el archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/sistema_citas
```

> Asegúrate de que la base de datos `sistema_citas` exista y que hayas ejecutado el DDL antes de arrancar.

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

El servidor arranca en: **http://localhost:8000**

## Documentación interactiva

| URL | Descripción |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (recomendado) |
| http://localhost:8000/redoc | ReDoc |

## Endpoints disponibles

### Especialidades `/especialidades`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/especialidades/` | Listar todas |
| GET | `/especialidades/{id}` | Obtener una |
| POST | `/especialidades/` | Crear |
| PUT | `/especialidades/{id}` | Actualizar |
| DELETE | `/especialidades/{id}` | Eliminar |

### Médicos `/medicos`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/medicos/` | Listar todos |
| GET | `/medicos/{id}` | Obtener uno |
| POST | `/medicos/` | Crear |
| PUT | `/medicos/{id}` | Actualizar |
| DELETE | `/medicos/{id}` | Eliminar |

### Pacientes `/pacientes`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/pacientes/` | Listar todos |
| GET | `/pacientes/{cedula}` | Obtener uno por cédula |
| POST | `/pacientes/` | Crear |
| PUT | `/pacientes/{cedula}` | Actualizar |
| DELETE | `/pacientes/{cedula}` | Eliminar |

### Consultorios `/consultorios`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/consultorios/` | Listar todos |
| GET | `/consultorios/{id}` | Obtener uno |
| POST | `/consultorios/` | Crear |
| PUT | `/consultorios/{id}` | Actualizar |
| DELETE | `/consultorios/{id}` | Eliminar |

### Citas `/citas`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/citas/` | Listar todas |
| GET | `/citas/{id}` | Obtener una |
| POST | `/citas/` | Crear |
| PUT | `/citas/{id}` | Actualizar |
| DELETE | `/citas/{id}` | Eliminar |

## Estados válidos para una cita

- `pendiente`
- `confirmada`
- `cancelada`
- `completada`
