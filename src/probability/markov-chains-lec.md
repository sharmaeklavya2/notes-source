# Markov Chains

Summary of notes from lectures by Sheldon Jacobson
for the course IE 410 at UIUC in Fall 2021.

## Intro

* Markov chain definition. Discrete vs continuous.
* Transition function and transition matrix. Denoted by P. P(i,j) = Pr(go from state i to state j).
* Theorem: Each row of P sums to 1.
* Embedded markov chain:
    * Definition (markov chain that is obtained by eliminating self-loops).
    * Computing from P.

## Chapman-Kolmogorov Equations

* Definition of m-step transition function and matrix.
* Chapman-Kolmogorov equations for transition function.
* Matrix form of Chapman-Kolmogorov equations.

## Classification of States

### Communicability and state classes

* Definition: accessibility and communicability of states.
* Theorem: communicability is an equivalence relation.
* Definition: states classes and irreducibility.

### Recurrence

* Definition: recurrent state: P(eventually being re-visited) = 1. Non-recurrent state is called transient.
* Theorem: If a state is recurrent, then it is visited infinitely often with probability 1.
* Theorem: For a transient state, if P(eventual revisit) = f,
    then P(revisited exactly k times) = f^(k-1) * (1-f),
    so E(eventual revisits) = 1/(1-f).
* Theorem: A state is recurrent iff expected number of revisits is infinite.
* Theorem: E(eventual revisits) = `∑_{n≥0} P^n(i,i)`.
* Theorem: Finite state markov chain has at least one recurrent state.
* Theorem: recurrence is class property.
* Example: random walk with infinite number of states and probability p of going right. Recurrence?
* Theorem: `∏_(i≥0) (1-p_i) = 0 iff ∑_(i≥0) p_i = ∞`.
* Example: `P(i, j) = {p_i if j=0, 1-p_i if j=i+1, 0 otherwise}`. Is 0 recurrent?

## Infinitely often and almost everywhere

* Definition: infinitely often.
* Definition: almost everywhere.
* Lemma: {A a.e.} ⊆ {A i.o}.
* Borel-Cantelli Lemma (with proof): `∑_(i≥0) p_i` is finite implies P(A i.o.) = 0.
* Theorem: `∑_(i≥0) p_i = ∞` implies P(A i.o) = 1.

## Limiting probabilities

* Periodicity of a state.
* Definition: Positive (and null) recurrence.
* Theorem (without proof): In a finite markov chain, all recurrent states are positive recurrent.
* Definition: Ergodic: Positive recurrent and aperiodic.
* Theorem (without proof): For an irreducible ergodic markov chain, limiting probabilities π exist
    and are unique solutions to 'π = πP and sum(π) = 1'.
* Theorem (without proof): If π is the limiting probability distr, then the expected time between
    revisits to j is π_j.
* Theorem (without proof): rank(I-P) = n-1, where n is the number of states.
* Example: `P(i, j) = {p_i if j=0, 1-p_i if j=i+1, 0 otherwise}`. Is 0 positive recurrent?
    * Special cases: p_i = p, p_i = (i+1)/(i+2).
* Example: random walk with infinite number of states and probability p of going right. Positive Recurrence?
* Example: expected lengths of uptimes and downtimes in breakdown-and-repair process.

## Gambler's ruin problem

## Mean time spent in transient states

* Theorem: Let `P_T` be the submatrix of the transition matrix restricted to transient states.
    Let S be a matrix where S[i,j] = P(no. of visits to j | start at i). Then `S = (I-P_T)^(-1)`.
* Theorem: Let f[i,j] = P(eventually reach j | start at i). Then f[i,j] = (S[i,j] - I[i,j])/S[j,j].

## Branching Process

* Definition. Let `X_n` be the number of people in the nth generation.
* Compute `E(X_n|X_0)` and `Var(X_n|X_0)` in terms of `X_0`, `E(X_1|X_0)` and `Var(X_1|X_0)`.
* Compute P(extinction).

## Time-Reversible Markov chains

* Theorem: Time-reverse of a markov chain is a markov chain.
* Definition: Time-reversibility.
* Theorem: `x_iP[i,j] = x_jP[j,i]` has `x = π` as the unique solution.
* Theorem: A random walk (even with different transition probability for different states) is time-reversible.
* Example: Stationary probabilities of a bounded random walk
    with different transition probabilities for different states.

## Markov Decision Process

* Definition
* Theorem: Each stationary distribution corresponds to a policy and vice-versa.
* Solving for the optimal stationary distribution using a linear program.
