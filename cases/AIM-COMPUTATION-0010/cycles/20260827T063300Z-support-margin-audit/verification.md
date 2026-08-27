# Independent direct-dynamics verification

## Fresh-context method

`python -I verify.py` reads only `input.json`. It imports neither theory code nor
theory outputs and does not integrate the theory's scalar support polynomial.
For each constant-input segment it integrates x3 first, then x2, then x1 using
exact rational arithmetic. Its independent transition from (p,q,r) over dt is

    (p + 2*q*dt + 3*r*dt^2 + w*dt^3,
     q + 3*r*dt + 3*w*dt^2/2,
     r + w*dt).

Both executables were authored by the same assistant. Independence is algorithmic
and execution-context based, not independent human or fresh-model review. No
network, external model, randomness or floating-point operation is used by either.

## Counterexample and boundary search first

Before checking the scaling family, integrate the base +,-,+ input directly.
The endpoint is (13/2700,1/200,1/300); its objective is 11/5400. It violates b=1/500
by 1/27000, although the signed-radius value is only 1/600. All input amplitudes
obey their bounds. Thus the counterexample is reachable, not just box-feasible.

The correct box support is 19/600 and is inconclusive at b=1/400, while the exact
reachable support is below that threshold. Negative amplitudes, reversed time
intervals and out-of-bound sign certificates are rejected. Zero input and zero
horizon cases return zero and make no strict counterexample claim.

Time reversal is tested separately: for a=(0,1,-1), epsilon=1/100, T=1, the kernel
is 3*tau-1. Switching + to - at forward time 2/3 gives 1/120; the erroneous switch
at 1/3 gives only 1/200. This explicitly detects a mistake hidden by the base
case's symmetric roots.

## Computation and all-input proof checks

All eight sign patterns on three equal time intervals are integrated for each
of 30 rational parameter cases: 240 exact trajectories. Every endpoint lies in
its coordinate box. The largest objectives and the designated attaining states
agree with the theory output when compared AFTER independent execution.

These trajectories alone cannot establish a supremum over all measurable inputs.
For that purpose the verifier independently multiplies A into B three times,
checks A^3B=0, and checks the exact coefficient vector of a.exp(A*tau)B:
(2*T^2/3,-3*T,3). The ordered roots T/3,2*T/3 and positive leading coefficient
give the global sign partition. Together with k*w<=epsilon*|k|, this supplies the
separate analytic upper bound; the realized +,-,+ input supplies the lower bound.
Coefficient identities, not sampled time points, establish the polynomial identity.
Additional point evaluations are regression checks only.

The local proof-step audit checks zero initial state, measurability and bounded
input, variation of constants, lag versus forward time, absolute values in box
support, correlated versus independently signed errors, and terminal versus
pathwise claims. No unformalized step is labeled kernel accepted.

## Citation and scope checks

The primary AIM PDF identifies A.7 as Ian Mitchell's contribution in its August
19, 2005 version. It motivates the selected structured, one-sided approximation
target; it neither supplies this system nor makes the faulty margin claim.
`sources.json` records the locator and separates imported research-summary claims
from independently derived evidence. No inaccessible secondary paper is used
as a verified theorem dependency.

## Outcome

The signed-radius shortcut is falsified. The sound box rule and sharper directional
certificate are distinguished on an exact, fully specified model. Generalization
to other dynamics, nonzero initial sets or actual controllers remains open work.
This is a bounded regression certificate, not a solution of the parent agenda.
