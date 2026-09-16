from datetime import datetime

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from models import User, WeeklyForm

from schemas import WeeklyFormRequest

from auth.dependencies import require_role


router = APIRouter(
    prefix="/api/student",
    tags=["Student"]
)


@router.get("/dashboard")
def student_dashboard(
    current_user: User = Depends(
        require_role("student")
    )
):

    return {
        "name": current_user.name,
        "roll_no": current_user.roll_no,
        "email": current_user.email,
        "department": current_user.department,
        "year": current_user.year,
        "section": current_user.section
    }


@router.post("/weekly-form")
def create_weekly_form(
    request: WeeklyFormRequest,
    current_user: User = Depends(
        require_role("student")
    ),
    db: Session = Depends(get_db)
):

    form = WeeklyForm(
        student_id=current_user.id,
        week_start=request.week_start,
        week_end=request.week_end,
        learning=request.learning,
        activities=request.activities,
        challenges=request.challenges,
        status="draft"
    )

    db.add(form)
    db.commit()
    db.refresh(form)

    return {
        "message": "Weekly form saved",
        "form_id": form.id,
        "status": form.status
    }


@router.post("/weekly-form/{form_id}/submit")
def submit_weekly_form(
    form_id: int,
    current_user: User = Depends(
        require_role("student")
    ),
    db: Session = Depends(get_db)
):

    form = db.query(WeeklyForm).filter(
        WeeklyForm.id == form_id,
        WeeklyForm.student_id == current_user.id
    ).first()

    if not form:

        return {
            "message": "Form not found"
        }

    form.status = "submitted"
    form.submitted_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Weekly form submitted",
        "status": "submitted"
    }