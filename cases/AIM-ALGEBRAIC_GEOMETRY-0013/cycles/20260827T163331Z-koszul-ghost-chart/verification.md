# Counterexample-first verification

Method families: INDEPENDENT_IMPLEMENTATION, COUNTEREXAMPLE_SEARCH,
PRIMARY_SOURCE_AUDIT, PROOF_STEP_AUDIT.

## Independence actually obtained

`verify.py` was authored and its retained baseline executed before `theory.py`
existed. It starts from `input.json`, tests the specified counterexample and
boundaries, then exhausts the search domain. Only after recomputation does it
read a theory certificate. No theory module is imported. The two algorithms
are (a) Euclidean polynomial gcd with an explicit infinity check, versus a
24-term determinant, and (b) graded matrix ranks versus a monomial basis.
Fresh `python -I` children use an empty environment and CPU/memory/file limits.
There is no network-namespace isolation; the inspected programs do no network
I/O. Both programs, the scope choice, and these notes have same-assistant
authorship. A process is fresh execution context, not an independent model,
human referee, or Lean kernel. Shared assumptions include Python integer
arithmetic, coefficient ordering, and the frozen Koszul family.

One initial baseline ran before formatting; the retained baseline was rerun
after formatting while no theory implementation existed. Including that
initial run and the final replay, eight research child executions were used.

## First: failures and boundaries

The checker evaluates x²+xy+y² at all three F2 projective points, then evaluates
it at the encoded element t of F4 using bit-polynomial multiplication. Values
are [1,1,1] and 0, respectively. It checks zero forms, common zeros at infinity,
an irreducible common quadratic, and coprime powers. Sign controls distinguish
2xy!=0 in characteristic three from 2xy=0 in characteristic two; these are
algebraic boundary assertions, not mutation fuzzing. Negative graded pieces
are zero, and shift a=0 is included in the matrix census.

## Computation audit

All 16,418 ordered pairs agree exactly, including their full encoded accepted
sets and false-positive sets: 12,456 admissible and 267 rational-test failures.
All 64 power-ghost cases agree in 736 degree pieces; d2*d3 is checked directly
in every relevant piece before rank calculations. Only the specified degree
range is computationally checked. Universal vanishing follows, if accepted,
from the separate ordinary algebra argument, not finite sampling.

Seven mutations of the supplied certificate's recomputed core are rejected:
remove an admissible pair, inject the zero pair, hide extension obstructions,
alter H1, invent H2, alter a shift, and erase the F4 root. The checker uses
strict equality with its recomputed core. This validates these seven changes;
it is not a general malformed-input/security test or proof that arbitrary
bad certificates must be detected. Resource-bounded replays preserve all three
mathematical output hashes; execution logs separately record commands,
versions, inputs, source hashes and return codes.

## Claims, citations, and proof-step audit

- POINT-TEST: the exact F4 root defeats rational-only testing. The failure is
  positive sheaf homology, not merely an unsatisfied aesthetic condition.
- CENSUS: domains include zeros and leading-coefficient-zero forms; the
  infinity check prevents dehomogenization from silently losing a root.
- CHART: both implications in the determinant argument include proportional
  and zero forms. A unit on either local chart gives Koszul exactness. At a
  common zero, d2 cannot surject onto F1. This checks the reasoning structure,
  not its independent authorship or formal validity in a proof assistant.
- GHOST-CHECK: actual multiplication maps give the finite homology table.
- GHOST-FAMILY: coprimality justifies the kernel, domain-ness the injection,
  and the standard monomials the B-power annihilator. Fixed d and variable a
  preserves ranks and F0, but not Betti types. This does not classify ghosts
  up to a sheaf-derived equivalence, where they disappear.
- SOURCE: Definition 1.1 in the pinned primary paper was read separately in
  HTML and downloaded PDF text. Only its definition is used. AIM availability
  and the limited attribution are documented in `sources/verification-source.md`.

## Remaining objections

No general moduli-stack theorem, geometric quotient, relative family over an
arbitrary base, or new mathematical result is established. The original AIM
page could not be freshly read. The imported "proved" and "partial_result"
labels remain unverified external metadata. Universal algebra and sheaf
reasoning have no independently authored or kernel-accepted proof. A useful
next research step is a separately authored audit of the arbitrary-field
chart and an explicit choice of moduli equivalence/degree window.

## Reproduction and integrity

Run `python experiments/run.py replay` from a packet copy, then the repository
cycle validator and manifest verifier on the original. The runner preserves
an existing replay log; exact deterministic output files are rewritten with
identical bytes. It checks their previous SHA-256 before accepting the replay.
For a completely new reproduction without trusting stored expected hashes,
invoke each script with `input.json` and an output path outside the packet,
then invoke the verifier with `--certificate` pointing at the new theory file.
