# Contents

- **flatten** operator for type [real](#real)
- **flatten** operator for type [BFLOAT16, BOOL, FP64, FP32, FP16, INT16, INT32, INT4, INT64, INT8, STRING, UINT16, UINT32, UINT4, UINT64, UINT8](#types)

Based on ONNX documentation version 24.

<a id="real"></a>
# **flatten** (real)

## Signature
$Y = \text{flatten}(X)$

where:
- `X`: input tensor 
- `Y`: output tensor (2D Tensor)

## Restrictions
The following restrictions apply to the **flatten** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Attribute `axis` must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]`     | Sparse tensors are not supported              | General restriction [GR1](../general_restrictions.md#GR1) |
| `[R3]`     <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **flatten** reshapes the input tensor `X` into a 2D matrix `Y`. The first dimension of `Y` is determined by the product of the dimensions of `X` from the start up to (but not including) the specified `axis`. The second dimension of `Y` is determined by the product of the dimensions of `X` from the specified `axis` to the end.

$$\text{dY}_{0} = \prod_{i=0}^{\text{axis}-1} \text{dX}_{i}$$
$$\text{dY}_{1} = \prod_{i=\text{axis}}^{n-1} \text{dX}_{i}$$

Where 
- $i$ is a dimension index
- $n$ is the rank of tensor `X`

Flatten operation can be expressed as:

<a id="Y"></a>
$$
Y[a, b] = X[j_0, j_1, \ldots, j_{n-1}]
$$

Where:
- $n$ is the rank of tensor `X`
- $z \in [0, n-1]$

- $j_z \in [0, dX_z - 1]$
- $a = \displaystyle\sum_{z=0}^{\text{axis}-1} \left( j_z \prod_{k=z+1}^{\text{axis}-1} dX_k \right)$
- $b = \displaystyle\sum_{z=\text{axis}}^{n-1} \left( j_z \prod_{k=z+1}^{n-1} dX_k \right)$


### Example 1

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 0
```

```math
Y = \begin{bmatrix}\begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}\end{bmatrix}
```
### Example 2

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 1
```

```math
Y =  
  \begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 \\
12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}

```
### Example 3

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = 2
```
```math
Y = \begin{bmatrix}
  \begin{bmatrix} 0 & 1 & 2 & 3\end{bmatrix} \begin{bmatrix}  4 & 5 & 6 & 7 \end{bmatrix} \begin{bmatrix}  8 & 9 & 10 & 11 \end{bmatrix} \begin{bmatrix}  12 & 13 & 14 & 15 \end{bmatrix} \begin{bmatrix}  16 & 17 & 18 & 19 \end{bmatrix} \begin{bmatrix}  20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

## Error conditions
No error condition

## Inputs

### $X$: `real tensor`
Tensor `X` is the input tensor to be flattened.

### Constraints

 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor `X` and attribute `axis`
   - Statement: $n \geq \text{axis}$
   
   where $n$ is the rank of tensor `X`.
   - Rationale: Ensures that the specified axis is valid for the given tensor rank.
 
## Attributes

### axis: `int`
The axis starting from which the input tensor will be flattened into the second dimension of the output.

### Constraints
 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor `X` and attribute `axis`
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

 - `[C2]` <a id="C2ra"></a> Value domain
    - Statement: $\text{axis} \in [-n, n]$

    where $n$ is the rank of tensor `X`.
    - Rationale: Ensures that the attribute `axis` is a valid axis for tensor `X`

## Outputs

### $Y$: `real tensor`
Tensor `Y` is the flattened output tensor.

### Constraints

 - `[C1]` Shape consistency
   - Statement: The shape of tensor `Y` is $(dY_0, dY_1)$, where:
     - $dY_0 = \prod_{i=0}^{\text{axis}-1} dX_i$

     - $dY_1 = \prod_{i=\text{axis}}^{n-1} dX_i$
   
   Where 
   - $dX_i$ is the size of dimension $i$ of tensor `X`
   - $n$ is the rank of tensor `X`.

 - `[C2]` Value Domain
    - Statement: Each element in tensor `Y` must correspond to the appropriate flattened element from tensor `X` based on the flattening parameters. [<b><span style="font-family: 'Courier New', monospace">Y</span></b>](#Y)

    - Rationale: Ensures that the output tensor `Y` accurately reflects the flattening operation performed on tensor `X`.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The **flatten** operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.


<a id="type"></a>
# **flatten** (type)
Where type in in { BFLOAT16, BOOL, FP64, FP32, FP16, INT16, INT32, INT4, INT64, INT8, STRING, UINT16, UINT32, UINT4, UINT64, UINT8 }

## Signature
$Y = \text{flatten}(X)$

where:
- `X`: input tensor 
- `Y`: output tensor (2D Tensor)

## Restrictions
The following restrictions apply to the **flatten** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Attribute `axis` must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]`     | Sparse tensors are not supported              | General restriction [GR1](../general_restrictions.md#GR1) |
| `[R3]`     <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R4]`     <a id="tR9"></a>     | `X` and `Y` tensor must have the same type   |  General restriction [GR3](../general_restrictions.md#GR3) |

## Informal specification

Operator **flatten** reshapes the input tensor `X` into a 2D matrix `Y`. The first dimension of `Y` is determined by the product of the dimensions of `X` from the start up to (but not including) the specified `axis`. The second dimension of `Y` is determined by the product of the dimensions of `X` from the specified `axis` to the end.

$$\text{dY}_{0} = \prod_{i=0}^{\text{axis}-1} \text{dX}_{i}$$
$$\text{dY}_{1} = \prod_{i=\text{axis}}^{n-1} \text{dX}_{i}$$

Where 
- $i$ is a dimension index
- $n$ is the rank of tensor `X`

Flatten operation can be expressed as:

<a id="Yt"></a>
$$
Y[a, b] = X[j_0, j_1, \ldots, j_{n-1}]
$$

Where:
- $n$ is the rank of tensor `X`
- $z \in [0, n-1]$

- $j_z \in [0, dX_z - 1]$
- $a = \displaystyle\sum_{z=0}^{\text{axis}-1} \left( j_z \prod_{k=z+1}^{\text{axis}-1} dX_k \right)$
- $b = \displaystyle\sum_{z=\text{axis}}^{n-1} \left( j_z \prod_{k=z+1}^{n-1} dX_k \right)$


### Example 1

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 0
```

