import os
from app import create_app
from flask import make_response
from mongoengine import connect
from modules.database import User
from modules import login_manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.after_request
def af_request(resp):
    """
    #請求鉤子，在所有的請求發生後執行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


if __name__ == "__main__":
    connect(host=app.config.get('DATABASE_URL'))
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))