from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db
from models import User, WeeklyForm

from auth.dependencies import require_role
from services.report_service import generate_weekly_report


router = APIRouter(
    prefix="/api/coordinator/weekly-reports",
    tags=["Weekly Reports"]
)


@router.get("/{week_start}/{week_end}")
def view_week(
    week_start: str,
    week_end: str,
    current_user: User = Depends(
        require_role("coordinator")
    ),
    db: Session = Depends(get_db)
):

    forms = db.query(WeeklyForm).filter(
        WeeklyForm.week_start == week_start,
        WeeklyForm.week_end == week_end
    ).all()

    return {
        "week_start": week_start,
        "week_end": week_end,
        "total_submissions": len(forms),
        "submissions": [
            {
                "id": form.id,
                "student_id": form.student_id,
                "status": form.status
            }
            for form in forms
        ]
    }


@router.post("/{week_start}/{week_end}/generate")
def generate_report(
    week_start: str,
    week_end: str,
    current_user: User = Depends(
        require_role("coordinator")
    ),
    db: Session = Depends(get_db)
):

    report = generate_weekly_report(
        week_start,
        week_end,
        current_user.id,
        db
    )

    return {
        "message": "Weekly report generated",
        "report_id": report.id,
        "week_start": report.week_start,
        "week_end": report.week_end,
        "generated_at": report.generated_at
    }