```math
Y = \begin{bmatrix}\begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}\end{bmatrix}
```
### Example 2

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 1
```

```math
Y =  
  \begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 \\
12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}

```
### Example 3

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = 2
```
```math
Y = \begin{bmatrix}
  \begin{bmatrix} 0 & 1 & 2 & 3\end{bmatrix} \begin{bmatrix}  4 & 5 & 6 & 7 \end{bmatrix} \begin{bmatrix}  8 & 9 & 10 & 11 \end{bmatrix} \begin{bmatrix}  12 & 13 & 14 & 15 \end{bmatrix} \begin{bmatrix}  16 & 17 & 18 & 19 \end{bmatrix} \begin{bmatrix}  20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

## Error conditions
No error condition

## Inputs

### $X$: `type tensor`
Tensor `X` is the input tensor to be flattened.

### Constraints

 - `[C1]` <a id="C1ta"></a> Consistency between the shape of tensor `X` and attribute `axis`
   - Statement: $n \geq \text{axis}$
   
   where $n$ is the rank of tensor `X`.
   - Rationale: Ensures that the specified axis is valid for the given tensor rank.

 - `[C2]` <a id="C20ta"></a> Type consistency
   - Statement: Tensors X and Y must have the same type. [<b><span style="font-family: 'Courier New', monospace">[R4]</span></b>](#tR9)
 
## Attributes

### axis: `int`
The axis starting from which the input tensor will be flattened into the second dimension of the output.

### Constraints
 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor `X` and attribute `axis`
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ta) on tensor $X$.

 - `[C2]` <a id="C2ra"></a> Value domain
    - Statement: $\text{axis} \in [-n, n]$

    where $n$ is the rank of tensor `X`.
    - Rationale: Ensures that the attribute `axis` is a valid axis for tensor `X`

## Outputs

### $Y$: `type tensor`
Tensor `Y` is the flattened output tensor.

### Constraints

 - `[C1]` Shape consistency
   - Statement: The shape of tensor `Y` is $(dY_0, dY_1)$, where:
     - $dY_0 = \prod_{i=0}^{\text{axis}-1} dX_i$

     - $dY_1 = \prod_{i=\text{axis}}^{n-1} dX_i$
   
   Where 
   - $dX_i$ is the size of dimension $i$ of tensor `X`
   - $n$ is the rank of tensor `X`.

 - `[C2]` Value Domain
    - Statement: Each element in tensor `Y` must correspond to the appropriate flattened element from tensor `X` based on the flattening parameters. [<b><span style="font-family: 'Courier New', monospace">Y</span></b>](#Yt)

    - Rationale: Ensures that the output tensor `Y` accurately reflects the flattening operation performed on tensor `X`.

 - `[C3]` Type consistency
    - Statement: see constraint  [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C20ta) on tensor $X$.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The **flatten** operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.

