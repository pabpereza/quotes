import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def _get_database_url() -> tuple[str, dict]:
    """
    Determina la URL de la base de datos.
    Si POSTGRES_HOST está configurado, usa PostgreSQL.
    De lo contrario, usa SQLite automáticamente.
    """
    postgres_host = os.getenv("POSTGRES_HOST")
    
    if postgres_host:
        # PostgreSQL configurado
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        database = os.getenv("POSTGRES_DB", "quotes")
        url = f"postgresql://{user}:{password}@{postgres_host}/{database}"
        return url, {}
    else:
        # SQLite para desarrollo local (sin configuración de PostgreSQL)
        url = "sqlite:///./quotes.db"
        return url, {"check_same_thread": False}


SQLALCHEMY_DATABASE_URL, _connect_args = _get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=_connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
