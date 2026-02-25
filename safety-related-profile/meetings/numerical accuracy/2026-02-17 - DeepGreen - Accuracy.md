Date : 

---

## Participants

* Yves THUILLIER (CEA)
* Franck VEDRINE (CEA)
* Augustin LEMESLE (CEA)
* Pierre GAILLARD (CEA)
* Jean SOUYRIS (Airbus)
* Eric JENN (IRT St-Ex)
* Mariem TURKI (IRT St-Ex)

---

## Purpose of the Meeting

* Presentation of the various works carried out by CEA on the numerical precision of neural networks.
* Discussion on the overall articulation of the work, particularly its relationship with the objectives of the SONNX working group and those of the Aidge platform.

---

## Minutes

### Presentation of the Context

* Brief presentation of the SONNX group’s work
* Brief presentation of the Aidge platform

### Presentation of the Work on Numerical Precision

* Presentation by Yves (see slides)
* Presentation by Franck (see slides)
* Presentation by Augustin (see slides)

---

## (Attempted) Summary

From SONNX’s perspective, the objective is to ensure that the specification is sufficiently precise to:

(i) capture the intentions of the model designer,
(ii) preserve a set of properties that have been verified on the model (e.g., ML performance, robustness, etc.),
(iii) enable the model implementer to preserve (i) and (ii).

Regarding (i), SONNX describes the semantics of operators *while taking into account certain implementation-related aspects.* In general, it is simply impossible to implement exactly a specification that would be purely mathematical. Therefore, the “user” must be aware of certain consequences related to implementation choices.

In practice, each operator is specified by explicitly describing the effects of IEEE special values and domain bounds, but *the precision of the operators is not specified.* This is, of course, debatable since, *in principle*, not specifying the precision of the result of a numerical computation amounts to saying nothing at all.

However, it is difficult to specify precision in absolute terms without referring to the original need (i.e., linking it to the network’s own performance) and without over-specifying. This is particularly true in ML, where:

1. The performance of the function (e.g., network accuracy) does not depend very directly on computational precision (see quantization).
2. Performance (latency) plays a major role given the large number of computations involved, which encourages numerous optimizations.

In reality, mathematical libraries that provide guaranteed precision values are relatively rare (please correct me if this is wrong).

The approach proposed by SONNX, as described by Franck, consists in providing methodological means and tools to evaluate a guaranteed formal error, rather than specifying it.

The analytical formulation of precision depends on the chosen computation method (“algorithm”). In the example of ( \tanh ) presented by Franck, a computation method is proposed that is generally more precise than the usual formulation. However, it is certainly not the only or the best method; it is one method, and it is the one that will be implemented in the SONNX reference implementation.

One could consider that any implementation of ( \tanh ) should be at least as precise as the reference implementation, but in that case, we would return to the idea of specifying precision. Instead, it will be considered as indicative guidance.

It should also be noted that certain characteristics of value domains inherent to neural networks are not taken into account (e.g., the fact that values are often normalized to belong to the interval ([0,1])).

The analysis of error introduction is analytical (sometimes defined recursively with respect to the number of dimensions) and conservative. Again, there is no single unique way to perform the analysis, and the choice of method is mainly guided by complexity and effort considerations. The user remains free to perform a more precise analysis.

(It should also be noted that an analysis of error propagation is proposed, but this is mainly for informative purposes.)

Franck also proposes a tooling approach (a class library) that, by simply changing the variable types, makes it possible to obtain an error estimate for a given algorithm implementation (code). If I understood correctly, this could replace manual analysis, although it cannot be fully automated, as certain choices require user intervention.

The methods and tools proposed by Yves operate through code instrumentation (via the same operator overloading mechanism used by Franck, if I understood correctly). Error computation is performed trajectory by trajectory by introducing a random perturbation in each computation (rounding upward or downward). The method is slightly more complex in order to avoid being overly conservative (for example, the error on the computation of the expression ( a - a ) must be zero regardless of the error made in evaluating ( a )).

The result is not an upper bound on the error, unlike Franck’s approach, but rather an error closer to empirical observation. It notably accounts for compensation effects that may occur during computations. Yves’ method makes it possible to compute errors on complete graphs.

The method proposed by Augustin does not aim to calculate the introduction and propagation of errors, but rather to provide bounds on the values taken by the outputs of a network (final or intermediate), assuming the operators are ideal (i.e., mathematically exact). However, the effects of errors are taken into account in the computation of abstract domains. Thus, if an interval ([m, M]) is computed, the values of ( m ) and ( M ) are determined so that they are valid lower and upper bounds, considering that they were computed using floating-point numbers.

The objective of the PyRat tool is therefore to provide bounds on network values, which is useful for assessing network robustness, a property often required for safety. Since operators are considered mathematically perfect (i.e., free of errors), it is possible that conclusions drawn by PyRat on the abstract model may not be preserved in the implementation of the model.

One could imagine combining the approach aimed at estimating upper error bounds (Yves and Franck) with the abstract interpretation implemented by Augustin: each “ideal” computation would take into account the error (worst-case or average) computed using Yves’ and Franck’s methods.
