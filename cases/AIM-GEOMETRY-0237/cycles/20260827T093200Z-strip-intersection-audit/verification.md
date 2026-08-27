# Counterexample-first verification

## Independence and order

`verify.py` starts in a fresh `python -I` process. It imports neither the theory
script nor its mathematical construction routine. First it reads only
`input.json`, tests its generic polygon clipping implementation on boundary,
empty and reversed-orientation cases, and searches for oversized rectangles
that could fit a single strip. Only then does it read the proposed rectangle
coordinates from `theory-output.json` as **untrusted certificate input**.
The certificate is not an independent discovery; independence here is generic
checking by a different algorithm and isolated execution context. Both programs
and both notes have same-assistant authorship. There is no independent model,
human referee, or formal kernel acceptance.

## Falsification and boundaries

Five polygon controls pass, including a clipped half-square, empty intersection,
zero-area tangency, diagonal half-square, and reversed vertex order. For all 216
configured combinations of width, excess factor, aspect ratio and rational
orientation, direct vertex projections exceed the available single-strip width.
Translations cannot change this span. A length-10, width-1 horizontal rectangle
fits the width-1 band exactly, so equality is not rejected. These finite tests
exercise the implementation; they do not prove the universal obstruction.

An independent proof of the obstruction uses an inscribed circle: every rectangle
of shorter side w contains a disk of radius w/2. A disk contained in a strip of
width delta has diameter at most delta. Hence w<=delta. This also handles all
rotations/translations and does not depend on the theory's projection formula.
It is a proof-step audit, not kernel verification.

## Exact certificate checking

For each certificate the verifier independently checks normal normalization,
the input direction relation `s=u(1+c)`, positive dimensions, exact dimensions
and area, and the stated point outside S+ but inside S-. It computes four
complement polygons using generic half-plane clipping: each is R intersected
with one exterior side of S+ and one exterior side of S-. Their exact shoelace
areas are zero for all 96 certificates, across 384 complement-region tests.

Why does zero area certify **all points**, not just almost-everywhere containment?
S+ union S- is closed. If a point of the nondegenerate closed rectangle were
outside that union, a sufficiently small relative neighborhood of that point
inside the rectangle would be outside too and have positive area, even at an
edge/corner. It would lie in one of the four exterior combinations. Thus a
nonempty true complement cannot hide on a zero-area boundary. The clipping uses
closed exterior half-planes, a superset of the strict complement, so zero area
is sufficient. No floating-point tolerance or grid sampling is used.

63 certificates have shorter side > delta; all 96 are outside the intersection
at their stated witness. The exact example is rechecked against input parameters,
and its intersection-violation margin is 9/10.

Seven deliberately corrupted certificates are rejected: wrong normalization,
extended right endpoint, widened rectangle, false area, reversed interval,
zero strip width and false witness margin. The extension beyond b has a concrete
gap point `(b+1,0)`, outside both strips by `2000/1000001` in the example.
This exposes the necessity of the overlap endpoint, not just metadata checks.

## Citation and proof-step audit

The primary survey's printed pp.13–14 confirms the surrounding question,
commentary boundary and intersection wording. Its passage concerns a closed
surface of genus at least two; the exact planar experiments make no surface
construction. No inference that its finiteness theorem is false is warranted.

The separately checked [Wu v4 abstract and revision record](https://arxiv.org/abs/1309.6539v4)
is dated March 31, 2015, later than the v3 citation in the survey. It states
additional hypotheses and reports a proof-gap correction. This is provenance
triage only: the full proof and any link to the local wording are **not** audited.
Do not conflate that documented correction with this packet's local observation.

Checks on the mathematical steps: c^2+s^2=1 establishes full perpendicular
width; intervals need overlap before filling their union; positive x determines
which lower endpoint limits the rectangle; shorter-side and designated-height
conventions are kept separate. The asymptotic claim requires u tend to zero
after epsilon is chosen and enough length to make height the shorter side.

## Remaining objections

- The source's intended geometric construction/wording needs expert review.
- A local planar union is not automatically a globally defined immersed or
  embedded strip on a closed surface; no global development is certified.
- No maximal-strip counting convention, periodicity theorem, general finiteness
  theorem, or imported area estimate was checked.
- No current-status, novelty, parent-problem or kernel-accepted claim.

The verification delta is a new exact certificate-checking result plus a
counterexample/boundary suite; it is not independent human agreement.
