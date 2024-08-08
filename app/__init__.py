from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
