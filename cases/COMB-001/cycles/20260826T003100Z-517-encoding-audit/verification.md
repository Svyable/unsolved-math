# Independent verification lane

## Independence basis

The verification began from the pinned edge and CNF byte streams, not from the
theory conclusion. The first derivation used direct clause-count reasoning in a
separate JavaScript context. Verification used a fresh, dependency-free Python
implementation with a strict parser, explicit expected-clause construction,
set equality, and adversarial mutations. The Python source and machine-readable
output are stored in this packet.

## 1. Counterexample and boundary search first

The checker rejected or detected the following falsification cases:

- deleting one expected clause produced exactly one missing clause;
- injecting the tautology (x_{1,1}lorlnot x_{1,1}) produced exactly one
  unexpected clause;
- virtually deleting any of {1,2}, {1,6}, or {2,6} made the triangle
  precondition false and left four edge/color clauses unexpected;
- strict parsing checked headers, terminators, literal and vertex ranges,
  loops, duplicate edges, duplicate clauses, tautologies, and input hashes.

All three triangle edges were present in the unmodified graph. No malformed
input or clause-set mismatch was found.

## 2. Computation check

Command:

```bash
python experiments/verify_coloring_encoding.py \
  --edge /path/to/517.edge \
  --cnf /path/to/517-4-sbp.cnf \
  --output experiments/independent-check.json
```

The script refuses inputs unless their SHA-256 digests are:

- `517.edge`:
  `dc5085db9682aa246c3fc56efed9767e2a294a43e621a3e67a690d0489bdadc9`
- `517-4-sbp.cnf`:
  `c9757e78853383462ca20b4702fc6b1cc46d88c5de71d305726396856f4765b8`

Observed result: 517 vertices, 2,579 edges, 2,068 variables, and 13,935
clauses; zero missing and zero unexpected clauses.

## 3. Proof-step check

For any proper coloring (f), the triangle edges force
(f(1),f(2),f(6)) to be pairwise distinct. A permutation of four colors exists
that sends these three values to 1, 2, and 3 respectively. Applying that
permutation to every vertex preserves inequality across every edge. Thus the
three positive unit locks preserve satisfiability of the graph-coloring formula.

The exact boundary condition is the triangle: if any of the three edges is
removed, this argument no longer applies without an additional reason.

## 4. Primary-source audit

- Aubrey de Grey, arXiv:1804.02385, states that a family of finite plane
  unit-distance graphs is not four-colorable and reports a 1,581-vertex graph.
- Marijn Heule, arXiv:1805.12181, reports SAT-based reduction to 553-vertex
  unit-distance graphs and says the non-four-colorability can be mechanically
  validated.
- The pinned CNP-SAT repository commit supplies the specific 517-vertex edge
  and CNF artifacts audited here. The arXiv abstract alone does not identify
  these exact 517-vertex bytes, so repository provenance and paper claims are
  intentionally recorded separately.

Access date: 2026-08-26.

## Verification delta

The finite input has moved from an opaque external artifact to a reproducible,
hash-pinned structural certificate: the CNF is an exact symmetry-fixed
four-coloring encoding of the graph, and the color locks have an explicit
triangle-based justification.

## Blocking objections

1. No coordinate artifact was audited. The claim that all graph edges arise
   from unit distances in the plane remains unchecked here.
2. No SAT solver or DRAT checker was run. The CNF's unsatisfiability remains
   unchecked here.
3. The paper-to-517-artifact lineage needs a more detailed primary-source audit
   than the arXiv abstracts and pinned repository path provide.
4. Nothing in this cycle determines the minimum chromatic number of the plane.
