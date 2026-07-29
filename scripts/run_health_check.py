import sys

from dbsentinel.config import load_config
from dbsentinel.verify import health_report


cfg = load_config("config.yml")
report = health_report(cfg)
print(report)

if any(status != "ok" for status in report.values()):
    sys.exit(1)
