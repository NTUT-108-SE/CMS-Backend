import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))