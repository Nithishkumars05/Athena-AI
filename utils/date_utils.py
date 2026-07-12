from datetime import datetime


def group_from_date(date_string: str):

    try:

        date = datetime.fromisoformat(date_string)

    except Exception:

        return "Older"

    now = datetime.now()

    days = (now.date() - date.date()).days

    if days == 0:
        return "Today"

    if days == 1:
        return "Yesterday"

    if days <= 7:
        return "Previous 7 Days"

    if days <= 30:
        return "Previous 30 Days"

    return "Older"