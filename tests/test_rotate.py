from datetime import date
from dbsentinel.rotate import parse_backup_date

def test_parses_date_from_filename():
    resultado = parse_backup_date("app_db_2026-07-20T06-00.sql.gz")
    assert resultado == date(2026, 7, 20)

def test_filename_not_match():
    resultado = parse_backup_date("random.txt")
    assert resultado is None
