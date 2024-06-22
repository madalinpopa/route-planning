from route_planning.db import db_session
from . import create_app


app = create_app()


@app.route("/")
def index():
    return "Hello, World!"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
