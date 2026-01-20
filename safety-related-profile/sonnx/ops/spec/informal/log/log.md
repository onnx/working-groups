
# Contents

- **Log** operator for type [real](#real)
- **Log** operator for types [float16, float, double](#float)

Based on ONNX documentation \[Log version 13](https://onnx.ai/onnx/operators/onnx__Log.html).

<a id="real"></a>
# **Log** (real)

## Signature
Definition of operator $\text{Log}$ signature:  
$Y = \textbf{Log}(X)$

where:
- $X$: Input tensor
- $Y$: Natural logarithm of $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Log** operator, besides domain constraints explicitly stated below.

## Informal specification

The **Log** operator computes the element-wise natural logarithm of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\log(X[i]) & \text{if } X[i] > 0 \\
\text{\it undefined} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 1 & 2 & 4 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0 & 0.693147 & 1.386294 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  2.718 & 7.389 \\
  0.01  & 0.1   \\
  10    & 1000
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.999896 & 1.999992 \\
  -4.605170 & -2.302585 \\
  2.302585 & 6.907755
\end{bmatrix}
```

## Error conditions

No error condition beyond the undefined behavior for non-positive inputs in the mathematical model.

## Attributes

Operator **Log** has no attribute.

## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2rdomain"></a> Definition domain  
  - Statement: $\forall i,\ X[i] > 0$.

## Outputs

### $\text{Y}$: real

Natural logarithm of tensor $X$.

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Log** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \log(X)$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\log$ ($\mathrm{d}\log(x)/\mathrm{d}x = 1/x$), a first-order bound is:

- For every index $I$ such that $X[I] > 0$ and $X[I] + X_{\textit{err}}[I] > 0$ (no crossing of the singularity at 0):
  - $$
    |Y_{\textit{err}}^{\textit{propag}}[I]|
      \;\le\; \left|\frac{X_{\textit{err}}[I]}{X[I]}\right|
    $$

- If $X[I]$ and $X[I] + X_{\textit{err}}[I]$ have different signs or approach zero too closely, the bound may become very large (logarithm near its singularity at 0).

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
<a id="float"></a>
# **Log** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Log}$ signature:  
$Y = \text{Log}(X)$

where:
- $X$: Input tensor
- $Y$: Natural logarithm of $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Log** operator.

## Informal specification

The **Log** operator computes the element-wise natural logarithm of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\log(X[i]) & \text{if } X[i] > 0 \\
-\infty & \text{if } X[i] = 0 \\
\text{NaN} & \text{if } X[i] < 0
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1
```math
X = \begin{bmatrix} 1 & 2 & 4 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0 & 0.693147 & 1.386294 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  2.718  & -7.389 \\
  0      & 0.1    \\
  10     & -1000
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.999896 & \text{NaN}  \\
  -\infty  & -2.302585   \\
  2.302585 & \text{NaN}
\end{bmatrix}
```

## Error conditions

Values of the output tensor may be IEEE 754 $-\infty$ or NaN (case of null or negative input values).

## Attributes

Operator **Log** has no attribute.

## Inputs

### $\text{X}$: floating-point tensor

Input tensor.

#### Constraints

- `[C1]` <a id="C1fx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2fx"></a> Type consistency  
  - Statement: $X$ and $Y$ shall have the same floating-point type.

## Outputs

### $\text{Y}$: floating-point tensor

Natural logarithm of tensor $X$ (with IEEE 754 handling of zero and negative inputs).

#### Constraints

- `[C1]` Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).