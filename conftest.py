import pytest
from app import create_app, db
from app.config import TestConfig
from flask_jwt_extended import JWTManager

@pytest.fixture
def app():
    app = create_app(TestConfig)
    jwt = JWTManager(app)

    with app.app_context():
        db.init_app(app)
        db.create_all()
    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()