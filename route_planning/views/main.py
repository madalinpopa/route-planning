from flask import Blueprint, render_template, g
from .auth import login_required

from .. import db
from ..models import Company

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    user_companies = Company.query.filter_by(user_id=g.user.id).all()
    if not user_companies:
        new_company = Company(
            vat="123456789", name="Default Company", user_id=g.user.id
        )
        db.session.add(new_company)
        db.session.commit()
        return render_template("index.html", company=new_company)
    else:
        return render_template("index.html", company=user_companies[0])
