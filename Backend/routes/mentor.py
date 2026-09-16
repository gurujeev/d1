from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from models import User

from auth.dependencies import require_role


router = APIRouter(
    prefix="/api/mentor",
    tags=["Mentor"]
)


@router.get("/dashboard")
def mentor_dashboard(
    current_user: User = Depends(
        require_role("mentor")
    ),
    db: Session = Depends(get_db)
):

    students = db.query(User).filter(
        User.mentor_id == current_user.id,
        User.role == "student"
    ).all()

    return {
        "mentor": current_user.name,
        "students": [
            {
                "id": student.id,
                "roll_no": student.roll_no,
                "name": student.name,
                "email": student.email,
                "year": student.year,
                "section": student.section
            }
            for student in students
        ]
    }