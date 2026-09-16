import secrets

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import (
    User,
    ActivationToken,
    PasswordResetToken
)

from schemas import (
    LoginRequest,
    SetPasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

from services.email_service import (
    send_activation_email,
    send_password_reset_email
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/activate")
def activate_account(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email.lower()
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Email is not in the approved user list"
        )

    if user.email_verified:

        raise HTTPException(
            status_code=400,
            detail="Account is already activated"
        )

    token = secrets.token_urlsafe(32)

    activation = ActivationToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.add(activation)
    db.commit()

    send_activation_email(
        user.email,
        token
    )

    return {
        "message": "Activation link sent to your registered email"
    }


@router.get("/activate/verify")
def verify_activation(
    token: str,
    db: Session = Depends(get_db)
):

    activation = db.query(
        ActivationToken
    ).filter(
        ActivationToken.token == token,
        ActivationToken.used == False
    ).first()

    if not activation:

        raise HTTPException(
            status_code=400,
            detail="Invalid activation link"
        )

    if activation.expires_at < datetime.utcnow():

        raise HTTPException(
            status_code=400,
            detail="Activation link expired"
        )

    return {
        "message": "Activation link is valid",
        "token": token
    }


@router.post("/set-password")
def set_password(
    request: SetPasswordRequest,
    db: Session = Depends(get_db)
):

    activation = db.query(
        ActivationToken
    ).filter(
        ActivationToken.token == request.token,
        ActivationToken.used == False
    ).first()

    if not activation:

        raise HTTPException(
            status_code=400,
            detail="Invalid activation token"
        )

    if activation.expires_at < datetime.utcnow():

        raise HTTPException(
            status_code=400,
            detail="Activation token expired"
        )

    user = db.query(User).filter(
        User.id == activation.user_id
    ).first()

    user.password_hash = hash_password(
        request.password
    )

    user.email_verified = True

    activation.used = True

    db.commit()

    return {
        "message": "Account activated successfully"
    }


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email.lower()
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.email_verified:

        raise HTTPException(
            status_code=403,
            detail="Please activate your account first"
        )

    if not user.password_hash:

        raise HTTPException(
            status_code=403,
            detail="Please create your password first"
        )

    if not verify_password(
        request.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "name": user.name
    }


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email.lower()
    ).first()

    # Don't reveal whether the email exists.
    if user:

        token = secrets.token_urlsafe(32)

        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )

        db.add(reset_token)
        db.commit()

        send_password_reset_email(
            user.email,
            token
        )

    return {
        "message": (
            "If an account exists for this email, "
            "a password reset link has been sent."
        )
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    reset = db.query(
        PasswordResetToken
    ).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.used == False
    ).first()

    if not reset:

        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )

    if reset.expires_at < datetime.utcnow():

        raise HTTPException(
            status_code=400,
            detail="Reset token expired"
        )

    user = db.query(User).filter(
        User.id == reset.user_id
    ).first()

    user.password_hash = hash_password(
        request.password
    )

    reset.used = True

    db.commit()

    return {
        "message": "Password reset successfully"
    }


@router.get("/me")
def get_me(
    current_user: User = Depends(
        __import__(
            "auth.dependencies",
            fromlist=["get_current_user"]
        ).get_current_user
    )
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "department": current_user.department
    }