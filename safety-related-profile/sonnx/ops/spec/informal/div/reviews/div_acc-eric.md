# Numerical Accuracy

$C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains tight properties of $C_{\textit{err}}^{\textit{propag}}$, the propagated error, where $C$ is the tensor result of an operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$). For $C = A/B$, the propagated error $C_{\textit{err}}^{\textit{propag}}$ combines contributions from both $A$ and $B$:

- For every $I$ such that $B[I] \neq 0$ and $B[I]$ does not cross zero under perturbation:
  - $|C_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{A_{\textit{err}}[I]}{B[I]}\right| + \left|\frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]^2}\right| + \mathcal{O}\left(\max(|A_{\textit{err}}[I]|, |B_{\textit{err}}[I]|)^2\right)$

- The complete definition of $\mathcal{O}\left(\max(|A_{\textit{err}}[I]|, |B_{\textit{err}}[I]|)^2\right)$
  is available in the [guidelines](../../../docs/guidelines/accuracy.md#error-propagation).  
- If $B[I]$ and $B[I] + B_{\textit{err}}[I]$ have different signs, the bound may be unbounded (division by a near-zero denominator).

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $C_{\textit{err}}^{\textit{intro}} = [0]$.*

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\bf u} = \frac{\varepsilon}{2}$.

Floating-point division introduces rounding error bounded by $|C[i]|\times\textit{\bf u}$
for the standard rounding mode round to nearest even, provided $\frac{|A[I]|}{|B[I]|}$ is
a normal number (or for any normal number greater or equal than $\frac{|A[I]|}{|B[I]|}$).

- $|C_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{|A[I]|}{|B[I]|}\times\textit{\bf u}$.

## Error Introduction (int)

where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

Error introduction for int arithmetic is less than 1:

- $|C_{\textit{err}}^{\textit{intro}}| < [1]$.

Division by zero remains undefined and shall be prevented by input constraints.

## Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> A, B;

/* A, B symbolic initialization */

auto result = [&A,&B](auto I) {
  return (B[I].real != 0) ? A[I] / B[I] :
      /* undefined */ SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];
   if (b.real != 0 && b.real + b.err != 0) {
      auto c = result(I);
      double bound = std::abs(a.err / b.real) +
        std::abs(a.real * b.err / (b.real * b.real));
      assert(std::abs(c.err) <= bound + 1e-12);
   }
}
```

