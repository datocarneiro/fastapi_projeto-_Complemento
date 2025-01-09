

def test_login(client):
    # Realizar login com usuário fictício
    login_data = {"username": "admin", "password": "senha_errada"}
    response = client.post("/auth", json=login_data)
    assert response.status_code == 401

    # Tente login com credenciais corretas
    login_data = {"username": "admin", "password": "admin123"}
    response = client.post("/auth", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

