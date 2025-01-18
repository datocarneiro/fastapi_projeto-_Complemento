import json
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

def obter_token(client):
    """Função auxiliar para autenticação e obtenção do token."""
    login_data = {"username": os.getenv("ADMIN_USERNAME"), "password": os.getenv("ADMIN_PASSWORD")}
    login_response = client.post("/auth", json=login_data)
    assert login_response.status_code == 200
    return login_response.json()["access_token"]

def test_criar_tarefa(test_client):
    token = obter_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}

    tarefa_data = {"titulo": "Teste de Tarefa", "descricao": "Descrição da tarefa de teste", "status": "pendente", "nivel_prioridade": "baixo"}
    response = test_client.post("/tarefa", json=tarefa_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['data'][0]["titulo"] == "Teste de Tarefa"
    assert data['data'][0]["descricao"] == "Descrição da tarefa de teste"
    assert data['data'][0]["status"] == "pendente"
    assert data['data'][0]["nivel_prioridade"] == "baixo"


def test_obter_tarefas(test_client):
    token = obter_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}

    response = test_client.get("/tarefas", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    if data:  # Se houver tarefas, verificar a estrutura
        assert "titulo" in data[0]
        assert "descricao" in data[0]

def test_atualizar_tarefa(test_client):
    # Obter token de autenticação
    token = obter_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}

    # Criar uma tarefa para atualizar
    tarefa_data = {
        "titulo": "Titulo inicial",
        "descricao": "Descrição inicial",
        "status": "pendente",
        "nivel_prioridade": "baixo"
    }
    create_response = test_client.post("/tarefa", json=tarefa_data, headers=headers)
    assert create_response.status_code == 200
    tarefa_id = create_response.json()["data"][0]["id"]

    tarefa_update_data = {
        "id": tarefa_id,
        "status": "concluída",  
        "nivel_prioridade": "alto", 
        "titulo": "Titulo Atualizado",
        "descricao": "Descrição atualizada"
    }
    update_response = test_client.put("/tarefa", json=tarefa_update_data, headers=headers)
    
    assert update_response.status_code == 200
    data = update_response.json()["data"][0]
    assert data["id"] == tarefa_id
    assert data["status"] == "concluída"
    assert data["nivel_prioridade"] == "alto"
    assert data["titulo"] == "Titulo Atualizado"
    assert data["descricao"] == "Descrição atualizada"


def test_deletar_tarefa(test_client):
    # Obter token de autenticação
    token = obter_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}

    # Criar uma tarefa para deletar
    tarefa_data = {
        "titulo": "Tarefa para Deletar",
        "descricao": "Descrição para deletar",
        "status": "pendente",
        "nivel_prioridade": "baixo"
    }
    create_response = test_client.post("/tarefa", json=tarefa_data, headers=headers)
    assert create_response.status_code == 200
    tarefa_id = create_response.json()["data"][0]["id"]

    # Deletar a tarefa (enviando o corpo da requisição como JSON)
    delete_response = test_client.request(
        "DELETE",  # Usar o método request permite enviar JSON no corpo de uma requisição DELETE
        "/tarefa",
        json={"id": tarefa_id},
        headers=headers
    )
    assert delete_response.status_code == 200

    # Verificar a resposta
    data = delete_response.json() == {"message": f'Tarefa ID: {tarefa_id} deletada com sucesso. Informações da terefa excluída:',"data":[tarefa_data]}
