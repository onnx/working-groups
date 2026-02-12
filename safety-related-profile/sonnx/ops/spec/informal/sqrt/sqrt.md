# Contents

- **Sqrt** operator for type [real](#real)
- **Sqrt** operator for types [float16, float, double](#float)

Based on ONNX documentation [Sqrt version 13](https://onnx.ai/onnx/operators/onnx__Sqrt.html).

<a id="real"></a>
# **Sqrt** (real)

## Signature
Definition of operator $\text{Sqrt}$ signature:  
$Y = \textbf{Sqrt}(X)$

where:
- $X$: Input tensor
- $Y$: Square root of $X$



## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sqrt** operator, besides domain constraints explicitly stated below.

## Informal specification

The **Sqrt** operator computes the element-wise square root of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

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
Y \approx  \begin{bmatrix} 1 & 1.41421354 & 2 \end{bmatrix}
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
Y \approx  \begin{bmatrix}
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

<a id="float"></a>
# **Sqrt** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Sqrt}$ signature:  
$Y = \textbf{Sqrt}(X)$

where:
- $X$: Input tensor
- $Y$: Square root of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sqrt** operator.

## Informal specification

The **Sqrt** operator computes the element-wise square root of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\text{NaN} & \text{if } X[i]=\text{-inf} \\
\text{-0.0} & \text{if } X[i]=\text{-0.0} \\
\text{inf} & \text{if } X[i]=\text{inf} \\
\text{NaN} & \text{if } X[i]=\text{NaN} \\

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
Y \approx  \begin{bmatrix} 1.0 & 1.41421354 & 2.0 \end{bmatrix}
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
Y \approx  \begin{bmatrix}
  0.5   & \text{NaN} \\
  0.0   & 0.31622776       \\
  3.16227770 & \text{NaN}
\end{bmatrix}
```

### Example 3

```math
X = \begin{bmatrix}
  \text{+inf} & \text{NaN} & \text{-inf} & -0.0
\end{bmatrix}
```

```math
Y \approx  \begin{bmatrix}
  \text{+inf} & \text{NaN} & \text{NaN} & -0.0
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

- `[C1]` <a id="C1fy"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` <a id="C2fy"></a> Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).

## Numeric accuracy

[See the numeric accuracy note](./sqrt_acc.md).
