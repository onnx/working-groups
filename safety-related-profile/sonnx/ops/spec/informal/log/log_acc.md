## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Log** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \log(X)$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\log$ is $d\log(x)/dx = 1/x$, a first-order bound is:

- For every index $I$ such that $X[I] > 0$ and $X[I] + X_{\textit{err}}[I] > 0$ (no crossing of the singularity at 0):
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{X_{\textit{err}}[I]}{X[I]}\right|$


- If $X[I]$ and $X[I] + X_{\textit{err}}[I]$ have different signs or approach zero too closely, the bound may become very large (logarithm near its singularity at 0).

### Error Introduction
Error introduction for real (ideal) arithmetic is null:
- $Y_{\textit{err}}^{\textit{intro}} = [0]$.

### Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> X;

/* X symbolic initialization */

auto result = [&X](auto I) {
  // Real-domain log, undefined for non-positive inputs
  return (X[I].real > 0) ? log(X[I])
                         : SymbolicDomainError::undef();
};

for (auto I : X.indexes()) {
   auto x = X[I];

   // Ensure we stay in the domain of log under perturbation
   if (x.real > 0 && x.real + x.err > 0) {
      auto y = result(I);

      // First-order propagated error bound: |err_log| <= |err_x / x|
      double bound = std::abs(x.err / x.real);

      assert(std::abs(y.err) <= bound + 1e-12);
   }
}
```