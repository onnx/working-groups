## Numerical Accuracy (real)

$C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains tight properties of $C_{\textit{err}}^{\textit{propag}}$, the propagated error, where $C$ is the tensor result of an operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$). For $C = A/B$, the propagated error $C_{\textit{err}}^{\textit{propag}}$ combines contributions from both $A$ and $B$:

- For every $I$ such that $B[I] \neq 0$ and $B[I]$ does not cross zero under perturbation:
  - $|C_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{A_{\textit{err}}[I]}{B[I]}\right| + \left|\frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]^2}\right|$

- If $B[I]$ and $B[I] + B_{\textit{err}}[I]$ have different signs, the bound may be unbounded (division by a near-zero denominator).

### Error Introduction
Error introduction for real (ideal) arithmetic is null:
- $C_{\textit{err}}^{\textit{intro}} = [0]$.*

### Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

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




## Numerical Accuracy (float)

For $C = A / B$ with numerical errors $A_{\textit{err}}$, $B_{\textit{err}}$:

### Error Propagation

  For all valid indexes $i$ where $B[i] \neq 0$ and $B[i] + B_{\textit{err}}[i]$ does not cross zero,

  $$
  |C_{\textit{err}}^{\textit{propag}}[i]| \leq \left|\frac{A_{\textit{err}}[i]}{B[i]}\right| + \left|\frac{A[i] \cdot B_{\textit{err}}[i]}{B[i]^2}\right|
  $$

### Error Introduction

  Floating-point division introduces rounding error bounded by the unit in the last place (ulp) of $C[i]$ in the target floating-point format.
- $C_{\textit{err}}^{\textit{intro}} = ulp(C[i])$.

### Unit verification (symbolic)

```c++
Tensor<SymbolicDomainError> A, B;

/* Symbolic initialization of A, B */

auto result = [&A,&B](auto i) {
  if (B[i].real != 0) return A[i] / B[i];
  if (A[i].real != 0) return SymbolicDomainError::inf();
  return SymbolicDomainError::nan();
};

for (auto i : A.indexes()) {
   auto a = A[i];
   auto b = B[i];
   auto c = result(i);
   if (std::isfinite(b.real) && b.real != 0 && b.real + b.err != 0) {
      double bound = std::abs(a.err / b.real) + std::abs(a.real * b.err / (b.real * b.real));
      assert(std::abs(c.err) <= bound + ulp(c.real)); // includes intro. rounding
   }
   if (b.real == 0 && a.real != 0) { assert(c.is_inf()); }
   if (b.real == 0 && a.real == 0) { assert(c.is_nan()); }
}
```

<a id="int"></a>

# **Div** (int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature
Definition of operator $\text{Div}$ signature:
 $C = \textbf{Div}(A,B)$

 where
 - $A$: numerator
 - $B$: denominator
 - $C$: result of the element-wise division of $A$ by $B$

### Restrictions
[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1, GR2 and GR3 are applicable.

No specific restrictions apply to the **Div** operator.




## Numeric accuracy (int)
Hence $C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

Integer division is exact under the defined semantics; error is not introduced by the operator itself:

### Error Propagation
 For integer inputs modeled without error symbols, $C_{\textit{err}}^{\textit{propag}} = [0]$.
### Error Introduction
Error introduction for int arithmetic is null:
 $C_{\textit{err}}^{\textit{intro}} = [0]$.

Division by zero remains undefined and shall be prevented by input constraints.
### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:


```c++
Tensor<SymbolicDomainError> A, B;

/* A, B symbolic initialization */

auto result = [&A,&B](auto I) {
  return (B[I].int != 0) ? A[I] / B[I] :
         /* undefined */ SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];
   if (b.int != 0 && b.int + b.err != 0) {
      auto c = result(I);
      double bound = std::abs(a.err / b.int) +
          std::abs(a.int * b.err / (b.int * b.int));
      assert(std::abs(c.err) <= bound + 0);
   }
}
```







