import os
from dotenv import load_dotenv
import json
load_dotenv(dotenv_path=".environment")


class Config:
    DEBUG = False
    TESTING = False
    PORT = os.environ.get('PORT') or 8000
    HOST = os.environ.get('HOST') or '127.0.0.1'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "JWFDENWLI#J*)!$H@H#"
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or 'CMS Admin <NTUT.CMS@gmail.com>'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.gmail.com"
    MAIL_PROT = os.environ.get('MAIL_PROT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    DATABASE_URL = os.environ.get("DATABASE_URL") or "mongodb://localhost:27017/CMS"
    FHIR_URL = os.environ.get("FHIR_URL") or "http://localhost:8080/hapi-fhir-jpaserver/fhir"
    CORS_HOST = json.loads(os.environ.get("CORS_HOST") or '["http://localhost:8080"]')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "mongodb://localhost:27017/Development"
    SECRET_KEY = "DEBUG"
    PORT = 8000
    HOST = "127.0.0.1"


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = "mongomock://localhost"
    SECRET_KEY = "DEBUG"
    PORT = 8000
    HOST = "127.0.0.1"


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
