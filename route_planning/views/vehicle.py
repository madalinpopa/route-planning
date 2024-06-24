from flask import Blueprint, render_template
from ..forms import VehicleForm

vehicle = Blueprint("vehicle", __name__, url_prefix="/vehicle")


@vehicle.route("/list")
def vehicle_list():
    return render_template("vehicle/list.html")


@vehicle.route("/add", methods=["GET", "POST"])
def vehicle_add():
    form = VehicleForm()
    if form.validate_on_submit():
        return "Vehicle added"
    return render_template("vehicle/add.html", form=form)
