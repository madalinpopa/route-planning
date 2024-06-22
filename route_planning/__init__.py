import os
from flask import Flask
from .config import config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "route_planning.sqlite"),
    )

    if test_config is None:
        env_config = os.environ.get("FLASK_ENV", "development")
        app.config.from_object(config[env_config])
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from .db import init_db

        init_db()

    from . import auth

    app.register_blueprint(auth.auth)

    return app
