# Verification lane

## Order and independence

The verifier was authored and its baseline run before theory.py was authored.
It starts with omitted-summand, integral saturation, repeated-root, singular
matrix and pivot-swap controls, then reconstructs the census, and only then
reads the theory certificate if supplied. Each run is a fresh Python -I
process with empty environment and CPU/memory/time limits. No mathematical
code is shared between lanes.

Theory uses quadratic-character point counts and Newton power sums.
Verification enumerates every affine (x,y) pair plus the point at infinity,
then constructs Kronecker matrices and uses Bareiss elimination.
This is algorithmic and process independence, not independent authorship:
both implementations and notes have the same assistant author, share the
specification, and have no independent human/model or kernel review.

## Counterexample and boundary checks first

For q=5 and three zero traces, the rank-eight determinant has v_2=4
while the full rank-twenty determinant has v_2=10. This is a failure of
omitting summands, not a failure of the imported B formula. Direct point
enumeration witnesses the trace on y^2=x^3+1.

Modulo 49 the unit map has image size 49; multiplication by 7 has image
size 7 and cokernel size 7. Its rational lift is invertible but its
Z_7 image is not saturated. This only refutes a general rational-to-integral
shortcut, not a geometric vanishing theorem.

The auxiliary q=4,t_i=4 polynomial case has repeated roots and R=8^8.
It checks algebra only; no curve over F_4 was constructed. Determinant
controls include a row swap of determinant -1 and a singular matrix.

## Computation audit

The census covers 20+42+110=172 nonsingular short Weierstrass models.
Their trace sets have 9,11,13 elements, respectively. Unordered triples
with repetition number 165+286+455=906; models with identical trace have
the same determinant input. No isomorphism-class count is asserted.
All 906 R, B and D20 values match exactly. Additionally, 33 self-product
cases are checked by constructing and eliminating the entire 20x20 matrix,
not just multiplying its block determinants. All three closed-form
trace-zero rows agree. Seven one-field/deletion corruptions are rejected by
complete reconstructed-output comparison. These are narrow mutation tests,
not a claim of robustness to arbitrary hostile certificates.

The first baseline attempt and a diagnostic rerun failed: the provisional
normalization divided D20 by q^12. The trace-zero equality exposed the error.
Re-derivation of a 2x2 block gave q^3*N_i, hence q^18 for six blocks.
Both failed processes are disclosed here; the successful baseline contains
the corrected source hash. The theory code was then authored independently
using rank-twenty power sums. Subsequent theory, verification and replay
passed. Total mathematical subprocess invocations: seven, including failures.
No failed output was used as evidence.

## Proof-step and citation audit

The source audit is in sources/verification-source.md, separately from the
theory source notes. It checks what object the cited result actually controls.
The determinant proof has three separable obligations: six rank-two
contributions, q^3 per block, and ell not dividing q. The ordinary lattice
argument additionally requires a free lattice and rational invertibility.
It does not supply the geometric TRANSFER claim. The 906 finite cases
cannot validate that missing map or remove the divisible subgroup.

## Remaining objections

The AIM page is unavailable. The upstream proof text was not available;
the gap identified is in the evidence and summary inspected, not a verdict
that an unseen proof is false. The cited theorem is a dependency, not
reproved. Integral cycle classes, unramified cohomology, the Fermat-model
identification and the characteristic-primary part are not computed.
General identities and the lattice argument need independently authored
review. No parent problem or imported status is changed.

## Reproduce

python experiments/run.py baseline reconstructs without a theory input.
python experiments/run.py replay checks byte-identical theory and verifier
outputs. Baseline and verification evidence are distinct from theory output;
execution logs record timestamps, source/input/output SHA-256 and limits.
