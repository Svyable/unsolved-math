# All-points containment in a nonconvex strip union

## Scope and changed evidentiary state

This follows `20260827T093200Z-strip-intersection-audit`. That packet distinguished
intersection from union and supplied a sufficient family of rectangles. It did
not give a necessary-and-sufficient test for arbitrary translated rectangles or
optimize their height at fixed length. The present target is precisely that
local planar extension, with a counterexample to a tempting sampling test.
It does not continue the blocked surface-development argument.

All claims concern real coordinates, closed sets and positive dimensions.
There is no novelty claim, global flat-strip theorem, optimal rotated rectangle
claim, surface realization, or change to the imported open status.

## Definitions and quantifiers

Fix delta>0 and c,s>0 with c^2+s^2=1. Physical strips are
`|cy+sx|<=delta/2` and `|cy-sx|<=delta/2`. In normalized coordinates
X=2sx/delta and Y=2cy/delta their union is

`U = {|X+Y|<=1} union {|Y-X|<=1}`.

For every real a<b and c0<d, let R=[a,b] x [c0,d], length ell=b-a and
height H=d-c0. The symbol c0 is an endpoint, not the physical normal component c.
All translations are allowed, but rotations relative to these axes are not.
Physical dimensions are delta*ell/(2s) and delta*H/(2c); height is not necessarily
the shorter-side width mentioned in the source.

Let [p,q] be the image of [a,b] under absolute value and [r,t] the image of
[c0,d]. For an interval [u,v], its absolute minimum is zero if u<=0<=v,
otherwise min(|u|,|v|); its maximum is max(|u|,|v|).

## Approach 1: corner-plus-center sampling (retired)

SAMPLE, derived hypothesis, falsified: containment of the four corners and center
does not imply R subset U. For R=[-2,2]^2, each corner lies on one of the diagonal
centerlines and the center lies on both. But (2,0) has |X+Y|=|Y-X|=2>1,
with normalized violation 1. These are exact integers, not a numerical tolerance.

With physical delta=2,c=3/5,s=4/5, this is the rectangle
[-5/2,5/2] x [-10/3,10/3]. Its missed point (5/2,0) satisfies both physical
absolute linear forms equal to 2 although each permitted half-width is 1.
The convex-hull principle for one convex strip cannot be applied to their union.

Falsification condition: failure of any corner/center membership, or membership
of the exhibited missed point, would invalidate this certificate.

## Approach 2: exact absolute-range reduction

CRITERION, derived universal claim with ordinary proof (UNVERIFIED in the
machine-readable ledger pending independent proof review):

`R subset U iff q-r<=1 and t-p<=1`.

Proof steps:

1. For all real X,Y, min(|X+Y|,|Y-X|)=||X|-|Y||. Squaring both sides gives
   X^2+Y^2-2|XY|; both sides are nonnegative, so equality follows.
2. The absolute-value image of R is exactly the Cartesian product [p,q]x[r,t].
   Continuity gives each interval image, and independent coordinates give every
   combination, including extremizers. No convexity of U is assumed.
3. The maximum of |u-v| over this product is max(q-r,t-p). Its two extrema
   occur at (q,r) and (p,t), and each has a preimage in R.
4. Thus the exact worst violation is max(q-r,t-p)-1. Equality zero is allowed.

This supplies necessity as well as sufficiency and constructs a falsifying point
from either failed inequality. A wrong absolute-range endpoint, loss of coordinate
independence, or any rectangle disagreeing with the original strip inequalities
would falsify the reduction. The census includes crossing, touching, disjoint,
strictly interior and reflected interval placements.

## Sharp height at fixed normalized length

FRONTIER, derived ordinary universal claim, also awaiting independent proof review:

| Positive length ell | Greatest possible height |
| --- | --- |
| 0<ell<=1 | 4-2ell |
| 1<=ell<=2 | 2 |
| 2<ell<4 | 2-ell/2 |
| ell>=4 | No positive-height rectangle |

