# Verification: bar complexes before tensor certificates

## Independence and ordering

`verify.py` and its baseline execution were completed before `theory.py` was
authored. From the frozen algebra specification it first searches the
dimension-four boundary: I/I^2 has dimensions 1 and 2. It then checks empty bar
words and square-zero products before computing the full frozen domain. Only
certificate mode reads `theory-output.json`, after recomputing all bar results.
The theory uses dense ranks of tensor-periodic resolutions; verification uses
sparse pivot ranks of normalized bar complexes. Neither imports the other.
`sign.py` uses a third, literal two-path multiplication calculation, with the
odd-characteristic counterexample before proposal comparison.

These are fresh isolated Python processes and different mathematical method
families, with distinct evidence files. They have SAME-ASSISTANT authorship and
share the input, runtime, monomial conventions, iteration and JSON conventions.
There is no independently authored human/model or kernel proof review. The
baseline is evidence of ordering, not proof of psychological independence.

## Bar definition and finite proof-step checks

For an augmented algebra R=K plus I, the free normalized bar term is
B_n=R tensor_K I^(tensor n), augmented B_0 -> K. Its differential on
(a0|a1|...|an) multiplies the first pair with sign + and internal pair j,j+1
with sign (-1)^j. No terminal augmentation term survives because an lies in I.
The K-linear contraction is s_-1(c)=c*1 and
s_n(a0|a1|...)=1|(a0-epsilon(a0))|a1|... . On the monomial basis it inserts
the unit when a0 is nonunit, and is zero when a0=1.

Expanding ds+sd cancels the internal terms and restores the original tensor;
degree zero includes the augmentation and s_-1. This is an ordinary universal
argument, not kernel checked. The code checks the identity separately on all
1,119 basis elements in the frozen free-bar degrees 0 through 3. It also checks
2,379 reduced-bar d^2 identities through degree 5. These bounds are explicit;
they do not certify every degree of the universal resolution.

After tensoring B with K over R, C_n=I^(tensor n), C_0=K, and the differential
merges adjacent factors starting with sign minus. This computes Tor when the
bar resolution is exact. For Ext, Hom_R(B,K) is the K-dual of C degree by
degree, so its differential ranks are the same: beta_n=dim C_n-rank d_n-rank
d_(n+1). Every term here is finite dimensional. Thus the code is not silently
identifying Ext with Tor as modules, only comparing their dimensions through
dual chain matrices. Degree-one cocycles are the functionals annihilating I^2;
there are no degree-one coboundaries. This independently checks the small
dimension-four witness without the tensor-resolution formula.

## Exact outcomes

For each p in {2,3,5}, the exponent lists (2),(3),(4) have profile
(1,1,1,1,1), while (2,2) has (1,2,3,4,5), in degrees 0,...,4. All 12 rows
and 60 entries agree. Reduced-bar ranks d1,...,d5, per prime, are respectively
(0,0,0,0,0), (0,1,2,5,10), (0,2,6,20,60), and (0,1,5,18,58).
The output retains differential-stream SHA-256 values and rank/count tables;
matrices are regenerated, not stored in full.

All 12 Ext1 basis certificates pass field, exponent, vector dimension, coefficient
range, independence, product-annihilation and completeness checks. Seven
specified corruptions fail: missing, wrong algebra, wrong prime, wrong dimension,
zero functional, noncocycle and extra functional. This is a bounded mutation
suite, not a proof against arbitrary malformed input.

The sign checker accepts all three probes: unsigned d^2 has coefficient 2 on
xy for p=3,5 and is zero for p=2; signed d^2 is zero in all three. Four further
corruptions fail: erased odd-characteristic obstruction, invented char2
obstruction, broken signed value, and omitted prime. The implementation checks
literal multiplication paths rather than trusting the tensor matrix ranks.

## Claim, citation and proof audit

1. DIMENSION-SHORTCUT: compare algebras of equal dimension and residue field;
   distinguish exact profile determination from the stronger and untested claim
   that dimension cannot bound a profile. The two different Ext1 dimensions
   suffice to retire only the former shortcut.
2. PROFILE: check alternating annihilators, mixed Koszul signs, tensoring over a
   field, first-quadrant finite diagonals, and augmentation-zero Hom entries.
   No contradiction found; the infinite formula remains UNVERIFIED pending
   independent proof review. The experiment alone proves no all-n assertion.
3. FIELD: verify the two successive nonsquare valuation arguments, tower degree,
   characteristic-two translations, and tensor base k. The finite computation
   is over prime fields, not rational-function fields. The realization remains
   an ordinary derivation with primary irreducibility dependencies.
4. SOURCE: separately inspect the paper PDF, printed pages 13–14, Lemmas 2.13
   and 2.15; keep their hypotheses and length conventions distinct. Read Stacks
   tag 09HD for the field dependencies. AIM retrieval failed twice; no current
   source status or exact AIM scope is independently confirmed.
5. Category boundary: the examples refine the prior obstruction, not a positive
   gluing theorem. No actual homotopy-colimit construction, geometry, or new
   parent-problem conclusion is verified.

## Reproduction and resource evidence

From this packet directory run `python experiments/run.py baseline`, `theory`,
`verify`, `sign`, then `replay` and `signreplay`. These invoke seven children
total. Each child has Python -I, an empty environment, CPU 180 seconds, wall
timeout 200 seconds, address-space limit 512 MiB, file-size limit 16 MiB and
64 file descriptors. There is no network namespace; the programs make no
network calls. Logs record command, hashes, Python version, time and exit code.
Theory, verifier and sign replays are byte-identical. Operational repository
validation is separate from the eight-child mathematical budget.

Remaining objections: same-assistant provenance; no kernel; universal bar,
tensor and field proof dependencies; unavailable AIM page; no general categorical
comparison. None is concealed by the successful finite checks.
