import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 5


class DevelopmentConfig(Config):
    DB_USER = os.environ.get("DB_USER")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )


class ProductionConfig(Config):
    DB_USER = os.environ.get("DB_USER")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )


config = {"development": DevelopmentConfig, "production": ProductionConfig}
