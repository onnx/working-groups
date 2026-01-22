# Contents

- **Sqrt** operator for type [real](#real)
- **Sqrt** operator for types [float16, float, double](#float)

Based on ONNX documentation \[Sqrt version 13](https://onnx.ai/onnx/operators/onnx__Sqrt.html).

<a id="real"></a>
# **Sqrt** (real)

## Signature
Definition of operator $\text{Sqrt}$ signature:  
$Y = \textbf{Sqrt}(X)$

where:
- $X$: Input tensor
- $Y$: Square root of $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sqrt** operator, besides domain constraints explicitly stated below.

## Informal specification

The **Sqrt** operator computes the element-wise square root of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\sqrt{X[i]} & \text{if } X[i] \ge 0 \\
\text{\it undefined} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 1 & 2 & 4 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1 & 1.41421354 & 2 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  0.25 & 2.25 \\
  0.0 & 0.1 \\
  10   & 1000
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.5   & 1.5   \\
  0.0   & 0.31622776  \\
  3.16227770 & 31.62277603
\end{bmatrix}
```

## Error conditions

No error condition beyond the undefined behavior for negative inputs in the mathematical model.

## Attributes

Operator **Sqrt** has no attribute.

## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2rdomain"></a> Definition domain  
  - Statement: $\forall i,\ X[i] \ge 0$.

## Outputs

### $\text{Y}$: real

Square root of tensor $X$.

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Sqrt** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \sqrt{X}$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\sqrt{x}$ is $d\sqrt{x}/dx = 1/(2\sqrt{x})$, a first-order bound is:

- For every index $I$ such that $X[I] > 0$ and $X[I] + X_{\textit{err}}[I] \ge 0$ (no crossing of the singularity at 0):
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{X_{\textit{err}}[I]}{2\sqrt{X[I]}}\right|$

- If $X[I]$ and $X[I] + X_{\textit{err}}[I]$ have different signs or approach zero too closely, the bound may become very large (square root near its singularity at 0).

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
  // Real-domain sqrt, undefined for negative inputs
  return (X[I].real >= 0) ? sqrt(X[I])
                          : SymbolicDomainError::undef();
};

for (auto I : X.indexes()) {
   auto x = X[I];

   // Ensure we stay in the domain of sqrt under perturbation
   if (x.real > 0 && x.real + x.err >= 0) {
      auto y = result(I);

      // First-order propagated error bound: |err_sqrt| <= |err_x / (2*sqrt(x))|
      double bound = std::abs(x.err / (2.0 * std::sqrt(x.real)));

      assert(std::abs(y.err) <= bound + 1e-12);
   }
}
```

<a id="float"></a>
# **Sqrt** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Sqrt}$ signature:  
$Y = \text{Sqrt}(X)$

where:
- $X$: Input tensor
- $Y$: Square root of $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sqrt** operator.

## Informal specification

The **Sqrt** operator computes the element-wise square root of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\sqrt{X[i]} & \text{if } X[i] \ge 0 \\
\text{NaN} & \text{if } X[i] < 0
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1
```math
X = \begin{bmatrix} 1.0 & 2.0 & 4.0 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0 & 1.41421354 & 2.0 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  0.25 & -1.0 \\
  0.0    & 0.1 \\
  10   & -1000
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.5   & \text{NaN} \\
  0.0   & 0.31622776       \\
  3.16227770 & \text{NaN}
\end{bmatrix}
```

### Example 3

```math
X = \begin{bmatrix}
  +\infty & \text{NaN} & -\infty
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  +\infty & \text{NaN} & \text{NaN}
\end{bmatrix}
```

## Error conditions

Values of the output tensor may be IEEE 754 NaN (case of negative input values), a NaN in input is propagated; $+\infty$ is mapped to $+\infty$.

## Attributes

Operator **Sqrt** has no attribute.

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

Square root of tensor $X$ (with IEEE 754 handling of zero, negative, and infinite inputs).

#### Constraints

- `[C1]` Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` Type consistency  

  - Statement: See [constraint (C2) on X](#C2fx).
