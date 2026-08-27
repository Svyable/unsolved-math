# Theory lane: exact unit-distance realization

## Frozen target

For `vtx/517.vtx` and `edge/517.edge` at CNP-SAT commit
`bb414955a6ef5f49f7df2b245b1e778aa67c068a`, test the finite biconditional

\[
\{u,v\}\in E \quad\Longleftrightarrow\quad
(x_u-x_v)^2+(y_u-y_v)^2=1
\]

for every pair of distinct indices `1 <= u < v <= 517`, and test that the 517
coordinate pairs are distinct. This target is strictly smaller than checking
four-uncolorability or deciding the plane's chromatic number.

## Definitions and quantifiers

- `K = Q(sqrt(3), sqrt(5), sqrt(11))`, represented on the basis
  `1, sqrt(3), sqrt(5), sqrt(11), sqrt(15), sqrt(33), sqrt(55), sqrt(165)`.
- `p_v = (x_v,y_v)` is the exact coordinate pair on row `v` of the pinned
  vertex file.
- `E` is the simple undirected edge set in the pinned edge file.
- A *complete unit-distance realization* here means that the coordinate map is
  injective and, for all `u < v`, membership in `E` is equivalent to exact
  squared distance one. Completeness is stronger than the subgraph condition
  needed for a unit-distance lower-bound certificate.

## Assumptions

1. The fetched vertex and edge files match their recorded SHA-256 digests.
2. `Sqrt[n]` denotes the positive real square root and ordinary arithmetic in
   the displayed coordinate expressions.
3. Vertex row numbers correspond to edge-file endpoint numbers.
4. No satisfiability, DRAT, or paper-to-artifact-lineage conclusion is assumed.

## Approaches considered

1. **Exact multiquadratic arithmetic.** Parse a restricted expression grammar
   and reduce every operation in `K`; compare every squared distance with the
   exact field element `1`. This approach was executed exhaustively.
2. **Upstream Singular reduction.** The pinned `check_dist_one.py` translates
   listed-edge obligations into polynomial reductions modulo radical relations.
   This is a useful independent method family, but Singular is not present in
   the execution environment and the upstream generator does not check nonedge
   pairs or coordinate collisions.
3. **High-precision numerical screening.** This could rapidly locate suspected
   failures, but a tolerance cannot certify an exact algebraic equality and was
   therefore not accepted as the evidentiary endpoint.

## Typed claims and falsifiers

| Claim | Origin | Status | Statement | Falsification condition |
|---|---|---|---|---|
| G1 | Derived from pinned coordinate syntax | Experimentally supported | All 517 coordinate expressions parse in `K`. | An unsupported token/radical occurs, a denominator is zero, or a parsed value lies outside the eight-element field basis. |
| G2 | Exact exhaustive computation | Experimentally supported | The 517 coordinate pairs are distinct. | Two coordinate rows reduce to the same ordered pair in `K^2`. |
| G3 | Exact exhaustive computation | Experimentally supported | Among all `517 choose 2 = 133,386` pairs, exactly 2,579 have squared distance one, and that pair set equals `E`. | A listed edge has nonunit distance, an unlisted pair has unit distance, or the pair/edge counts differ. |
| G4 | Pinned repository inspection | Primary-source supported with scope limit | The upstream repository contains an edge-distance checker generator and a 517 DRAT artifact. | The pinned tree lacks either path or its blob identity differs; existence alone does not validate either artifact. |

## Progress unit: exact finite certificate

The coordinate vocabulary reduces to the multiquadratic field `K`: radicals
such as `sqrt(33)`, `sqrt(55)`, and `sqrt(165)` are products of the three field
generators, while `sqrt(11/3) = sqrt(33)/3` and
`sqrt(5/3) = sqrt(15)/3`. Exact multiplication uses

\[
\sqrt a\sqrt b = \gcd(a,b)\sqrt{ab/\gcd(a,b)^2}
\]

for square-free basis radicands. Consequently every distance comparison is a
rational-coefficient identity, not a floating-point tolerance test.

The exhaustive result is: 517 distinct coordinate pairs, 2,579 exact
unit-distance pairs, 2,579 listed edges, zero listed nonunit pairs, and zero
omitted unit pairs. The previously opaque geometric obligation has therefore
moved to a reproducible exact finite certificate for these pinned bytes.

This does not establish that the graph is not four-colorable.

## Next theoretical obligation

Pin a maintained DRAT checker and validate
`proof/517-4-sbp.drat` against the already-audited CNF. Only after that check may
a forcing implication or checked core be extracted; the parent problem remains
outside the conclusion vocabulary.
