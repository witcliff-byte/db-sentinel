from dbsentinel.config import load_config
from dbsentinel.backup import run_backup
from dbsentinel.rotate import rotate

cfg = load_config("config.yml")
for db in cfg["mysql"]["databases"]:
    run_backup(cfg, db)

rotate(cfg["backup"]["directory"], cfg["backup"]["retention_days"], dry_run=False)
