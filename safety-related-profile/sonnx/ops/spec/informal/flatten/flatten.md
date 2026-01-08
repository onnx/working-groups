# Contents

- **Flatten** operator for type [real](#real)
- **Flatten** operator for type [BFLOAT16, BOOL, FP64, FP32, FP16, INT16, INT32, INT4, INT64, INT8, STRING, UINT16, UINT32, UINT4, UINT64, UINT8](#types)

Based on ONNX documentation version 24.

<a id="real"></a>
# **Flatten** (real)

## Signature
$Y = \text{Flatten}(X)$

where:
- $X$: input tensor 
- $Y$: output tensor (2D Tensor)

## Restrictions
The following restrictions apply to the $\text{Flatten}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification

Operator $\text{Flatten}$ reshapes the input tensor $X$ into a 2D matrix $Y$. The first dimension of $Y$ is determined by the product of the dimensions of $X$ from the start up to (but not including) the specified $\text{axis}$. The second dimension of $Y$ is determined by the product of the dimensions of $X$ from the specified $\text{axis}$ to the end.

$$\text{dY}_{0} = \prod_{i=0}^{\text{axis'}-1} \text{dX}_{i}$$
$$\text{dY}_{1} = \prod_{i=\text{axis'}}^{rX-1} \text{dX}_{i}$$

Note that the product over an empty range/interval is defined to be 1. That means:
- If $\text{axis'} = 0$, then $\text{dY}_{0} = 1$

- If $\text{axis'} = rX$, then $\text{dY}_{1} = 1$

Where 
- $i$ is a dimension index
- $la$ is the length of attribute `axis`

- $\text{axis'}$  is the normalized $\text{axis}$ and is calculated as follows:

$$\forall a \in [0, la -1]. \begin{cases}
      \text{axis'[a]} = \text{axis[a]} & \text{if } \text{axis[a]} \geq 0 \\
      \text{axis'[a]} = \text{axis[a]} + rX & \text{if } \text{axis[a]} < 0
\end{cases}$$

Flatten operation can be expressed as:

<a id="Y"></a>

$$Y[a, b] = X[j_0, j_1, \ldots, j_{rX-1}]$$


Where:
- $z \in [0, rX-1]$
- $j_z \in [0, dX_z - 1]$
- $a = \displaystyle\sum_{z=0}^{\text{axis}-1} \left( j_z \prod_{k=z+1}^{\text{axis}-1} dX_k \right)$

- $b = \displaystyle\sum_{z=\text{axis}}^{rX-1} \left( j_z \prod_{k=z+1}^{rX-1} dX_k \right)$


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
Tensor $X$ is the input tensor to be flattened.

### Constraints

 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor $X$ and attribute `axis`
   - Statement: $rX \geq \text{axis}$
   
   - Rationale: Ensures that the specified axis is valid for the given tensor rank.
 
## Attributes

### axis: `integer`
The axis starting from which the input tensor will be flattened into the second dimension of the output.

### Constraints
 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor $X$ and attribute `axis`
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

 - `[C2]` <a id="C2ra"></a> Value domain
    - Statement: $\text{axis} \in [-rX, rX]$
    - Rationale: Ensures that the attribute `axis` is a valid axis for tensor $X$

## Outputs

### $Y$: `real tensor`
Tensor $Y$ is the flattened output tensor.

### Constraints

 - `[C1]` Shape consistency
   - Statement: The shape of tensor $Y$ is $(dY_0, dY_1)$, where:
     - $dY_0 = \prod_{i=0}^{\text{axis}-1} dX_i$

     - $dY_1 = \prod_{i=\text{axis}}^{rX-1} dX_i$
   
   Where 
   - $dX_i$ is the size of dimension $i$ of tensor $X$
## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Flatten}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.


<a id="type"></a>
# **Flatten** (type)
Where type in in { BFLOAT16, BOOL, FP64, FP32, FP16, INT16, INT32, INT4, INT64, INT8, STRING, UINT16, UINT32, UINT4, UINT64, UINT8 }

## Signature
$Y = \text{Flatten}(X)$

where:
- $X$: input tensor 
- $Y$: output tensor (2D Tensor)

## Restrictions
The following restrictions apply to the $\text{Flatten}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification

Operator $\text{Flatten}$ reshapes the input tensor $X$ into a 2D matrix $Y$. The first dimension of $Y$ is determined by the product of the dimensions of $X$ from the start up to (but not including) the specified $\text{axis}$. The second dimension of $Y$ is determined by the product of the dimensions of $X$ from the specified $\text{axis}$ to the end.

$$\text{dY}_{0} = \prod_{i=0}^{\text{axis'}-1} \text{dX}_{i}$$
$$\text{dY}_{1} = \prod_{i=\text{axis'}}^{rX-1} \text{dX}_{i}$$

Note that the product over an empty range/interval is defined to be 1. That means:
- If $\text{axis'} = 0$, then $\text{dY}_{0} = 1$

- If $\text{axis'} = rX$, then $\text{dY}_{1} = 1$

Where 
- $i$ is a dimension index
- $la$ is the length of attribute `axis`

- $\text{axis'}$  is the normalized $\text{axis}$ and is calculated as follows:

$$\forall a \in [0, la -1]. \begin{cases}
      \text{axis'[a]} = \text{axis[a]} & \text{if } \text{axis[a]} \geq 0 \\
      \text{axis'[a]} = \text{axis[a]} + rX & \text{if } \text{axis[a]} < 0
\end{cases}$$

Flatten operation can be expressed as:

<a id="Yt"></a>

$$Y[a, b] = X[j_0, j_1, \ldots, j_{rX-1}]$$

Where:
- $z \in [0, rX-1]$
- $j_z \in [0, dX_z - 1]$
- $a = \displaystyle\sum_{z=0}^{\text{axis}-1} \left( j_z \prod_{k=z+1}^{\text{axis}-1} dX_k \right)$

- $b = \displaystyle\sum_{z=\text{axis}}^{rX-1} \left( j_z \prod_{k=z+1}^{rX-1} dX_k \right)$


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
Tensor $X$ is the input tensor to be flattened.

### Constraints

 - `[C1]` <a id="C1ta"></a> Consistency between the shape of tensor $X$ and attribute $\text{axis}$
   - Statement: $rX \geq \text{axis}$
   
   - Rationale: Ensures that the specified axis is valid for the given tensor rank.

 - `[C2]` <a id="C20ta"></a> Type consistency
   - Statement: Tensors $X$ and $Y$ must have the same type.
 
## Attributes

### axis: `int`
The axis starting from which the input tensor will be flattened into the second dimension of the output.

### Constraints
 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor $X$ and attribute $\text{axis}$
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ta) on tensor $X$.

 - `[C2]` <a id="C2ra"></a> Value domain
    - Statement: $\text{axis} \in [-rX, rX]$

    - Rationale: Ensures that the attribute $\text{axis}$ is a valid axis for tensor $X$
## Outputs

### $Y$: `type tensor`
Tensor $Y$ is the flattened output tensor.

### Constraints

 - `[C1]` Shape consistency
   - Statement: The shape of tensor $Y$ is $(dY_0, dY_1)$, where:
     - $dY_0 = \prod_{i=0}^{\text{axis}-1} dX_i$

     - $dY_1 = \prod_{i=\text{axis}}^{rX-1} dX_i$
   
   Where 
   - $dX_i$ is the size of dimension $i$ of tensor $X$

 - `[C2]` Type consistency
    - Statement: see constraint  [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C20ta) on tensor $X$.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Flatten}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.
