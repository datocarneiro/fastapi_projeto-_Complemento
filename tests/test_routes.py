import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.conn_database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker
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

def test_obter_tarefas_vazio(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    login_response = test_client.post("/auth", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/tarefas", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Não há tarefas criadas", "data": []}

def test_criar_tarefa(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    login_response = test_client.post("/auth", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    tarefa_data = {"titulo": "Teste de Tarefa", "descricao": "Descrição da tarefa de teste", "status": "pendente", "nivel_prioridade": "baixo"}
    response = test_client.post("/tarefas", json=tarefa_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['data'][0]["titulo"] == "Teste de Tarefa"
    assert data['data'][0]["descricao"] == "Descrição da tarefa de teste"
    assert data['data'][0]["status"] == "pendente"
    assert data['data'][0]["nivel_prioridade"] == "baixo"

def test_obter_tarefas_nao_vazio(test_client):
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    login_response = test_client.post("/auth", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = test_client.get("/tarefas", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert data[0]["titulo"] == "Teste de Tarefa"
