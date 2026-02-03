#!/usr/bin/env python3
"""
Script para poblar la base de datos con citas célebres de ejemplo.

Uso:
    python -m app.seed

Este script crea un usuario admin y varias citas célebres de ejemplo.
"""
import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.misc.database import SessionLocal, engine, Base
from app.db.user import User
from app.db.quote import Quote
from app.misc.hashing import get_password_hash


# Citas célebres de ejemplo
SAMPLE_QUOTES = [
    {
        "text": "La vida es lo que pasa mientras estás ocupado haciendo otros planes.",
        "author": "John Lennon",
        "category": "Vida"
    },
    {
        "text": "El único modo de hacer un gran trabajo es amar lo que haces.",
        "author": "Steve Jobs",
        "category": "Trabajo"
    },
    {
        "text": "Sé el cambio que quieres ver en el mundo.",
        "author": "Mahatma Gandhi",
        "category": "Inspiración"
    },
    {
        "text": "La imaginación es más importante que el conocimiento.",
        "author": "Albert Einstein",
        "category": "Ciencia"
    },
    {
        "text": "El éxito no es definitivo, el fracaso no es fatal: lo que cuenta es el coraje para continuar.",
        "author": "Winston Churchill",
        "category": "Éxito"
    },
    {
        "text": "La felicidad no es algo hecho. Proviene de tus propias acciones.",
        "author": "Dalai Lama",
        "category": "Felicidad"
    },
    {
        "text": "No he fracasado. He encontrado 10.000 maneras que no funcionan.",
        "author": "Thomas Edison",
        "category": "Perseverancia"
    },
    {
        "text": "Vivir es la cosa más rara del mundo. La mayoría de la gente solo existe.",
        "author": "Oscar Wilde",
        "category": "Vida"
    },
    {
        "text": "El conocimiento habla, pero la sabiduría escucha.",
        "author": "Jimi Hendrix",
        "category": "Sabiduría"
    },
    {
        "text": "La mejor manera de predecir el futuro es crearlo.",
        "author": "Peter Drucker",
        "category": "Futuro"
    },
    {
        "text": "No cuentes los días, haz que los días cuenten.",
        "author": "Muhammad Ali",
        "category": "Motivación"
    },
    {
        "text": "La creatividad es la inteligencia divirtiéndose.",
        "author": "Albert Einstein",
        "category": "Creatividad"
    },
    {
        "text": "El que tiene un porqué para vivir puede soportar casi cualquier cómo.",
        "author": "Friedrich Nietzsche",
        "category": "Filosofía"
    },
    {
        "text": "Piensa en grande, empieza pequeño, actúa ahora.",
        "author": "Robin Sharma",
        "category": "Acción"
    },
    {
        "text": "La única forma de hacer un buen trabajo es amar lo que haces.",
        "author": "Steve Jobs",
        "category": "Trabajo"
    }
]


def seed_database():
    """Puebla la base de datos con datos de ejemplo."""
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el usuario admin
        existing_user = db.query(User).filter(User.username == "admin").first()
        
        if not existing_user:
            # Crear usuario admin
            admin_user = User(
                username="admin",
                email="admin@quotes.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✓ Usuario 'admin' creado (password: admin123)")
        else:
            print("→ Usuario 'admin' ya existe")
        
        # Verificar cuántas citas existen
        existing_quotes_count = db.query(Quote).count()
        
        if existing_quotes_count == 0:
            # Insertar citas de ejemplo
            for quote_data in SAMPLE_QUOTES:
                quote = Quote(
                    text=quote_data["text"],
                    author=quote_data["author"],
                    category=quote_data["category"]
                )
                db.add(quote)
            
            db.commit()
            print(f"✓ {len(SAMPLE_QUOTES)} citas célebres insertadas")
        else:
            print(f"→ Ya existen {existing_quotes_count} citas en la base de datos")
        
        print("\n¡Base de datos poblada exitosamente!")
        print("\nCredenciales de acceso:")
        print("  Usuario: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
