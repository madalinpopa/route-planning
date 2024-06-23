from flask import Blueprint, render_template

driver = Blueprint("driver", __name__, url_prefix="/driver")


@driver.route("/list")
def driver_list():
    return render_template("driver/list.html")
