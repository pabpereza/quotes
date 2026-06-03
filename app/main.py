from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .misc.database import engine, Base, SessionLocal
from .routers import quote, probes, user, auth
from .db.quote import Quote
from .db.user import User
from .misc.hashing import get_password_hash


# Citas célebres de ejemplo
SAMPLE_QUOTES = [
    {"text": "La vida es lo que pasa mientras estás ocupado haciendo otros planes.", "author": "John Lennon", "category": "Vida"},
    {"text": "El único modo de hacer un gran trabajo es amar lo que haces.", "author": "Steve Jobs", "category": "Trabajo"},
    {"text": "Sé el cambio que quieres ver en el mundo.", "author": "Mahatma Gandhi", "category": "Inspiración"},
    {"text": "La imaginación es más importante que el conocimiento.", "author": "Albert Einstein", "category": "Ciencia"},
    {"text": "El éxito no es definitivo, el fracaso no es fatal: lo que cuenta es el coraje para continuar.", "author": "Winston Churchill", "category": "Éxito"},
    {"text": "La felicidad no es algo hecho. Proviene de tus propias acciones.", "author": "Dalai Lama", "category": "Felicidad"},
    {"text": "No he fracasado. He encontrado 10.000 maneras que no funcionan.", "author": "Thomas Edison", "category": "Perseverancia"},
    {"text": "Vivir es la cosa más rara del mundo. La mayoría de la gente solo existe.", "author": "Oscar Wilde", "category": "Vida"},
    {"text": "El conocimiento habla, pero la sabiduría escucha.", "author": "Jimi Hendrix", "category": "Sabiduría"},
    {"text": "La mejor manera de predecir el futuro es crearlo.", "author": "Peter Drucker", "category": "Futuro"},
    {"text": "No cuentes los días, haz que los días cuenten.", "author": "Muhammad Ali", "category": "Motivación"},
    {"text": "La creatividad es la inteligencia divirtiéndose.", "author": "Albert Einstein", "category": "Creatividad"},
    {"text": "El que tiene un porqué para vivir puede soportar casi cualquier cómo.", "author": "Friedrich Nietzsche", "category": "Filosofía"},
    {"text": "Piensa en grande, empieza pequeño, actúa ahora.", "author": "Robin Sharma", "category": "Acción"},
    {"text": "La única forma de hacer un buen trabajo es amar lo que haces.", "author": "Steve Jobs", "category": "Trabajo"},
]


def load_sample_data():
    """Carga datos de prueba si la base de datos está vacía."""
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        if db.query(Quote).count() == 0:
            # Insertar citas de ejemplo
            for quote_data in SAMPLE_QUOTES:
                db.add(Quote(**quote_data))
            db.commit()
            print("✓ Datos de prueba cargados: 15 citas célebres")
        
        # Crear usuario admin si no existe
        if db.query(User).filter(User.username == "admin").first() is None:
            admin = User(
                username="admin",
                email="admin@quotes.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✓ Usuario admin creado (password: admin123)")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    load_sample_data()
    yield


app = FastAPI(
    title="API de Citas Célebres",
    description="Una API REST para gestionar citas célebres",
    version="1.0.0",
    default_response_class=JSONResponse,
    lifespan=lifespan
)

# Include routers
app.include_router(quote.router)
app.include_router(probes.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return JSONResponse(
        content={"message": "Bienvenido a la API de Citas Célebres"},
        media_type="application/json; charset=utf-8"
    )

