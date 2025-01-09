import pytest
from fastapi.testclient import TestClient
from app.main import app

# Criar o cliente de teste
@pytest.fixture
def client():
    client = TestClient(app)

    # Realizar login para obter o token
    login_data = {"username": "admin", "password": "admin123"}
    response = client.post("/auth", json=login_data)
    assert response.status_code == 200

    # Extrair o token
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})

    return client
