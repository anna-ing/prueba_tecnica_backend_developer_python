import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Primero sobrescribimos la configuración antes de importar cualquier módulo de src
from src.core.config import settings
settings.DATABASE_URL = "sqlite:///./test.db"

from src.databases.base import Base
from src.databases.session import get_db
from src.main import app
import src.databases.session as session_module

# Configurar base de datos en memoria para pruebas
test_engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Sobrescribir las variables globales en el módulo session
session_module.engine = test_engine
session_module.SessionLocal = TestingSessionLocal


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    # Crear tablas antes de cada test
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as c:
        yield c
    # Eliminar tablas después de cada test
    Base.metadata.drop_all(bind=test_engine)
