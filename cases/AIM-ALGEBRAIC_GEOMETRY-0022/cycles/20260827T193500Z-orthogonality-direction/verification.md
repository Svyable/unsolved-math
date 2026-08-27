# Independent-method verification

The verifier was authored and its baseline executed before theory.py existed.
It reads the frozen input, computes counterexamples and boundaries, reconstructs
the full core, and only then reads the theory certificate. The method uses
exact rational row reduction and explicit integer matrices, while theory uses
cohomology windows and binomial formulas. There are no imports between them.

Both implementations have same-assistant authorship and share the specification,
Python arithmetic, and the Čech model. Fresh execution and distinct algorithms
do not provide independent human/model review or proof-kernel acceptance.

## Counterexample and boundaries first

The check on P2xP2 with degrees (-1,0) gives zero for RHom(O,L) and dimension
three in degree zero for RHom(L,O). Boundary checks on P2 cover degree -2
(zero), -3 (one degree-two class), and 0 (one degree-zero class). These checks
occur before the product census or certificate comparison.

## Computation

The verifier builds signed incidence matrices from subsets containing each
negative support. It checks consecutive differentials compose to zero and
computes kernel/image dimensions by exact Fraction row reduction. All 28
single-factor support profiles are reconstructed. It independently builds the
tensor total differential for all 160 product-support patterns, including the
degree-dependent Leibniz sign; no cohomological tensor formula supplies those
matrix ranks.

For all 22 mixed supports it stores the contracting-homotopy matrices and
verifies dh+hd=I over the integers. Such weights may have unbounded coordinates;
their cochain type depends only on the support. The remaining monomial weights
are counted by recursive nonnegative compositions, not binomial coefficients.
This explains why no arbitrary finite lattice cutoff hides possible classes.

All 2,535 line-bundle cases and both Hom directions agree with theory. The
complete tables show 940 asymmetric vanishing answers. All six fan rays are
also independently compared by rational rank; none of the 15 pairs is collinear.

Seven corrupted certificate cores are rejected: change either counterexample
direction, invent a mixed-support class, erase a product H0 class, remove a
line-bundle row, invent a collinear ray pair, and alter a top-degree dimension.
This checker reconstructs a fixed finite core; it is not a general proof parser.

## Proof and source audit

The audit checks three separate bridges: the affine-cover Čech model,
tensor-product cohomology over a field, and the variance of Hom under an
equivalence. Finite exact ranks do not on their own establish an equivalence
with a mirror category. The universal immaculate-locus argument is recorded
as UNVERIFIED pending independent authorship or formal proof review.

The separate source note compares the downloaded versioned Borisov–Duncan PDF
with the HTML theorem and checks its smoothness, properness, algebraic-closure
and characteristic-zero assumptions. Its criterion concerns forbidden cones
in real Picard space. It is not a statement that collinear fan rays are always
necessary, nor does it settle the mirror question. The unavailable AIM page
prevents fresh confirmation of its full context.

## Reproducibility

run.py uses fresh python -I processes, an empty environment, CPU limit 180
seconds, wall timeout 200 seconds, 512 MiB memory and a 16 MiB file limit.
There are no network calls in either mathematical program. This is resource
and process isolation, not a network namespace. Logs include interpreter,
commands, timestamps, source/input/output hashes, exit codes and output.
Replay reproduced both result files byte for byte.

Remaining objections: independently authored or kernel proof review, live AIM
scope, and any claimed general CCC or wrapped-Floer correspondence. No parent
status was changed and no new solution is claimed.
