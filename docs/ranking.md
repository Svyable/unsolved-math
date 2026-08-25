# Ranking model

Ranking answers “which records best fit this repository's next bounded unit of
work?” It does not estimate mathematical importance or the probability of a
breakthrough.

## Research queue

Eligibility is a hard gate configured in `config/ranking.toml`. The default
gate excludes imported solved records, L4/L5 problems, and statements known to
be reconstructed or unrecoverable.

Eligible records receive a 0–100 score from six components:

| Component | Default weight | Interpretation |
|---|---:|---|
| Tractability | 30% | Conservative upstream difficulty fit |
| Statement quality | 20% | Exactness/recovery audit quality |
| Provenance | 15% | Presence of source URL and/or citation |
| Literature freshness | 10% | Age of the imported literature check |
| Research traction | 15% | Partial progress versus untriaged metadata |
| Computational affordance | 10% | Transparent keyword signal only |

Every output entry contains the component values and reasons. Keyword matches
are intentionally weak signals and are visible in the output.

## Status-review queue

This is a separate queue, scored by deterministic audit needs:

- disagreement between imported `status` and `research_classification`;
- missing or stale literature review dates;
- missing provenance;
- reconstructed or unrecoverable statements;
- suspicious instruction-like content in imported text.

High status-review rank means “verify soon,” not “research mathematically.”

## Changing the model

Change the TOML configuration in a reviewed pull request. A model change should
include:

1. the intended decision it improves;
2. before/after queue samples;
3. failure cases and category bias analysis;
4. a version increment;
5. tests for any new hard gate.
