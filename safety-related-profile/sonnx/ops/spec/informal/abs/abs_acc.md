## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Abs** operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = |X|$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\text{abs}(x)$:

- For $x > 0$:  $\dfrac{d|x|}{dx} = 1$
- For $x < 0$:  $\dfrac{d|x|}{dx} = -1$
- For $x = 0$: derivative is undefined, but the function is Lipschitz continuous with constant 1.

A first-order bound is:

- For every index $I$ such that $X[I] \neq 0$ and $X[I] + X_{\textit{err}}[I] \neq 0$ (no sign crossing through zero):

  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |X_{\textit{err}}[I]|$

- If $X[I]$ and $X[I] + X_{\textit{err}}[I]$ have different signs (crossing zero), the propagated error may still be bounded by the same Lipschitz constant, but the output may switch from $|x|$ to $|-x|$ and thus require the bound:

  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |X_{\textit{err}}[I]|$
    (This holds because Abs is 1-Lipschitz everywhere.)

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
  // Real-domain abs
  return abs(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];

   auto y = result(I);

   // First-order propagated error bound: |err_abs| <= |err_x|
   double bound = std::abs(x.err);

   assert(std::abs(y.err) <= bound + 1e-12);
}
```