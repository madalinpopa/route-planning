from route_planning.db import db_session
from . import create_app
from flask import render_template

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run()
