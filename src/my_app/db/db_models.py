from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class Bike(Base):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    battery: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100
    status: Mapped[str] = mapped_column(
        String, nullable=False
    )  # available/rented/maintenance

    station_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stations.id", ondelete="SET NULL"), # we allow bike_id to become NULL via ondelete="SET NULL"
        nullable=True,
    )
    
    rentals: Mapped[List["Rental"]] = relationship(
        back_populates="bike", # This sets up a bidirectional relationship between Bike and Rental. The rentals attribute on the Bike model will contain a list of Rental objects that are associated with that bike, and the bike attribute on the Rental model will reference the Bike object that is associated with that rental.
        passive_deletes=True, # Keep rentals for history if bike is deleted
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="rider")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    rentals: Mapped[List["Rental"]] = relationship(
        back_populates="user",
        passive_deletes=True,
    )


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # History-friendly: if Bike/User deleted, keep Rental and set FK to NULL
    bike_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("bikes.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    bike: Mapped[Optional["Bike"]] = relationship(back_populates="rentals")
    user: Mapped[Optional["User"]] = relationship(back_populates="rentals")
