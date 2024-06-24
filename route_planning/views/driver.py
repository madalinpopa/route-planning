from flask import Blueprint, current_app, redirect, render_template, request, url_for

from ..models import Company, Driver
from ..forms import DriverForm

driver = Blueprint("driver", __name__, url_prefix="/driver")


@driver.route("/list")
def driver_list():
    page = request.args.get("page", 1, type=int)
    pagination = Driver.query.paginate(
        page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False
    )
    drivers = pagination.items
    return render_template("driver/list.html", drivers=drivers, pagination=pagination)


@driver.route("/add", methods=["GET", "POST"])
def driver_add():
    form = DriverForm()
    company = Company.query.first()
    if request.method == "POST":
        if form.validate_on_submit():
            driver_obj = Driver()
            driver_obj.company = company
            driver_obj.name = form.name.data
            driver_obj.surname = form.surname.data
            driver_obj.email = form.email.data
            driver_obj.phone = form.phone.data
            driver_obj.save()
            return redirect(url_for("driver.driver_list"))
    return render_template("driver/add.html", form=form)


@driver.route("/edit/<int:driver_id>")
def driver_edit(driver_id):
    driver_obj = Driver.query.get(driver_id)
    if driver_obj is None:
        return redirect(url_for("driver.driver_list"))
    return render_template("driver/edit.html", driver=driver_obj)


@driver.route("/delete/<int:driver_id>")
def driver_delete(driver_id):
    driver_obj = Driver.query.get(driver_id)
    if driver_obj is not None:
        driver_obj.delete()
    return redirect(url_for("driver.driver_list"))
