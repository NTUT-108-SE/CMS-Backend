from app import app
from sanic.response import json


@app.route("/")
async def index(request):
    return json({"hello": "world"})
