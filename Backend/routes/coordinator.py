from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException
)

from sqlalchemy.orm import Session

from database import get_db
from models import User

from auth.dependencies import require_role
from services.csv_service import import_users_from_csv


router = APIRouter(
    prefix="/api/coordinator",
    tags=["Coordinator"]
)


@router.get("/dashboard")
def coordinator_dashboard(
    current_user: User = Depends(
        require_role("coordinator")
    )
):

    return {
        "message": "Coordinator dashboard",
        "name": current_user.name
    }


@router.post("/users/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(
        require_role("coordinator")
    ),
    db: Session = Depends(get_db)
):

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    content = await file.read()

    try:

        result = import_users_from_csv(
            content,
            db
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "message": "CSV imported successfully",
        **result
    }


@router.get("/users")
def get_users(
    current_user: User = Depends(
        require_role("coordinator")
    ),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "roll_no": user.roll_no,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "year": user.year,
            "section": user.section
        }
        for user in users
    ]