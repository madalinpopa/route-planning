import functools

from flask import (
    Blueprint,
    g,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from route_planning import db
from ..models import User

from ..forms import UserRegistrationForm
from ..forms import LoginForm

auth = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.query(User).filter_by(id=user_id).first()


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the user already exists
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            flash("Email address already exists")
            return redirect(url_for("auth.register"))

        user = User(
            username=username, password=generate_password_hash(password), email=email
        )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)