from flask import Flask
from flask_babel import Babel
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
babel = Babel()


def create_app(config_object: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    babel.init_app(app)
    CORS(app)

    from app.routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
