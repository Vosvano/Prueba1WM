from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True)
    
    name: Mapped[str] = mapped_column(
        nullable=False,
        index=True)
    
    email: Mapped[str] = mapped_column(
        nullable=False, 
        unique=True)

    reservations = relationship("Reservation", back_populates="user")


class Space(Base):
    __tablename__ = "spaces"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True)
    
    name: Mapped[str] = mapped_column(
        nullable=False,
        index=True)
    
    location: Mapped[str] = mapped_column(
        nullable=False)
    
    capacity: Mapped[int] = mapped_column(
        nullable=False,
        default=3)
    
    full_availability: Mapped[bool] = mapped_column(
        default=True)

    reservations = relationship("Reservation", back_populates="space")


class Reservation(Base):
    __tablename__ = "reservations"
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        index=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        nullable=False,
        index=True)
    
    space_id: Mapped[int] = mapped_column(
        ForeignKey("spaces.id"), 
        nullable=False,
        index=True)
    
    date: Mapped[datetime] = mapped_column(
        nullable=False)
    
    start_time: Mapped[datetime] = mapped_column(
        nullable=False)
    
    end_time: Mapped[datetime] = mapped_column(
        nullable=False)
    
    status: Mapped[str] = mapped_column( 
        nullable=False
        ,default="Confirmed")

    user = relationship("Users", back_populates="reservations")
    space = relationship("Space", back_populates="reservations")