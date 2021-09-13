import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../test.db')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///../app.db')