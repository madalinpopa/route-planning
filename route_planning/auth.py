from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db_session
from .models import User

from .forms import UserRegistrationForm

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    return "Login"


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the user already exists
        existing_user = db_session.query(User).filter_by(email=email).first()
        if existing_user:
            flash("Email address already exists")
            return redirect(url_for("auth.register"))

        user = User(
            username=username, password=generate_password_hash(password), email=email
        )
        db_session.add(user)
        db_session.commit()

        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
