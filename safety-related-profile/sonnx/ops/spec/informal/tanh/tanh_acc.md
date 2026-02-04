## Note Algorithm
Tanh is subject to exponent overflow when evaluating large positive exponents (e.g. exp(2X) for very positive values of X).
To remain numerically stable in float, the minimal precision algorithm shall split the `X` domain so that only negative exponents are computed.

```
if X < 0
    Y = (exp(2X) - 1) / (exp(2X) + 1)
else
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Tanh** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \tanh(X)$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\tanh$ is $d\tanh(x)/dx = 1 - \tanh^2(x)$, a first-order bound is:

- For every index $I$:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |1 - \tanh^2(X[I])|\cdot|X_{\textit{err}}[I]|
    $

- Since $0 \le 1 - \tanh^2(x) \le 1$ for all real $x$, a global bound is:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |X_{\textit{err}}[I]|$

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

auto tanh_real = [](const SymbolicDomainError &v) {
  // Tanh in the real domain
  SymbolicDomainError r;
  r.real = std::tanh(v.real);
  // float/err/rel_err are set by the abstract interpreter / analysis framework
  return r;
};

auto result = [&X,&tanh_real](auto I) {
  return tanh_real(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];
   auto y = result(I);

   // First-order propagated error bound:
   // |err_tanh| <= |1 - tanh(x)^2| * |err_x|
   double tanh_x = std::tanh(x.real);
   double local_lipschitz = std::abs(1.0 - tanh_x * tanh_x);
   double bound = local_lipschitz * std::abs(x.err);

   assert(std::abs(y.err) <= bound + 1e-12);
}
```



