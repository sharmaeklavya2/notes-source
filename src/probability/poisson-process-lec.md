# Exponential Distribution and Poisson Processes

Summary of notes from lectures by Sheldon Jacobson
for the course IE 410 at UIUC in Fall 2021.

## The exponential distribution

* PDF, CDF, E(X), Var(X).
* Memorylessness.
* Definition: hazard rate.
* CDF from hazard rate.
* Sum of n exponential random variables.
* PDF of a gamma variable.
* Theorem: `P(X_1 < X_2) = λ_1/(λ_1 + λ_2)`,
    where `X_i ~ Exponential(λ_i)` and `X_1` and `X_2` are independent.
* Example: Taxi arrival.
* Theorem: Probability distributions of `min_i X_i` and `max_i X_i`, where `X_i ~ Exponential(λ_i)`.
* Theorem: `P(X_1 = min(X_1, X_2, ..., X_n)) = λ_1/(λ_1 + λ_2 + ... + λ_n)`,
    where `X_i ~ Exponential(λ_i)` and all `X_i` are independent.

## Poisson Process

* Definition: counting process.
* Definition: Independent increments, stationary increments.
* Definitions of Poisson process and their equivalence.
* Theorem: P(N(s)=k | N(t)=n) = C(n,k) (s/t)^k (1-s/t)^(n-k).
* Definition: Inter-arrival times and arrival times of a counting process.
* Theorem: Inter-arrival times of a poisson process are IID exponential(λ).
* Theorem: Sum of n exp(λ) variables is Gamma(n, λ).

## Decomposition of Poisson process

* Theorem: Suppose each event receives a label i with probability `p_i`, and there are k distinct labels.
    Let `N_i(t)` be the number of events labeled i in time t.
    Then `N_i` is a poisson process with parameter `λp_i`.
    Also, for every t, all `N_i(t)` are independent.
    Also, conditional on N(t)=n, we get that `N_i(t) ~ Binomial(n, p_i)`.
* Theorem: Let `{N_i: i ∈ [k]}` be independent poisson processes, where `N_i` has parameter `λ_i`.
    Let `N(t) = N_1(t) + ... + N_k(t)`. Then N is a poisson process with parameter `λ_1 + ... + λ_k`.

## Coupon collector problem

## Competing poisson processes

* If there are two poisson processes, what is the probability of seeing
    m events of the first before n events of the second?

## Conditional on n events, arrival times are distributed as order statistics of uniform distribution

## Inhomogeneous poisson process

* Definition
* Theorem: An inhomogeneous Poisson process can be reformulated as a random sample
    from a (homogeneous) Poisson proces.

## Compound poisson process
