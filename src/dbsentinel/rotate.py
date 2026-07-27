import re
from datetime import datetime, timedelta
from pathlib import Path


def parse_backup_date(filename: str):
    match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}", filename)

    if not match:
        return None

    date_part = match.group(0)
    return datetime.strptime(date_part, "%Y-%m-%dT%H-%M").date()


def find_expired(files, retention_days, today=None):
    today = today or date.today()
    cutoff = today - timedelta(days=retention_days)
    expired = []
    for filename in files:
        file_date = parse_backup_date(filename)

        if file_date is None:
            continue

        if file_date < cutoff:
            expired.append(filename)

    return expired


def rotate(directory, retention_days, dry_run=False, today=None):
    all_backups = list(Path(directory).glob("*.sql.gz"))
    names = [p.name for p in all_backups]

    expired_names = find_expired(names, retention_days, today)

    expired_paths = [p for p in all_backups if p.name in expired_names]

    if not dry_run:
        for p in expired_paths:
            p.unlink()

    return expired_paths
