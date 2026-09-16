from datetime import datetime

from sqlalchemy.orm import Session

from models import WeeklyReport


def generate_weekly_report(
    week_start: str,
    week_end: str,
    coordinator_id: int,
    db: Session
):

    existing = db.query(
        WeeklyReport
    ).filter(
        WeeklyReport.week_start == week_start,
        WeeklyReport.week_end == week_end
    ).first()

    if existing:

        return existing

    report = WeeklyReport(
        week_start=week_start,
        week_end=week_end,
        status="generated",
        generated_by=coordinator_id,
        generated_at=datetime.utcnow()
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report