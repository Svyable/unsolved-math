# Independent verification of the fill-edge obstruction

## Independence and execution order

The verifier was authored, linted and run on the frozen input before theory.py was written. Initial RUF005 style feedback was corrected before that baseline; there were no failed mathematical subprocesses. Both implementations share the specification and author. Independence is fresh-process and algorithmic, not independent human/model review. No sub-agent, paid external model, or proof kernel was used.

Every run uses fresh Python -I, an empty environment, and resource limits: 180 CPU seconds, 200 seconds wall timeout, 512 MiB address space. This is not a network namespace. Mathematical code makes no network calls. Five subprocesses were run: baseline, theory, verification, and two replays. Source/input/output hashes are verified at assembly. Both replay outputs are byte-identical.

## Counterexample and boundary search first

The verifier constructs edges by extending paths, enumerates simple cycles from their least vertex, and retains exactly the induced ones. On the frozen W(3,3,3) it finds lengths 5,5,5,9 and degeneracy two. It then computes exact treewidth three without consuming a theory certificate.

Controls with sector lengths (1,3,3), (2,3,3), and (3,3,3,3) expose respectively a triangle, an even sector hole of length four, and an even rim of length twelve despite odd sector holes. C4 and K4 return treewidth two and three. These prevent confusing "odd number of spokes" with all required parity conditions.

## Independent algorithms and finite quantifiers

Theory predicts induced cycles from rim sectors. Verification enumerates all simple cycles generically and tests the induced degree-two condition. Its batched core peeling differs from the theory's minimum-degree single-vertex order. Both agree on the complete canonical 1,344-row table and its SHA-256, including all 40 eligible instances. This is not a census of all graphs or isomorphism classes.

For the 10-vertex witness, the treewidth checker uses dynamic programming over 1,024 eliminated-vertex sets and 5,120 transitions. Filled neighbors are independently reconstructed as endpoints of original-graph paths whose internal vertices have been eliminated. The recurrence minimizes the largest remaining filled degree over every vertex ordering. The stored optimal order is 0,1,...,9, with value three. No minor certificate is an input to this computation.

After reconstructing the summary, the verifier reads theory certificates. It checks graph reconstruction, permutation validity and actual no-fill widths; four connected, disjoint, mutually adjacent branch sets; a connected acyclic bag graph; bag size; vertex and edge coverage; and connected occurrence sets for every vertex. All 40 certificates pass. This stage intentionally consumes certificates, unlike the earlier baseline.

Seven deliberately damaged certificates are rejected by these semantic checks: missing edge, duplicated peeling vertex, empty branch set, overlapping branches, missing branch adjacency, uncovered edge after bag removal, and disconnected bag tree. These are targeted controls, not a complete security audit of the validator.

## Claim and proof-step audit

CERTIFICATES and SHORTCUT: exact cycle enumeration, peeling, and independent treewidth optimization establish the finite obstruction. The named branch sets and bag tree give separately checked upper/lower certificates. The first two fill edges are also transparent in the explicit edge list; the full fill trace is a theory artifact, not separately claimed as a verifier output.

EXPERIMENT: the summary hashes the full canonical table, which is also retained as theory-table.json. Assembly checks that file's bytes against the summary digest. Verification generates its own table in memory and hashes it before comparison.

FAMILY: the hub-free versus hub-containing cycle dichotomy explains the parity test. Bag edge coverage and connected occurrences extend directly with the rim size; the minor argument uses only three spoke vertices. These ordinary all-size proof steps, the elimination/treewidth equivalence and minor monotonicity lack independent human/model or kernel review. The finite computation cannot discharge that objection.

SOURCE: primary pages were fetched and mapped in sources/source-audit.md. The incomplete AIM extraction remains unchanged. The 2024 replacement theorem is a dependency of the earlier corollary, not a theorem reproved by these wheels. A separate primary paper already describes stronger minor obstructions, so the small witness is calibration rather than novelty.

## Delta and remaining objections

The verifier newly separates degeneracy from filled-elimination width inside the intended graph class and validates concrete graph-theoretic certificates, rather than repeating the earlier list-coloring enumeration. It retires one proposed shortcut. The global structural dependency and human scope review remain; no parent or upstream status change is supported.
