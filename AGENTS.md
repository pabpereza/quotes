# Contexto y Reglas del Proyecto: API de Citas Célebres

Este documento define la arquitectura, el estilo de código y las directrices técnicas para el desarrollo de la API REST de "Citas Célebres". **Como agente de IA, debes leer y seguir estas reglas estrictamente antes de generar cualquier código.**

## 1. Stack Tecnológico
- **Lenguaje:** Python 3.11+
- **Framework:** FastAPI
- **Servidor:** Uvicorn
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validación:** Pydantic V2
- **Gestión de Paquetes:** `pip` (standard requirements.txt)
- **Tests:** Pytest

## 2. Arquitectura del Proyecto
La estructura de carpetas es estricta. No crees archivos fuera de su lugar correspondiente.

```text
/
├── app/
│   ├── main.py            # Entry point. Configuración de FastAPI e inclusión de routers.
│   ├── controllers/       # Lógica de negocio agrupada por recursos.
│   │   ├── __init__.py
│   │   ├── auth.py        # Controlador para autenticación.
│   │   ├── quote.py       # Controlador para citas.
│   │   └── user.py        # Controlador para usuarios.
│   ├── db/                # Modelos de la base de datos (SQLAlchemy).
│   │   ├── __init__.py
│   │   ├── quote.py
│   │   └── user.py
│   ├── misc/              # Archivos misceláneos (base de datos, seguridad, hashing).
│   │   ├── __init__.py
│   │   ├── database.py    # Configuración de la conexión a la base de datos y sesión.
│   │   ├── hashing.py     # Funciones de hashing de contraseñas.
│   │   └── security.py    # Lógica de autenticación y seguridad (JWT, dependencias).
│   ├── models/            # Modelos de datos de la API (Pydantic schemas).
│   │   ├── __init__.py
│   │   ├── quote.py
│   │   ├── token.py
│   │   └── user.py
│   ├── routers/           # Lógica de endpoints (Path Operations).
│   │   ├── __init__.py
│   │   ├── auth.py        # Endpoints para autenticación.
│   │   ├── probes.py      # Endpoints para health checks.
│   │   ├── quote.py       # Endpoints para /quotes.
│   │   └── user.py        # Endpoints para /users.
│   └── test/              # Tests unitarios y de integración.
│       ├── __init__.py
│       ├── conftest.py    # Configuraciones y fixtures para Pytest.
│       ├── test_auth.py
│       ├── test_main.py
│       ├── test_quotes.py
│       └── test_users.py
├── .gemini/GEMINI.md      # Este archivo de reglas.
├── compose.yml            # Configuración de Docker Compose.
└── requirements.txt       # Dependencias del proyecto.
```

## 3. Convenciones de Código

### General
- **Idioma del Código:** Variables, funciones y clases en **Inglés** (ej: `get_quotes`, `QuoteModel`).
- **Idioma de Comentarios:** Español o Inglés (mantener consistencia).
- **Type Hinting:** **Obligatorio**. Todo argumento y retorno de función debe estar tipado.

### Separación de Modelos
- **`app/models` (Pydantic):** Define la forma de los datos en la API. Se usan para validación de requests, serialización de responses y documentación OpenAPI.
- **`app/db` (SQLAlchemy):** Define la estructura de las tablas en la base de datos. Se usan para las operaciones con el ORM.
- Esta separación es intencionada para desacoplar la capa de API de la capa de datos.

### Capa de Controladores (`app/controllers`)
- Contiene la lógica de negocio principal para cada recurso.
- Las funciones de los controladores interactúan directamente con la base de datos (SQLAlchemy) y con otras capas como la de seguridad/hashing.
- Reciben los datos de los routers (ya validados por Pydantic) y devuelven los resultados.
- Son responsables de aplicar reglas de negocio y de lanzar excepciones HTTP si es necesario.

### FastAPI & Routers (`app/routers`)
- **Modularidad:** Usar siempre `APIRouter`.
- Los routers deben ser "delgados": su única responsabilidad es definir las rutas, validar los datos de entrada con Pydantic y llamar al método apropiado del controlador.
- **Inyección de Dependencias:** Usar `Depends()` para obtener la sesión de la base de datos (`get_db`) y para la autenticación (`get_current_user`).

## 4. Ejemplos de Implementación Esperada

### Modelo Pydantic (`app/models/quote.py`)
```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class QuoteBase(BaseModel):
    text: str = Field(..., title="Texto de la cita", min_length=10)
    author: str = Field(..., title="Autor", min_length=3)
    category: Optional[str] = "General"

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
```

