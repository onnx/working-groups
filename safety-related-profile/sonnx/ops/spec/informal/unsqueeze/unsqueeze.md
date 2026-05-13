# Contents

- **Unsqueeze** operator for type [real,integer](#real_integer)
- **Unsqueeze** operator for type [float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64, bool, string](#type)

Based on ONNX [Unsqueeze version 25](https://onnx.ai/onnx/operators/onnx__Unsqueeze.html).

<a id="real_integer"></a>
# **Unsqueeze** (real, integer)

## Signature
Definition of operator **Unsqueeze** signature: 


$Y = \textbf{Unsqueeze}(X, A)$

where:
- $X$: input tensor
- $A$: axes tensor (1D Tensor)
- $Y$: output tensor

## Restrictions
The following restrictions apply to the **Unsqueeze** operator for the SONNX profile:

[General restrictions](../common/general_restrictions.md) are applicable.

## Informal specification

Operator **Unsqueeze** inserts single-dimensional entries to the shape of an input tensor $X$ at the specified axes $A$, producing an output tensor $Y$. The rank of the output tensor $Y$ is equal to the rank of the input tensor $X$ plus the number of axes specified in $A$.

$$
X[i_0, i_1, \ldots, i_{rX-1}] = Y[j_0, j_1, \ldots, j_{rY-1}]
$$

where:
- $rY$ = $rA$ + $rX$


The mapping between input index $(i_0, i_1, \ldots, i_{rX-1})$ and output index $(j_0, j_1, \ldots, j_{rY-1})$ is defined as follows:


For each input index $(i_0, i_1, \ldots, i_{rX-1})$, the corresponding output index is obtained by inserting singleton dimensions at the axes specified in $A'$:

$$
(j_0, j_1, \ldots, j_{rY-1}) = \forall k \in A'. \quad \text{f (0,k, $(i_0, i_1, \ldots, i_{rX-1})$)}
$$

where
- $f$ is a function that inserts 0 at position $k$ in the index ($i_0, i_1, \ldots, i_{rX-1}$)

- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$


To calculate the ouput shape:

$$
(dY_0, dY_1, \ldots, dY_{rY-1}) = \forall k \in A'. \quad \text{f (1,k, $(dX_0, dX_1, \ldots, dX_{rX-1})$)}
$$

where
- $f$ is a function that inserts 1 at position $k$ in the shape ($dX_0, dX_1, \ldots, dX_{rX-1}$)
- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$

### Example 1

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = \begin{bmatrix} 0 \end{bmatrix}
```

```math
Y = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
      0 & 1 & 2 & 3 \\
      4 & 5 & 6 & 7 \\
      8 & 9 & 10 & 11
    \end{bmatrix}
    \quad
    \begin{bmatrix}
      12 & 13 & 14 & 15 \\
      16 & 17 & 18 & 19 \\
      20 & 21 & 22 & 23
    \end{bmatrix}
  \end{bmatrix}
\end{bmatrix}
```
### Example 2

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = \begin{bmatrix} -1 \end{bmatrix}
```
```math
Y = \begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}0 \end{bmatrix} & \begin{bmatrix}1 \end{bmatrix} & \begin{bmatrix}2 \end{bmatrix} & \begin{bmatrix}3 \end{bmatrix} \\
    \begin{bmatrix}4 \end{bmatrix} & \begin{bmatrix}5 \end{bmatrix} & \begin{bmatrix}6 \end{bmatrix} & \begin{bmatrix}7 \end{bmatrix} \\
    \begin{bmatrix}8 \end{bmatrix} & \begin{bmatrix}9 \end{bmatrix} & \begin{bmatrix}10 \end{bmatrix} & \begin{bmatrix}11 \end{bmatrix}
  \end{bmatrix}
  \quad
  \begin{bmatrix}
    \begin{bmatrix}12 \end{bmatrix} & \begin{bmatrix}13 \end{bmatrix} & \begin{bmatrix}14 \end{bmatrix} & \begin{bmatrix}15 \end{bmatrix} \\
    \begin{bmatrix}16 \end{bmatrix} & \begin{bmatrix}17 \end{bmatrix} & \begin{bmatrix}18 \end{bmatrix} & \begin{bmatrix}19 \end{bmatrix} \\
    \begin{bmatrix}20 \end{bmatrix} & \begin{bmatrix}21 \end{bmatrix} & \begin{bmatrix}22 \end{bmatrix} & \begin{bmatrix}23 \end{bmatrix}
  \end{bmatrix}
\end{bmatrix}
```
### Example 3

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = \begin{bmatrix} 0, 1 \end{bmatrix}
```
```math
Y =
\begin{bmatrix} 
  \begin{bmatrix}
      \begin{bmatrix}
        \begin{bmatrix}
          0 & 1 & 2 & 3 \\
          4 & 5 & 6 & 7 \\
          8 & 9 & 10 & 11
        \end{bmatrix}
        \quad
        \begin{bmatrix}
          12 & 13 & 14 & 15 \\
          16 & 17 & 18 & 19 \\
          20 & 21 & 22 & 23  
        \end{bmatrix}
    \end{bmatrix}
  \end{bmatrix}
\end{bmatrix}
```

### Example 4 
```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = \begin{bmatrix} 1, 2 \end{bmatrix}
```

```math
\begin{bmatrix} 
        \begin{bmatrix}
          \begin{bmatrix}
            \begin{bmatrix}
          0 & 1 & 2 & 3 \\
          4 & 5 & 6 & 7 \\
          8 & 9 & 10 & 11
          \end{bmatrix}
          \end{bmatrix}
        \end{bmatrix}
        \quad
        \begin{bmatrix}
          \begin{bmatrix}
            \begin{bmatrix}
          12 & 13 & 14 & 15 \\
          16 & 17 & 18 & 19 \\
          20 & 21 & 22 & 23
          \end{bmatrix}
          \end{bmatrix}  
        \end{bmatrix}
\end{bmatrix}
```

## Error conditions
No error condition

## Attributes
Operator **Unsqueeze** has no attributes.

## Inputs

### $X$: `real tensor`
Tensor $X$ is the input tensor to be unsqueezed.

### Constraints
Tensor $X$ has no constraints.
 
### $A$: `integer tensor`
Tensor $A$ is a 1D tensor containing the axes at which to insert singleton dimensions.

Note that any negative index, $a$, represents the corresponding non-negative index calculated as $a + rA$.

### Constraints

 - `[C1]` Value Domain
   - Statement:
   $$\forall i \in [0, rA-1], \; A[i] \in [-rY, rY-1]$$

 - `[C2]` Uniqueness
   - Statement: An axis shall only be designated once in A.
        $$\forall i, j \in [0, rA-1], \; (A[i] + rY) \bmod rY = ((A[j] + rY) \bmod rY)\implies (i = j)$$
   - Rationale: Prevents ambiguity when the same axis is specified multiple times using different representations (negative and positive).


## Outputs

### $Y$: `real tensor`
Tensor $Y$ is the output tensor after unsqueezing tensor $X$ at the axes designated by 
$A$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: 
$$
(dY_0, dY_1, \ldots, dY_{rY-1}) = \forall k \in A'. \quad \text{f (1,k, $(dX_0, dX_1, \ldots, dX_{rX-1})$)}
$$

where
- $f$ is a function that inserts 1 at position $k$ in the shape ($dX_0, dX_1, \ldots, dX_{rX-1}$)
- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$



## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Unsqueeze}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.



<a id="type"></a>
# **Unsqueeze** (type, int64)
where type is in: { float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64, bool, string }

See specification for [real numbers](#real_integer).

