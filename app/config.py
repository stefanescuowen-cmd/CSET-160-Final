import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", "sqlite:///local.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False