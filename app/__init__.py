import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic.error_wrappers import ValidationError as PydanticValidationErrorWrapper
from config import config


db = SQLAlchemy()


def handle_400_error(error):
    """Handle 400 errors raised"""
    status_code = getattr(error, "status_code", 400)
    error_message = getattr(error, "message", str(error))
    # TODO : refactor with Case matching when repo is moved to Py 3.10
    response = jsonify({"message": error_message, "status_code": status_code})
    response.status_code = status_code
    return response


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or "default"))

    db.init_app(app)

    # Import blueprints here
    from .routes.user import users_routes
    from .routes.weather import weather_routes

    app.register_blueprint(users_routes)
    app.register_blueprint(weather_routes)
    app.register_error_handler(ValueError, handle_400_error)
    app.register_error_handler(PydanticValidationErrorWrapper, handle_400_error)

    return app
