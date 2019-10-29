import os
from app import create_app
from mongoengine import connect
from modules.database import User
from modules import login_manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    connect(host=app.config.get('DATABASE_URL'))
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))