import re
from datetime import datetime


def parse_backup_date(filename: str):
    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}", filename)

    if not match:
        return None

    date_part = match.group(0)
    return datetime.strptime(date_part, "%Y-%m-%dT%H-%M").date()