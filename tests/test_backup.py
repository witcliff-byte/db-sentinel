import os
from datetime import datetime
import pytest
import gzip
from dbsentinel.backup import (
    backup_filename,
    build_dump_command,
    compress_file,
    run_backup,
)

def _cfg():
    return {
        "mysql": {
            "host": "localhost",
            "port": 3306,
            "user": "backup_user",
            "databases": ["app_db"],
        },
        "backup": {"directory": "/tmp/backups"},
    }

def test_build_dump_command_starts_with_mysqldump():
    cmd = build_dump_command(_cfg(), "app_db")
    assert cmd[0] == "mysqldump"

def test_build_dump_command_carries_connection_flags():
    cmd = build_dump_command(_cfg(), "app_db")
    assert cmd[cmd.index("--host") + 1] == "localhost"
    assert cmd[cmd.index("--port") + 1] == "3306"
    assert cmd[cmd.index("--user") + 1] == "backup_user"

def test_build_dump_command_ends_with_the_database_name():
    cmd = build_dump_command(_cfg(), "app_db")
    assert cmd[-1] == "app_db"

def test_password_never_leaks_into_the_command_line():
    cfg = _cfg()
    cfg["mysql"]["password"] = "sup3r-s3cret"
    cmd = build_dump_command(cfg, "app_db")
    assert "sup3r-s3cret" not in cmd
    assert not any ("password" in part.lower() for part in cmd)

def test_backup_filename_embeds_the_injected_timestamp():
    name = backup_filename("app_db", when=datetime(2026, 7, 20, 6, 0))
    assert name == "app_db_2026-07-20T06-00.sql"

def test_backup_filename_uses_colon_free_stamp_for_filesystem_safety():
    name = backup_filename("leads_db", when=datetime(2026, 1, 2, 23, 59))
    assert ":" not in name
    assert name == "leads_db_2026-01-02T23-59.sql"

def test_compress_file_gzips_and_removes_original(tmp_path):
    original = tmp_path / "app_db_2026-07-20T06-00.sql"
    original.write_text("CREATE TABLE t (id INT);\n")

    gz = compress_file(original)

    assert gz.name == "app_db_2026-07-20T06-00.sql.gz"
    assert not original.exists()

    with gzip.open(gz, "rt") as fh:
        assert fh.read() == "CREATE TABLE t (id INT);\n"

def _integration_cfg(tmp_path):
    return {
        "mysql": {
            "host": os.environ.get("NYSQL_HOST", "127.0.0.1"),
            "port": int(os.environ.get("MYSQL_PORT", "3306")),
            "user": os.environ.get("MYSQL_USER", "backup_user"),
            "password": os.environ.get("MYSQL_PWD", ""),
            "database": ["app_db"],
        },
        "backup": {"directory":str(tmp_path), "compress":False},
    }

@pytest.mark.integration
def test_run_backup_writes_a_dump_with_schema(tmp_path):
    path = run_backup(_integration_cfg(tmp_path), "app_db")
    assert path.exists()
    assert "CREATE TABLE" in path.read_text(errors="ignore")


    
