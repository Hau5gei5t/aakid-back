import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, Boolean, Date, Unicode, Enum, types
from sqlalchemy_utils import PasswordType, PhoneNumber
from sqlalchemy.orm import Relationship, Composite, mapped_column, Mapped

from database import Base

# TODO:
#   [  ] many to many for student and (group, event)
#   [  ] do other tables:
#       [  ] Group
#       [  ] Event
#       [  ] Payment
#       [  ] Visit


class Role(enum.Enum):
    """
    Represents the role of a user.
    
    Attributes:
        STUDENT: Represents a student role.
        TRAINER: Represents a trainer role.
    """
    STUDENT = "student"
    TRAINER = "trainer"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
    role: Mapped[Role] = mapped_column(default=Role.student)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    hash_password: Mapped[str]
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[datetime]
    _phone_number: Mapped[types.Unicode] = mapped_column(Unicode(20))
    country_code: Mapped[types.Unicode] = mapped_column(Unicode(8))
    phone_number = Composite(PhoneNumber,
                             _phone_number,
                             country_code)
    conf_phone: Mapped["ConfirmedPhone"] = Relationship(back_populates="user")
    conf_email: Mapped["ConfirmedEmail"] = Relationship(back_populates="user")
    trainer_data: Mapped["Trainer"] = Relationship(back_populates="user")
    student_data: Mapped["Student"] = Relationship(back_populates="user")


class ConfirmedPhone(Base):
    __tablename__ = "confPass"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True, index=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = Relationship(back_populates="conf_phone")


class ConfirmedEmail(Base):
    __tablename__ = "confEmail"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True, index=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    user: Mapped["User"] = Relationship(back_populates="conf_email")


class Trainer(Base):
    __tablename__ = "trainer"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True, index=True)
    user: Mapped["User"] = Relationship(back_populates="trainer_data")
    groups: Mapped[List["Group"]] = Relationship(back_populates="trainer")
    events: Mapped[List["Event"]] = Relationship(back_populates="trainer")

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True, index=True)
    user: Mapped["User"] = Relationship(back_populates="student_data")
    # groups: Mapped[List["Group"]] = Relationship(back_populates="student") *-*
    # events: Mapped[List["Event"]] = Relationship(back_populates="student") *-*
    payments: Mapped[List["Payment"]] = Relationship(back_populates="student")
    visits: Mapped[List["Visit"]] = Relationship(back_populates="student")


