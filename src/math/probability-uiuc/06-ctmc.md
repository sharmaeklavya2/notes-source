# Continuous-Time Markov Chain

Summary of notes from lectures by Sheldon Jacobson
for the course IE 410 at UIUC in Fall 2021.

## Introduction

* Definition (CTMC, stationarity)
* Theorem: transition times are exponential.
* Example: Jobs appear according to Poisson process. Each job is serviced sequentially by 2 machines,
    each of which has a waiting queue, and service times are exponential.
    This is a markov chain where the state space is {(n_1, n_2): n_1 ≥ 0, n_2 ≥ 0}, where
    n_i is the number of jobs waiting for or being serviced by machine i.

## Birth and Death Processes

* Definition: `λ_i` and `μ_i` are birth and death rates when population is i.
* Finding E(X(t) | X(0)=i) as a function of t when `λ_i = λi+θ` and `μ_i = μi`.
* Let T be the time for population to reach j. Find E(T | X(0)=i) and Var(T | X(0)=i).

## Chapman-Kolmogorov Equations

* CK eqn
* CK backward diffeq
* CK forward diffeq
(Incomplete)

## Limiting Probabilities

(Incomplete)
