import json

import pytest

from app.models.user import User


@pytest.mark.creation_test
def test_create_user(client, app):
    # Ensure we can create a new user
    response = client.post(
        "/users/user",
        json={"name": "John", "email": "john@example.com", "password": "password"},
    )
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "john@example.com" == data['email']

    # Ensure the user is in the database
    user = User.query.filter_by(email="john@example.com").first()
    assert user is not None
    assert user.name == "John"
    assert user.password != "password"  # Password should be hashed


def test_get_user(client, app, user):
    # Ensure we can retrieve a user by id
    response = client.get(f"/users/{user.id}")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "John"
    assert data["email"] == "john@example.com"
    assert "password" not in data  # Password should not be exposed


def test_update_user(client, app, user):
    # Ensure we can update a user's name and email
    response = client.put(
        f"/users/{user.id}", json={"name": "Jane", "email": "jane@example.com"}
    )
    data = json.loads(response.data)
    assert response.status_code == 200

    # Ensure the user is updated in the database
    updated_user = User.query.filter_by(id=user.id).first()
    assert updated_user is not None
    assert updated_user.name == "Jane"
    assert updated_user.email == "jane@example.com"


def test_create_user_missing_fields(client):
    # Ensure we can't create a new user with missing fields
    response = client.post("/users/user", json={"name": "John", "password": "password"})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "required" in data["message"]


def test_delete_user(client, app, user):
    # Ensure we can delete a user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    # data = json.loads(response.data)
    # assert "User deleted successfully" in data["message"]
