# Verification lane

## Independence and order

The verifier was authored and its baseline executed before theory.py existed.
Original source bytes are retained in verify-original.py.txt and
theory-original.py.txt. Later changes only replace list concatenation with
unpacking and wrap long lines; final replay checks their unchanged outputs.
The baseline starts only from input.json. It checks counterexamples and boundary
cases first, reconstructs the full finite census, and writes baseline.json and
verification-table.json. Later verification repeats reconstruction before
reading theory-output.json. No theory functions are imported.

Method families: COUNTEREXAMPLE_SEARCH, INDEPENDENT_IMPLEMENTATION,
PRIMARY_SOURCE_AUDIT and PROOF_STEP_AUDIT. Union-find connectivity and literal
path traversal are distinct from the theory's reachability search and cycle
coordinates/divmod. Processes use Python -I, an empty environment and recorded
resource limits. Isolation is not a network namespace or independent authorship.
Both implementations and this review are by the same assistant using the same
frozen specification; no separate human/model or formal kernel participated.

## Counterexamples and boundary cases first

The baseline confirms the supplied three-sheet action is transitive and closes
the n=5 walk. Its first positive B-return is at time 2. Counting returns gives
2 complete traversals, not 1. Literal stepping ends at 1, whereas reducing the
exponent modulo total degree ends at 0. Thus the proposed algebraic shortcut
is genuinely false, without invoking any topological theorem.

Boundary controls: d=1,n=0 yields a valid one-edge graph loop; n=0 closure
depends on A fixing x even if B moves it; disconnected actions are excluded;
nonbijective lists are rejected. Enumeration includes n=0, d=1, exact period
multiples, residual partial cycles and several B-cycles in one connected action.

## Claim, computation and certificate checks

- P1: checked permutations, transitivity, orientation/order, exact endpoint,
  closure and return count. No floating point or tolerance is used.
- P2: every rooted case checks the endpoint modulo its first return, and counts
  literal positive-time returns against floor(n/m). Zero mismatches.
- P3: each construction checks bijections, transitivity, closure and distinct
  preclosure vertices. This certifies embedded graph circles, not a necessary
  test for surface simplicity. If n>=d no enumerated path passes that criterion.
- All 65 rows agree, including all 742,417 rooted exponent cases. The table
  covers every pair in S_d squared for d=1,...,5, filtered by transitivity, all
  base sheets and n=0,...,12. It is not a sample of isomorphism classes.
- Seventeen constructions for n=0,...,16 pass. Seven altered certificates fail:
  changed period, endpoint, winding, closure, census count, permutation and
  omitted exponent. Full reconstruction also detects omissions and extra fields.
- Replay reproduces both outputs byte-for-byte. Seven mathematical subprocesses
  total: baseline, theory, verify, initial replay pair and post-style-fix replay
  pair. Original logs resolve to the archived source bytes; the final replay
  resolves to current .py files. Per process:
  CPU 180s, wall 200s, address space 512MiB and output-file limit 16MiB.

## Proof-step and citation audit

The local-period proof uses invertibility, not connectedness. Time zero is
excluded from the winding count. The closing A-step is excluded from B returns.
The n=0 construction has two differently labelled loops available but traverses
only its A-edge. For general n the closing edge is labelled A, not the unused
closing B-edge; equal permutations do not identify those edges.

The source ledger records a separate HTML check of the versioned primary paper
and locators. No PDF source bytes or figure topology are certified here. The
paper's contradiction hypothesis includes surface simplicity; our example does
not satisfy it. Consequently the example cannot refute that theorem or its
full implication. It only prevents a transcription from using connectedness
alone to infer a full-degree B-cycle. The required surface-neighborhood and
minimal-intersection arguments remain explicit external dependencies.

For the concentration step, forall gamma exists finite D_gamma is weaker than
exists D forall gamma. A growing sequence of minimal degrees supplies no
infinite bounded subfamily of that sequence, but says nothing against another
infinite bounded subfamily. This distinction prevents an overstatement about
all simple geodesics or the neighboring three-manifold question.

## Remaining objections

The source fragment still needs human scope review. No surface simplicity
checker, metric realization or uniform geometric degree hypothesis was added.
The general proofs are ordinary mathematics with same-assistant review, not
independent proof acceptance. Larger permutation tables would not resolve any
of these objections and should not be counted as another progress unit.
