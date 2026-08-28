# Verification: exhaustive labelings before structural conclusions

## Fresh context and actual independence

verify.py and its baseline were completed before theory.py was written. The
baseline begins from frozen input and counts every label assignment directly,
without cycle lengths or theory outputs. Each run is a fresh Python -I process
with an empty environment; the certificate is read only after reconstruction.
The verification method families are COUNTEREXAMPLE_SEARCH,
INDEPENDENT_IMPLEMENTATION and a separately recorded source-scope audit.

Theory uses indegree peeling, cycle obstructions and reverse-tree labels.
Verification uses literal modular equations and tuple exhaustion, including a
separate surjectivity filter. No mathematical helper is imported from theory.
However both programs have the same assistant author, specification, Python
runtime, product iterator and serialization convention. This is not independent
human/model authorship or kernel proof verification.

## Counterexamples and seven boundaries first

Before the main sweep or certificate reads, all 27 assignments for T=[0,0,0],
N=3 are exhausted. The unconstrained minimum is 1 with 3 minimizers; the
surjective minimum is 2 with 6 minimizers. The witnesses are [0,2,2] and [0,1,2].
Thus n>=N does not preserve the minimum when surjectivity is imposed.

The boundary assertions check: one exact empty labeling; no surjective empty
labeling; singleton modulus 1 cost zero; singleton modulus 2 cost one;
noninjective T=[1,0,1] at modulus 2 with two exact maps; invalid destination
rejection; and nonpositive modulus rejection. Self-loops count as one equation.
Repeated destinations are intentionally valid, not rejected as nonbijective.

## Exact computation and acceptance checks

For every specified T and N, enumerate all N^n tuples in fixed label order.
Compute sum(f[T[x]] != (f[x]+1)%N) directly. Track the minimum, its multiplicity,
and number of exact maps; also track the surjective minimum separately.
Every tuple has exactly n equations, including loops. No random sampling,
floating tolerance or cycle formula enters this calculation.

10,531 systems across 23 n,N domains require 955,958 label assignments in the
main census. Each canonical per-system row contributes to the stream hash;
both algorithms produce the same stream hash and identical aggregate tables.
This is stronger than comparing just totals, subject to the ordinary SHA-256
collision assumption. The full ordered stream can be regenerated from the code.
Verification-only surjectivity counts are in verification-surjectivity.json.
These counts are not falsely attributed to the theory implementation.

Twenty-four constant-map cases independently test the constrained formulas,
including n<N, N=1, N=2 and n=N boundaries. Twenty-eight proposed labels are
checked against the original equations and the independently exhausted optimum.
The verifier emits its own lexicographically first witnesses in
verification-certificates.json; theory's phase-based witnesses need not match.

The authentic proposal passes. Seven corruptions fail: changed minimum,
false star surjective minimum, missing domain, missing certificate, out-of-range
label, false system count and invalid destination. They are executable assertion
tests, not inferred rejection claims. The bad-label check exercises validation
independently of aggregate equality. Deterministic replay reruns both programs
and requires unchanged output hashes; source/input/output hashes are recorded.

## Proof-step audit and limits

1. Finite total outdegree-one graphs have one cycle per weak component: follow
   successors until repetition; two distinct cycles cannot join under a
   single-valued successor map. This fails for broader directed-graph models.
2. Sum closing increments modulo N on each cycle separately. Changing an
   incoming edge cannot remove a contradiction wholly on that cycle.
3. At minimum, one failed edge per bad cycle leaves no failures available for
   trees or good cycles. Hence tree labels are uniquely forced backward.
4. On a bad cycle, phase and unique failed edge are recoverable from a minimum
   labeling. The LN count has neither an extra phase quotient nor an omitted
   edge factor. N=1 has no bad cycles, avoiding an impossible failed edge.
5. Nonempty exact solutions are surjective because a cycle covers the regular
   target. Positive-defect solutions lack that argument; the star certificate
   isolates exactly this gap. The empty exception is not dropped.
6. The star's N-2 exceptional leaf colors are distinct and occur once at the
   constrained minimum, giving a falling factorial rather than a power.

These are same-assistant proof checks, not an independent proof of the universal
claim. Exhaustion proves only the stated finite domain; the arbitrary-size
theorem remains ordinary mathematics awaiting independently authored review.

## Citation check and unresolved objections

sources/verification-source-audit.md checks the primary text separately from
the theory note. The source does not identify an arbitrary abstract labeling
with a natural ASM factor, and we do not make that inference. Its title,
date and neighboring problem numbers are checked, not current solution status.

No actual combinatorial action or natural target is computed. Source-scope
review, independent universal proof review and a justified application remain
open. This is an assumption reduction and a surjectivity-gap regression audit,
not a definition or solution of the parent resonance problem.
