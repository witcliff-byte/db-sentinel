import gzip
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def ssl_flags(cfg):
    if cfg["mysql"].get("ssl", True):
        return []
    return ["--ssl=0"]


def build_dump_command(cfg, database):
    mysql = cfg["mysql"]
    return [
        "mysqldump",
        "--host",
        str(mysql["host"]),
        "--port",
        str(mysql.get("port", 3306)),
        "--user",
        str(mysql["user"]),
        *ssl_flags(cfg),
        "--single-transaction",
        "--routines",
        database,
    ]


def backup_filename(database, when=None):
    when = when or datetime.now()
    stamp = when.strftime("%Y-%m-%dT%H-%M")
    return f"{database}_{stamp}.sql"


def dump_env(cfg):
    env = dict(os.environ)
    password = cfg["mysql"].get("password")
    if password:
        env["MYSQL_PWD"] = str(password)
    return env


def compress_file(path):
    path = Path(path)
    gz_path = Path(str(path) + ".gz")
    with open(path, "rb") as src, gzip.open(gz_path, "wb") as dst:
        shutil.copyfileobj(src, dst)
        path.unlink()
        return gz_path


def run_backup(cfg, database, when=None):
    directory = Path(cfg["backup"]["directory"])
    directory.mkdir(parents=True, exist_ok=True)
    out_path = directory / backup_filename(database, when)
    cmd = build_dump_command(cfg, database)
    with open(out_path, "wb") as fh:
        subprocess.run(cmd, stdout=fh, env=dump_env(cfg), check=True)
        if cfg["backup"].get("compress"):
            out_path = compress_file(out_path)
    return out_path
