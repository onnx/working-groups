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

The following restrictions apply to the **Relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../common/general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../common/general_restrictions.md#GR2) |

## Informal specification

Operator **Relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

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

The following restrictions apply to the **Relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../common/general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../common/general_restrictions.md#GR2) |

## Informal specification

Operator **Relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

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

The following restrictions apply to the **Relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../common/general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../common/general_restrictions.md#GR2) |

## Informal specification

Operator **Relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

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

