# A fixed-Betti Koszul chart, and a false rational-point test

Agent output is unverified research assistance, not a mathematical result.
This is a known-algebra calibration and a new repository certificate, not a
novelty or parent-problem claim. The exact AIM question is in `snapshot.json`;
its text, imported status, and broad scope have not been altered.

## Frozen scope and definitions

For a field k let S=k[x,y], with the standard grading, and B=(x,y). Write
S(-b)_n=S_(n-b), with negative pieces zero. For integers a>=0 and d>=1 and
homogeneous forms f,g of degree d, fix the augmented free complex

    0 -> S(-a-2d) --(-g,f)^T--> S(-a-d)^2 --(f,g)--> S(-a) --0--> S -> S -> 0.
          F3                       F2                F1        F0   M

The last arrow is the identity. Products commute, so d2*d3=0. A ghost means
the positive-degree subcomplex is sheaf-exact on P1, although its S-module
homology may be nonzero. "Graded-minimal" here means every differential entry
lies in B, not that this is a minimal free resolution of S as an S-module.
Geometric exactness is tested at all geometric points, not just P1(k).

For d=2, f=f0*y²+f1*xy+f2*x², similarly for g. This six-parameter *subfamily*
is not the space of all complexes of the same Betti type. Its based parameter
chart and the failure of a rational-point shortcut are the bounded target.
We do not construct the general Artin stack described in imported metadata.

## Two approaches and a retired shortcut

1. Form the degree-three multiplication map S1² -> S3. Its 4-by-4 Sylvester
   determinant gives an exact algebraic open condition, including roots at
   infinity and roots over field extensions.
2. Localize the Koszul complex at a point. If f or g is a unit after choosing
   local trivializations, it is exact. For the powers x^d,y^d, standard
   monomials explicitly compute the remaining irrelevant homology.
3. Enumerating only P1(k) is cheaper, but is retired as an exactness certificate
   by the F2/F4 counterexample below. It is only a necessary screening test.

## Claims, derivations, and falsifiers

**POINT-TEST — FALSIFIED proposal, DERIVED origin.** Proposed shortcut:
no common k-rational projective zero implies this complex is a virtual
resolution. Take k=F2, d=2, f=g=h=x²+xy+y². At [0:1], [1:1], [1:0], h=1.
In F4=F2[t]/(t²+t+1), h(t,1)=0. Thus the image of d2 at that local ring lies
in the maximal ideal and cannot equal F1. The sheaf has nonzero positive
homology. This is a closed degree-two obstruction, not a floating-point issue.
Falsifier of the witness: a wrong projective evaluation, reducible extension
polynomial, or an actual surjective d2 at the exhibited geometric point.
The polynomial is irreducible over F2 since it has neither 0 nor 1 as a root.

**CENSUS — EXPERIMENTALLY_SUPPORTED, DERIVED.** Both implementations exhaust
every ordered pair of binary quadratics, including zero forms, over F2,F3,F5.
Indices encode six coefficients in lexicographic order; the output stores all
accepted and all falsely accepted indices, not just counts.

| k | pairs | determinant nonzero | rational test false positives |
|---|---:|---:|---:|
| F2 | 64 | 24 | 3 |
| F3 | 729 | 432 | 24 |
| F5 | 15,625 | 12,000 | 240 |
| Total | 16,418 | 12,456 | 267 |

Falsifier: any omitted coefficient tuple, index disagreement, or differing
geometric admissibility classification. These finite counts are not a proof
for arbitrary fields or higher-degree charts.

**CHART — UNVERIFIED ordinary derivation, DERIVED.** For any field k, any a>=0,
and degree-two forms, this subfamily is virtual precisely on D(det) in A6_k.
The matrix, with columns yf,xf,yg,xg and bases ordered by increasing x power, is

    [ f0  0  g0  0 ]
    [ f1 f0  g1 g0 ]
    [ f2 f1  g2 g1 ]
    [  0 f2   0 g2 ].

Proof steps: after extending to an algebraic closure, a common linear factor
gives a linear syzygy (divide f,g by that factor). If the forms are proportional,
multiply their constant syzygy by a linear form. Zero forms also make the matrix
singular. Conversely, with no common factor, a linear syzygy uf+vg=0 would
force f to divide v, impossible unless v=0; then u=0. The determinant is
therefore nonzero exactly when there is no common geometric zero. Local Koszul
exactness gives sufficiency; failure of d2 to surject at a common zero gives
necessity. Nonvanishing of one polynomial is an affine open finite-type chart.
This argument does not identify its quotient or prove the imported general
moduli assertion. Falsifier: an exceptional field, zero-form or infinity case
breaking either direction; independent proof/kernel review is still absent.

**GHOST-CHECK — EXPERIMENTALLY_SUPPORTED, DERIVED.** For f=x^d,g=y^d, the
certificate gives H1 in 736 graded pieces across 64 triples: p in [2,3], a in
[0,7], d in [1,4]. Every H2,H3 piece checked is zero. The theory uses the
monomial basis x^i*y^j with 0<=i,j<d. The verifier builds actual multiplication
matrices and computes kernels/images by modular elimination. Falsifier: a
wrong graded dimension, degree shift, or nonzero composition/higher homology.

**GHOST-FAMILY — UNVERIFIED ordinary derivation, DERIVED.** For every field,
a>=0 and d>=1, H0=S, H1=S/(x^d,y^d)(-a), and H2=H3=0. A syzygy of x^d,y^d
must be a multiple of (-y^d,x^d), since these monomials are coprime; d3 is
injective in the domain S. The quotient basis above has d² elements, and
B^(2d-1) annihilates it. Therefore its sheaf vanishes. All entries of the
positive differentials have positive degree. For fixed d, changing a gives
distinct graded Betti types while keeping length 3, ranks (1,1,2,1), and F0=S.
Thus those constraints alone do not give finitely many graded Betti types.
This repeats a mechanism in the imported summary with explicit certificates;
no novel obstruction is claimed. Falsifier: an incorrect annihilator/syzygy,
or an equivalence notion which intentionally forgets the graded Betti type.

## Exact remaining boundary

The broad question asks which extra structure yields useful moduli. We audited
one based family only. General bounded charts, changes-of-basis stacks,
families over nonreduced bases, and independent recession directions remain
unchecked. Sheafifying forgets these ghosts, so the equivalence relation is
essential. The live AIM source was unavailable; the pinned exact record is
preserved, not presented as a freshly verified AIM transcription.
Both implementations have same-assistant authorship; ordinary universal
arguments remain UNVERIFIED pending independent author or kernel review.

## Reproduction

From this packet, `python experiments/run.py replay` checks deterministic
outputs in resource-limited fresh Python processes. See `verification.md`
for the independence limits and `sources/` for citation checks.
