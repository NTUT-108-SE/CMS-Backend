import os
from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/")
async def index(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    debug = False if os.getenv("PYTHON_PROD") else True
    if debug:
        from aoiklivereload import LiveReloader
        LiveReloader().start_watcher_thread()

    app.run(host="0.0.0.0", port=8000, debug=debug)
