# 2 - Polyhedron Theory

## 2.1 - Linear and Affine Independence

* Defn: Linear combination, Conical combination, Affine combination, Convex combination.
* Defn: Linear independence, Affine independence.
* Lemma: {x^1, ..., x^n} are affinely independent iff {x^2 - x^1, x^3 - x^1, ..., x^n - x^1} are linindep.
* Lemma: {x^1, ..., x^n} are affinely independent iff {(x^1, a), (x^2, a), ..., (x^n, a)} are linindep,
    for any non-0 constant a.
* Lemma: size of max-size set of affinely independent solutions of Ax = b is n+1-rank(A).

## 2.2 - Polyhedra

* Defn: polyhedron and polytope.
* Defn: dimension of a polyhedron, full-dim polyhedron.
* Defn: implicit defining equalities of polyhedron.
* Lemma: If constraint a^Tx ≤ b is not an implicit equality, then a is not in span(A^=).
* Defn: inner point and interior point.
* Lemma: every non-empty polyhedron has an inner point.
* Lemma: dim(P) = n - rank(A^=).

## 2.3 - Valid Inequalities

* Lemma: valid inequality.
* Defn: face and proper face.
* Lemma: every face can be obtained by tightening some inequality constraints.
* Lemma: every subset of a polyhedron that can be obtained by tightening some inequality constraints is a face.
* Defn: facet and facet-defining inequalities.
* Lemma: facet-defining inequalities are necessary and sufficient.

## 2.4 - Extreme points and extreme rays

* Lemma: If P := {x: Ax≤b} is non-empty, then P has a face of dim n - rank(A), and no proper face of lower dim.
* Defn: extreme point
* Lemma: x is an extreme point of P iff {x} is a 0-dim face of P.
* Defn: cone, ray and extreme ray.
* Lemma: r is extreme ray of P iff {λr: λ≥0} is a 1D face.
* Lemma: finite optimum implies optimal solution is at extreme point
* Lemma: for each extreme point, there is a direction for which it is a maximizer.
* Lemma: unbounded optimum implies there is an optimizing extreme ray.
* Lemma: representation theorem.
