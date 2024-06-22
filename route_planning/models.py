from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from . import db


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
