from flask import Flask
from .db import engine, Base, SessionLocal
from .routes.interviews import bp as interviews_bp

def create_app(config_object=None):
    app = Flask(__name__)
    if config_object:
        app.config.from_object(config_object)

    # register blueprints
    app.register_blueprint(interviews_bp)

    return app
