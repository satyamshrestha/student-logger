from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_signup_login_and_me():
    print(app.routes)
    signup_response = client.post(
        "/api/v1/auth/signup",
        json={
            "username": "testuser",
            "password": "1234"
        }
    )

    assert signup_response.status_code == 200

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "1234"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["username"] == "testuser"
    print(signup_response.status_code, signup_response.json())
    print(login_response.status_code, login_response.json())
    print(me_response.status_code, me_response.text)