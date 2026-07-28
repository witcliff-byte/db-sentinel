
import pytest

from dbsentinel.config import ConfigError, load_config


def _write(tmp_path, text):
    p = tmp_path / "config.yml"
    p.write_text(text)
    return p


def test_loads_a_minimal_valid_config(tmp_path):
    path = _write(tmp_path, """
mysql:
  host: localhost
  user: backup_user
  databases: [app_db]
backup:
  directory: /tmp/backups
  retention_days: 7
""")
    cfg = load_config(path)
    assert cfg["mysql"]["host"] == "localhost"
    assert cfg["mysql"]["databases"] == ["app_db"]
    assert cfg["backup"]["retention_days"] == 7


def test_missing_file_raises_config_error(tmp_path):
    with pytest.raises(ConfigError):
        load_config(tmp_path / "does_not_exist.yml")


def test_missing_required_section_raises(tmp_path):
    path = _write(tmp_path, "mysql: {host: localhost}") 
    with pytest.raises(ConfigError):
        load_config(path)


def test_retention_days_must_be_positive(tmp_path):
    path = _write(tmp_path, """
mysql: {host: localhost, user: u, databases: [x]}
backup: {directory: /tmp/b, retention_days: 0}
""")
    with pytest.raises(ConfigError):
        load_config(path)
