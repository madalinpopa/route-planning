from flask import Blueprint, current_app, render_template, request

from ..models import Driver

driver = Blueprint("driver", __name__, url_prefix="/driver")


@driver.route("/list")
def driver_list():
    page = request.args.get("page", 1, type=int)
    pagination = Driver.query.paginate(
        page=page, per_page=current_app.config["ITEMS_PER_PAGE"], error_out=False
    )
    return render_template("driver/list.html")
