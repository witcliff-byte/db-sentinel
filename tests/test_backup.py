"""Tests for the backup module.

Written test-first, following the config module as the model. The guiding
split of this phase: build_dump_command / backup_filename are PURE functions
(no I/O) and are unit-tested here; run_backup shells out to mysqldump and is
covered by an @pytest.mark.integration test that only runs with a live server.
"""
from dbsentinel.backup import build_dump_command


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
    assert cmd[cmd.index("--port") + 1] == "3306"      # coerced to string for argv
    assert cmd[cmd.index("--user") + 1] == "backup_user"


def test_build_dump_command_ends_with_the_database_name():
    # The database is the final positional argument to mysqldump.
    cmd = build_dump_command(_cfg(), "app_db")
    assert cmd[-1] == "app_db"
