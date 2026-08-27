# Fresh execution, adversarial checks, and dependency review

## Independence basis

`python -I verify.py` reads only `input.json` and runs in a fresh isolated process.
It does not import the theory program, read its certificate orders, or accept its
classification. Instead of subset-degree hole recognition it builds explicit
cycle edge/chord masks. Instead of peeling it checks every induced subgraph's
minimum degree. Instead of inferring ordinary chromatic numbers from a structural
class it enumerates color assignments. Both executables are deterministic and
standard-library-only. Both were written by the same assistant: independence is
algorithmic and execution-context based, NOT independent human or model review.

## Counterexamples and boundaries first

Before the main enumeration, test all 64 assignments of the K2,4 two-list fixture:
none is proper. Independently compute chi=2 and degeneracy=2. Each of its eight
single-edge deletions restores a coloring for those fixed lists. This verifies
an edge-sensitive obstruction and rejects the broader 2-degenerate/bipartite
shortcut, not the intended even-hole-free claim.

Nine controls cover C4 rejection, acceptance of a chorded C4 by the hole recognizer,
C5 acceptance, K4 without triangle-freeness, K3,3 without even-hole-freeness, the
K2,4 obstruction, all eight edge-deletion repairs, null-graph value zero, and
nonempty edgeless value one. The chorded C4 is tested only for hole recognition;
its triangle correctly excludes it from the target class.

## Independent finite computation

All 33,868 simple labelled graphs on 0..6 vertices were considered. The 3,716
accepted graphs have degeneracy at most two. Explicit coloring search returns
the same classifications as the theory lane. The two independently generated
streams of [n, edge-mask, chromatic number, degeneracy] have the same SHA-256:
`2ddc43d4eabcab5a6e8990b61fc5bde0c69c381e8e4e251a38da62de583d80e0`.
This digest is computed during replay; the theory also stores the peeling orders.

Counts by n=0,1,2,3,4,5,6 are 1,1,2,7,38,303,3364. There are 444 accepted cyclic
graphs (12 on five vertices and 432 on six). No finite violation was found.

This is not exhaustive enumeration of arbitrary list assignments. The latter
upper bound follows from the supplied order and the reverse-greedy argument;
independent ordinary coloring search supplies finite lower bounds. Conflating
ordinary coloring with choosability would be an invalid proof step.

After the fresh search completes, `check_certificates.py` independently validates
all 3,716 stored removal orders using edge sets. It detects a duplicated vertex
and a center-first star order that exceeds the allowed width, then matches the
entire certificate classification digest to the fresh enumeration. This second
phase intentionally reads theory certificates; it does not supply inputs to the
earlier independent search. Its separate output is `certificate-check-output.json`.

## Primary-source and proof-step checks

The AIM PDF placement confirms a splice across prose, not a complete statement
of its actual Conjecture 2. The author-hosted replacement paper identifies the
older proof's clique-transfer error and states the needed theorem; its June 26,
2024 revision is distinct from arXiv v2 (May 15, 2020). Full provenance is in
`sources.json`. Primary texts were inspected independently of imported summaries.
Their entire proofs were NOT reverified, and the PDFs were not redistributed.

The local proof-step audit checks: hereditary hypotheses; neighborhood independence;
the two-clique size bound; reverse rather than forward use of the removal order;
the quantifier over arbitrary lists; identical-list lower bounds; shortest-cycle
chordlessness and odd parity; and the explicit null-graph convention. These are
mathematical arguments, not Lean-accepted lemmas or independent human review.

## Remaining objections

The canonical record still lacks a conclusion. An unbounded result depends on
the external theorem and the unformalized corollary argument. Small-case agreement
does not validate that long proof. The evidence supports this bounded audit and
human review of the fragment, not a claim of a new solved problem.
