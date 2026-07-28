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
        target_db,
    ]