### Modelo SQLAlchemy (`app/db/quote.py`)
```python
from sqlalchemy import Column, Integer, String
from ..misc.database import Base # Importar desde misc

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    author = Column(String)
    category = Column(String, default="General")
```

### Controlador (`app/controllers/user.py`)
```python
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import user as user_model
from ..db import user as user_db
from ..misc.hashing import get_password_hash # Importar desde misc

class UserController:
    def _get_user_by_email(self, db: Session, email: str):
        return db.query(user_db.User).filter(user_db.User.email == email).first()

    def create_user(self, db: Session, user: user_model.UserCreate):
        db_user = self._get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        db_user = user_db.User(email=user.email, username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_controller = UserController()
```

### Router (`app/routers/quotes.py`)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models import quote as quote_model
from ..misc.database import get_db # Importar desde misc
from ..misc.security import get_current_user # Importar desde misc
from ..models.user import User as UserModel
from ..controllers.quote import quote_controller

router = APIRouter(prefix="/quotes", tags=["Quotes"])

@router.get("/", response_model=List[quote_model.Quote])
async def read_quotes(db: Session = Depends(get_db)):
    return quote_controller.read_quotes(db=db)

@router.post("/", response_model=quote_model.Quote, status_code=201)
async def create_quote(
    quote: quote_model.QuoteCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    return quote_controller.create_quote(db=db, quote=quote)
```

## 5. Ejecución de Tests
Los tests se ejecutan dentro de un contenedor Docker para asegurar un ambiente consistente.

Para ejecutar todos los tests:
```bash
docker-compose run test
```

Para ejecutar tests localmente (sin Docker):
```bash
python -m pytest app/test/ -v
```

## 6. Configuración de Base de Datos

### Detección Automática
La aplicación detecta automáticamente qué base de datos usar:
- **PostgreSQL**: Si la variable de entorno `POSTGRES_HOST` está configurada.
- **SQLite**: Si no hay configuración de PostgreSQL (modo desarrollo local).

### Variables de Entorno para PostgreSQL
```bash
POSTGRES_HOST=localhost      # Host de PostgreSQL
POSTGRES_USER=postgres       # Usuario
POSTGRES_PASSWORD=postgres   # Contraseña
POSTGRES_DB=quotes           # Nombre de la base de datos
```

### Carga Automática de Datos de Prueba
Al arrancar la aplicación:
1. Se crean las tablas automáticamente si no existen.
2. Si la base de datos está vacía, se cargan **15 citas célebres de ejemplo**.
3. Se crea un **usuario admin** con credenciales:
   - Usuario: `admin`
   - Password: `admin123`

## 7. Endpoints de la API

### Citas (`/quotes`)
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/quotes` | Devuelve una cita aleatoria | No |
| GET | `/quotes/all` | Devuelve todas las citas (paginación: `skip`, `limit`) | No |
| POST | `/quotes` | Crea una nueva cita | Sí |

### Usuarios (`/users`)
| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/users/` | Lista todos los usuarios | No |
| GET | `/users/{id}` | Obtiene un usuario por ID | No |
| POST | `/users/` | Crea un nuevo usuario | No |
| PUT | `/users/{id}` | Actualiza un usuario | Sí |
| DELETE | `/users/{id}` | Elimina un usuario | Sí |

### Autenticación (`/token`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/token` | Obtiene un token JWT (OAuth2 password flow) |

### Health Checks (`/probes`)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/probes/startup` | Verifica que el servicio ha arrancado |
| GET | `/probes/health` | Verifica que el servicio está funcionando |
| GET | `/probes/ready` | Verifica que el servicio está listo para recibir peticiones |

## 8. Instrucciones de Comportamiento para el Agente
1.  Al añadir una nueva entidad, crea o modifica los modelos en `app/models` (Pydantic) y `app/db` (SQLAlchemy).
2.  Implementa la lógica de negocio en un controlador dedicado en `app/controllers`. Las funciones CRUD deben estar integradas en el controlador o ser métodos privados del mismo.
3.  Implementa los endpoints en un router dedicado en `app/routers`, el cual solo debe llamar a los métodos del controlador.
4.  Si el endpoint modifica datos o requiere información del usuario, protégelo con la dependencia de autenticación (`get_current_user`).
5.  Registra el nuevo router en `app/main.py`.
6.  Asegúrate de que los tests cubran la nueva funcionalidad.
7.  Mantén los ficheros de configuración (`app/misc/database.py`, `app/misc/security.py`, `app/misc/hashing.py`) y sus importaciones correctos.
8.  Para desarrollo local, no es necesario configurar PostgreSQL; la aplicación usará SQLite automáticamente.
