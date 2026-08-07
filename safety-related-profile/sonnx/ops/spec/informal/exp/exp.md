# Contents

- **Exp** operator for type [real](#real)
- **Exp** operator for types [float16, float, double](#float)

Based on ONNX documentation [Exp version 13](https://onnx.ai/onnx/operators/onnx__Exp.html).

<a id="real"></a>
# **Exp** (real)

## Signature
 
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
Y \approx \begin{bmatrix} 1 & 2.71828175 & 0.36787945 \end{bmatrix}
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
Y \approx  \begin{bmatrix}
  0.135335281 & 1        \\
  2.71828175 & 7.38905621 \\
  0.018315639 & 54.5981483
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Exp** has no attribute.

## Inputs

### $\text{X}$: real tensor

Input tensor.

#### Constraints

- `[C1]` <a id="C1rx"></a> Shape consistency  
  - Statement: $X$ and $Y$ shall have the same shape.

## Outputs

### $\text{Y}$: real tensor

Exponential of tensor $X$.

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
$Y = \textbf{Exp}(X)$

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
Y[i] =
\begin{cases}
\text{NaN} & \text{if } X[i]=\text{NaN} \\
\text{0.0} & \text{if } X[i]=\text{-inf} \\
\text{+inf} & \text{if } X[i]=\text{+inf} ~\text{or}~X[i]> X_{max}\\

e^{X[i]} & \text{otherwise}   \\
\end{cases}
$$

The values of $X_{max}$ are defined hereafter:
- float16: $X_{max}= \ln(\text{maxfp16}) \approx 11.09375$.
- float: $X_{max}= \ln(\text{maxfp32}) \approx 88.72283935546875$.
- double: $X_{max} = \ln(\text{maxfp64}) \approx 709.782712893384$.

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 1 & -1 \end{bmatrix}
```

```math
Y \approx  \begin{bmatrix} 1.0 & 2.71828175 & 0.36787945 \end{bmatrix}
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
Y \approx  \begin{bmatrix}
  0.135335281 & 1.0        \\
  2.71828175 & 7.38905621 \\
  0.0183156393 & 54.5981483
\end{bmatrix}
```


### Example 3

```math
X = \begin{bmatrix}
  \text{+inf} & \text{NaN} & \text{-inf}
\end{bmatrix}
```

```math
Y =  \begin{bmatrix}
  \text{+inf} & \text{NaN} & 0.0
\end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

Operator **Exp** has no attribute.

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

Exponential of tensor $X$.

#### Constraints

- `[C1]` <a id="C1fy"></a> Shape consistency  
  - Statement: See [constraint (C1) on X](#C1fx).
- `[C2]` <a id="C2fy"></a> Type consistency  
  - Statement: See [constraint (C2) on X](#C2fx).

## Numeric accuracy

[See the numeric accuracy note](./exp_acc.md).
