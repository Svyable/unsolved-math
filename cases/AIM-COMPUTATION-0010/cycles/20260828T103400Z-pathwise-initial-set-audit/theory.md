# Pathwise certification with correlated initial uncertainty

## Scope and exact delta

The frozen Mitchell agenda is broader than this model. The prior cycle studied terminal support with zero initial state in a three-state chain. Its requested next step was a second sparse model with nonzero initial uncertainty. This packet supplies that model and changes the time quantifier from one terminal instant to every time in a closed interval. It is elementary known-method calibration, not a novel reachability algorithm or solution of the parent agenda.

Fix real d,e,a,epsilon,T >= 0 and real vbar. For every z=(z1,z2) in [-1,1]^2 and every measurable w with |w|<=epsilon almost everywhere, let

    x'=v, v'=-a+w,
    x(0)=d(z1+z2), v(0)=vbar+e(z1-z2).

The initial set is the image of the square under this affine map, including degenerate d=0 or e=0. Safety here means x(t)<=b for all z,w,t in [0,T], not safety of a physical controller. Supremum is over input functions and initial points, not over feedback strategies. The census uses all 648 rational tuples in input.json, with order d,e,vbar,a,epsilon,T.

## Approaches and falsifiers

1. Certify the interval from the three times 0,T/2,T. Retire this proposed shortcut if one admissible trajectory exceeds their worst upper bound between samples. This is our proposed test, not a claim made by the source.
2. Propagate independent coordinate intervals for initial x and v, then maximize continuously in time. This is sound but can be loose. Refute any claim of tightness by a strictly smaller attainable upper bound using the actual correlated set.
3. Preserve the two initial generators and derive a piecewise quadratic support envelope, then check endpoints, its kink, and feasible stationary points. A missed critical point, wrong integral sign, or nonattainable maximum falsifies the claimed exactness.

## Ordinary proof argument (not independently authored or kernel-checked)

Twice integrating the differential equations gives

    x(t)=d(z1+z2)+[vbar+e(z1-z2)]t-a*t^2/2
         + integral_0^t (t-s)w(s) ds.

For t>=0 the integral kernel is nonnegative, so its maximum is epsilon*t^2/2, attained by the same constant input w=epsilon for every t. Maximizing the two square coordinates separately gives, with c=a-epsilon,

    h(t)=vbar*t-c*t^2/2+|d+e*t|+|d-e*t|
        =vbar*t-c*t^2/2+2*max(d,e*t).

At each t a square corner attains this value. Exchanging two suprema over a Cartesian product is valid: sup_(z,w) sup_t x = sup_t sup_(z,w) x. No single trajectory is asserted to attain h(t) at every time. Compactness/continuity of h on [0,T] gives a maximizing time and its attaining corner plus constant input, hence an attained pathwise maximum.

For e>0 split at d/e if it lies in the interval. On the left the constant and linear coefficients are 2d,vbar; on the right they are 0,vbar+2e. For c>0 include each piece's stationary time slope/c when it lies in that piece. For c<=0 each piece is convex or affine and endpoints suffice. Include 0,T and the internal kink. If e=0 only the left piece is needed; the implementation's zero-length right piece adds no new time. T=0 and d=0 are allowed. This proves the finite candidate rule by elementary calculus, not by finite testing.

The coordinate box is x0 in [-2d,2d], v0 in [vbar-2e,vbar+2e]. Its support envelope is 2d+(vbar+2e)t-c*t^2/2. This bounds the true initial set from outside; failure of this box test is inconclusive, not evidence of an unsafe trajectory from the original set.

## Exact certificate and changed evidentiary state

Set (d,e,vbar,a,epsilon,T)=(1/20,1/10,1,2,1/5,1). The support kink is 1/2. On [0,1/2], h=1/10+t-9t^2/10 and is increasing, ending at 3/8. On [1/2,1],

    h(t)=6t/5-9t^2/10=2/5-(9/10)(t-2/3)^2.

Thus the exact pathwise maximum is 2/5 at 2/3. The admissible corner z=(1,-1) yields x0=0,v0=6/5; w=1/5 realizes this polynomial. At the sample times the whole reachable-set upper bounds are 1/10,3/8,3/10. Therefore b=3/8 passes all samples yet is violated by 1/40. This refutes deterministic sample-only certification; it says nothing about sampling methods with rigorous interpolation or probabilistic error bounds.

For b=9/20 the exact bound certifies a 1/20 margin. The coordinate-box maximum is 1/2, so that method cannot certify this threshold. Its maximizing initial pair (1/10,6/5) would require z1=2 and is outside the original square. No actual feasible trajectory is discarded by the sharper calculation.

The 648-row exact table records parameters, pathwise maximum, earliest maximizing time, sample maximum, and coordinate-box maximum. It finds 35 strict sample misses and 160 strict box gaps, with 216 concave, 216 affine and 216 convex cases. Rows include zero time, zero generators, zero disturbance, negative center velocity, and c=0. These are parameter instances, not distinct dynamical systems up to equivalence.

## Claim ledger

- SHORTCUT — FALSIFIED, DERIVED: three-point upper bounds imply a bound throughout the interval. The exact witness is the falsifier.
- CERTIFICATE — EXPERIMENTALLY_SUPPORTED, DERIVED: the stated rational witness and all table entries pass independent direct arithmetic; a differing maximum, inadmissible input, or failed row falsifies this finite claim.
- GENERAL — UNVERIFIED, DERIVED: the ordinary all-measurable-input support and critical-point argument above; a flaw in variation of constants, attainment or time maximization is a proof gap. Independent author/kernel review is absent.
- SOURCE — PRIMARY_SOURCE_SUPPORTED: A.7 asks about structured reachability approximations. It does not supply our model or endorse the retired shortcut. See sources/primary-audit.json.

Remaining: no nonlinear extension, HJ PDE solver, feedback synthesis, dimension-scaling benefit, independent human/model proof review or kernel certificate. Do not inflate another parameter census into progress. Next useful work requires a structurally different obstruction, such as sign-changing kernels with coupled input constraints, plus an independently reviewed proof target.
