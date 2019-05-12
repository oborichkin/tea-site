from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tea_site.config import Config, TestConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from tea_site.main.routes import main
    from tea_site.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app