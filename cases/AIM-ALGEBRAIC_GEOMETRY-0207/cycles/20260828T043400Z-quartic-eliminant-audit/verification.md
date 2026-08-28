# Independent-process verification

## Independence and order

The initial verifier and its baseline execution preceded creation of theory.py.
Both implementations have same-assistant authorship and share the frozen target,
coefficient convention and output contract. This is algorithm/process independence,
NOT an independent human, model, or kernel proof review. The initial source and
execution log are retained. A style-only pairwise/line-wrap correction was followed
by a new baseline, theory, verification, and two-process replay: six mathematical
subprocesses total, within the eight-process budget. Both baselines have identical
result bytes. No external model calls were made.

Each child uses fresh Python -I, empty environment and CPU/memory/file limits.
There is no network namespace. Scripts make no network requests and import no
theory helpers. Verification reconstructs its complete expected result BEFORE
opening theory-output.json. Logs record source, input and output SHA-256 values.

## Counterexample and boundary checks first

1. Exact rational Sturm chains compute 0 and 4 real roots of the two squarefree
   quartics. This differs from theory's positivity and sign-change intervals.
   Neither has a root at infinity because the leading coefficient is nonzero.
2. Polynomial degree and the first nonzero coefficient recover the monomial
   multiplicities at zero and infinity: (4) versus (3,1).
3. Coefficient substitution verifies the nonsingular I=0 control; J=0 is covered
   by the real examples and harmonic rational parameters. Singular s or t at 0,1
   occur in identity interpolation only, never in the equivalence census.

## Computation checks

For each of 2,025 ordered pairs, enumerate all 24 target orderings of
{infinity,0,1,t}: 48,600 candidate projectivities in total. If A,B,C are the desired
images of infinity,0,1, use matrix columns det(C,B)A and det(A,C)B, then test the
fourth image with a homogeneous determinant. The three distinct targets guarantee
nonzero determinant. No six-value orbit formula is used in this implementation.

Results: 213 pairs admit a map and there are 888 maps in total. Every direct-map
existence result agrees with the invariant equation and with theory's orbit counts.
The census is exhaustive only for the explicitly listed 45 rational parameters.

The independent identity check uses 49 evaluations on {-3,...,3}^2, comparing
coefficient-derived invariants with the six-factor expression. Both polynomials
have separate degrees at most six. An ordinary repeated univariate root-bound
argument makes this grid sufficient for identity; that mathematical justification
is not a kernel proof. Theory instead uses exact sparse coefficient expansion.

Seven single-field mutations (real invariant, real count, multiplicity, identity
grid value, map count, I=0 control, total pair count) are rejected by full equality
with the independently reconstructed data. This checks these corrupted outputs,
not arbitrary software faults. Replay reproduces theory and verification byte-for-byte.

## Claim, citation and proof-step audit (same-assistant supplementary review)

BOUNDARY and IDENTITY have fresh-process checks above. COMPLETENESS remains
UNVERIFIED in the cycle contract because the five-step universal argument is not
independently authored. Review checked that E has balanced weights, normalization
requires distinct roots, t cannot be 0 or 1, and no cancellation by I or J occurs.
The field and multiplicity counterexamples are not claimed to refute the imported
squarefree-complex wording. The root-divisor and genus-one-curve equivalence
conventions are separated: arbitrary quartic scalars are allowed here, unlike the
square-scalar convention in Fisher; over C a nonzero scalar has a square root.

Source audit rechecked Fisher Section 2, printed page 2, for unscaled coefficients,
I,J weights and the factor of 16 in its discriminant. Our D0 is explicitly normalized.
The generalized Kruppa source concerns projections of a common spatial curve,
not automatically apparent contours of a surface. No geometric transfer is accepted.
These locator/prose checks are not falsely registered as fresh-context proof checks.

## Remaining objections

- Ordinary complex completeness and root/multiplicity preservation need independent
  mathematical review; finite arithmetic is not that review.
- Real descent, geometric admissibility, dual-section gluing, smooth-quadric
  realization, and fundamental-matrix uniqueness are not verified.
- The AIM page was unavailable. Imported status is unchanged and remains unverified.
- Known-result calibration only; no novelty, parent solution, or formal acceptance.
