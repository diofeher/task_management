from fastapi.testclient import TestClient


def test_create_user_incomplete(client: TestClient):
    # No password, pwd is needed
    response = client.post("/users/", json={"username": "pikachu"})
    assert response.status_code == 422


def test_create_user_and_token(client: TestClient):
    response = client.post(
        "/users/", json={"username": "pikachu", "password": "ash"}
    )
    assert response.status_code == 200

    response = client.post(
        "/users/token", data={"username": "pikachu", "password": "ash"}
    )
    print(response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "pikachu"
    assert data["access_token"] is not None


def test_current_user(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert (
        response.json()["username"] == "rayquaza"
    )  # this name is related to test user
