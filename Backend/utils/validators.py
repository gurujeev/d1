import re
from typing import Dict, Any


# Allowed roles in Demo 1
ALLOWED_ROLES = {
    "student",
    "mentor",
    "coordinator",
    "attendance_operator",
    "hod",
}


# Required CSV columns
REQUIRED_CSV_COLUMNS = {
    "roll_no",
    "name",
    "email",
    "role",
    "department",
    "year",
    "section",
    "mentor_roll_no",
}


def validate_email(email: str) -> bool:
    """
    Basic college email validation.
    """

    if not email:
        return False

    email = email.strip().lower()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    """

    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must contain at least 8 characters"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain a number"

    return True, "Password is valid"


def validate_role(role: str) -> bool:
    """
    Check whether the role is allowed.
    """

    if not role:
        return False

    return role.strip().lower() in ALLOWED_ROLES


def validate_required_text(
    value: str,
    field_name: str
) -> str:

    if not value or not value.strip():
        raise ValueError(
            f"{field_name} is required"
        )

    return value.strip()


def validate_year(year: str | int | None) -> int | None:
    """
    Validate academic year.

    Allowed values:
    1, 2, 3, 4

    Empty value is allowed for roles such as coordinator.
    """

    if year is None:
        return None

    if isinstance(year, str):

        year = year.strip()

        if not year:
            return None

    try:
        year = int(year)

    except (ValueError, TypeError):

        raise ValueError(
            "Year must be a number"
        )

    if year not in {1, 2, 3, 4}:

        raise ValueError(
            "Year must be between 1 and 4"
        )

    return year


def validate_csv_columns(
    columns: list[str]
) -> None:

    actual_columns = {
        column.strip().lower()
        for column in columns
        if column
    }

    missing = REQUIRED_CSV_COLUMNS - actual_columns

    if missing:

        raise ValueError(
            "Missing CSV columns: "
            + ", ".join(sorted(missing))
        )


def validate_csv_row(
    row: Dict[str, Any],
    row_number: int
) -> Dict[str, Any]:

    # -------------------------
    # Name
    # -------------------------

    name = row.get("name", "").strip()

    if not name:

        raise ValueError(
            f"Row {row_number}: name is required"
        )


    # -------------------------
    # Email
    # -------------------------

    email = row.get("email", "").strip().lower()

    if not validate_email(email):

        raise ValueError(
            f"Row {row_number}: invalid email '{email}'"
        )


    # -------------------------
    # Role
    # -------------------------

    role = row.get("role", "").strip().lower()

    if not validate_role(role):

        raise ValueError(
            f"Row {row_number}: invalid role '{role}'"
        )


    # -------------------------
    # Department
    # -------------------------

    department = row.get(
        "department",
        ""
    ).strip()

    if not department:

        raise ValueError(
            f"Row {row_number}: department is required"
        )


    # -------------------------
    # Year
    # -------------------------

    year = validate_year(
        row.get("year")
    )


    # -------------------------
    # Section
    # -------------------------

    section = row.get(
        "section",
        ""
    ).strip() or None


    # -------------------------
    # Roll number
    # -------------------------

    roll_no = row.get(
        "roll_no",
        ""
    ).strip() or None


    # -------------------------
    # Mentor
    # -------------------------

    mentor_roll_no = row.get(
        "mentor_roll_no",
        ""
    ).strip() or None


    # -------------------------
    # Role-specific validation
    # -------------------------

    if role == "student":

        if not roll_no:

            raise ValueError(
                f"Row {row_number}: "
                "student must have roll_no"
            )

        if not mentor_roll_no:

            raise ValueError(
                f"Row {row_number}: "
                "student must have mentor_roll_no"
            )

        if year is None:

            raise ValueError(
                f"Row {row_number}: "
                "student must have year"
            )


    elif role == "mentor":

        if not roll_no:

            raise ValueError(
                f"Row {row_number}: "
                "mentor must have roll_no"
            )


    elif role in {
        "coordinator",
        "attendance_operator",
        "hod"
    }:

        # These roles don't necessarily require
        # academic year/section.
        pass


    return {
        "roll_no": roll_no,
        "name": name,
        "email": email,
        "role": role,
        "department": department,
        "year": year,
        "section": section,
        "mentor_roll_no": mentor_roll_no,
    }