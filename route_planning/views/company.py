from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Company
from ..forms import CompanyForm
from .. import db

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/details", methods=["GET"])
def details():
    default_company = Company.query.first()
    if default_company is None:
        new_company = Company(vat="123456789", name="Company Name")
        db.session.add(new_company)
        db.session.commit()
    if request.headers.get("HX-Request") == "true":
        return render_template("company/partials/details.html", company=default_company)
    return render_template("company/details.html", company=default_company)


@company.route("/edit", methods=["GET", "POST"])
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
