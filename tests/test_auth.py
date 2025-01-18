import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.conn_database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from app.auth import create_access_token
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

def test_login_sucesso(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    response = test_client.post("/auth", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_falha(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": "senha_incorreta"}
    response = test_client.post("/auth", json=login_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Usuário ou senha inválidos"}

def test_rotea_autenticada(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    login_response = test_client.post("/auth", json=login_data)
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/tarefas", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Não há tarefas criadas", "data": []}