# Fan-based verification, before projection certificates

## Fresh context and limitations

The verifier was authored and its baseline executed before theory.py existed.
It begins with the frozen fan/divisor data, not the projection formula. It checks
Euler cancellation, the b=-1 failure, F0, relative degree -1, K and K+F before
the census and before reading theory-output.json. Theory uses direct-image
splitting, index and Serre duality; verification uses exact rational Cech ranks
and integer ray inequalities. No mathematical code is imported between lanes.
The source checker uses literal cocycle/separating-functional identities, not
the other programs' rank routines.

All programs have SAME-ASSISTANT authorship and share the frozen input, fan
convention, Python runtime and serialization/iteration conventions. Fresh
processes and distinct methods do not amount to independent human/model or
kernel verification. The model-to-geometry bridge remains an ordinary proof
dependency, explicitly not established by finite enumeration.

## Counterexample and boundary results

The six first controls return, in order:

- F2, (a,b)=(1,0): (1,1,0), chi=0;
- F2, (1,-1): (0,2,0), chi=-2;
- F0, (1,-1): (0,0,0);
- F2, (-1,100): (0,0,0), with no imposed character box;
- F2, (-2,-4)=K: (0,0,1);
- F2, (-2,-3)=K+F: (0,0,0).

These test necessity versus sufficiency, twisting, negative relative degree,
and the one-fibre shift relevant to the source discrepancy.

## Completeness of the character calculation

For each of the 16 subsets N of violated rays, the code intersects the ray sets
of each nonempty subset of maximal cones. The weight appears on that chart
intersection precisely when no common ray belongs to N. This gives C0 through
C3 and their alternating Cech differentials. Consecutive maps are checked to
compose to zero, then Fraction row reduction determines all four Betti entries.
The full face lists, matrices and ranks are stored in baseline.json and
verify-output.json. No product-cohomology formula supplies these ranks.

Only masks 0,5,10,15 have nonzero cohomology. Their inequalities reduce to:

| Violated rays | Degree | y bounds | x bounds |
|---|---:|---|---|
| empty | 0 | -a <= y <= 0 | -b <= x <= ny |
| {0,2} | 1 | 1 <= y <= -a-1 | -b <= x <= ny |
| {1,3} | 1 | -a <= y <= 0 | ny+1 <= x <= -b-1 |
| all | 2 | 1 <= y <= -a-1 | ny+1 <= x <= -b-1 |

The code derives lower and upper bounds from good/bad inequalities after
computing the pattern ranks. Empty integer intervals contribute nothing.
Every nonacyclic pattern has both bounds; all other weights belong to one of
the acyclic patterns. Thus the enumeration is exhaustive within each frozen
bundle, not evidence from a guessed finite lattice truncation. The universal
identification with sheaf cohomology still needs independent proof review.

## Computation and certificate checks

All 1,827 rows agree with theory's independent projection calculation, with
canonical row-stream SHA-256
`f1f20acf4b3a81ab16c1f04905adbea0a089de80e9f9fb253397ce123d1785b6`.
There are 36,841 nonzero character classes across the census. Counts: 223
immaculate bundles, 27 Euler-zero false acceptances, 42 b=-1 false acceptances.
The latter count tests b=-1 alone; it is not a claim that the earlier product
criterion was false on its original product domain.

Eight submitted bundle certificates contain 26 class vectors. The checker
reconstructs the complete expected weight list, checks parameter and Betti
agreement, tests each cocycle equation, and requires rank to increase by one
when its vector is appended to incoming boundaries. Each weight cohomology has
dimension one, so this and the complete weight list certify a basis. Seven
mutations fail: missing class, wrong weight, zero vector, noncocycle, wrong
dimension, wrong twist and duplicate class. The immaculate certificate is an
empty class list, checked against an independently empty weight list.

The separate source.py checker verifies the canonical character, a closed
degree-two vector, and a functional annihilating boundaries but not that vector.
Seven n-values pass; four corruptions fail (weight, zero, nonclosed vector,
zero separating functional). This is a lower-bound/nonvanishing certificate,
not a complete independent computation of all cohomology in source.py.
The main census already includes all seven K and K+F bundles; the six explicit
controls contain the n=2 pair. No source formula is used as a truth oracle.

## Proof and citation audit

Checked the coefficient convention H=S+nF, all a>=0 direct-image summands,
the a=-1 boundary, and the dual substitution (-a-2,-b-n-2). The claimed locus
requires every P1 summand to have degree -1, rather than cancellation of an
alternating sum. The index formula and parity restriction are checked against
every finite row, not used to supply the verifier's Betti values.

The separate source note records the versioned PDF-text and HTML agreement on
the disputed entry. A PDF screenshot was unavailable, so no visual PDF check
is claimed. The proposed correction is a human-review item, not an author
erratum. Stacks 01XS supports projection formulas, not the entire mirror claim.
AIM failed twice; exact AIM context and current imported status remain unchecked.

Seven mathematical children were used: baseline, theory, verify, two replays,
source and source replay. Replays are byte-identical. run.py supplies Python -I,
empty environment, CPU180s, wall200s, memory512MiB, file16MiB and fd64 limits.
No mathematical program makes network calls; no network namespace is claimed.
Logs retain source/input/output hashes, interpreter, command, timestamps and exit.
The runner was mechanically adapted between lanes; child source hashes remain
unchanged and verified. No executed mathematical program changed after its run.

Remaining objections: independently authored/kernel proof review, the geometric
bridge, source interpretation, and any mirror construction. No parent solution.
