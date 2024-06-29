from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField
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
        "Combustible", choices=("Motorina", "Benzina"), validators=[DataRequired()]
    )
    consumption = StringField("Consumption", validators=[DataRequired()])

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
    start_address = StringField("Start address", validators=[DataRequired()])
    start_km = IntegerField("Start km", validators=[DataRequired()])
    end_address = StringField("End address", validators=[DataRequired()])
    end_km = IntegerField("End km", validators=[DataRequired()])
    driver = QuerySelectField(
        "Driver",
        query_factory=lambda: Driver.query.all(),
        allow_blank=True,
        get_label="name",
    )
    vehicle = QuerySelectField(
        "Vehicle",
        query_factory=lambda: Vehicle.query.all(),
        allow_blank=True,
        get_label="plate",
    )

    # def __init__(self, *args, **kwargs):
    #     super(RouteForm, self).__init__(*args, **kwargs)
    #     self.vehicle.choices = [
    #         (vehicle.id, vehicle.plate) for vehicle in Vehicle.query.order_by("plate")
    #     ]
    #     self.driver.choices = [
    #         (driver.id, f"{driver.name} {driver.surname}")
    #         for driver in Driver.query.order_by("name")
    #     ]
