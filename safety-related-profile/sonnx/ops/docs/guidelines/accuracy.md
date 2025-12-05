#### Numerical Accuracy
 
This section provides a tight and verifiable specification of the numerical error
on the operator's results. It decomposes the error into two parts:
the first, the propagated error, depends on the numerical error and the
numerical values of the inputs ; the second part, the introduced error,
depends only on the numerical value of the inputs.

The provided specification results from an over-approximated semantics (ex: IEEE-754) of the
numerical error of native computer operations approximating real number
operations. In order to preserve the readability of the formulas, the general specification introduces additional (conservative) simplifications compared to the original specifications.
However, this general specification may be too over-approximated for some specific inputs (ex tensor representing diagonal matrices). In this case, more precise specific specifications are provided alongside the general specification.

The error specification comes with unit verification scenarios to verify the implementation's conformity. In the absence of value ranges for the inputs, the unit verification scenarios operate on symbolic values and errors to propagate correct formulas throughout the scenario and thus provide a proof for the assertions. In particular, the C implementation generated from the Why3 formal specification must be verified using these scenarios, for example by using symbolic instrumentation libraries.


###### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of an operator.

###### Error Introduction

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$, the introduced error, where $Y$ is the tensor result of an operator.

Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

###### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

# Formal specification guidelines

*To be completed.*
