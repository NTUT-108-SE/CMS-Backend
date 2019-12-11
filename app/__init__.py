from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from config import config
from mongoengine import connect

mail = Mail()
login_manager = LoginManager()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    connect(host=config[config_name].DATABASE_URL)
    from .blueprint import main_bp, login_bp, patient_bp, registration_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(registration_bp)

    return app
