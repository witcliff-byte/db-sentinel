from datetime import date
from dbsentinel.rotate import parse_backup_date, find_expired

def test_parses_date_from_filename():
    resultado = parse_backup_date("app_db_2026-07-20T06-00.sql.gz")
    assert resultado == date(2026, 7, 20)

def test_filename_not_match():
    resultado = parse_backup_date("random.txt")
    assert resultado is None

def test_finds_a_file_older_than_retention():
    files = ["app_db_2026-07-01T06-00.sql.gz"]
    resultado = find_expired(files, retention_days=7, today=date(2026, 7, 20))
    assert resultado == ["app_db_2026-07-01T06-00.sql.gz"]

def test_ignores_files_within_retention():
    files = [
        "app_db_2026-07-01T06-00.sql.gz",
        "app_db_2026-07-19T06-00.sql.gz",
    ]
    resultado = find_expired(files, retention_days=7, today=date(2026, 7, 20))
    assert resultado == ["app_db_2026-07-01T06-00.sql.gz"]

def test_ignores_files_that_dont_match_the_pattern():
    files = [
        "app_db_2026-07-01T06-00.sql.gz",
        "random.txt",
    ]
    resultado = find_expired(files, retention_days=7, today=date(2026, 7, 20))
    assert resultado == ["app_db_2026-07-01T06-00.sql.gz"]