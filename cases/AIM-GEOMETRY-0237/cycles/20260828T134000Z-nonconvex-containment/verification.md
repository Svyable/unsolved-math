# Verification lane: exact exterior-region LPs

## Independence and chronology

The verifier was authored and its baseline executed before `theory.py` existed.
It started from frozen input, not a theory output. Each run starts a fresh
Python -I process with an empty environment; evidence and outputs are distinct
from theory. Baseline hashes/timestamps are in `experiments/baseline-execution.json`.
The verifier reconstructs everything before reading any submitted certificate.

Method families: COUNTEREXAMPLE_SEARCH and INDEPENDENT_IMPLEMENTATION.
The implementation uses Cramer's rule for every nonsingular three-constraint
basis of an exact linear program. Theory uses absolute ranges and closed formulas.
No mathematical functions are shared or imported. Shared specification, shared
author, common rational arithmetic, and the common four-case frontier reduction
remain correlated risks. This is algorithm/process independence, not independent
human/model judgment or kernel proof acceptance.

## Counterexamples and boundaries first

Before table or certificate reads, four controls run against the original strip
forms: [-2,2]^2 has passing corners/center and maximum violation 1; [-1,1]^2
has violation exactly zero; [0,1/2]^2 is strictly inside; [2,3]x[0,1/2] is
outside. Physical normal coefficients are checked positive and unit length.
The missed point (2,0) is an exact noncontainment witness. Reflection and intervals
touching/crossing zero occur in the full endpoint grid. The cases ell=4 and 17/4
distinguish a zero-height relaxation from outright infeasibility.

## Independent containment computation

For each sign pair e,f in {-1,1}^2, maximize z subject to the rectangle box and
`e(X+Y)>=1+z`, `f(Y-X)>=1+z`. A positive optimum is a point outside both bands.
For fixed X,Y the largest common slack over signs is
min(|X+Y|,|Y-X|)-1, so taking maxima over the four LPs is precisely the original
union violation. The program does not use the theory absolute-range formula.

The rectangle is compact; z is bounded above and unrestricted below. A maximizing
point can be chosen at a vertex of this pointed polyhedron. Enumerating every
nonsingular triple, solving it exactly, and checking all inequalities therefore
finds the optimum. Degenerate bases are skipped, not rounded. The full-dimensional
box assumption a<b,c0<d excludes collapsed containment queries. This LP fact is an
ordinary proof dependency, not a theorem checked by a proof assistant.

All 36 intervals from the nine rational grid endpoints are crossed with all 36
others: 1,296 rectangles and 5,184 exterior LPs. The outputs agree entry-for-entry
with theory (including negative/zero/positive violations), not only on totals.
200 are contained; 266 are sampling false positives. No finite census proves
the all-real criterion, but it discriminates the failed rule and the exact rule.

## Frontier checks and proof-step audit

For each of 19 lengths, four separate LPs maximize 2t (Y crossing) or t-r
(Y noncrossing), in variables p,r,t. This checks 76 case maxima. The constraints
are in `frontier()`; no closed-form maximum is used by that function. The checker
also emits its own optimal rectangles in `verification-frontier.json`; they need
not match theory's chosen attainers. All 17 submitted positive-height attainers
are rechecked against dimensions and the original exterior LPs.

Audit of the universal steps, not an assertion of independent proof:

1. The absolute-value identity is valid for both signs and zero; it does not rely
   on choosing one band for all points of the rectangle.
2. Images of independent intervals form the full product; extremizers exist.
3. Centering a zero-crossing interval decreases its maximum absolute coordinate
   and preserves zero as its minimum. Reflection preserves the union.
4. Four crossing/noncrossing cases exhaust axis-aligned placements, but say
   nothing about rotations. Each stated upper bound has the displayed attainer.
5. The p,r,t<=2 LP bound is justified by the translation gauge argument in the
   theory proof, not an experimental truncation: subtract min(p,r) when neither
   interval crosses, then one minimum is zero; the constraints bound all others.
6. ell=2 has height 2 but ell=33/16 has height 31/32, so interpolating across the
   change of placement type is invalid. At ell=4, zero height is not an admissible
   positive rectangle. These distinctions survive exact arithmetic.

The proof steps were reviewed by the same assistant; any missed reduction
assumption remains a blocking objection to claiming independently proved sharpness.

## Adversarial acceptance and replay

The authentic output is accepted. Seven corruptions are rejected: changed
containment slack, omitted rectangle, changed frontier maximum, missing attainer,
reversed attainer, false aggregate count, and a correctly dimensioned attainer
translated outside the union. The last test prevents acceptance based only on
dimension arithmetic. Output equality and canonical table SHA-256 checks are
recorded in execution logs and `verify-output.json`. Replay reruns both algorithms
and requires unchanged output hashes. No random seed, floating tolerance, or
network dependency enters the computation.

Reproduce: `python experiments/run.py baseline` (no certificate), then theory,
verify and replay modes in order. The already sealed baseline records the original
chronology; rerunning baseline after theory exists does not recreate authorship
independence. Source/input/output hashes cover the scripts actually executed.

## Citation and scope audit

See `sources/verification-source-audit.md`, distinct from theory's source note.
The primary text supplies context, not this normalized criterion or its frontier.
Imported statement/hash/revision/status remain frozen. No current global status
was inferred from a historical problem-list passage.

Remaining: same-assistant authorship; no kernel/independent human/model proof
review; local axis-aligned model only; ambiguous source counting/development and
global geometric claims unresolved. Neither the source theorem nor the parent
problem is refuted by the sampling counterexample.
