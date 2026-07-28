import gzip
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from dbsentinel.backup import dump_env, ssl_flags


@dataclass
class VerifyResult:
    ok: bool
    tables_found: list
    error: str = ""


def build_restore_command(cfg, target_db):
    mysql = cfg["mysql"]
    return [
        "mysql",
        "--host",
        str(mysql["host"]),
        "--port",
        str(mysql.get("port", 3306)),
        "--user",
        str(mysql["user"]),
        *ssl_flags(cfg),
        target_db,
    ]


def _recreate_scratch_db(cfg):
    scratch = cfg["verify"]["scratch_database"]
    mysql = cfg["mysql"]
    cmd = [
        "mysql",
        "--host",
        str(mysql["host"]),
        "--user",
        str(mysql["user"]),
        *ssl_flags(cfg),
        "-e",
        f"DROP DATABASE IF EXISTS {scratch}; CREATE DATABASE {scratch};",
    ]
    subprocess.run(cmd, env=dump_env(cfg), check=True)


def _restore(cfg, target_db, backup_path):
    cmd = build_restore_command(cfg, target_db)

    opener = gzip.open if str(backup_path).endswith(".gz") else open

    with opener(backup_path, "rb") as f:
        data = f.read()

    subprocess.run(cmd, input=data, env=dump_env(cfg), check=True)


def _list_tables(cfg, database):
    mysql = cfg["mysql"]
    cmd = [
        "mysql",
        "--host",
        str(mysql["host"]),
        "--user",
        str(mysql["user"]),
        *ssl_flags(cfg),
        "-N",
        "-e",
        f"SHOW TABLES from {database}",
    ]
    resultado = subprocess.run(
        cmd, capture_output=True, text=True, env=dump_env(cfg), check=True
    )

    return resultado.stdout.splitlines()


def verify_backup(cfg, backup_path):
    _recreate_scratch_db(cfg)
    target_db = cfg["verify"]["scratch_database"]
    _restore(cfg, target_db, backup_path)
    resultado = _list_tables(cfg, target_db)
    return VerifyResult(ok=True, tables_found=resultado)


def health_report(cfg, today=None):
    today = today or date.today()
    directory = Path(cfg["backup"]["directory"])
    min_size = cfg["alerts"]["min_backup_size_bytes"]
    databases = cfg["mysql"]["databases"]

    report = {}
    for db in databases:
        matches = list(directory.glob(f"{db}_{today}*"))

        if not matches:
            report[db] = "missing"
        else:
            size = matches[0].stat().st_size
            if size < min_size:
                report[db] = "suspicious"
            else:
                report[db] = "ok"

    return report
