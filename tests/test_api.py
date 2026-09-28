from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_empty_question():

    response = client.post(
        "/qa",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


def test_empty_explanation():

    response = client.post(
        "/explain",
        json={
            "text": ""
        }
    )

    assert response.status_code == 422


def test_empty_quiz():

    response = client.post(
        "/quiz",
        json={
            "text": ""
        }
    )

    assert response.status_code == 422


def test_empty_summary():

    response = client.post(
        "/summarize",
        json={
            "text": ""
        }
    )

    assert response.status_code == 422


def test_empty_learning_path():

    response = client.post(
        "/learn/recommendations",
        json={
            "topic": ""
        }
    )

    assert response.status_code == 422