import os
from datetime import date

import pytest

from dbsentinel.backup import run_backup
from dbsentinel.verify import build_restore_command, health_report, verify_backup


def _integration_cfg(tmp_path):
    return {
        "mysql": {
            "host": os.environ.get("DBS_TEST_HOST", "127.0.0.1"),
            "port": int(os.environ.get("DBS_TEST_PORT", "3306")),
            "user": os.environ.get("DBS_TEST_USER", "backup_user"),
            "ssl": False,
            "password": os.environ.get("DBS_TEST_PASSWORD", ""),
        },
        "backup": {"directory": str(tmp_path), "retention_days": 7, "compress": True},
        "verify": {"scratch_database": "dbsentinel_verify"},
    }


@pytest.mark.integration
def test_verify_backup_succeeds_for_a_real_dump(tmp_path):
    cfg = _integration_cfg(tmp_path)
    backup_path = run_backup(cfg, "app_db")
    result = verify_backup(cfg, backup_path)
    assert result.ok is True
    assert "customers" in result.tables_found
    assert "orders" in result.tables_found


CFG = {
    "mysql": {
        "host": "localhost",
        "port": 3306,
        "user": "backup_user",
        "password": "secret",
    },
}


def test_build_restore_command():
    resultado = build_restore_command(CFG, "dbsentinel_verify")
    assert resultado[0] == "mysql"
    assert "--host" in resultado
    assert resultado[-1] == "dbsentinel_verify"


def test_restore_command_never_leaks_the_password():
    resultado = build_restore_command(CFG, "dbsentinel_verify")
    assert "secret" not in " ".join(resultado)


def test_health_report_ok_when_todays_backup_exists(tmp_path):
    today = date(2026, 7, 29)
    backup_file = tmp_path / f"app_db_{today}T02-00.sql.gz"
    backup_file.write_text("x" * 2000)

    cfg = {
        "mysql": {"databases": ["app_db"]},
        "backup": {"directory": str(tmp_path)},
        "alerts": {"min_backup_size_bytes": 1024},
    }

    resultado = health_report(cfg, today=today)

    assert resultado == {"app_db": "ok"}


def test_health_report_missing_when_today_backups_not_exists(tmp_path):
    today = date(2026, 7, 29)

    cfg = {
        "mysql": {"databases": ["app_db"]},
        "backup": {"directory": str(tmp_path)},
        "alerts": {"min_backup_size_bytes": 1024},
    }

    resultado = health_report(cfg, today=today)

    assert resultado == {"app_db": "missing"}


def test_health_report_suspicious_when_size_not_match(tmp_path):
    today = date(2026, 7, 29)
    backup_file = tmp_path / f"app_db_{today}T02-00.sql.gz"
    backup_file.write_text("x" * 20)

    cfg = {
        "mysql": {"databases": ["app_db"]},
        "backup": {"directory": str(tmp_path)},
        "alerts": {"min_backup_size_bytes": 1024},
    }

    resultado = health_report(cfg, today=today)

    assert resultado == {"app_db": "suspicious"}
