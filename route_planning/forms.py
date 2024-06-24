from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])


class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])


class CompanyForm(FlaskForm):
    vat = StringField("VAT Number", validators=[DataRequired()])
    name = StringField("Company Name", validators=[DataRequired()])
    address = TextAreaField("Address")


class DriverForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])


class VehicleForm(FlaskForm):
    plate = StringField("Plate", validators=[DataRequired()])
    brand = StringField("Brand", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    combustible = SelectField(
        "Combustible", choices=("Motorina", "Benzina"), validators=[DataRequired()]
    )
    consumption = StringField("Consumption", validators=[DataRequired()])

    def validate_consumption(self, field):
        try:
            float(field.data)
        except ValueError:
            raise ValidationError("Consumption must be a number")


class RouteForm(FlaskForm):
    start = StringField("Start", validators=[DataRequired()])
    end = StringField("End", validators=[DataRequired()])
    distance = StringField("Distance", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    status = StringField("Status", validators=[DataRequired()])
    driver = StringField("Driver", validators=[DataRequired()])
    vehicle = StringField("Vehicle", validators=[DataRequired()])
    notes = StringField("Notes", validators=[DataRequired()])
