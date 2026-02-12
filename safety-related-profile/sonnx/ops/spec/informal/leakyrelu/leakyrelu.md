# Contents

- **LeakyRelu** operator for type [real](#real)
- **LeakyRelu** operator for types [float16, float, double](#float)

Based on ONNX documentation version 14.

<a id="real"></a>
# **LeakyRelu** (real)

## Signature
$Y = \text{LeakyRelu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **LeakyRelu** on $X$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Attribute alpha must be set |  [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |


## Informal specification

Operator **LeakyRelu** is defined as follows: 

$$
Y[i] =
\begin{cases}
X[i] & \text{if } X[i] \ge 0 \\
\alpha \cdot X[i] & \text{if } X[i] < 0 \\
\end{cases}
$$



### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix} \\
\alpha=0.1
```

```math
Y \approx  \text{LeakyRelu}(X) = \begin{bmatrix} 6.1 & -0.95 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

## Attributes

### $\text{alpha}$: real
Coefficient of leakage.

#### Constraints

No constraint.

## Inputs

### $\text{X}$: `real tensor`
Argument of the **LeakyRelu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `real tensor`

Tensor $Y$ is the output of the **LeakyRelu** applied to $X$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **LeakyRelu** has no attribute.

## Formal specification
 
See the Why3 specification.

<a id="float"></a>
# **LeakyRelu** (float)
where float is in {float16, float, double}

## Signature
$Y = \text{LeakyRelu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **LeakyRelu** on $X$

[General restrictions](./../common/general_restrictions.md) are applicable.


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Attribute alpha must be set |  [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

## Informal specification

Operator **LeakyRelu** is defined as follows: 

$$
Y[i] =
\begin{cases}
\text{NaN} & \text{if } X[i] = \text{NaN} \\
\alpha \cdot X[i] & \text{if } X[i] < 0 \text{ and } \alpha \neq \text{NaN} \\
\text{NaN} & \text{if } X[i] < 0 \text{ and } \alpha = \text{NaN} \\
\text{inf} & \text{if } X[i] = \text{inf} \\
\text{-inf} & \text{if } X[i] = \text{-inf} \text{ and } \alpha \neq \text{NaN} \\
\text{NaN} & \text{if } X[i] = \text{-inf} \text{ and } \alpha = \text{NaN} \\
-0 & \text{if } X[i] = -0 \\
X[i] & \text{if } X[i] > 0 \\
\end{cases}
$$



### Example 1

```math
 \alpha = 0.01
```

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```


```math
Y = \text{LeakyRelu}(X) \approx  \begin{bmatrix} 6.1 & -0.95 & 35.7 \end{bmatrix}
```

### Example 2

```math
 \alpha = 0.01
```

```math
X = \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{-inf} & -0.0 & 0.0 & 1.0 & -1.0
\end{bmatrix}
```

```math
Y \approx  \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{-inf} & \text{-0.0} & \text{0.0} & \text{1.0} & \text{-0.01}
\end{bmatrix}
```

### Example 3

```math
 \alpha = \text{Nan}
```

```math
X = \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{-inf} & -0.0 & 0.0 & 1.0 & -1.0
\end{bmatrix}
```

```math
Y \approx  \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{Nan} & \text{-0.0} & \text{0.0} & \text{1.0} & \text{Nan}
\end{bmatrix}
```

### Example 4

```math
 \alpha = \text{-inf}
```

```math
X = \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{-inf} & -0.0 & 0.0 & 1.0 & -1.0
\end{bmatrix}
```

```math
Y \approx  \begin{bmatrix}
  \text{inf} & \text{NaN} & \text{inf} & \text{-0.0} & \text{0.0} & \text{1.0} & \text{inf}
\end{bmatrix}
```



## Error conditions
The function returns $\text{NaN}$ only when the input is $\text{NaN}$, or when the input is negative and alpha is $\text{NaN}$.

## Inputs

### $\text{X}$: `floating-point tensor`
Argument of the **LeakyRelu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the output of the **LeakyRelu** applied to $X$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **LeakyRelu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numeric accuracy

[See the numeric accuracy note](./leakyrelu_acc.md).


