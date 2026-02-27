
# Contents

- **Log** operator for type [real](#real)
- **Log** operator for types [float16, float, double](#float)

Based on ONNX documentation [Log version 13](https://onnx.ai/onnx/operators/onnx__Log.html).

<a id="real"></a>
# **Log** (real)

## Signature 
$Y = \textbf{Log}(X)$

where:
- $X$: Input tensor
- $Y$: Natural logarithm of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Log** operator, besides domain constraints explicitly stated below.

## Informal specification

The **Log** operator computes the element-wise natural logarithm of the input tensor $X$.

The mathematical definition of the operator is given hereafter.

**Log** is only defined for strictly positive values.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \log(X[i]) 
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 1 & 2 & 4 \end{bmatrix}
```

```math
Y \approx  \begin{bmatrix} 0 & 0.693147 & 1.386294 \end{bmatrix}
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
Y \approx  \begin{bmatrix}
  0.999896 & 1.999992 \\
  -4.605170 & -2.302585 \\
  2.302585 & 6.907755
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Log** has no attribute.

## Inputs

### $\text{X}$: real tensor

Input tensor.

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2rdomain"></a> Definition domain  
  - Statement: $\forall i,\ X[i] > 0$.

## Outputs

### $\text{Y}$: real tensor

Natural logarithm of tensor $X$.

#### Constraints

- `[C1]` <a id="C1ry"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1rx).
 

<a id="float"></a>
# **Log** (float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Log}$ signature:  
$Y = \textbf{Log}(X)$

where:
- $X$: Input tensor
- $Y$: Natural logarithm of $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Log** operator.

## Informal specification

The **Log** operator computes the element-wise natural logarithm of the input tensor $X$ according to IEEE 754 floating-point semantics.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:


$$
Y[i] =
\begin{cases}
\text{NaN} & \text{if } X[i]=\text{NaN} \\
\text{NaN} & \text{if } X[i] \in [\text{-inf}, \text{-0}[ \\
\text{-inf} & \text{if } X[i] = 0 \\
\text{inf} &  \text{if } X[i] = \text{inf} \\
\log(X[i]) & \text{otherwise} \\

\end{cases}
$$


The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 1 & 2 & 4 \end{bmatrix}
```

```math
Y \approx  \begin{bmatrix} 0 & 0.69314718 & 1.38629436 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix}
  2.718  & -7.389 \\
  0.0      & 0.1    \\
  10     & -1000
\end{bmatrix}
```

```math
Y \approx  \begin{bmatrix}
  0.99989629 & \text{NaN}  \\
  \text{-inf}  & -2.30258512   \\
  2.30258512 & \text{NaN}
\end{bmatrix}
```


### Example 3

```math
X = \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{-inf} & -0.0 & 0.0
\end{bmatrix}
```

```math
Y =  \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{NaN} & \text{-inf} & \text{-inf}
\end{bmatrix}
```

## Error conditions

The function returns $\text{NaN}$ when the input is strictly negative and different from -0.0.

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

- `[C1]` <a id="C1fy"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` <a id="C2fy"></a> Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).

## Numeric accuracy

[See the numeric accuracy note](./log_acc.md).
