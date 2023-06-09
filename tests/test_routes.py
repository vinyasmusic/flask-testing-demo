from app.models.user import User


def test_create_user(client, app):
    # Ensure we can create a new user
    response = client.post(
        "/users/user",
        json={"name": "Anakin", "email": "darth@deathstar.com", "password": "StormTr00per"},
    )
    assert response.status_code == 201
    data = response.json
    assert "darth@deathstar.com" == data["email"]

    # Ensure the user is in the database
    user = User.query.filter_by(email="darth@deathstar.com").first()
    assert user is not None
    assert user.name == "Anakin"
    assert user.password != "password"  # Password should be hashed


def test_get_user(client, app, user):
    # Ensure we can retrieve a user by id
    response = client.get(f"/users/{user.id}")

    assert response.status_code == 200
    data = response.json
    assert data["name"] == "Darth Vader"
    assert data["email"] == "darth@deathstar.com"
    assert "password" not in data  # Password should not be exposed


def test_update_user(client, app, user):
    # Ensure we can update a user's name and email
    response = client.put(
        f"/users/{user.id}", json={"name": "Skywalker", "email": "skywalker@midichlorian.com"}
    )
    assert response.status_code == 200
    data = response.json
    assert len(data.keys()) > 0

    # Ensure the user is updated in the database
    updated_user = User.query.filter_by(id=user.id).first()
    assert updated_user is not None
    assert updated_user.name == "Skywalker"
    assert updated_user.email == "skywalker@midichlorian.com"


def test_create_user_missing_fields(client):
    # Ensure we can't create a new user with missing fields
    response = client.post("/users/user", json={"name": "R2D2", "password": "c3P0@Tatooine"})
    assert response.status_code == 400
    data = response.json
    assert "required" in data["message"]


def test_delete_user(client, app, user):
    # Ensure we can delete a user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    # data = json.loads(response.data)
    # assert "User deleted successfully" in data["message"]
