from flask import Blueprint, render_template, request, current_app, redirect, url_for

from ..models import Route, Driver, Vehicle
from ..forms import RouteForm
from .auth import login_required

route = Blueprint("route", __name__, url_prefix="/route")


@route.route("/list")
@login_required
def route_list():
    page = request.args.get("page", 1, type=int)
    pagination = Route.query.order_by(Route.created_at.desc()).paginate(
        page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False
    )
    routes = pagination.items
    return render_template("route/list.html", routes=routes, pagination=pagination)


@route.route("/add", methods=["GET", "POST"])
@login_required
def route_add():
    form = RouteForm()
    if request.method == "POST":
        if form.validate_on_submit():
            date = form.date.data
            start_address = form.start_address.data
            start_km = form.start_km.data
            end_address = form.end_address.data
            end_km = form.end_km.data
            vehicle_id = form.vehicle.data
            driver_id = form.driver.data

            # Fetch the actual vehicle and driver instances
            vehicle = Vehicle.query.get(vehicle_id)
            driver = Driver.query.get(driver_id)

            route_obj = Route(
                date=date,
                start_address=start_address,
                start_km=start_km,
                end_address=end_address,
                end_km=end_km,
                vehicle=vehicle,
                driver=driver,
            )
            route_obj.save()
            return redirect(url_for("route.route_list"))
    return render_template("route/add.html", form=form)


@route.route("/edit/<int:route_id>", methods=["GET", "POST"])
@login_required
def route_edit(route_id):
    route_obj = Route.query.get(route_id)
    if route_obj is None:
        return redirect(url_for("route.route_list"))

    form = RouteForm(obj=route_obj)

    if request.method == "POST":
        if form.validate_on_submit():
            route_obj.date = form.date.data
            route_obj.start_address = form.start_address.data
            route_obj.start_km = form.start_km.data
            route_obj.end_address = form.end_address.data
            route_obj.end_km = form.end_km.data
            route_obj.driver = form.driver.data
            route_obj.vehicle = form.vehicle.data
            route_obj.save()
            print("After updating object", route_obj.driver, route_obj.vehicle)
            return redirect(url_for("route.route_list"))
    return render_template("route/edit.html", form=form, route=route_obj)


@route.route("/delete/<int:route_id>", methods=["POST"])
@login_required
def route_delete(route_id):
    route_obj = Route.query.get(route_id)
    if route_obj is not None:
        route_obj.delete()
    return redirect(url_for("route.route_list"))
