from flask import Flask
from app.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(DevConfig)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models