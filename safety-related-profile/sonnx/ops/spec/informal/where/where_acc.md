# Numerical Accuracy

$Z_{\textit{err}} = Z_{\textit{err}}^{\textit{propag}} + Z_{\textit{err}}^{\textit{intro}}$.



## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains tight properties of $Z_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Z$ is the tensor result of the **Where** operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$).

For $Z = \textbf{Where}(condition, X, Y)$, the propagated error depends only on the selected branch.

For every tensor index $I$:

- If $condition[I] = \text{True}$:

  - $Z[I] = X[I]$
  - $Z_{\textit{err}}^{\textit{propag}}[I] = X_{\textit{err}}[I]$

- If $condition[I] = \text{False}$:

  - $Z[I] = Y[I]$
  - $Z_{\textit{err}}^{\textit{propag}}[I] = Y_{\textit{err}}[I]$

Therefore:

$$
|Z_{\textit{err}}^{\textit{propag}}[I]| =
\begin{cases}
|X_{\textit{err}}[I]| & \text{if } condition[I] = \text{True} \
|Y_{\textit{err}}[I]| & \text{otherwise}
\end{cases}
$$

The operator **Where** does not combine numerical values and does not introduce amplification of propagated errors.
It only forwards the error of the selected input element.



## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $Z_{\textit{err}}^{\textit{intro}} = [0]$.

The **Where** operator performs no arithmetic computation and therefore introduces no additional numerical error.



## Error Introduction (IEEE-754 floating-point)

The **Where** operator does not perform any floating-point arithmetic operation.
It only copies either $X[I]$ or $Y[I]$ depending on $condition[I]$.

Therefore, no rounding is introduced by the operator itself:

- $Z_{\textit{err}}^{\textit{intro}} = [0]$.

Any floating-point error present in the output originates solely from the selected input tensor and is entirely captured by $Z_{\textit{err}}^{\textit{propag}}$.



## Error Introduction (int)

where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

The **Where** operator performs no arithmetic computation on integer values.
It only selects between two integer operands.

Therefore:

- $Z_{\textit{err}}^{\textit{intro}} = [0]$.

There is no loss of precision and no rounding involved in integer selection.



## Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation.
It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification.

```c++
Tensor<bool> condition;
Tensor<SymbolicDomainError> X, Y;

/* condition, X, Y symbolic initialization */

auto result = [&condition,&X,&Y](auto I) {
  return condition[I] ? X[I] : Y[I];
};

for (auto I : X.indexes()) {
   auto z = result(I);
   if (condition[I]) {
      assert(z.real == X[I].real);
      assert(std::abs(z.err) == std::abs(X[I].err));
   } else {
      assert(z.real == Y[I].real);
      assert(std::abs(z.err) == std::abs(Y[I].err));
   }
}
```
