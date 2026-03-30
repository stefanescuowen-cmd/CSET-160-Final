from flask import Flask
from app.config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Import routes after app is created to avoid circular imports
    from app.routes import routes
    app.register_blueprint(routes.bp)

    return app