from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
import enum
from email_validator import validate_email, EmailNotValidError
from app.db.connection import Base


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    @validates("email")
    def validate_email(self, key, email):
        try:
            validation = validate_email(email, check_deliverability=False)
            return validation.normalized.lower()
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {email}") from e

    passport = relationship(
        "Passport",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Passport(Base):
    __tablename__ = "passports"

    id = Column(Integer, primary_key=True, index=True)
    passport_number = Column(Integer, nullable=False, unique=True, index=True)
    city = Column(String(30), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    user = relationship("User", back_populates="passport")
