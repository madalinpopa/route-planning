from flask import Blueprint, render_template

vehicle = Blueprint("vehicle", __name__, url_prefix="/vehicle")


@vehicle.route("/list")
def vehicle_list():
    return render_template("vehicle/list.html")
