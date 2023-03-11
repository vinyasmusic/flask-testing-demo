from app import app, db
from app.models import User
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, world!' in response.data

def test_get_users_empty(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert b'[]' in response.data

def test_get_users_one_user(client):
    user = User(name='Alice')
    db.session.add(user)
    db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert b'[{"id":1,"name":"Alice"}]' in response.data


def test_mock_external_api(client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'message': 'mocked response'}

        response = client.get('/external-api')
        assert response.status_code == 200
        assert b'mocked response' in response.data
        mock_get.assert_called_once_with('https://api.example.com')
        
