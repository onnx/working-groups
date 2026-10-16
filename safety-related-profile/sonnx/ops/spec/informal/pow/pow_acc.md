## Numerical Accuracy

$C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $C_{\textit{err}}^{\textit{propag}}$, the propagated error, where $C$ is the tensor result of the **Pow** operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$, $B_{\textit{err}}$). For $C = A^B$, the propagated error $C_{\textit{err}}^{\textit{propag}}$ comes from the input errors $A_{\textit{err}}$ and $B_{\textit{err}}$.

Using the first-order derivative of (A^B) with respect to (A) and (B):

$$
\frac{\partial (A^B)}{\partial A} = B \cdot A^{B-1}, \quad
\frac{\partial (A^B)}{\partial B} = A^B \cdot \ln(A)
$$

a first-order bound is:

- For every index $I$ such that $A[I] > 0$ and $A[I] + A_{\textit{err}}[I] \ge 0$ (no crossing of singularities):

  - $|C_{\textit{err}}^{\textit{propag}}[I]| \le |B[I] \cdot A[I]^{B[I]-1} \cdot A_{\textit{err}}[I]| + |A[I]^{B[I]} \cdot \ln(A[I]) \cdot B_{\textit{err}}[I]|$

- If $A[I] \le 0$ or approaches zero, the bound may become very large or undefined, as ($\ln(A[I])$) or ($A[I]^{B[I]-1}$) may be undefined.

- For integer exponents $B[I]$, the term $\ln(A[I]) \cdot B_{\textit{err}}[I]$ is replaced by exact integer power propagation rules.

### Error Introduction
Error introduction for real (ideal) arithmetic is null:

- $C_{\textit{err}}^{\textit{intro}} = [0]$.

### Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.
- The `float` field is a symbolic abstract domain for the computed value.
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> A, B;

/* A and B symbolic initialization */

auto result = [&A, &B](auto I) {
  // Real-domain pow, undefined for negative base with non-integer exponent
  return (A[I].real > 0 || (A[I].real < 0 && std::floor(B[I].real) == B[I].real))
         ? pow(A[I], B[I])
         : SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];

   // Ensure we stay in the domain of pow under perturbation
   if (a.real > 0 && a.real + a.err >= 0) {
      auto y = result(I);

      // First-order propagated error bound
      double bound_A = std::abs(b.real * std::pow(a.real, b.real - 1.0) * a.err);
      double bound_B = std::abs(std::pow(a.real, b.real) * std::log(a.real) * b.err);

      assert(std::abs(y.err) <= bound_A + bound_B + 1e-12);
   }
}
```
