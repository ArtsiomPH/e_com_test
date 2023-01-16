import datetime
import re
from email_validator import validate_email, EmailNotValidError


def is_date(value: str) -> bool:
    try:
        datetime.datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False
        else:
            return True
    else:
        return True


def is_phone_number(value: str) -> bool:
    pattern = r"^(\+| )7(\s{1}\d{3}\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}$)"
    result = re.search(pattern, value)

    if result is not None and result.string == value:
        return True
    return False


def is_email(value: str) -> bool:
    try:
        validate_email(value)
    except EmailNotValidError:
        return False
    return True
