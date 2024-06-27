from flask import Blueprint, render_template, request, current_app, redirect, url_for

from ..models import Route, Company, Driver, Vehicle
from ..forms import RouteForm

route = Blueprint("route", __name__, url_prefix="/route")


@route.route("/list")
def route_list():
    page = request.args.get("page", 1, type=int)
    pagination = Route.query.order_by(Route.created_at.desc()).paginate(
        page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False
    )
    routes = pagination.items
    return render_template("route/list.html", routes=routes, pagination=pagination)


@route.route("/add", methods=["GET", "POST"])
def route_add():
    form = RouteForm()
    form.driver.choices = [
        (driver.id, f"{driver.name} {driver.surname}")
        for driver in Driver.query.order_by("name")
    ]
    form.vehicle.choices = [
        vehicle.plate for vehicle in Vehicle.query.order_by("plate")
    ]
    if request.method == "POST":
        company = Company.query.first()
        if form.validate_on_submit():
            date = form.date.data
            start_address = form.start_address.data
            start_km = form.start_km.data
            end_address = form.end_address.data
            end_km = form.end_km.data
            vehicle = form.vehicle.data
            driver = form.driver.data
            route_obj = Route(
                date=date,
                start_address=start_address,
                start_km=start_km,
                end_address=end_address,
                end_km=end_km,
                vehicle=vehicle,
                driver=driver,
                company=company,
            )
            route_obj.save()
            return redirect(url_for("route.route_list"))
    return render_template("route/add.html", form=form)


@route.route("/edit/<int:route_id>", methods=["GET", "POST"])
def vehicle_edit(route_id):
    route_obj = Route.query.get(route_id)
    if route_obj is None:
        return redirect(url_for("route.route_list"))

    form = RouteForm(obj=route_obj)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(route_obj)
            route_obj.save()
            return redirect(url_for("route.route_list"))
    return render_template("vehicle/edit.html", form=form, vehicle=route_obj)


@route.route("/delete/<int:route_id>", methods=["POST"])
def route_delete(route_id):
    route_obj = Route.query.get(route_id)
    if route_obj is not None:
        route_obj.delete()
    return redirect(url_for("route.route_list"))
