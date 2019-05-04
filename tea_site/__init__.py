from flask import Flask
from tea_site.config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from tea_site.main.routes import main

    app.register_blueprint(main)

    return app