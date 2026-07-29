# db-sentinel

**Automated MySQL/MariaDB backup, verification and monitoring for on-premise environments.**

Built from scratch, test-driven, around one principle:

> **A backup you never restored is not a backup. It's a hope.**

## What it does

- **Per-database dumps** with `mysqldump`, compressed and timestamped
- **Retention policy** — expired backups rotated out automatically, with a
`dry_run` mode to preview deletions before they happen
- **Restore verification** — restores a backup into a scratch database and
compares the resulting tables, so you *know* the backup is usable
- **Health reporting** — checks that today's backup exists for every configured
database and isn't suspiciously small; exits non-zero when something is wrong
- **Scheduled with cron** — nightly backup and a morning health check, both
validated against cron's minimal environment



## Why on-premise

Cloud providers give you managed snapshots. On-premise, *you* are the backup
system. db-sentinel packages the discipline: dump → compress → rotate →
verify → report, with no manual steps.

## Architecture

```
┌─────────────┐   cron    ┌────────────┐     ┌──────────────┐
│   MySQL     │─────────▶│  backup    │───▶│ backups/     │
│ (databases) │           │  + rotate  │     │ *.sql.gz     │
└─────────────┘           └────────────┘     └──────┬───────┘
                                                    │
                          ┌────────────┐            │
                          │  verify    │◀──────────┘
                          │ (restore   │
                          │  to scratch│──▶ health report ──▶ exit code
                          │  DB+check) │
                          └────────────┘
```



## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .                    # install the package itself
cp config.example.yml config.yml    # edit with your settings

pytest -v                           # unit tests (fast, no database needed)

python scripts/run_backup.py        # dump every configured database + rotate
python scripts/run_health_check.py  # report on today's backups
```

Integration tests need a reachable MySQL/MariaDB server and are excluded by
default. To run them:

```bash
DBS_TEST_HOST=<ip> DBS_TEST_USER=<user> DBS_TEST_PASSWORD=<pass> \
  pytest -m integration -v
```



## Development

Built test-first (TDD): every feature started as a failing test in `tests/`.
Run `pytest -v` to read the full behaviour specification.

Design notes:

- **Pure logic is separated from I/O.** Functions that *decide* (building a
command, finding expired files, producing a health report) are pure and test
in microseconds; only a thin layer actually touches the database or disk.
- **Time is injected, not read.** Functions take `today=`/`when=` parameters so
date-dependent behaviour is deterministic under test.
- **Secrets stay out of process arguments.** The password travels via
`MYSQL_PWD`, never in the command line, where `ps aux` would expose it — and
there's a regression test guarding that.



## Known limitations

Deliberate trade-offs:

- **Restore loads the dump into memory.** Fine for the dump sizes this was
built against; multi-gigabyte dumps would need streaming via `Popen` instead.
- **TLS is configurable and defaults to on.** The development VM has no TLS
configured, so `ssl: false` is set there explicitly — production defaults are
safe unless deliberately overridden.
- **No CLI yet.** Cron currently invokes small entry-point scripts under
`scripts/`; a proper `argparse` CLI is the next step.
- **Health reporting has no alerting channel.** It reports and exits non-zero;
wiring that to a webhook or monitoring system is next.



## Roadmap

- [ ] CLI with `argparse` (`backup` / `rotate` / `verify` / `health` subcommands)
- [ ] Webhook alerting on health check failures
- [ ] Streaming restore for large dumps
- [ ] Ansible playbook for one-command deployment
- [ ] Backup encryption at rest
- [ ] Configurable storage backends (local disk today; S3-compatible next)



## License

MIT — see [LICENSE](LICENSE).