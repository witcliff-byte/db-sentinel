## Local MySQL setup for development

Tested on Rocky Linux 9 (RHEL-compatible), also works on Ubuntu.

### 1. Install MySQL Server
​```bash
sudo dnf install -y mysql-server
sudo systemctl enable --now mysqld
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