## Note Algorithm
Sigmoid is subject to exponent overflow when evaluating large positive exponents (e.g. exp(-X) for very negative values of X).
To remain numerically stable in float, the minimal precision algorithm shall split the `X` domain so that only negative exponents are computed.

```
if X >= 0
    Y = 1 / (1 + exp(-X))
else
    Y = exp(X) / (1 + exp(X))
```

## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Sigmoid** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \sigma(X)$ with $\sigma(x) = 1/(1+e^{-x})$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\sigma$ is $d\sigma(x)/dx = \sigma(x)(1-\sigma(x))$, a first-order bound is:

- For every index $I$:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |\sigma(X[I])(1-\sigma(X[I]))|\cdot|X_{\textit{err}}[I]|$

- Since $0 \le \sigma(x)\,(1-\sigma(x)) \le 1/4$ for all real $x$, a global bound is:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \frac{1}{4}|X_{\textit{err}}[I]|$

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

auto sigmoid = [](const SymbolicDomainError &v) {
  // Sigmoid in the real domain: sigma(x) = 1 / (1 + exp(-x))
  SymbolicDomainError r;
  r.real = 1.0 / (1.0 + std::exp(-v.real));
  // float/err/rel_err are set by the abstract interpreter / analysis framework
  return r;
};

auto result = [&X,&sigmoid](auto I) {
  return sigmoid(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];
   auto y = result(I);

   // First-order propagated error bound:
   // |err_sigmoid| <= |sigma(x) * (1 - sigma(x))| * |err_x|
   double sigma_x = 1.0 / (1.0 + std::exp(-x.real));
   double local_lipschitz = std::abs(sigma_x * (1.0 - sigma_x));
   double bound = local_lipschitz * std::abs(x.err);

   // Using the global bound 1/4 * |x.err| is also valid but less tight.
   assert(std::abs(y.err) <= bound + 1e-12);
}
```


