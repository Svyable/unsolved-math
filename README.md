# Unsolved Math Research Queue

An evidence-first, local-first workbench for tracking the
[`ulamai/UnsolvedMath`](https://huggingface.co/datasets/ulamai/UnsolvedMath)
dataset and producing transparent queues of open problems worth reviewing or
investigating.

> **Agent output and imported status metadata are unverified research
> assistance, not mathematical results.** A dataset label, automated ranking,
> experiment, or model response never establishes that a problem is open or
> solved.

The upstream collection changes over time. This repository therefore pins each
sync to an immutable Hugging Face commit, hashes the source file and every
normalized record, records status changes as external claims, and proposes all
tracked updates through a pull request for human review.

## What this first slice does

- Resolves `ulamai/UnsolvedMath` to an immutable upstream commit.
- Stores an immutable raw snapshot locally (raw data is not committed).
- Builds a compact, deterministic status index containing provenance—not full
  problem text.
- Records upstream status changes without promoting them to verified facts.
- Produces two explainable queues:
  - **research candidates**: scoped, lower-difficulty, adequately sourced
    records with reproducible avenues for progress;
  - **status-review candidates**: stale, conflicting, malformed, or weakly
    sourced records that need human literature review.
- Runs a daily GitHub Action that opens or refreshes a sync pull request only
  when the immutable upstream revision changes.
- Defines a bounded, two-lane research-cycle contract: every accepted cycle
  must advance both theory exploration and independent progress verification.

The initial upstream inspection on 2026-08-25 found dataset version 1.6.0 with
15,458 records. That number is documentation only; the software never assumes
it is current.

## Quick start

Requirements: Python 3.12 and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras

# Offline and reproducible: import an already downloaded problems.json.
uv run oplab sync --local-path /path/to/problems.json

# Network use is explicit. `main` is resolved to a commit SHA before import.
uv run oplab sync --revision main --allow-network

uv run oplab status
uv run oplab problems search --status open --max-difficulty 3 --limit 20
uv run oplab validate
```

Local immutable snapshots live under `.oplab/snapshots/` and are ignored by
Git. Derived review artifacts live under `data/`:

```text
data/
  current/
    manifest.json
    problems.jsonl
    sync-summary.md
  queues/
    research.json
    research.md
    status-review.json
    status-review.md
  status-history.jsonl
```

## Ranking contract

Ranking is deterministic and inspectable. It uses only explicitly configured
metadata features; it does not ask an LLM which problems look promising.
Default research eligibility is deliberately narrow:

- imported status is `open` or `partially_solved`;
- difficulty is L1–L3;
- the statement is not flagged `reconstructed_unverified` or `unrecoverable`;
- every score includes its component values and human-readable reasons.

Weights and keyword signals are in [`config/ranking.toml`](config/ranking.toml).
They are hypotheses about research fit, not mathematical judgments. See
[`docs/ranking.md`](docs/ranking.md) before changing them.

## Breakthrough loop contract

The hourly loop is designed to compound verified insight, not manufacture
activity. A cycle is material only when both lanes contain hashed evidence:

1. **Theory exploration** — a new falsifiable hypothesis, assumption reduction,
   equivalent formulation, reproducible experiment, or other concrete advance.
2. **Independent verification** — a counterexample search, primary-source
   check, proof-gap audit, reproduction, or formal check performed without
   accepting the theory lane's conclusion.

Cycles use cooldown and anti-thrashing gates, remain explicitly unresolved,
and are proposed through a single review PR. See
[`docs/hourly-loop.md`](docs/hourly-loop.md) and
[`config/research-loop.toml`](config/research-loop.toml).

```bash
uv run oplab loop next
uv run oplab loop validate-cycle cases/<problem-id>/cycles/<cycle-id>
uv run oplab loop build-manifest cases/<problem-id>/cycles/<cycle-id>
uv run oplab loop record-cycle cases/<problem-id>/cycles/<cycle-id>
```

## Scheduled synchronization

`.github/workflows/sync.yml` runs daily and can also be started manually. It:

1. resolves the upstream `main` revision to a commit SHA;
2. exits without changing files when that SHA is already indexed;
3. rebuilds the status index and queues when the SHA changes;
4. pushes the result to `automation/unsolvedmath-sync`;
5. opens or refreshes a pull request for human review.

The workflow never writes to Hugging Face, UnsolvedMath, papers, forums, or
social media. Merging a sync PR means only “accept this imported snapshot,” not
“verify these mathematical statuses.”

## Development

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

Architecture, operating procedures, and research-integrity boundaries are in
[`docs/`](docs/). The next planned slice is a human-owned review ledger with
primary-source evidence and named reviewer sign-off; the loop cannot substitute
for that review.

## Licensing and attribution

Repository code is MIT licensed. UnsolvedMath curation and original metadata
are CC BY 4.0; linked source material retains its own terms. Derived artifacts
must retain the upstream dataset identifier, revision, retrieval time, and
checksums recorded in `manifest.json`.
