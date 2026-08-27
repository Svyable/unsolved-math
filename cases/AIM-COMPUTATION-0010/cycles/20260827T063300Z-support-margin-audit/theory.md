# Signed radii are not a support bound

Agent output is unverified research assistance, not a mathematical result.

## Frozen question and bounded target

The exact source agenda is in `snapshot.json`, selected at actual queue rank 3
after the two earlier candidates entered cooldown. Its source asks about one-sided
approximations and structured dynamics; it does NOT propose the faulty margin
tested here. This is an assistant-derived regression target, not an attribution
of an error to the source authors or a solution to the entire research agenda.

One falsifiable claim: given certified coordinate error radii rho, can a signed
dot product a.rho certify a terminal halfspace a.x<=b? We compare that shortcut
with the correct box support and a correlation-aware reachable-set support.

## Definitions, quantifiers and assumptions

Take every T>=0 and epsilon>=0. The state is in R^3 with initial condition x(0)=0,
and dynamics x1'=2*x2, x2'=3*x3, x3'=w. The scalar input is any measurable function
with |w(s)|<=epsilon almost everywhere on [0,T]. These bounded inputs have unique
absolutely continuous solutions for this fixed linear system. The zero trajectory
is the surrogate (w=0). Coupling coefficients 2 and 3 are not claimed small;
epsilon bounds the residual forcing, not those couplings.

R(T) is the set of terminal states over all such inputs. A support value is
h_R(a)=sup{x.a : x in R}. Coordinate radii mean |x_i(T)|<=rho_i(T). The outer box
is the Cartesian product [-rho_i,rho_i]; its support is sum_i |a_i|rho_i.
The halfspace is safe at T if EVERY admissible input has a.x(T)<=b. This packet
does not automatically extend a terminal claim to pathwise safety, nonzero initial
uncertainty, nonlinear dynamics, or a numerical HJ solver.

## Two approaches

1. Coordinate comparison: integrate nonnegative impulse-response components to
   bound each coordinate, then use the dual box norm sum |a_i|rho_i. It is sound
   but discards correlations from the shared scalar input.
2. Directional convolution: integrate the absolute value of the scalar impulse
   kernel and exhibit an input attaining it. Rational kernel roots give exact
   certificates without floating-point quadrature or a full state-space grid.

The signed-radius shortcut is retired by a realizable trajectory, not merely a
box corner that might lie outside the reachable set. No novelty claim is made.

## Exact derivation and certificate

Here A^3=0 and exp(A*tau)B=(3*tau^2,3*tau,1). Variation of constants gives
x(T)=integral_0^T exp(A*(T-s))B*w(s) ds. Thus
rho=epsilon*(T^3, 3*T^2/2, T). Each coordinate bound is attained by a constant
positive input, but the coordinates cannot generally choose signs independently.

Choose a(T)=(1,-T,2*T^2/3). Its scalar lag kernel factors as

    k_T(tau) = 3*tau^2 - 3*T*tau + 2*T^2/3
             = 3*(tau-T/3)*(tau-2*T/3).

For every admissible w, a.x(T)<=epsilon*integral_0^T |k_T(tau)| d tau.
The kernel is positive, negative, positive on its three successive thirds.
The input w(s)=epsilon*sign(k_T(T-s)) attains the bound. In this symmetric case
its forward-time signs are also +,-,+. Exact integration gives

    h_R(a(T)) = 11*epsilon*T^3/54,
    a(T).rho(T) = epsilon*T^3/6,
    h_box(a(T)) = 19*epsilon*T^3/6.

The attaining endpoint is
(13*epsilon*T^3/27, epsilon*T^2/2, epsilon*T/3).
The all-input upper bound uses the sign factorization and the inequality
k*w<=epsilon*|k|, not the number of trajectories sampled. This is a transparent
analytic argument backed by exact coefficient/trajectory checks, not a kernel proof.

## Base case: epsilon=1/100, T=1

| Quantity | Exact value | Consequence |
|---|---:|---|
| Signed-radius shortcut | 1/600 | Incorrectly passes threshold 1/500 |
| Exact reachable support | 11/5400 | Exceeds 1/500 by 1/27000 |
| Correct box support | 19/600 | Sound but too conservative to certify 1/400 |

The explicit input is +1/100 until 1/3, -1/100 until 2/3, then +1/100 until 1.
It reaches (13/2700,1/200,1/300), which lies within the certified box but violates
the purported terminal guarantee. This gives a concrete false-safe certificate
for the shortcut. At the looser threshold 1/400, the exact support is smaller by
1/2160, so the directional bound certifies the terminal halfspace while the box
bound is inconclusive. An inconclusive box bound is not evidence of unsafety.

## Evidence and boundaries

`theory_check.py` computes the convolution integrals with exact fractions for
30 (epsilon,T) cases, including ten zero-scale boundaries and twenty strict
counterexamples in the scaling family. `theory-output.json` includes all attaining
states and bounds. These repetitions test scaling and arithmetic; they are not
thirty unrelated discoveries or evidence for arbitrary system matrices.

The independent lane integrates the triangular ODE directly, checks all eight
third-wise sign patterns for each case, and reconstructs polynomial coefficients
from A, AB and A^2B. An asymmetric kernel test catches the time-reversal mistake
that the symmetric base example alone cannot detect.

Remaining: no general comparison theorem or nonlinear model-mismatch analysis,
no verified numerical solver, no formal kernel or independent human/model proof
review, and no real-world control deployment. The imported status is unchanged.
