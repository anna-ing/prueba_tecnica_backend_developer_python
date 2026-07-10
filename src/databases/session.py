from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Variables globales que se pueden sobrescribir para testing
engine = None
SessionLocal = None


def init_db():
    """Inicializar la base de datos. Se llama automáticamente cuando es necesario."""
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )


def get_db():
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
