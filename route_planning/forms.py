from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    IntegerField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


from .models import Vehicle, Driver


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
    email = StringField("Email", validators=[Email()])
    phone = StringField("Phone")


class VehicleForm(FlaskForm):
    plate = StringField("Plate", validators=[DataRequired()])
    brand = StringField("Brand", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    combustible = SelectField(
        "Combustible",
        choices=(("Motorina", "Motorina"), ("Benzina", "Benzina")),
        validators=[DataRequired()],
    )
    consumption_mixt = IntegerField("Consumption Mixt", validators=[DataRequired()])
    consumption_urban = IntegerField("Consumption Urban", validators=[DataRequired()])
    consumption_extra_urban = IntegerField(
        "Consumption Extra Urban", validators=[DataRequired()]
    )
    category = SelectField(
        "Category",
        choices=(("M1", "M1"), ("M2", "M2"), ("M3", "M3")),
        default="M1",
        validators=[DataRequired()],
    )

    def validate_plate(self, field):
        plate = Vehicle.query.filter_by(plate=field.data).first()
        if plate:
            raise ValidationError("Plate already exists")

    def validate_consumption(self, field):
        try:
            float(field.data)
        except ValueError:
            raise ValidationError("Consumption must be a number")


class RouteForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    start_time = TimeField("Start time", validators=[DataRequired()])
    end_time = TimeField("End time", validators=[DataRequired()])
    start_address = StringField("Start address", validators=[DataRequired()])
    start_km = IntegerField("Start km", validators=[DataRequired()])
    end_address = StringField("End address", validators=[DataRequired()])
    end_km = IntegerField("End km", validators=[DataRequired()])
    route_reason = TextAreaField("Route reason")
    route_type = SelectField(
        "Route type",
        choices=(("Urban", "Urban"), ("Mixt", "Mixt"), ("Extra Urban", "Extra Urban")),
        default="Urban",
        validators=[DataRequired()],
    )
    driver = QuerySelectField(
        "Driver",
        query_factory=lambda: Driver.query.all(),
        allow_blank=True,
        get_label=lambda d: f"{d.name} {d.surname}",
    )
    vehicle = QuerySelectField(
        "Vehicle",
        query_factory=lambda: Vehicle.query.all(),
        allow_blank=True,
        get_label="plate",
    )
