from flask import Blueprint, render_template, g, redirect, url_for
from .auth import login_required

from ..models import Company
from ..forms import CompanyForm

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    form = CompanyForm()
    user_companies = Company.query.filter_by(user_id=g.user.id).all()
    if not user_companies:
        return render_template("index.html", show_company_modal=True, form=form)
    else:
        return redirect(url_for("company.details"))
