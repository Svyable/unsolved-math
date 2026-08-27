# Local strip-widening audit

## Frozen scope and definitions

The exact imported record is in `snapshot.json`; selection and the separately
unverified imported research summary are in `selection.json`. The selected text
includes commentary, a question-number fragment and a page header. It is not
silently replaced by a neighboring question. This cycle tests one explicit
sentence's **local Euclidean interpretation**, not the existence, periodicity,
or finiteness of flat strips on a closed surface.

Fix full perpendicular width delta > 0. A closed planar strip is the set
`|n dot z - q| <= delta/2`, where n is a unit normal. A nondegenerate rectangle
has orthogonal side lengths L >= w > 0; its width means the shorter side w,
not a half-width or a chosen long side. Translation and orientation are arbitrary.
No immersion, global surface identification, or counting convention is built
into this local model. This distinction limits the source inference below.

## Two approaches

1. Follow a literal intersection-widening route. This is retired in the planar
   model: normal projection gives a universal obstruction, independently of
   how shallow the crossing angle is.
2. Construct a rectangle in the **union** using overlapping vertical sections.
   Exact rational normals allow a generic polygon checker to test the proposed
   repair without accepting the construction algebra. This is a local alternative,
   not a claimed correction of the cited global proof.

## C1: obstruction to the literal intersection claim

Origin: imported-unverified sentence, explicitly interpreted in the local model.
Status: FALSIFIED under that interpretation. Falsifier: any claimed rectangle in
the intersection with shorter side > delta contradicts the following projection.

Let e1,e2 be the rectangle's orthonormal side directions. Its projection onto
the unit normal n of the first strip has length

`L |n dot e1| + w |n dot e2| >= w (|n dot e1| + |n dot e2|) >= w`.

The last inequality follows because the two squared components sum to one.
Containment in that strip forces this projection to have length at most delta,
so w <= delta. The intersection is a subset of the first strip. Thus **no**
rectangle in the intersection has shorter side > delta, at **any** angle or
translation. In particular no sequence of such widths can tend to 2 delta.
The equality boundary w=delta is possible in a single strip; no strict
inequality is asserted there. This is a written elementary proof, not a
kernel-accepted result, and the finite tests are not its justification.

## C2: exact union construction

Origin: DERIVED. Status: EXPERIMENTALLY_SUPPORTED, with the following written
all-parameter argument. Falsifier: a point of the specified rectangle outside
both strips, a non-unit normal, or incorrect exact coordinates/dimensions.

For 0 < u < 1 define c=(1-u^2)/(1+u^2), s=2u/(1+u^2).
Then c,s>0 and c^2+s^2=1. Consider

`S+ = {|c y + s x| <= delta/2}`, `S- = {|c y - s x| <= delta/2}`.

For 0 < epsilon < 1 put

`b = delta/(2s)`, `a=(1-epsilon)b`,
`H=delta(2-epsilon)/(2c)`, `R=[a,b] x [-H,H]`.

At x in [a,b], the vertical strip sections are centered at +/-sx/c and have
half-height delta/(2c). They overlap since sx <= delta/2. Their union is the
single interval `[-(delta/2+sx)/c, (delta/2+sx)/c]`. Its smallest extent on
[a,b] occurs at a and equals H. Consequently all of R lies in S+ union S-.
The point (a,H) lies on the upper boundary of S- but violates S+ by exactly
`cH+sa-delta/2 = delta(1-epsilon)>0`.

The rectangle has length epsilon*delta/(2s) and height delta(2-epsilon)/c.
Only when length >= height is that height its shorter-side width. The table
does not silently assume this: 63 of the 96 certificates have **both** sides
longer than delta. All 96 satisfy union containment and non-containment in the
intersection.

For any desired width tolerance eta in (0,1) and length target K>0, first take
epsilon=eta/2. As u tends to zero, c tends to 1, s tends to 0, height/delta
tends to 2-epsilon, and length/delta diverges. Choosing sufficiently small
positive rational u therefore gives length at least max(K,2)*delta and
shorter-side width strictly between (2-eta)*delta and 2*delta. The crossing
angle tends to zero. This establishes the intended near-double, arbitrarily
long behavior **in the union**, not the intersection.

## Concrete changed evidence

`theory.py` generates 96 exact rational certificates. For delta=1,
epsilon=1/10, u=1/1000:

- c=999999/1000001, s=2000/1000001;
- x runs from 9000009/40000 to 1000001/4000;
- H=19000019/19999980;
- length=1000001/40000, width=19000019/9999990;
- (a,H) violates the first strip by exactly 9/10.

This rectangle belongs to the union but cannot belong to the intersection.
The exact stored certificate and general obstruction retire the literal local
intersection route and give a discriminating replacement test. This is elementary
geometry, not a novelty claim or a solution to a geodesic problem.

## Source and remaining dependencies

The [Burns–Matveev survey](https://aimath.org/pastworkshops/geodesicsproblems.pdf),
printed pp.13–14, places the passage after Question 6.2.1 and uses the word
“intersection” in the local widening explanation. The geometric model above
shows why that wording cannot be used literally for two planar strips with
full-width convention. It does **not** establish what the authors intended.

No global union-development, immersion, maximal-strip counting, area bound,
or Cao–Xavier argument is verified here. Nor does the union certificate show
that the needed planar region develops injectively on a surface. These remain
human-review obligations. No upstream statement/status was changed.
