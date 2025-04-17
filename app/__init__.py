from flask import Flask
from .config import Config
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Папка для голосовых
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(bp)
    return app
