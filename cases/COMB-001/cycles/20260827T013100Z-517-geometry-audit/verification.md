# Independent verification lane

## Independence basis

Verification began from the raw, hash-pinned `517.vtx` and `517.edge` files and
the frozen biconditional, not from a theory-lane conclusion. The verifier is a
new dependency-free implementation: it tokenizes a restricted coordinate
grammar, rejects unsupported syntax, performs rational multiquadratic field
arithmetic, and enumerates all unordered vertex pairs. It does not invoke or
translate the upstream Singular generator and does not reuse the prior cycle's
CNF checker.

## 1. Counterexample and boundary search first

Before accepting the unmodified inputs, the verifier exercised three
falsification probes:

- perturbing vertex 1's x-coordinate by `1/1000` made listed edge `{1,2}`
  fail the exact unit-distance test;
- injecting nonunit pair `{1,8}` as an edge was detected;
- replacing a coordinate by an existing coordinate triggered the collision
  predicate.

The strict parsers additionally reject input-hash mismatches, unsupported
coordinate tokens, negative or out-of-field radicals, division by zero,
malformed edge rows, loops, duplicate edges, and count/range mismatches.

## 2. Exact computation check

Command:

```bash
python experiments/verify_unit_embedding.py \
  --vertices /path/to/517.vtx \
  --edges /path/to/517.edge \
  --output experiments/independent-geometry-check.json
```

The script refuses inputs unless their SHA-256 hashes are:

- `517.vtx`: `402aa7b8a1145843366cff178dcfac44b97f8a748e318ae753520cbeb6a784d5`
- `517.edge`: `dc5085db9682aa246c3fc56efed9767e2a294a43e621a3e67a690d0489bdadc9`

Observed exact result:

- 517 coordinate pairs and no duplicates;
- 133,386 unordered pairs exhausted;
- 2,579 exact squared-distance-one pairs;
- 2,579 graph edges;
- zero listed nonunit edges and zero omitted unit pairs.

## 3. Algebra and quantifier check

The checker represents field elements as eight rational coefficients. Products
of basis radicals are reduced exactly, and division is implemented by solving
the eight-dimensional rational multiplication system. Equality with one means
coefficient vector `(1,0,0,0,0,0,0,0)` exactly.

The loops cover `u = 1,...,516` and `v = u+1,...,517`, so each unordered pair
appears once and only once. Set differences check both directions of the target
biconditional. Coordinate-set cardinality checks injectivity separately.

## 4. Source and scope check

The pinned repository tree independently confirms the coordinate, edge,
upstream checker-generator, and DRAT paths and their Git blob identities. The
current arXiv abstract for `1805.12181` supports a mechanical-validation claim
for 553-vertex graphs, not the identity of these later 517-vertex bytes. The
claim-to-source mapping therefore remains deliberately split.

Access date: 2026-08-27.

## Verification delta

The exact geometry objection from the prior cycle is discharged for the pinned
files: the coordinates injectively realize precisely the 2,579-edge graph as
their complete unit-distance graph. This is a finite reproducible computation,
not a claim about CNF unsatisfiability or the exact chromatic number of the
plane.

## Blocking objections

1. The 2.38 MB DRAT artifact exists and is hash-pinned, but no independent DRAT
   checker has accepted it in this cycle.
2. Exact paper-to-517-artifact publication lineage remains incomplete; the 2018
   abstract names 553 vertices.
3. Even a fully checked finite five-chromatic unit-distance graph supplies only
   the known lower-bound side of the parent problem.
