
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    mobile: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    profile: Mapped["FarmerProfile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_farmer_profile_user"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="kn",
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(80),
        default="Karnataka",
        nullable=False,
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    taluk: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    village: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    land_area: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    land_unit: Mapped[str] = mapped_column(
        String(30),
        default="acres",
        nullable=False,
    )

    land_ownership: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )

    crops: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    irrigation_method: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    farming_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    needs: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped[User] = relationship(
        back_populates="profile",
    )
