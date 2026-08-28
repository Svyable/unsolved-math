# Fresh-method verification

## Order of work and independence

The verifier baseline was written and executed from snapshot/input before
the theory implementation was authored. It begins with the proposed
target-H-implies-closure shortcut, exact sign boundaries and the unscaled
control. It has no theory imports. Confirmation recomputes the full baseline
before opening the theory certificate.

Verifier arithmetic is a+b*sqrt(5), with signs from exact comparisons of
a^2 and 5b^2. It tests every coordinate difference, enumerates all 32 candidate
order ideals and counts their maximal elements, and explicitly reflects all
ten signed vectors under both generators. Theory uses rational coefficients
in 1,phi, signs via rational isolation of phi, simplified pairwise comparison
conditions, direct antichains, and a closure criterion. Both serialize results
into a shared canonical format; that format and the frozen specification are
shared dependencies, not independent evidence by themselves.

The lower-bound checker is a further fresh process that accepts a coefficient
certificate and derives the three constraint rows from the original rays,
then reduces polynomial products modulo t^2-t-1. It checks algebra rather
than solving the optimization by sampling. Same assistant authored all code
and prose. No independent human/model or proof-kernel review occurred.

## Counterexample and boundary search first

At scales (1,phi,phi), direct cone comparisons and ideal maxima yield target H,
but s2(v0)=(1,phi) is not in the signed vector set. The fixed swap permutation
also fails to preserve the order. The baseline makes these checks before the
grid. At (1,1,1), closure and swap invariance pass and target H fails.

Five arithmetic probes cover zero, signs of +-1, sqrt(5)-2>0 and
sqrt(5)-9/4<0. For delta=1/n, n=2,4,...,256, three boundary families are checked:
(1,phi-delta,phi) fails target H, (1,phi+delta,phi+delta) succeeds,
and (1,phi,phi-delta) fails retention. Both exact equality-case attainers pass.
Coordinate equality is permitted: replacing nonnegative with strictly positive
coordinate comparisons would wrongly reject the displayed attainers.

## Exact computation and certificate results

The 11^3=1,331 triples produce 285 retained orders and 38 successful repairs.
There are 525 swap-invariant orders but zero successful swap-invariant orders.
Exactly one triple is reflection closed and it is not successful. Closure is
tested against both generators on the ten signed vectors, stopping at the first
missing image for a failed configuration; no full-image census count is claimed.

All per-case fields, not just totals, agree through the canonical case-stream
SHA-256. The 121 aggregate rows, 24 boundary records and two featured records
are saved in separate theory/verification table files, with equal file hashes.
The two full coordinate certificates are checked against raw reconstruction;
each missing-reflection witness is evaluated and tested against the signed set.

Seven main-packet corruptions are rejected: lower claimed budget, altered
success count, claimed closure, changed coordinate, changed reflected image,
missing attainer, and claimed swap invariance. These are semantic checks, not
only comparisons of file hashes.

The two lower-bound certificates are checked coefficient by coefficient.
For bottom root 2, its second coordinate gives a-1>=0, the first-coordinate
middle comparison gives b-phi*a>=0, and the budget gives D-b>=0. Weights
(phi,1,1) are nonnegative and sum these to D-phi. Root 3 gives the mirrored
certificate. Four altered dual certificates (wrong weight, negative weight,
wrong coordinate sign, missing orientation) are rejected. This validates the
two exact algebraic certificates, not an independently authored proof of the
claim that these two orientations exhaust every feasible target order.

## Proof-step and citation audit

The target polynomial has only one incomparable pair, the marked minima.
With old relations retained, only the middle pair can change; the two
orientation inequalities are necessary and sufficient. The old maximal-root
comparisons give c>=a,b. At D=phi, equality in the nonnegative combination
forces the two middle scales, then c is forced by its bounds. Reflection
closure uses images of fixed simple roots, so it cannot be rescued by merely
renaming rescaled roots. The swap obstruction concerns a fixed permutation,
not isomorphism of the two repairs. No contradiction found in these ordinary
steps; they remain pending independent proof review.

The separate source audit checks the H variable convention and the abstract
dihedral model. The scaling theorem and closure obstruction are not attributed
to the paper. No current-status or full-paper correctness audit is claimed.

## Reproduction and limitations

Run `python experiments/run.py baseline`, `theory`, `verify`, `dual`,
`replay`, and `dualreplay` in a disposable packet copy. Seven mathematical
children were used: baseline, theory, verify, dual, then three replay children.
Main outputs and the dual output are byte-stable. Logs record Python version,
source/input/output SHA-256, empty environment and fresh Python -I process.
Limits: 180 CPU seconds, 200 wall seconds, 512 MiB address space per child;
no network/model calls, but no OS network namespace was created.

The finite grid does not prove the universal claims. The dual identities give
exact algebraic evidence but do not remove the same-author scope/reduction
objection. A fixed-ray point configuration is not a repaired reflection system.
No broader root-system convention or parent solution is settled.
