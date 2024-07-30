from flask import Blueprint, current_app, redirect, render_template, request, url_for, g
from sqlalchemy import desc
from ..models import Company, Driver
from ..forms import DriverForm
from .auth import login_required
from .. import db

driver = Blueprint("driver", __name__, url_prefix="/driver")


@driver.route("/list")
@login_required
def driver_list():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["ITEMS_PER_PAGE"]

    # Join Company and Driver tables to get drivers for the user's company in one query
    query = (
        Driver.query.join(Company)
        .filter(Company.user_id == g.user.id)
        .with_entities(Driver)
    )

    pagination = query.order_by(desc(Driver.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    drivers = pagination.items
    return render_template("driver/list.html", drivers=drivers, pagination=pagination)


@driver.route("/add", methods=["GET", "POST"])
@login_required
def driver_add():
    form = DriverForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(user_id=g.user.id).first()
        if not company:
            return redirect(url_for("company.details"))

        new_driver = Driver(
            company=company,
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        new_driver.save()
        return redirect(url_for("company.details"))
    return render_template("driver/add.html", form=form)


@driver.route("/edit/<int:driver_id>", methods=["GET", "POST"])
@login_required
def driver_edit(driver_id):
    driver_obj = Driver.query.get(driver_id)
    if driver_obj is None:
        return redirect(url_for("company.details"))

    form = DriverForm(obj=driver_obj)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(driver_obj)
            db.session.commit()
            return redirect(url_for("company.details"))
    return render_template("driver/edit.html", form=form, driver=driver_obj)


@driver.route("/delete/<int:driver_id>", methods=["POST"])
@login_required
def driver_delete(driver_id):
    driver_obj = Driver.query.get(driver_id)
    if driver_obj is not None:
        driver_obj.delete()
    return redirect(url_for("company.details"))
