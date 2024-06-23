from flask import Blueprint, render_template
from .auth import login_required

from .. import db
from ..models import Company

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    default_company = Company.query.first()
    if default_company is None:
        new_company = Company(vat="123456789", name="Company Name")
        db.session.add(new_company)
        db.session.commit()
        return render_template("index.html", company=new_company)
    else:
        return render_template("index.html", company=default_company)
