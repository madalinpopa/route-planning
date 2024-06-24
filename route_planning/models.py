from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column
from route_planning import db


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<User {self.username}>"


class Company(db.Model):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vat: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=True)
    drivers = db.relationship("Driver", backref="company")
    vehicles = db.relationship("Vehicle", backref="company")

    def __repr__(self):
        return f"<Company {self.name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Driver(db.Model):
    __tablename__ = "drivers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    company_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("companies.id"), nullable=False
    )

    routes = db.relationship("Route", backref="driver")

    def __repr__(self):
        return f"<Driver {self.name} {self.surname}>"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting vehicle: {e}")


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plate: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    combustible: Mapped[str] = mapped_column(String, nullable=False)
    consumption: Mapped[float] = mapped_column(Float, nullable=False)
    company_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("companies.id"), nullable=False
    )
    routes = db.relationship("Route", backref="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.plate}>"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting vehicle: {e}")


class Route(db.Model):
    __tablename__ = "routes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    start_km: Mapped[float] = mapped_column(Float, nullable=False)
    end_km: Mapped[float] = mapped_column(Float, nullable=False)
    start_from: Mapped[str] = mapped_column(String, nullable=False)
    end_to: Mapped[str] = mapped_column(String, nullable=False)
    distance: Mapped[float] = mapped_column(Float, nullable=False)

    driver_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("drivers.id"), nullable=False
    )

    vehicle_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("vehicles.id"), nullable=False
    )

    def __repr__(self):
        return f"<Route {self.date}>"
