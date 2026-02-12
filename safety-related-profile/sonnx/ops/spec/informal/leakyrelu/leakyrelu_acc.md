## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **LeakyRelu** operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $(Y = \text{LeakyRelu}(X))$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of LeakyRelu:

- $if (X[i] > 0): (\dfrac{dY}{dX} = 1)$
- $if (X[i] < 0): (\dfrac{dY}{dX} = \alpha)$
- $if (X[i] = 0)$: derivative is undefined, but LeakyRelu is Lipschitz continuous with constant $(\max(1, |\alpha|))$

A first-order bound is:

- For every index (I) such that (X[I] > 0) and (X[I] + X_{\textit{err}}[I] > 0) (no sign crossing through 0):

  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |X_{\textit{err}}[I]|$

- For every index (I) such that (X[I] < 0) and (X[I] + X_{\textit{err}}[I] < 0) (no sign crossing through 0):

  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |\alpha| \cdot |X_{\textit{err}}[I]|$

- If (X[I]) and (X[I] + X_{\textit{err}}[I]) have different signs (crossing 0), the propagated error may be bounded using the Lipschitz constant:

  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \max(1,|\alpha|) \cdot |X_{\textit{err}}[I]|$

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
  // Real-domain leakyrelu
  return leakyrelu(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];

   auto y = result(I);

   // First-order propagated error bound
   double bound;
   if (x.real > 0 && x.real + x.err > 0) {
       // Positive region: derivative = 1
       bound = std::abs(x.err);
   } else if (x.real < 0 && x.real + x.err < 0) {
       // Negative region: derivative = alpha
       bound = std::abs(x.alpha * x.err);
   } else {
       // Crossing zero: use Lipschitz constant max(1, |alpha|)
       bound = std::max(1.0, std::abs(x.alpha)) * std::abs(x.err);
   }

   assert(std::abs(y.err) <= bound + 1e-12);
}
```