At ell=4 the relaxed degenerate maximum is 0; for ell>4 even the degenerate
placement is infeasible. At ell=2 the maximum is 2, whereas its right-hand limit
is 1. This genuine discontinuity comes from the change of possible placements.
The limit as ell tends to zero is 4, not a positive-length maximum of 4.

Here is the complete four-case upper-bound proof. Reflect noncrossing intervals
to the nonnegative axes. An interval containing zero can be centered at zero
without changing its length and without increasing its absolute maximum. This
only relaxes the criterion. Boundary-touching intervals may be assigned to either
case; this overlap does not omit or enlarge any actual rectangle.

* X noncrossing, Y crossing: q=p+ell,r=0,H=2t. Constraints p+ell<=1,
  t<=p+1 give ell<=1 and H<=4-2ell, attained at p=1-ell,t=2-ell.
* Both crossing: p=r=0,q=ell/2,H=2t. Feasibility requires ell<=2 and t<=1,
  hence H<=2, attained by the centered rectangle.
* X crossing, Y noncrossing: p=0,q=ell/2,H=t-r. Here t<=1,
  r>=max(0,ell/2-1), giving H<=min(1,2-ell/2), feasible only up to ell=4
  when zero height is allowed.
* Neither crossing: q=p+ell,H=t-r. From r>=p+ell-1 and t<=p+1,
  H<=2-ell. This is attainable for ell<=2: take p=max(0,1-ell),
  r=max(0,ell-1),t=p+1. For ell>2 no nonnegative H is possible.

Taking the largest of these four case bounds gives the table. Explicit global
attainers for positive height are, respectively:

`[1-ell,1] x [ell-2,2-ell]`,
`[-ell/2,ell/2] x [-1,1]`, and
`[-ell/2,ell/2] x [ell/2-1,1]`.

They have exactly the required dimensions and satisfy both containment
inequalities. The closed convention matters at ell=1 and ell=2. No assertion is
made for ell=0 or arbitrary rotations.

## Approach 3 and finite certificate interface

The verifier independently maximizes common slack in each of four exterior
sign regions using rational three-variable LP vertex enumeration. It does not
import this code or use absolute-range evaluation for rectangle containment.
For the frontier, its four LPs share the case reduction, so their agreement is
not an independently authored proof of the reduction.

The LP gauge p,r,t<=2 is lossless: in the neither-crossing case subtract min(p,r)
from all four extrema. Length, height and both difference constraints persist.
Then p=0 implies t<=1 and r<=1; r=0 implies p+ell<=1 and t<=2. In a crossing
case p=0 or r=0 already gives these bounds. Thus no arbitrarily translated
optimizer is lost. The bound is not inferred from finite tests.

`experiments/theory.py` uses the interval formula, four closed-form case maxima,
and explicit attainers. Its LP-count fields describe the comparison workload,
not LPs executed by theory. Output: 1,296 rectangles, 200 contained, 266 false
positives for sampling; 19 lengths (including 31/16,2,33/16 around the jump),
17 positive-height certificates. Every table entry agrees with the separate
verifier; see its lane for controls and limitations.

Reproduce from this packet: `python experiments/run.py theory`, then
`python experiments/run.py verify` and `python experiments/run.py replay`.
Five mathematical child processes were used: baseline, theory, verify, two replay
children. All use exact Fraction arithmetic and resource limits.

## Remaining objections and next step

The progress is an exact failed sampling rule and an equivalence/optimization
formulation beyond the prior sufficient family, not more rows of its old census.
The ordinary universal arguments, case completeness, and LP theorem are not
kernel checked or independently authored. Both implementations have same-assistant
authorship. Human review of the source fragment and a genuine geometric development
are still prerequisites for any surface inference. Retain these certificates;
do not repeat a larger grid as a purported breakthrough. Rotate to the next
eligible problem, reserving this local result for review or an actual new geometric
bridge.
