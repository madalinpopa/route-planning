import functools

import click
import sqlalchemy
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

auth = Blueprint("auth", __name__, url_prefix="/auth", cli_group="user")


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
        g.user = User.query.filter_by(id=user_id).first()


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("company.details"))
        else:
            flash("Invalid username or password")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


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


@auth.cli.command("create")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_user(username, email, password):
    """Create a new user."""
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        click.echo(f"User {username} created successfully.")
    except sqlalchemy.exc.IntegrityError:
        click.echo(f"User {username} already exists.")


@auth.cli.command("delete")
@click.argument("username")
def delete_user(username):
    """Delete a user."""
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        click.echo(f"User {username} deleted successfully.")
    else:
        click.echo(f"User {username} not found.")


@auth.cli.command("list")
def list_users():
    """List all users."""
    users = User.query.all()
    for user in users:
        click.echo(f"{user.username} - {user.email}")
