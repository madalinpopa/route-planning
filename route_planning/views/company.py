from flask import Blueprint, render_template, request, redirect, url_for, g
from ..models import Company
from ..forms import CompanyForm
from .. import db
from .auth import login_required

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/details", methods=["GET"])
@login_required
def details():
    # Get all companies for the current user
    user_companies = Company.query.filter_by(user_id=g.user.id).all()
    if not user_companies:
        # Create a default company for the user if they don't have any
        new_company = Company(
            vat="123456789", name="Default Company", user_id=g.user.id
        )
        db.session.add(new_company)
        db.session.commit()
    return render_template("company/details.html", company=new_company)


@company.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    default_company = Company.query.first()
    form = CompanyForm(obj=default_company)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(default_company)
            default_company.save()
            return redirect(url_for("company.details"))
        print(form.errors)
    return render_template("company/edit.html", form=form)
