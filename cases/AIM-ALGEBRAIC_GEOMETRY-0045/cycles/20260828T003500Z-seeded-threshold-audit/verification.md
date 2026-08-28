# Independent-method verification

The baseline verifier was authored and run before theory.py existed. It starts
with k=1,d=2 (ceiling versus floor), k=0,d=2 (zero seed), and k=4,d=3 (exact
division), then reconstructs the full bounded domain before reading any theory
output. It shares the frozen specification, not mathematical implementation.

Binomials are constructed as Fraction products; the recurrence uses the adjacent
binomial identity. Thresholds are found by exponential bracketing and binary
search of the dimension inequality, not quotient/remainder ceiling arithmetic.
Every candidate must satisfy the inequality and have a failing predecessor.
The seed power uses repeated multiplication; powers of two are searched by
doubling. Factorial exponents are accumulated independently.

All seven recurrence rows, 1111 boundary cases and sixteen exponent comparisons
agree with theory. Of the grid cases, 351 reject floor substitution. At d=5 the
exact predecessor deficit is 204337; thus the recorded failure has a concrete
integer witness. The dyadic comparison has strictly positive gaps on both sides.
The d=7 exponent comparison is 3595 versus 3600; the exact recurrence remains
stronger. Seven mutations are rejected by full reconstructed-table equality:
floor rounding, seed decrement, omitted row, altered slack, decreased log bound,
changed exponent and wrong boundary threshold. These include integrity tests;
rejection does not mean every mutated number is an invalid sufficient bound.

## Proof-step and source checks

The threshold witness is only minimal for the stated dimension inequality.
It is not a lower bound on actual unirationality. The seed propagation separates
the base d=5 from induction d>=6; A_d is integral in the stated range. Ceilings
must be applied after multiplying the rational log bound by A_d. General versus
every smooth hypersurface quantifiers must not be interchanged.

The universal recurrence estimate is located in the primary source and the
algebraic induction is recorded, but neither its arbitrary-degree proof nor the
geometric construction has independent human/model/kernel verification here.
The two programs have same-assistant authorship and shared specification; their
algorithmic separation does not remove correlated specification/source errors.
The original AIM page was unavailable. Imported status and statement are unchanged.

## Reproduction

From this packet directory run:

```
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

The runner uses fresh Python -I processes, empty environments and explicit
CPU/wall/memory limits. There are no network calls or imported code execution in
the mathematical programs; resource isolation is not a network namespace.
Replay requires identical output bytes. Execution logs pin source/input/output
hashes. One preliminary arithmetic probe preceded these five logged children;
the run stayed within the eight-child research budget. A mistyped replay path
failed before any child experiment and was corrected; successful replay is logged.
