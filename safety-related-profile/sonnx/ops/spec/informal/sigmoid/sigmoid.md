# Contents

- **Sigmoid** operator for type [real](#real)
- **Sigmoid** operator for types [float16, float, double](#float)

Based on ONNX documentation [Sigmoid version 13](https://onnx.ai/onnx/operators/onnx__Sigmoid.html).

<a id="real"></a>
# **Sigmoid** (real)

## Signature
Definition of operator $\text{Sigmoid}$ signature:  
$Y = \textbf{Sigmoid}(X)$

where:
- $X$: Input tensor
- $Y$: Sigmoid of $X$



## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sigmoid** operator.

## Informal specification

The **Sigmoid** operator computes the element-wise logistic sigmoid of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \frac{1}{1 + e^{-X[i]}}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0.5 & 0.73105860 & 0.26894143 \end{bmatrix}
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
  0.11920291 & 0.5       \\
  0.73105860 & 0.88079709 \\
  0.01798624 & 0.98201376
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Sigmoid** has no attribute.

## Inputs

### $\text{X}$: real

*Input tensor.*

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.

## Outputs

### $\text{Y}$: real

*Sigmoid of tensor $X$.*

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).

## Formal specification
 
See the Why3 specification.

<a id="float"></a>
# **Sigmoid** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Sigmoid}$ signature:  
$Y = \textbf{Sigmoid}(X)$

where:
- $X$: Input tensor
- $Y$: Sigmoid of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sigmoid** operator.

## Informal specification

The **Sigmoid** operator computes the element-wise logistic sigmoid of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \frac{1}{1 + e^{-X[i]}} = \frac{e^{X[i]}}{e^{X[i]} + 1}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 0.5 & 0.73105860 & 0.26894143 \end{bmatrix}
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
  0.11920291 & 0.5       \\
  0.73105860 & 0.88079709 \\
  0.01798624 & 0.98201376
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
  1.0 & \text{NaN} & 0.0
\end{bmatrix}
```

## Error conditions

Values of the output tensor may be IEEE 754 between 0, 1 (case of -inf and +inf in input), or NaN (case of NaN in input); a NaN in input is propagated.

## Attributes

Operator **Sigmoid** has no attribute.

## Inputs

### $\text{X}$: floating-point tensor

*Input tensor.*

#### Constraints

- `[C1]` <a id="C1fx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2fx"></a> Type consistency  
  - Statement: $X$ and $Y$ shall have the same floating-point type.

## Outputs

### $\text{Y}$: floating-point tensor

*Sigmoid of tensor $X$.*

#### Constraints

- `[C1]` <a id="C1fy"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` <a id="C2fy"></a> Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).

## Numeric accuracy

[See the numeric accuracy note](./assets/numeric_accuracy/numeric_accuracy.md).
