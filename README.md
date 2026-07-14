# db-sentinel

**Automated MySQL backup, verification and monitoring for on-premise environments.**

I run backup automation for business-critical MySQL databases every day. db-sentinel is built from
scratch, test-driven, and designed around one principle:

> **A backup you never restored is not a backup. It's a hope.**

## What it does

- **Per-database dumps** with `mysqldump`, compressed and timestamped
- **Retention policy** — old backups rotated out automatically (configurable)
- **Restore verification** — restores each backup into a scratch database and
  checks integrity, so you *know* your backups work
- **Health monitoring** — verifies last night's backup ran and alerts
  (webhook/email) if anything is missing, too small, or failed
- **Deployable with Ansible** — one playbook installs and schedules everything
  on a clean Linux host

## Why on-premise

Cloud providers give you managed snapshots. On-premise, *you* are the backup
system. db-sentinel packages the discipline: dump → compress → rotate →
verify → alert, with no manual steps.

## Architecture

```
┌─────────────┐   cron    ┌────────────┐     ┌──────────────┐
│   MySQL     │──────────▶│  backup    │────▶│ backups/     │
│ (databases) │           │  + rotate  │     │ *.sql.gz     │
└─────────────┘           └────────────┘     └──────┬───────┘
                                                     │
                          ┌────────────┐             │
                          │  verify    │◀────────────┘
                          │ (restore   │
                          │  to scratch│──▶ health report ──▶ alert (webhook)
                          │  DB+check) │
                          └────────────┘
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yml config.yml   # edit with your settings
pytest                              # run the test suite
python -m dbsentinel.cli backup     # run a backup cycle
```

## Development

Built test-first (TDD): every feature starts as a failing test in `tests/`.
Run `pytest -v` to see the full behavior specification.

## Roadmap

- [ ] Backup encryption at rest
- [ ] Configurable storage backends (local disk today; S3-compatible next)
- [ ] Prometheus metrics endpoint

## License

MIT
