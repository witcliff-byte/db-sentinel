"""Backup module — build and execute MySQL dumps.

Design: the *logic* of composing a command line is a pure function
(build_dump_command) so it can be unit-tested without a database. The *effect*
of running it lives in run_backup, which is covered by integration tests.
"""
from datetime import datetime


def build_dump_command(cfg, database):
    """Return the mysqldump argv (a list of strings) for one database.

    The password is deliberately NOT included here — it travels via the
    environment (MYSQL_PWD) at execution time, so it never shows up in the
    process argument list that anyone can read with `ps aux`.
    """
    mysql = cfg["mysql"]
    return [
        "mysqldump",
        "--host", str(mysql["host"]),
        "--port", str(mysql.get("port", 3306)),
        "--user", str(mysql["user"]),
        "--single-transaction",   # consistent snapshot without locking writes out
        "--routines",             # include stored procedures and functions
        database,                 # positional: the database name comes last
    ]


def backup_filename(database, when=None):
    """Return a timestamped backup filename, e.g. 'app_db_2026-07-20T06-00.sql'.

    `when` is injected so callers (and tests) control the clock; it defaults to
    the current time only in real use. The timestamp avoids ':' so the name is
    safe on every filesystem.
    """
    when = when or datetime.now()
    stamp = when.strftime("%Y-%m-%dT%H-%M")
    return f"{database}_{stamp}.sql"
