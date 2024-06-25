import os

from flask import Flask, g, request
from flask.cli import AppGroup

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .config import config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_babel import Babel


class Base(DeclarativeBase):
    pass


def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, "user", None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(["de", "fr", "en"])


def get_timezone():
    user = getattr(g, "user", None)
    if user is not None:
        return user.timezone


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
csrf = CSRFProtect()
cache = Cache()
babel = Babel()
user_cli = AppGroup("user")


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
    csrf.init_app(app)
    babel.init_app(app)
    cache.init_app(
        app,
        config={
            "CACHE_TYPE": "MemcachedCache",
            "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
            "CACHE_MEMCACHED_SERVERS": app.config["CACHE_MEMCACHED_SERVERS"],
        },
    )

    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    from .views import auth, main, company, driver, route, vehicle

    app.register_blueprint(main.main)
    app.register_blueprint(auth.auth)
    app.register_blueprint(company.company)
    app.register_blueprint(driver.driver)
    app.register_blueprint(route.route)
    app.register_blueprint(vehicle.vehicle)

    return app
