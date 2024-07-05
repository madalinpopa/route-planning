from flask import Blueprint, render_template, request, redirect, url_for, current_app

from ..models import Vehicle, Company
from ..forms import VehicleForm
from .auth import login_required

vehicle = Blueprint("vehicle", __name__, url_prefix="/vehicle")


@vehicle.route("/list", methods=["GET"])
@login_required
def vehicle_list():
    page = request.args.get("page", 1, type=int)
    pagination = Vehicle.query.order_by(Vehicle.created_at.desc()).paginate(
        page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False
    )
    vehicles = pagination.items
    return render_template(
        "vehicle/list.html", vehicles=vehicles, pagination=pagination
    )


@vehicle.route("/add", methods=["GET", "POST"])
@login_required
def vehicle_add():
    form = VehicleForm()
    if request.method == "POST":
        company = Company.query.first()
        if form.validate_on_submit():
            vehicle_obj = Vehicle(
                plate=form.plate.data,
                brand=form.brand.data,
                model=form.model.data,
                category=form.category.data,
                combustible=form.combustible.data,
                consumption_mixt=form.consumption_mixt.data,
                consumption_urban=form.consumption_urban.data,
                consumption_extra_urban=form.consumption_extra_urban.data,
                company=company,
            )
            vehicle_obj.save()
            return redirect(url_for("vehicle.vehicle_list"))
    return render_template("vehicle/add.html", form=form)


@vehicle.route("/edit/<int:vehicle_id>", methods=["GET", "POST"])
@login_required
def vehicle_edit(vehicle_id):
    vehicle_obj = Vehicle.query.get(vehicle_id)
    if vehicle_obj is None:
        return redirect(url_for("vehicle.vehicle_list"))

    form = VehicleForm(obj=vehicle_obj)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(vehicle_obj)
            vehicle_obj.save()
            return redirect(url_for("vehicle.vehicle_list"))
    return render_template("vehicle/edit.html", form=form, vehicle=vehicle_obj)


@vehicle.route("/delete/<int:vehicle_id>", methods=["POST"])
@login_required
def vehicle_delete(vehicle_id):
    vehicle_obj = Vehicle.query.get(vehicle_id)
    if vehicle_obj is not None:
        vehicle_obj.delete()
    return redirect(url_for("vehicle.vehicle_list"))
