from fastapi.testclient import TestClient

from app.core.config import settings

def test_get_access_token_incorrect_email_password(client: TestClient) -> None:
    login_data = {
        "email": "john@doe.com",
        "password": "123"
    }

    r = client.post(f"{settings.API_V1}/auth/login", json=login_data)
    tokens = r.json()

    assert r.status_code == 400
    assert tokens["status"] == 'error'
    assert tokens["message"] == 'Invalid email or password!'