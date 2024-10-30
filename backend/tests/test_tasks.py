from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.task import Task


def test_create_task(client: TestClient):
    response = client.post(
        "/tasks/",
        json={
            "title": "Deadpond",
            "description": "Dive Wilson",
            "due_date": "2023-01-01T00:01:01",
        },
    )
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["title"] == "Deadpond"
    assert data["description"] == "Dive Wilson"
    assert data["due_date"] == "2023-01-01T00:01:01"
    assert data["id"] is not None


def test_create_task_incomplete(client: TestClient):
    # No title, title is needed
    response = client.post("/tasks/", json={"description": "Deadpond"})
    assert response.status_code == 422


def test_create_task_invalid(client: TestClient):
    # status has an invalid type
    response = client.post(
        "/tasks/",
        json={
            "title": "test",
            "description": "test",
            "status": "oxente",
        },
    )
    assert response.status_code == 422


def test_read_tasks(session: Session, client: TestClient):
    task_1 = Task(
        title="Deadpond", description="Dive Wilson", due_date="2023-01-01"
    )
    task_2 = Task(
        title="Rusty-Man",
        description="Tommy Sharp",
        due_date="2023-01-01",
        status="started",
    )
    session.add(task_1)
    session.add(task_2)
    session.commit()

    response = client.get("/tasks/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["title"] == task_1.title
    assert data[0]["description"] == task_1.description
    assert data[0]["id"] == task_1.id
    assert data[1]["title"] == task_2.title
    assert data[1]["description"] == task_2.description
    assert data[1]["id"] == task_2.id


def test_read_task(session: Session, client: TestClient):
    task_1 = Task(
        title="Deadpond", description="Dive Wilson", due_date="2023-01-01"
    )
    session.add(task_1)
    session.commit()

    response = client.get(f"/tasks/{task_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == task_1.title
    assert data["description"] == task_1.description


def test_update_task(session: Session, client: TestClient):
    task_1 = Task(
        title="Deadpond", description="Dive Wilson", due_date="2023-01-01"
    )
    session.add(task_1)
    session.commit()

    response = client.patch(
        f"/tasks/{task_1.id}", json={"title": "Deadpuddle"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Deadpuddle"
    assert data["description"] == "Dive Wilson"
    assert data["id"] == task_1.id


def test_delete_task(session: Session, client: TestClient):
    task_1 = Task(
        title="Deadpond", description="Dive Wilson", due_date="2023-01-01"
    )
    session.add(task_1)
    session.commit()

    response = client.delete(f"/tasks/{task_1.id}")

    task_in_db = session.get(Task, task_1.id)

    assert response.status_code == 200

    assert task_in_db.status == "deleted"
