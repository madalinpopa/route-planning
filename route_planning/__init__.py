import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        env_config = os.environ.get("FLASK_ENV", "development")
        app.config.from_object(config[env_config])
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from . import auth

    app.register_blueprint(auth.auth)

    return app
