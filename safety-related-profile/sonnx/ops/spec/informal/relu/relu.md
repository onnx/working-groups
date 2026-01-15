# Contents

- **Relu** operator for type [real](#real)
- **Relu** operator for types [float16, float, double](#float)
- **Relu** operator for types [int8, int16, int32, int64](#int)

Based on ONNX documentation version 14.

<a id="real"></a>
# **Relu** (real)

## Signature
$Y = \text{Relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **Relu** on $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1 and GR2 are applicable.

No specific restrictions apply to the **Relu** operator.

## Informal specification

Operator **Relu** is defined as follows: 
- if $X[i] < 0$ then $Y[i] = 0$
- If $X[i] \ge 0$ then $Y[i]=X[i]$

### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```

```math
Y = \text{Relu}(X) = \begin{bmatrix} 6.1 & 0 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `real tensor`
Argument of the **Relu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `real tensor`

Tensor $Y$ is the output of the **Relu** applied to $X$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **Relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **Relu** does not introduce any numerical error. 


<a id="float"></a>
# **Relu** (float)
where float is in {float16, float, double}

## Signature
$Y = \text{Relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **Relu** on $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1 and GR2 are applicable.

No specific restrictions apply to the **Relu** operator.

## Informal specification

Operator **Relu** is defined as follows: 
- if $X[i] = \text{NaN}$ then $Y[i]=\text{NaN}$
- if $X[i] < 0$ then $Y[i] = 0$
- If $X[i] \ge 0$ then $Y[i]=X[i]$

### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```


```math
Y = \text{Relu}(X) = \begin{bmatrix} 6.1 & 0 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `floating-point tensor`
Argument of the **Relu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the output of the **Relu** applied to $X$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **Relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **Relu** does not introduce any numerical error. 




<a id="int"></a>
# **Relu** (int)
where int is {int8, int16, int32, int64}

## Signature
$Y = \text{Relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **Relu** on $X$

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) : GR1 and GR2 are applicable.

No specific restrictions apply to the **Relu** operator.

## Informal specification

Operator **Relu** is defined as follows: 
- if $X[i] < 0$ then $Y[i] = 0$
- If $X[i] \ge 0$ then $Y[i]=X[i]$

### Example 1

```math
X = \begin{bmatrix} 6 & -9 & 35 \end{bmatrix}
```


```math
Y = \text{Relu}(X) = \begin{bmatrix} 6 & 0 & 35 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `integer tensor`
Argument of the **Relu**.

#### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `integer tensor`

Tensor $Y$ is the output of the **Relu** applied to $X$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $X$.

## Attributes

Operator **Relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **Relu** does not introduce any numerical error. 

