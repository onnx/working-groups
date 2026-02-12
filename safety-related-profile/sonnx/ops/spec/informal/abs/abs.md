# Contents

- **Abs** operator for type [real](#real)
- **Abs** operator for types [bfloat16, float16, float, double](#float)
- **Abs** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Abs version 13](https://onnx.ai/onnx/operators/onnx__Abs.html).

<a id="real"></a>
# **Abs** (real)

## Signature
Definition of operator $\text{Abs}$ signature:
$Y = \textbf{Abs}(X)$

where:
- $X$: Input tensor
- $Y$: Absolute value of $X$
   
## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Abs** operator.

## Informal specification

The **Abs** operator computes the element-wise absolute value of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$Y[i] = |X[i]|$$

The effect of the operator is illustrated on the following examples.

### Example 1
```math
X = \begin{bmatrix} -2.1 & 3.4 & -7 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 2.1 & 3.4 & 7 \end{bmatrix}
```

### Example 2
```math
X = \begin{bmatrix} -1.123 & 0 \\ 4 & -5 \\ 2 & -3 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 1.123 & 0 \\ 4 & 5 \\ 2 & 3 \end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Abs** has no attribute.

## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

 - `[C1]` <a id="C1rx"></a> Shape consistency
   - Statement: $X$ and $Y$ shall have the same shape.
    
## Outputs

### $\text{Y}$: real

Absolute value of tensor $X$

#### Constraints

 - `[C1]` <a id="C1ry"></a> Shape consistency
   - Statement: See [constraint (C1) on X](#C1rx)

## Formal specification
 
See the Why3 specification.

<a id="float"></a>
# **Abs** (float)
where float is in {float16, float, double}

## Signature
Definition of operator $\text{Abs}$ signature:
$Y = \textbf{Abs}(X)$

where:
- $X$: Input tensor
- $Y$: Absolute value of $X$
   
## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Abs** operator:

## Informal specification

The **Abs** operator computes the element-wise absolute value of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = 
\begin{cases} 
\text{NaN} & \text{if } X[i] = \text{NaN} \\
\text{+Inf} & \text{if } X[i] = \pm \text{Inf} \\
\text{+0} & \text{if } X[i] = \pm \text{0} \\
X[i] & \text{otherwise} 
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1
```math
X =  \begin{bmatrix} -2.1 & \text{-Inf} & \text{NaN} & -0 \end{bmatrix}
```

```math
Y \approx  \begin{bmatrix} 2.1 & \text{Inf} & \text{NaN} & +0 \end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Abs** has no attribute.

## Inputs

### $\text{X}$: float

Input tensor.

#### Constraints

 - `[C1]` <a id="C1rx"></a> Shape consistency
   - Statement: $X$ and $Y$ shall have the same shape.
    
## Outputs

### $\text{Y}$: float

Absolute value of tensor $X$

#### Constraints

 - `[C1]` <a id="C1ry"></a> Shape consistency
   - Statement: See [constraint (C1) on X](#C1rx)

## Numeric accuracy

[See the numeric accuracy note](./assets/abs_acc.md).


<a id="int"></a>
# **Abs** (int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

See specification for [real numbers](#real).







