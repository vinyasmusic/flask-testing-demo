# Flask Testing Demo
A demo project to showcase Testing with a Flask app

## Why ? What ?  How ? 

### Getting Started

1. Clone the repo
2. Install Poetry by following the instructions on their [website]( https://python-poetry.org/docs/#installation
)
3. Navigate to the root of the project and run:

```bash
$ poetry install
```

   This will create a virtual environment and install all the dependencies listed in pyproject.toml. 

4. You can then activate the virtual environment by `poetry shell`
5. Some environment variables might be needed to kickstart the app

```dotenv
export POSTGRES_PASSWORD=PASSWORD
export WEATHER_API_KEY=TEST
export FLASK_APP=run.py
export FLASK_ENV=testing
export FLASK_DEBUG=1
```
6. Start the flask app by `flask run`

The app will be accessible at http://localhost:5000.
