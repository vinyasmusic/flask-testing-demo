import os

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "your-secret-key-here"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://testinguser:password@localhost/dbname"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/dbname"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/dbname"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://testinguser:{POSTGRES_PASSWORD}@localhost:5432/testingdemo"
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    # Add more configurations as needed
    "default": Config,
    "production": ProductionConfig,
    "staging": StagingConfig,
}
