## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Exp** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \exp(X)$ with $\exp(x) = e^x$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\exp$ is $d\exp(x)/dx = \exp(x)$, a first-order bound is:

- For every index $I$:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |\exp(X[I])|\cdot|X_{\textit{err}}[I]|$

There is no uniform finite global Lipschitz bound on $\exp$ over $\mathbb{R}$, since $|\exp(x)|$ grows unboundedly as $x \to +\infty$.

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

auto exp_real = [](const SymbolicDomainError &v) {
  // Exp in the real domain: exp(x) = e^x
  SymbolicDomainError r;
  r.real = std::exp(v.real);
  // float/err/rel_err are set by the abstract interpreter / analysis framework
  return r;
};

auto result = [&X,&exp_real](auto I) {
  return exp_real(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];
   auto y = result(I);

   // First-order propagated error bound:
   // |err_exp| <= |exp(x)| * |err_x|
   double exp_x = std::exp(x.real);
   double local_lipschitz = std::abs(exp_x);
   double bound = local_lipschitz * std::abs(x.err);

   assert(std::abs(y.err) <= bound + 1e-12);
}
```
