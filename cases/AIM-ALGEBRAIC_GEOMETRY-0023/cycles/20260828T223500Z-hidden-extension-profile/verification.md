# Verification lane: direct sums of digits before block formulas

## Independence and order of work

The baseline verifier was written and run before theory.py existed. It started
with one-digit, split, nonsplit and rearranged-carry boundaries, then enumerated
the domain from input.json. It uses literal addition and repeated addition to
zero, not the block decomposition, gcd formula or order-count formula.
Each run uses a fresh Python -I process and distinct output. This provides
algorithm/process separation, not independent authorship: the same assistant
wrote both programs, which share the model, tuple order, JSON serialization
and Python runtime. No independent human/model or kernel verification occurred.

## Counterexamples and boundaries first

The five initial rows have exponents 2,2,4,8,4. In particular the last two
have the same number of digits and 1-edges but different exponents. This
search is performed before reading any theory certificate, even on replays.
The exhaustive census covers p=2,n=1..7; p=3,n=1..5; p=5,n=1..4, all binary
edge words at each length. There are 173 groups and 21,142 elements. The entire
ordered per-element order digest agrees in every row, not just a grand total.
The row digest is b58a75cc2f21d31dbeeb9c435f5084881209829dd71d4fdd334509a56823631c.

For p=2,n<=3 all associativity triples and all commutativity/truncation pairs
were checked: 2,184 and 292 respectively. Filtration-layer cardinalities were
also checked there. This is finite evidence; group laws for arbitrary length
and prime still rely on the displayed presentation/decomposition argument.

## Certificate audit and a real checker failure

Six supplied matrices are checked against literal digit addition. The revised
checker requires both injectivity and surjectivity onto the proposed cyclic
product, plus addition compatibility with each generator for every element.
It verifies exact witness order, a surviving exponent/p multiple, and that
the claimed exponent kills all elements. There are 904 generator checks.

The first certificate run failed its mutation test: reducing a cyclic modulus
gave a surjective homomorphism, and the original checker mistook this for an
isomorphism. A diagnostic rerun reproduced this failure. The repair adds the
missing requirement that the image cardinality equals the domain cardinality.
The original verifier is archived in experiments/baseline-verifier.txt; its
hash matches the baseline execution and failed-execution.json. The failed
run's stderr is retained. The first failed invocation did not persist stderr
because the runner used check=True; execution-notes.md discloses this gap.

After repair the same 173 rows remain unchanged; all six certificates pass.
Seven mutations are rejected: wrong exponent, erased surviving multiple,
zeroed matrix entry, shortened modulus, missing census row, wrong order count,
and missing certificate. The shortened-modulus test is the regression test
for the actual defect. These tests are not a proof of verifier completeness.

## Proof-step audit

The normal form maps within a finite block to an ordinary base-p residue; the
zero edges remove cross-block relations. The inverse transition deletes high
digits, so the infinite product decomposition respects the frozen system.
A subtle case is infinitely many finite blocks of unbounded lengths: there
need not be any infinite block, but the element taking value 1 in every block
is still not torsion. Replacing the product by a direct sum would break this
step. A final infinite block is the other case and uses the old coordinate
escape argument. Bounded blocks give a single annihilator, not merely one
annihilator per associated-graded piece.

The zero-differential filtered complexes have entries only in total degree
zero; the filtration direction is unbounded. Every page can coincide while
the additive extensions differ. Completeness and separation are checked for
the integral filtration, not assumed to survive rationalization. In the
all-carry case, rationalizing each finite filtration step makes every step
the whole rationalized group, so separation is exactly what fails. The
finite-width proof uses p F^i subset F^(i+1) exactly L times; its exponent
p^L is attained by an all-carry block. No independent universal proof review
or spectral-to-TC comparison has been completed.

## Reproduction

From the packet directory run:

```
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

The stored baseline used the archived verifier; future baseline runs use the
repaired verifier, whose census is byte-identical. To preserve the historical
log, reproduce in a copy. Successful theory and verification replays reproduce
exact bytes. Execution logs record input/source/output SHA-256, Python version,
commands, empty environment and limits. Resource/process isolation is not a
network namespace; the programs contain no networking or dynamic execution.
Seven mathematical children were used, including the two failures. Remaining
operational checks and packet hashing are not new mathematical experiments.

## Citation and scope checks

See sources/verification-source.md for precise primary-source locators. The
new source distinction is finite filtration versus bounded homological degree,
not a claim that a published theorem is wrong. AIM failed twice, so its live
scope and the imported status are unverified. The earlier Segal and current
HRW abstracts are contextual only. No TC, TP, THH, Frobenius, motivic weight
or parent-solution assertion follows from these finite abelian groups.
