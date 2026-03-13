# Contents

- **Shape** operator for type [real](#real)
- **Shape** operator for type [ BFLOAT16, FP64, FP32, FP16, INT2, INT4, INT8, INT16, INT32, INT64, UINT2, UINT4, UINT8, UINT16, UINT32, UINT64, STRING, BOOL](#types)

Based on ONNX documentation version 25.

<a id="real"></a>
# **Shape** (real)

## Signature
$Y = \text{Shape}(X)$

where:
- $X$: input tensor 
- $Y$: output tensor (1D Tensor)

## Restrictions
The following restrictions apply to the $\text{Shape}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification
The $\text{Shape}$ operator takes a tensor $X$ as input and produces a 1D tensor $Y$ containing the sliced shape of $X$ according to the `start` and `end` attributes.

Shape operation can be divided into two steps:

### 1. Clamping of `start` and `end` attributes
The `start` and `end` attributes are clamped based on the rank of the input tensor $X$:

#### Start
$$ start < 0 \implies start = start + rX $$

If the clamped `start` is still less than 0, it is set to 0:

$$ start' < 0 \implies start' = 0 $$

Where:
- $start'$ is the clamped value of `start` 

#### End
$$ end < 0 \implies end = end + rX $$

If `end` is greater than the rank of $X$, it is set to the rank of $X$:

$$ end > rX \implies end = rX $$

### 2. Slicing the shape of input tensor
The output tensor $Y$ is obtained by slicing the shape of the input tensor $X$ from index `start` to index `end` (exclusive):


$$ \forall i \in [start', end'[. \quad Y[i - start'] = S[i]  $$

Where:
- $S$ is the shape of input tensor $X$
- $start'$ is the clamped value of `start`
- $end'$ is the clamped value of `end`

Note that if `start` is greater than or equal to `end`, the output tensor $Y$ will be an empty tensor.

### Example 1
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 0 \quad start' = 0
```
```math
end = 3 \quad end' = 3
```
```math
Y = [2, 3, 4]
```

### Example 2
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 1 \quad start' = 1
```
```math
end = 2 \quad end' = 2
```
```math
Y = [3]
```

### Example 3
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 2 \quad start' = 2
```
```math
end = 2 \quad end' = 2
```
```math
Y = []
```

### Example 4
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = -500 \quad start = -500 + 3 = -497 \quad start' = 0
```
```math
end = 2 \quad end' = 2
```
```math
Y = [2,3]
```



### Example 5
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 0 \quad start' = 0
```
```math
end = 1000 \quad end' = 3
```
```math
Y = [2, 3, 4]
```

## Error conditions
No error condition


## Inputs

### $X$: `real tensor`
Tensor $X$ is the input tensor to extract the shape from.

### Constraints
Tensor $X$ has no constraints.

## Attributes

### start: `integer`
Specifies the starting index of the slice.

### Constraints
Attribute `start` has no constraints.

### end: `integer`
Specifies the ending index of the slice (exclusive).
### Constraints
Attribute `end` has no constraints.

## Output

### $Y$: `integer tensor`
Tensor $Y$ is a 1D tensor containing the sliced shape of input tensor $X$.
### Constraints
Tensor $Y$ has no constraints.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Shape}$ operator does not introduce any numerical error. Hence, all valid indices of the output values belong to the shape of the input tensor.


<a id="type"></a>
# **Shape** (type)

Where type in { BFLOAT16, FP64, FP32, FP16, INT2, INT4, INT8, INT16, INT32, INT64, UINT2, UINT4, UINT8, UINT16, UINT32, UINT64, STRING, BOOL}

## Signature
$Y = \text{Shape}(X)$

where:
- $X$: input tensor 
- $Y$: output tensor (1D Tensor)

## Restrictions
The following restrictions apply to the $\text{Shape}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification
The $\text{Shape}$ operator takes a tensor $X$ as input and produces a 1D tensor $Y$ containing the sliced shape of $X$ according to the `start` and `end` attributes.

Shape operation can be divided into two steps:

### 1. Clamping of `start` and `end` attributes
The `start` and `end` attributes are clamped based on the rank of the input tensor $X$:

#### Start
$$ start < 0 \implies start = start + rX $$

If the clamped `start` is still less than 0, it is set to 0:

$$ start' < 0 \implies start' = 0 $$

Where:
- $start'$ is the clamped value of `start` 

#### End
$$ end < 0 \implies end = end + rX $$

If `end` is greater than the rank of $X$, it is set to the rank of $X$:

$$ end > rX \implies end = rX $$

### 2. Slicing the shape of input tensor
The output tensor $Y$ is obtained by slicing the shape of the input tensor $X$ from index `start` to index `end` (exclusive):


$$ \forall i \in [start', end'[. \quad Y[i - start'] = S[i]  $$

Where:
- $S$ is the shape of input tensor $X$
- $start'$ is the clamped value of `start`
- $end'$ is the clamped value of `end`

Note that if `start` is greater than or equal to `end`, the output tensor $Y$ will be an empty tensor.

### Example 1
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 0 \quad start' = 0
```
```math
end = 3 \quad end' = 3
```
```math
Y = [2, 3, 4]
```

### Example 2
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 1 \quad start' = 1
```
```math
end = 2 \quad end' = 2
```
```math
Y = [3]
```

### Example 3
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 2 \quad start' = 2
```
```math
end = 2 \quad end' = 2
```
```math
Y = []
```

### Example 4
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = -500 \quad start = -500 + 3 = -497 \quad start' = 0
```
```math
end = 2 \quad end' = 2
```
```math
Y = [2,3]
```



### Example 5
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
X.shape = [2, 3, 4]
```
```math
start = 0 \quad start' = 0
```
```math
end = 1000 \quad end' = 3
```
```math
Y = [2, 3, 4]
```

## Error conditions
No error condition


## Inputs

### $X$: `type tensor`
Tensor $X$ is the input tensor to extract the shape from.

### Constraints
Tensor $X$ has no constraints.

## Attributes

### start: `integer`
Specifies the starting index of the slice.

### Constraints
Attribute `start` has no constraints.

### end: `integer`
Specifies the ending index of the slice (exclusive).
### Constraints
Attribute `end` has no constraints.

## Output

### $Y$: `integer64 tensor`
Tensor $Y$ is a 1D tensor containing the sliced shape of input tensor $X$.
### Constraints
Tensor $Y$ has no constraints.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Shape}$ operator does not introduce any numerical error. Hence, all valid indices of the output values belong to the shape of the input tensor.
