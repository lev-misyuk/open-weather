from flask import Flask
from app.config import BaseConfig, DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
db = SQLAlchemy()

def create_app(config: BaseConfig) -> Flask:
    from app.routes import routes
    from app import models
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(routes)
    return app

app = create_app(DevConfig)
jwt = JWTManager(app)
migrate = Migrate(app, db)