import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.conn_database import Base, engine
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Criar uma sessão de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)  # Criar tabelas para teste
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)  # Dropar tabelas após os testes

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
