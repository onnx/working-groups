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

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1 and GR2 are applicable.


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Attribute alpha must be set |  [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |


## Informal specification

Operator **LeakyRelu** is defined as follows: 
- if $X[i] < 0$ then $Y[i] = \alpha X[i]$
- If $X[i] \ge 0$ then $Y[i]=X[i]$

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

## Numerical Accuracy

Operator **LeakyRelu** does not introduce any numerical error. 


<a id="float"></a>
# **LeakyRelu** (float)
where float is in {float16, float, double}

## Signature
$Y = \text{LeakyRelu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **LeakyRelu** on $X$

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1 and GR2 are applicable.


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Attribute alpha must be set |  [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

## Informal specification

Operator **LeakyRelu** is defined as follows: 
- if $X[i] = \text{NaN}$ then $Y[i]=\text{NaN}$
- if $X[i] < 0$ then 
  - if $\alpha \neq \text{NaN}$ then $Y[i] = \alpha X[i]$
  - else $Y[i] = \text{NaN}$
- If $X[i] \ge 0$ then $Y[i]=X[i]$

### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```


```math
Y \approx  \text{LeakyRelu}(X) = \begin{bmatrix} 6.1 & -0.95 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

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

## Numerical Accuracy

Operator **LeakyRelu** does not introduce any numerical error. 


