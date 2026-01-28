# Contents

- **Tanh** operator for type [real](#real)
- **Tanh** operator for types [float16, float, double](#float)

Based on ONNX documentation \[Tanh version 13](https://onnx.ai/onnx/operators/onnx__Tanh.html).

<a id="real"></a>
# **Tanh** (real)

## Signature
Definition of operator $\text{Tanh}$ signature:  
$Y = \textbf{Tanh}(X)$

where:
- $X$: Input tensor
- $Y$: Hyperbolic tangent of $X$



## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Tanh** operator.

## Informal specification

The **Tanh** operator computes the element-wise hyperbolic tangent of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] = \tanh(X[i]) = \frac{e^X[i]-e^{-X[i]}}{e^X[i]+e^{-X[i]}} = \frac{e^{2X[i]}-1}{e^{2X[i]}+1} = \frac{1 - e^{-2X[i]}}{1 + e^{-2X[i]}}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0.0 & 0.76159418 & -0.76159418 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  -2 & 0 \\
  1  & 2  \\
  -4 & 4
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  -0.96402758 & 0.0         \\
  0.76159418  & 0.96402758  \\
  -0.99932921 & 0.99932921
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Tanh** has no attribute.

## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.

## Outputs

### $\text{Y}$: real

Hyperbolic tangent of tensor $X$.

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).

## Formal specification
 
See the Why3 specification.

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

<a id="float"></a>
# **Tanh** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Tanh}$ signature:  
$Y = \text{Tanh}(X)$

where:
- $X$: Input tensor
- $Y$: Hyperbolic tangent of $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Tanh** operator.

## Informal specification

The **Tanh** operator computes the element-wise hyperbolic tangent of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$
Y[i] = \tanh(X[i]) = \frac{e^X[i]-e^{-X[i]}}{e^X[i]+e^{-X[i]}} = \frac{e^{2X[i]}-1}{e^{2X[i]}+1} = \frac{1 - e^{-2X[i]}}{1 + e^{-2X[i]}}
$$

### Algorithm
Tanh is subject to exponent overflow when evaluating large positive exponents (e.g. exp(2X) for very positive values of X).
To remain numerically stable, the algorithm shall split the `X` domain so that only negative exponents are computed.

```
if X < 0
    Y = (exp(2X) - 1) / (exp(2X) + 1)
else
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0.0 & 0.76159418 & -0.76159418 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  -2 & 0 \\
  1  & 2  \\
  -4 & 4
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  -0.96402758 & 0.0         \\
  0.76159418  & 0.96402758  \\
  -0.99932921 & 0.99932921
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
  1.0 & \text{NaN} & -1.0
\end{bmatrix}
```

## Error conditions

Values of the output tensor may be IEEE 754 between -1 and 1 (case of -inf and +inf in input), or NaN (case of NaN in input); a NaN in input is propagated.

## Attributes

Operator **Tanh** has no attribute.

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

Hyperbolic tangent of tensor $X$.

#### Constraints

- `[C1]` Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` Type consistency  

  - Statement: See [constraint (C2) on X](#C2fx).

