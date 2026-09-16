from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    roll_no = Column(String(50), unique=True, nullable=True)
    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=True)

    role = Column(String(30), nullable=False)

    department = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    section = Column(String(20), nullable=True)

    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    token = Column(String(255), unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    used = Column(Boolean, default=False)


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    token = Column(String(255), unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    used = Column(Boolean, default=False)


class WeeklyForm(Base):
    __tablename__ = "weekly_forms"

    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    week_start = Column(String(20), nullable=False)
    week_end = Column(String(20), nullable=False)

    learning = Column(Text, nullable=True)
    activities = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)

    status = Column(String(30), default="draft")

    submitted_at = Column(DateTime, nullable=True)


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True)

    week_start = Column(String(20), nullable=False)
    week_end = Column(String(20), nullable=False)

    status = Column(String(30), default="generated")

    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    generated_at = Column(DateTime, default=datetime.utcnow)