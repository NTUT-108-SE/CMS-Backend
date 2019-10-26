import os
from app import app
from app.handles import index


def get_app():
    return app


if __name__ == "__main__":
    debug = False if os.getenv("PYTHON_PROD") else True
    if debug:
        from aoiklivereload import LiveReloader
        LiveReloader().start_watcher_thread()
    app.run(host="0.0.0.0", port=8000, debug=debug)
