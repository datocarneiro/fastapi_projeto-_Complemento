import pytest
from app.models import TarefaCreate

# Testar o endpoint para criar uma tarefa
def test_criar_tarefa(client):
    tarefa = {
        "titulo": "Dato teste 1",
        "descricao": "Testando Criação de tarefa ",
        "status": "pendente"
    }
    response = client.post("/tarefas/", json=tarefa)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == tarefa["titulo"]
    assert data["descricao"] == tarefa["descricao"]
    assert data["status"] == tarefa["status"]

# Testar o endpoint para listar tarefas
def test_listar_tarefas(client):
    response = client.get("/tarefas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Testar o endpoint para buscar tarefa por ID
def test_buscar_tarefa_por_id(client):
    # Primeiro, cria uma nova tarefa
    nova_tarefa = {
        "titulo": "Teste Tarefa por ID",
        "descricao": "Teste buscando Tarefa por ID",
        "status": "pendente"
    }
    response = client.post("/tarefas/", json=nova_tarefa)
    assert response.status_code == 200
    tarefa_id = response.json()["id"]

    # Busca a tarefa criada pelo ID
    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    assert response.json()["id"] == tarefa_id

# Testar a atualização de uma tarefa
def test_atualizar_tarefa(client):
    # Criar tarefa para ser atualizada
    tarefa = {
        "titulo": "Teste atualizar Tarefa",
        "descricao": "Teste atualizando uma Tarefa",
        "status": "pendente"
    }
    response = client.post("/tarefas/", json=tarefa)
    assert response.status_code == 200
    tarefa_id = response.json()["id"]

    # Atualizar a tarefa
    nova_info = {"status": "em andamento"}
    response = client.put(f"/tarefas/{tarefa_id}", json=nova_info)
    assert response.status_code == 200
    assert response.json()["status"] == nova_info["status"]

# Testar a exclusão de uma tarefa
def test_deletar_tarefa(client):
    # Criar tarefa para ser deletada
    tarefa = {
        "titulo": "Tarefa Deletar Tarefa",
        "descricao": "Teste deletando uma tarefa",
        "status": "pendente"
    }
    response = client.post("/tarefas/", json=tarefa)
    assert response.status_code == 200
    tarefa_id = response.json()["id"]

    # Deletar a tarefa
    response = client.delete(f"/tarefas/{tarefa_id}")
    assert response.status_code == 200
    assert response.json()["msg"] == f"Tarefa com ID:{tarefa_id} deletada com sucesso!"

    # Verificar se a tarefa foi removida
    response = client.get(f"/tarefas/{tarefa_id}")
    assert response.status_code == 404
