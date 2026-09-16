import csv
import io

from sqlalchemy.orm import Session

from models import User


REQUIRED_COLUMNS = {
    "roll_no",
    "name",
    "email",
    "role",
    "department",
    "year",
    "section",
    "mentor_id"
}


def import_users_from_csv(
    file_content: bytes,
    db: Session
):

    text = file_content.decode("utf-8-sig")

    reader = csv.DictReader(
        io.StringIO(text)
    )

    if not reader.fieldnames:

        raise ValueError(
            "CSV has no header"
        )

    missing = REQUIRED_COLUMNS - set(
        reader.fieldnames
    )

    if missing:

        raise ValueError(
            f"Missing columns: {', '.join(missing)}"
        )

    imported = 0
    updated = 0

    rows = list(reader)

    # First pass: create/update users
    for row in rows:

        email = row["email"].strip().lower()

        existing = db.query(User).filter(
            User.email == email
        ).first()

        if existing:

            existing.name = row["name"].strip()
            existing.role = row["role"].strip().lower()
            existing.department = row["department"].strip()
            existing.section = row["section"].strip()

            if row["year"].strip():
                existing.year = int(row["year"])

            updated += 1

        else:

            user = User(
                roll_no=row["roll_no"].strip() or None,
                name=row["name"].strip(),
                email=email,
                role=row["role"].strip().lower(),
                department=row["department"].strip(),
                year=int(row["year"]) if row["year"].strip() else None,
                section=row["section"].strip() or None,
                email_verified=False,
                is_active=True
            )

            db.add(user)

            imported += 1

    db.commit()

    return {
        "imported": imported,
        "updated": updated,
        "total_rows": len(rows)
    }