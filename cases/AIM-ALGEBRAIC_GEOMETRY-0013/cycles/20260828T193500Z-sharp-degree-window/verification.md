# Counterexample-first degree-window verification

## Concrete independence basis

The retained baseline was executed before theory.py was authored. verify.py
starts from input.json and actual multiplication maps, never importing theory
code. It first checks equal-power cancellation, early-cutoff failures and a
negative relative degree; only then runs the census. It constructs homogeneous
factor tables by enumerating products h*q and intersecting divisor sets, not
by Euclidean gcd. The theory lane instead uses dehomogenized Euclidean gcd
plus the infinity factor and a Hilbert-series formula, with no matrix ranks.

Each execution is a fresh Python -I process with an empty environment and
CPU/memory/file limits. The runner is reused infrastructure. Five mathematical
child processes are used: baseline, theory, certificate verification, and two
replays. There is no network namespace; inspected programs do no network I/O.
Authorship, frozen specification, coefficient ordering, iteration/serialization,
Python runtime and hardware are shared. No independent human/model or kernel
proof review is claimed. This is method and execution independence only.

## Counterexamples and boundaries first

For d=1,...,8 over F3, exact maps give (1,0,0) one degree before the cutoff
for the good pair (x^d,y^d), (0,0,0) at the cutoff, and (d,d,0) for the bad
pair (x^d,x^d). The bad pair at relative degree -1 has (0,0,0), exposing the
need to bound shifts. These baseline assertions precede confirmation.

The exhaustive factor table includes pure powers, leading/trailing zero
coefficients, common irreducibles, one zero form and both zero forms.
Homogeneous multiplication means the point at infinity is not discarded.
Every nonconstant common homogeneous divisor, not only a linear factor over
the ground field, makes a pair bad. For finite fields, normalized factors
represent every nonzero divisor up to scalar; product enumeration tests
divisibility without using the proposed cutoff. The all-zero pair is explicitly
bad rather than assigned gcd degree zero.

## Independent computation and certificate checks

Actual columns of d2 and d3 are formed in every graded piece. Compositions are
checked before ranks; the dimensions are obtained from kernels minus images.
The matrix implementation and gcd implementation agree on all 24,981 pairs
and 191,153 degree pieces, including their complete canonical case-stream
digest. Nine aggregate rows record gcd-degree histograms, 17,358 admissible
pairs, 7,623 Euler false acceptances and 17,358 early false rejections.
Finite results are not extrapolated into universal proof.

The verifier also computes the bounded cutoff for all selected A,D windows
on good and bad power controls at every a<=A,d<=D. All twelve windows pass;
64 explicit smaller-degree witnesses fail the proposed test in the required
direction. The matrix baseline does not accept a theory claim in place of
these recomputations. Shared window indexing remains an independence limit.

Eight certificates supply quotient-class and cycle bases for the equal-power
bad family at the cutoff. The checker verifies the fixed pair/field/degree,
that quotient vectors extend the image to full rank, that cycles are linearly
independent and killed by d2, and the exact homology dimensions. At this degree
d3's domain is zero, so none of those cycles is a boundary. Seven corruptions
are rejected: missing row, changed degree, field, form, quotient vector, cycle
vector or homology dimension. This checks those seven corruptions, not all
malformed inputs or general security properties.

## Claim and proof-step audit

- EULER-SHORTCUT: for d=2 the two quotient classes and two kernel vectors
  really coexist. The local common zero [0:1] is the geometric obstruction;
  cancellation does not annihilate either homology module.
- HILBERT: cancelling h leaves a coprime pair. Its generator has total degree
  a+2d-e in F2, whereas d3 starts at a+2d, so its image is h times the
  generator. A shift error here would change H2. The one-zero case has a
  unit cofactor; both-zero must be separate because injectivity fails.
- CUTOFF: the argument uses dimensions in degree n, not dimensions of a
  truncated Euler series. Above the bound, H1 alone detects the common factor.
  Lower-bound witnesses cover both n<a and a<=n<a+2d-1, and uniform sharpness
  uses the extremal pair of bounds a=A,d=D. With a unbounded, hidden bad
  complexes persist below any fixed degree. No assertion about arbitrary
  free complexes follows from this two-generator presentation.
- EULER-TAIL: chain dimensions force the cancellation regardless of maps.
  This explains why the shortcut is incapable of separating any parameters;
  the certificate shows a concrete harmful acceptance.
- SOURCE: Definition 1.1 was checked in a separate PDF rendering; it concerns
  sheaf exactness, not Euler characteristic. No sharp cutoff is attributed to
  the paper. AIM exact transcription and current status remain unchecked.

These are an explicit audit of proof steps by the same author, not independent
proof acceptance. No contradiction was found in the written universal steps,
but their status remains UNVERIFIED.

## Reproduction and objections

`python experiments/run.py replay` reruns both methods and requires identical
output hashes. Individual scripts accept input/output paths, allowing an
external reviewer to regenerate outside the packet without trusting stored
hashes. Output, executable and input hashes are linked in the execution logs.

Remaining: universal UFD/sheaf and sharpness reasoning needs independent
review; source scope is unavailable; equivalence is deliberately restricted
to graded chain isomorphism. No general quotient/stack, family over a
nonreduced base, higher-dimensional Cox ring or parent solution is established.
More degrees or prime fields alone would not be another material cycle.
