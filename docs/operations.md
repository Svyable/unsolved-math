# Operations

## Daily sync

The scheduled workflow is intentionally review-gated. It updates one automation
branch and one pull request rather than committing directly to `main`.

Review a sync pull request in this order:

1. Confirm the upstream repository and immutable commit in `manifest.json`.
2. Inspect `sync-summary.md` for record counts and status changes.
3. Treat every status change as an external claim requiring follow-up.
4. Review large ranking movements for schema or scoring regressions.
5. Run CI, then merge only if the derived artifacts are internally consistent.

## Manual offline sync

```bash
uv run oplab sync --local-path /path/to/problems.json --source-revision <known-sha>
```

For a local file without a supplied revision, the CLI creates a
`local-<sha256>` revision. This is reproducible but does not claim a Hugging Face
identity.

## Recovery

- If upstream schema changes, the sync fails before replacing tracked data.
- If a scheduled PR is wrong, close it; `main` remains unchanged.
- If the automation branch is stale, the next scheduled run refreshes it from
  the latest `main`.
- Never delete raw snapshots needed to reproduce an accepted sync until a
  durable artifact-retention policy exists.
