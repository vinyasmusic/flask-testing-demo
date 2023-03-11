# Flask Testing Demo

A demo project to showcase Testing with a Flask app


## Example Flask App with Postgres SQLAlchemy and Tests

This document will guide you through the process of creating a Flask application that utilizes Postgres SQLalchemy and tests to ensure functionality. The application will act as a basic template that can be built upon to create more complex applications.

## Setting up the Environment

To start, ensure that you have Python 3 and pip installed on your machine. It is also recommended to use a virtual environment to avoid conflicts with other Python packages.

### Creating a Virtual Environment

1. Install virtualenv using pip by running the following command in your terminal:

```bash
pip install virtualenv
```

1. Create a new virtual environment by running the following command in your terminal:

```bash
virtualenv myenv
```

1. Activate the virtual environment by running the following command in your terminal:

```bash
source myenv/bin/activate
```

### Installing Dependencies

1. Create a new directory for your project and navigate to it in your terminal.
2. Install the required dependencies by running the following command in your terminal:

```bash
pip install flask flask_sqlalchemy psycopg2 pytest mock

```

## Setting up the Application

### Creating the Flask App

1. Create a new file called `app.py` in your project directory.
2. Add the following code to the `app.py` file:

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/example_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

```

This code imports Flask and SQLAlchemy, creates a Flask app object, sets the configuration for the Postgres database, initializes a SQLAlchemy instance, and starts the application.

### Creating the Database Model

1. Create a new file called `models.py` in your project directory.
2. Add the following code to the `models.py` file:

```
from app import db

class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

```

This code defines a new model called `ExampleModel` with two columns, `id` and `name`.

### Creating the Routes

1. Add the following code to the `app.py` file:

```
from flask import jsonify
from models import ExampleModel

@app.route('/example', methods=['GET'])
def get_example():
    example = ExampleModel.query.filter_by(id=1).first()
    return jsonify({'name': example.name})

```

This code creates a new route that returns the name of an example model object with an id of 1.

### Creating the Tests

1. Create a new file called `test_app.py` in your project directory.
2. Add the following code to the `test_app.py` file:

```
import os
import pytest
from app import app, db
from models import ExampleModel
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        example = ExampleModel(name='Example')
        db.session.add(example)
        db.session.commit()

    yield client

def test_get_example(client):
    response = client.get('/example')
    assert response.status_code == 200
    assert response.json['name'] == 'Example'

@patch('models.ExampleModel.query')
def test_get_example_with_mock(mock_query, client):
    mock_query.filter_by.return_value.first.return_value.name = 'Mock Example'
    response = client.get('/example')
    assert response.status_code == 200
    assert response.json['name'] == 'Mock Example'
    mock_query.filter_by.assert_called_once_with(id=1)
    mock_query.filter_by.return_value.first.assert_called_once()

```

This code imports the necessary modules, creates a fixture that sets up a test client and initializes a test database, and defines two tests that ensure the `get_example` route returns the correct JSON response, one of which mocks the database query with the `patch` decorator.

## Running the Application

To run the application, navigate to your project directory in your terminal and run the following command:

```
python app.py

```

The application will start running on your local machine at `http://localhost:5000/`.

## Running the Tests

To run the tests, navigate to your project directory in your terminal and run the following command:

```
pytest

```

The tests will run and output the results in your terminal.

### Creating Fixtures

1. Add the following code to the `test_app.py` file:

```
@pytest.fixture
def example_model():
    example = ExampleModel(name='Example')
    db.session.add(example)
    db.session.commit()
    return example

def test_example_model(example_model):
    assert example_model.name == 'Example'

```

This code defines a new fixture that creates an example model object in the database and returns it, and a test that ensures the fixture works correctly.

### Using Mocks for External Services

1. Add the following code to the `app.py` file:

```
import requests

@app.route('/weather', methods=['GET'])
def get_weather():
    response = requests.get('<https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=API_KEY>')
    return jsonify({'weather': response.json()['weather'][0]['description']})

```

This code creates a new route that gets the weather in London using the OpenWeatherMap API and returns the description of the weather.

1. Add the following code to the `test_app.py` file:

```
@patch('app.requests.get')
def test_get_weather_with_mock(mock_get, client):
    mock_get.return_value.json.return_value = {'weather': [{'description': 'mock weather'}]}
    response = client.get('/weather')
    assert response.status_code == 200
    assert response.json['weather'] == 'mock weather'
    mock_get.assert_called_once_with('<https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=API_KEY>')

```

This code defines a new test that mocks the API request using the `patch` decorator and ensures the correct JSON response is returned.

## Running the Application

To run the application, navigate to your project directory in your terminal and run the following command:

```
python app.py

```

The application will start running on your local machine at `http://localhost:5000/`.

## Running the Tests

To run the tests, navigate to your project directory in your terminal and run the following command:

```
pytest

```

The tests will run and output the results in your terminal.
