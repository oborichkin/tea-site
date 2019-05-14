from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tea_site.config import Config, TestConfig

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'alert alert-info'

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    db.app = app
    login_manager.init_app(app)

    from tea_site.main.routes import main
    from tea_site.users.routes import users
    from tea_site.testing.routes import testing

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(testing)

    return app