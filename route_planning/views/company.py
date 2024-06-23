from flask import Blueprint, render_template
from ..models import Company
from .. import db

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/details", methods=["GET"])
def details():
    default_company = Company.query.first()
    return render_template("company/details.html", company=default_company)
