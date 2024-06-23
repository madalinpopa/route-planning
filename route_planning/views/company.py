from flask import Blueprint, render_template

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/details")
def details():
    return render_template("company/details.html")
