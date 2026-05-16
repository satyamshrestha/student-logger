from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_signup_login_and_me():
    # signup_response = client.post(
    #     "/api/v1/auth/signup",
    #     json={
    #         "username": "testuser",
    #         "password": "1234"
    #     }
    # )

    # assert signup_response.status_code == 200

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

    assert data["username"] == "satyam"

    # create_response = client.post(
    #     "/api/v1/students",
    #     headers={
    #         "Authorization": f"Bearer {token}"
    #     },
    #     json={
    #         "student_id": "3",
    #         "name": "Deepson",
    #         "age": 19
    #     }
    # )
    # assert create_response.status_code == 200