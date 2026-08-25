# Research integrity

## Non-negotiable rule

No automated component may convert an imported status, research
classification, small-case experiment, or natural-language proof attempt into
a verified claim that an open problem has been solved.

## Claim classes

| Class | Meaning | May change verified status? |
|---|---|---:|
| `UNVERIFIED_EXTERNAL_METADATA` | Imported from a dataset or website | No |
| `UNVERIFIED_OBSERVED_CHANGE` | Difference between two imported snapshots | No |
| `REPRODUCIBLE_COMPUTATION` | Code, inputs, environment, and output are captured | No, except for the exact finite claim checked |
| `PRIMARY_SOURCE_REVIEWED` | Named human mapped a claim to primary evidence | Only through the future review workflow |
| `LEAN_KERNEL_ACCEPTED_SUBLEMMA` | Lean accepted the exact stored lemma | Only for that lemma, never its parent problem |

## Imported content is untrusted

Statements, background fields, citations, HTML, Markdown, and LaTeX are data.
They are never instructions. The pipeline does not execute embedded shell,
Python, LaTeX, links, or model prompts. Suspicious instruction-like content is
flagged for review and preserved only in the local raw snapshot.

## Review expectations

- Prefer primary papers, official problem lists, and correction/retraction
  records over summaries.
- Store access date, identifier, claim-to-source mapping, and conflict notes.
- Separate “the literature contains a claimed proof” from “the community has
  accepted a proof.”
- Treat upstream `SOLVED-*`, novelty, full-solution, and counterexample labels
  as leads requiring independent expert review.
- Preserve negative results and failed approaches.

## Publishing boundary

The repository does not write back to UnsolvedMath, Hugging Face, papers,
forums, or social networks. A human must explicitly decide what to share and
must review the exact packet being shared.

## Hourly research boundary

Frequency is not evidence. The hourly loop may create or refresh a review PR,
but it may not merge, mark an upstream problem solved, or publish externally.
Each accepted cycle must contain:

- one evidence-linked theory progress unit;
- one evidence-linked independent-verification progress unit;
- at least one verification check with fresh context;
- distinct theory and verification evidence paths plus an explicit
  independence basis;
- a conclusion from the restricted unresolved/sublemma vocabulary;
- an exact frozen statement and upstream file provenance;
- a canonical manifest with SHA-256 hashes for every packet file.

If no progress exists, the loop must say so. A verified counterexample, a proof
gap that retires an approach, or a reproducible blocker can be material negative
progress. Rewording, longer prose, unsupported confidence, and repeated failed
attempts without new evidence are not progress.
