## Local MySQL setup for development

Tested on Rocky Linux 9 (RHEL-compatible), also works on Ubuntu.

### 1. Install MySQL Server
​```bash
sudo dnf install -y mariadb-server
sudo systemctl enable --now mariadb
​```
or
​```bash
sudo apt install -y mysql-server
sudo systemctl enable --now mysql
​```

### 2. Create the sample databases
Two databases are used throughout development and in the integration tests:
`app_db` (a generic customers/orders schema) and `leads_db` (a generic
lead-capture schema). Both are illustrative only — not derived from any
employer's real data or schema.

​```bash
sudo mysql < docs/sql/app_db.sql
sudo mysql < docs/sql/leads_db.sql
​```

### 3. Create a dedicated backup user (least privilege)
db-sentinel never needs write access — only enough to read and lock tables for a consistent dump.
​```sql
CREATE USER 'backup_user'@'localhost' IDENTIFIED BY 'change_me';
GRANT SELECT, LOCK TABLES, SHOW VIEW, PROCESS ON *.* TO 'backup_user'@'localhost';
FLUSH PRIVILEGES;
​```

### 4. Running the integration tests

Integration tests are deselected by default (`pytest -m "not integration"`) since
they need a reachable MySQL/MariaDB server. Point them at your server via
environment variables — never hardcode credentials in the test files:

​```bash
DBS_TEST_HOST=<ip> DBS_TEST_PORT=3306 DBS_TEST_USER=backup_user DBS_TEST_PASSWORD=<pass> pytest -m integration -v
​```

Unset variables fall back to `127.0.0.1:3306` / `backup_user` with an empty
password, suitable for a local dev server with no password set.