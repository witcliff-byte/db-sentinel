from dbsentinel.verify import build_restore_command

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
