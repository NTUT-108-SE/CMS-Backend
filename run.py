import os
from app import create_app
from flask import make_response, request
from mongoengine import connect
import app.modules

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.after_request
def af_request(resp):
    """
    #請求鉤子，在所有的請求發生後執行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    if request.environ.get('HTTP_ORIGIN') in app.config.get('CORS_HOST'):
        resp.headers['Access-Control-Allow-Origin'] = request.environ['HTTP_ORIGIN']
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


if __name__ == "__main__":
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
