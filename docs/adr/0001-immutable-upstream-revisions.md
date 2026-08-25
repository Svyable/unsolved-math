# ADR 0001: Resolve mutable upstream names to immutable commits

Status: accepted

## Decision

Resolve `main` or a tag through the Hugging Face API and store the returned
commit SHA before downloading data. Address raw snapshots by that SHA and
record source-file SHA-256 separately.

## Consequences

Runs can be reproduced even after upstream `main` moves. A revision label alone
is never sufficient provenance. Network sync requires explicit permission.
