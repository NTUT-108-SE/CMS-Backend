from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from config import config
mail = Mail()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    from .login import login as login_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(login_blueprint)

    return app