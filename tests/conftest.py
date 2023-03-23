import pytest
import requests

from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    user = User(name="Darth Vader", email="darth@deathstar.com", password="D@rKseID")
    db.session.add(user)
    db.session.commit()
    return user


# @pytest.fixture(autouse=True)
# def disable_network_calls(monkeypatch):
#     def block_get():
#         raise RuntimeError("Test should be inside a blackbox")
#
#     monkeypatch.setattr(requests, "get", lambda *args, **kwargs: block_get())
