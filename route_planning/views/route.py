from flask import Blueprint, render_template

route = Blueprint("route", __name__, url_prefix="/route")


@route.route("/list")
def route_list():
    return render_template("route/list.html")
