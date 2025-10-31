# Contents

- **relu** operator for type [real](#real)
- **relu** operator for types [FP16, FP32, FP64](#float)
- **relu** operator for types [INT8, INT16, INT32, INT64](#int)

Based on ONNX documentation version 14.

<a id="real"></a>
# **relu** (real)

## Signature
$Y = \text{relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **relu** on $X$

## Restrictions

The following restrictions apply to the **relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```


```math
Y = \text{relu}(X) = \begin{bmatrix} 6.1 & 0 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `real tensor`
Argument of the **relu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `real tensor`

Tensor $Y$ is the output of the **relu** applied to $X$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **relu** does not introduce any numerical error. 


<a id="float"></a>
# **relu** (float)
where float is in {FP16, FP32, FP64}

## Signature
$Y = \text{relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **relu** on $X$

## Restrictions

The following restrictions apply to the **relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

### Example 1

```math
X = \begin{bmatrix} 6.1 & -9.5 & 35.7 \end{bmatrix}
```


```math
Y = \text{relu}(X) = \begin{bmatrix} 6.1 & 0 & 35.7 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `floating-point tensor`
Argument of the **relu**.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the output of the **relu** applied to $X$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Attributes

Operator **relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **relu** does not introduce any numerical error. 




<a id="int"></a>
# **relu** (int)
where int is {INT8, INT16, INT32, INT64}

## Signature
$Y = \text{relu}(X)$

where:
- $X$: input tensor
- $Y$: result of the element-wise application of **relu** on $X$

## Restrictions

The following restrictions apply to the **relu** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **relu** computes: $Y = \text{max}(0, X)$ where $\text{max}$ is ONNX **max** operator.

### Example 1

```math
X = \begin{bmatrix} 6 & -9 & 35 \end{bmatrix}
```


```math
Y = \text{relu}(X) = \begin{bmatrix} 6 & 0 & 35 \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $\text{X}$: `integer tensor`
Argument of the **relu**.

#### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape. 
  
## Outputs

### $\text{Y}$: `integer tensor`

Tensor $Y$ is the output of the **relu** applied to $X$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $X$.

## Attributes

Operator **relu** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **relu** does not introduce any numerical error. 

