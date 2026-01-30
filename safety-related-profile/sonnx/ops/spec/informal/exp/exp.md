# Contents

- **Exp** operator for type [real](#real)
- **Exp** operator for types [float16, float, double](#float)

Based on ONNX documentation [Exp version 13](https://onnx.ai/onnx/operators/onnx__Exp.html).

<a id="real"></a>
# **Exp** (real)

## Signature
Definition of operator $\text{Exp}$ signature:  
$Y = \textbf{Exp}(X)$

where:
- $X$: Input tensor
- $Y$: Exponential of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Exp** operator.

## Informal specification

The **Exp** operator computes the element-wise exponential function of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = e^{X[i]}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0 & 2.71828175 & 0.36787945 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  -2 & 0 \\
  1  & 2 \\
  -4 & 4
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.135335281 & 1.0        \\
  2.71828175 & 7.38905621 \\
  0.018315639 & 54.5981483
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Exp** has no attribute.

## Inputs

### $\text{X}$: real

*Input tensor.*

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.

## Outputs

### $\text{Y}$: real

*Exponential of tensor $X$.*

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).

## Formal specification
 
See the Why3 specification.

<a id="float"></a>
# **Exp** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Exp}$ signature:  
$Y = \text{Exp}(X)$

where:
- $X$: Input tensor
- $Y$: Exponential of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Exp** operator.

## Informal specification

The **Exp** operator computes the element-wise exponential function of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = e^{X[i]}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0 & 2.71828175 & 0.36787945 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  -2 & 0 \\
  1  & 2 \\
  -4 & 4
\end{bmatrix}
```

```math
Y = \begin{bmatrix}
  0.135335281 & 1.0        \\
  2.71828175 & 7.38905621 \\
  0.0183156393 & 54.5981483
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
  +\infty & \text{NaN} & 0.0
\end{bmatrix}
```

## Error conditions

Values of the output tensor may be IEEE 754 $+\infty$ (case of large positive inputs or $+\infty$ in input), $0$ (case of $-\infty$ in input), or NaN (case of NaN in input); a NaN in input is propagated.

## Attributes

Operator **Exp** has no attribute.

## Inputs

### $\text{X}$: floating-point tensor

*Input tensor.*

*FP16*: the input range for non +Inf values of `Y` is defined by $[-65504.0, \ln(65504.0)] = [-65504.0, 11.09375]$.

*FP32*: the input range for non +Inf values of `Y` is defined by $[-3.4028234663852886e+38, \ln(3.4028234663852886e+38)] = [-3.4028234663852886e+38, 88.72283935546875]$.

*FP64*: the input range for non +Inf values of `Y` is defined by $[-1.7976931348623157e+308, \ln(1.7976931348623157e+308)] = [-1.7976931348623157e+308, 709.782712893384]$.


#### Constraints

- `[C1]` <a id="C1fx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2fx"></a> Type consistency  
  - Statement: $X$ and $Y$ shall have the same floating-point type.

## Outputs

### $\text{Y}$: floating-point tensor

*Exponential of tensor $X$.*

#### Constraints

- `[C1]` <a id="C1fy"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` <a id="C2fy"></a> Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).

## Numeric accuracy

[See the numeric accuracy note](./assets/numeric_accuracy/numeric_accuracy.md).
