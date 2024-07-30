from flask import Blueprint, render_template, request, redirect, url_for, g
from ..models import Company
from ..forms import CompanyForm
from .auth import login_required

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/details", methods=["GET"])
@login_required
def details():
    # Get all companies for the current user
    user_company = Company.query.filter_by(user_id=g.user.id).first()
    if not user_company:
        return redirect(url_for("main.index"))
    return render_template("company/details.html", company=user_company)


@company.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    default_company = Company.query.filter_by(user_id=g.user.id).first()
    if not default_company:
        return redirect(url_for("main.index"))

    form = CompanyForm(obj=default_company)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(default_company)
            default_company.save()
            return redirect(url_for("company.details"))
        print(form.errors)
    return render_template("company/edit.html", form=form)


@company.route("/add", methods=["POST"])
@login_required
def add():
    form = CompanyForm()
    if form.validate_on_submit():
        company_obj = Company(
            name=form.name.data,
            vat=form.vat.data,
            address=form.address.data,
            user_id=g.user.id,
        )
        company_obj.save()
        return redirect(url_for("company.details"))
    return render_template("index.html", show_company_modal=True)
