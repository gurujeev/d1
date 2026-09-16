from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SetPasswordRequest(BaseModel):
    token: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class WeeklyFormRequest(BaseModel):
    week_start: str
    week_end: str
    learning: Optional[str] = None
    activities: Optional[str] = None
    challenges: Optional[str] = None