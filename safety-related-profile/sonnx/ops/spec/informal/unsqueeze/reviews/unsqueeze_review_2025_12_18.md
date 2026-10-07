# Contents

- **unsqueeze** operator for type [real](#real)
> We have two arguments, one is real, the other in integer.
> **unsqueeze** operator for type [real,integer](#real_integer)
> Beware of the link...

- **unsqueeze** operator for type [BFLOAT16, FP16, FP32, FP64, INT2, INT4, INT8, INT16, INT32, INT64, UINT2, UINT4, UINT8, UINT16, UINT32, UINT64, BOOL, STRING](#types)

> See notation for types: int32, float32, etc. 
> See the list of types supported by SONNX (see guidelines). For instance, we don't support bfloat16...  

Based on ONNX documentation version 25.

<a id="real"></a>
# **Unsqueeze** (real, integer)

## Signature
Definition of operator $\text{Unsqueeze}$ signature: $Y = \text{Unsqueeze}(X, A)$

> *If you have time*, please use notation **Unsqueeze** instead of \text{Unsqueeze}, see guidelines.

where:
- $X$: input tensor
- $A$: axes tensor (1D Tensor)
- $Y$: output tensor

## Restrictions
The following restrictions apply to the $\text{Unsqueeze}$ operator for the SONNX profile:

[General restrictions](../general_restrictions.md) are applicable.

## Informal specification

> coordinate => index

Operator $\text{Unsqueeze}$ inserts single-dimensional entries to the shape of an input tensor $X$ at the specified axes $A$, producing an output tensor $Y$. The rank of the output tensor $Y$ is equal to the rank of the input tensor $X$ plus the number of axes specified in $A$.
$$
Y[j_0, j_1, \ldots, j_{rY-1}] = X[i_0, i_1, \ldots, i_{rX-1}]
$$

where:
- $rY$ = $rA$ + $rX$

The mapping between output coordinates $(j_0, j_1, \ldots, j_{rY-1})$ and input coordinates $(i_0, i_1, \ldots, i_{rX-1})$ is defined as follows:


> We have to express the relation between the values of the input and output tensors X(index in X) = Y(index in Y)
> X[i_0,...,]=Y[j_0,j_1,...]$ where $j_k = 0$ for the axes that have been added... 

For each output coordinate $(j_0, j_1, \ldots, j_{rY-1})$, the corresponding input coordinate is obtained by removing all $j_p$ where $p \in A'$:

$$
(i_0, i_1, \ldots, i_{rX-1}) = (j_p : p \notin A')
$$

> $(j_p = 0 : p \in A')$

That is, for each $p \notin A'$, $j_p$ maps to the corresponding $i_q$ in $X$, preserving the order.


where 
- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$

> We must describe here (and as constraint, later...) how the shape of $Y$ is obtained (addition of axes with dimension 1)?


### Example 1

> Remark for the WG: the way tensors are displayed has to be explained. It not really homogeneous since 2D matrices are represented without brackets... Should we use Python notation? => to be discussed and formalized.

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


> axis => A
> Add an example that  adds a dimension not at the bounds.

## Error conditions
No error condition

## Inputs

### $X$: `real tensor`
Tensor $X$ is the input tensor to be unsqueezed.

### Constraints
Tensor $X$ has no constraints.
 
### $A$: `integer tensor`
Tensor $A$ is a 1D tensor containing the axes at which to insert singleton dimensions

> We have to define how axes can be designated either using positive or negative values. The definition given in ONNX is unclear: "counting from the back" does not really matches the intuitive way of counting... This should be defined in file [definition.md](../common/definitions.md). For instance, we could introduce the concept "extended index"... 
> Tensor A is a 1D tensor containing the [extended indexes](#...) at which...


### Constraints

 - `[C1]` Value Domain
   - Statement:
   $$\forall i \in [0, rA-1], \; A[i] \in [-rY, rY-1]$$

 - `[C2]` Uniqueness
   - Statement: After normalizing negative indices, all axes in tensor $A$ shall be unique.
        $$\forall i, j \in [0, rA-1], \; (A[i] + rY) \bmod rY = ((A[j] + rY) \bmod rY)\implies (i = j)$$
   - Rationale: Prevents ambiguity when the same axis is specified multiple times using different representations (negative and positive).

> Replace statement: "an axis shall only be designated once in A" does not refer to normalization (or define it first).


> Sorry... so sorry... the guidleines have changed and now section "Attributes" is placed before the "inputs" section.
> 
## Attributes
Operator $\text{Unsqueeze}$ has no attributes.

## Outputs

### $Y$: `real tensor`
Tensor $Y$ is the output tensor after unsqueezing tensor $X$ at the specified axes $A$.

> replace: "at the axes designated by $A$"
 
### Constraints

 - `[C1]` Shape consistency
   - Statement: 
$$
Y = (d'_0, d'_1, \ldots, d'_{rY-1})
$$

> We designate sizes with $dY_0, dY_1,...$ so the definition of the shape should use constraints on $dY_i$.

Where:
- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$.
- For each $p \in [0, rY-1]$:
  - If $p \in A'$, then $d'_p = 1$
  - If $p \notin A'$, then $d'_p = d_q$, where $q$ is the index corresponding to the original dimension of $X$

> Last bullet to be replaced by:
$$(dX_0, dX_1, \ldots, dX_{rX-1}) = (dY_p : p \notin A')$$


> Remove "original"
> $d_q$ => $dX_q$

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Unsqueeze}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.



<a id="type"></a>
# **Unsqueeze** (type, itype)
where 
- type is in: { BFLOAT16, FP16, FP32, FP64, INT2, INT4, INT8, INT16, INT32, INT64, UINT2, UINT4, UINT8, UINT16, UINT32, UINT64, BOOL, STRING }

- itype is in: { INT64 }

## Signature
Definition of operator $\text{Unsqueeze}$ signature: $Y = \text{Unsqueeze}(X, A)$

where:
- $X$: input tensor
- $A$: axes tensor (1D Tensor)
- $Y$: output tensor

> As this is operator operates on the structure the semantics does not depends on the type so we could use the following sentence: "See specification for real numbers." and remove the rest (see operator "Abs").


## Restrictions
The following restrictions apply to the $\text{Unsqueeze}$ operator for the SONNX profile:

[General restrictions](../general_restrictions.md) are applicable.

## Informal specification

Operator $\text{Unsqueeze}$ inserts single-dimensional entries to the shape of an input tensor $X$ at the specified axes $A$, producing an output tensor $Y$. The rank of the output tensor $Y$ is equal to the rank of the input tensor $X$ plus the number of axes specified in $A$.
$$
Y[j_0, j_1, \ldots, j_{rY-1}] = X[i_0, i_1, \ldots, i_{rX-1}]
$$

where:
- $rY$ = $rA$ + $rX$

The mapping between output coordinates $(j_0, j_1, \ldots, j_{rY-1})$ and input coordinates $(i_0, i_1, \ldots, i_{rX-1})$ is defined as follows:


For each output coordinate $(j_0, j_1, \ldots, j_{rY-1})$, the corresponding input coordinate is obtained by removing all $j_p$ where $p \in A'$:

$$
(i_0, i_1, \ldots, i_{rX-1}) = (j_p : p \notin A')
$$

That is, for each $p \notin A'$, $j_p$ maps to the corresponding $i_q$ in $X$, preserving the order.

where 
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
## Error conditions
No error condition

## Inputs

### $X$: `type tensor`
Tensor $X$ is the input tensor to be unsqueezed.

### Constraints
 - `[C1]` <a id="C1ta"></a> Type consistency
   - Statement: Tensors $X$ and $Y$ must have the same data type.
 
### $A$: `itype tensor`
Tensor $A$ is a 1D tensor containing the axes at which to insert singleton dimensions

### Constraints

 - `[C1]` Value Domain
   - Statement:
   $$\forall i \in [0, rA-1], \; A[i] \in [-rY, rY-1]$$

 - `[C2]` Uniqueness
   - Statement: After normalizing negative indices, all axes in tensor $A$ shall be unique.
        $$\forall i, j \in [0, rA-1], \; (A[i] + rY) \bmod rY = ((A[j] + rY) \bmod rY)\implies (i = j)$$
   - Rationale: Prevents ambiguity when the same axis is specified multiple times using different representations (negative and positive).


## Attributes
Operator $\text{Unsqueeze}$ has no attributes.

## Outputs

### $Y$: `type tensor`
Tensor $Y$ is the output tensor after unsqueezing tensor $X$ at the specified axes $A$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: 
$$
Y = (d'_0, d'_1, \ldots, d'_{rY-1})
$$

Where:
- $A'$ is the set of axes specified in tensor $A$, normalized and sorted to be in the range $[0, rY-1]$.
- For each $p \in [0, rY-1]$:
  - If $p \in A'$, then $d'_p = 1$
  - If $p \notin A'$, then $d'_p = d_q$, where $q$ is the index corresponding to the original dimension of $X$

 - `[C2]` Type consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ta) on tensor $X$.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

The $\text{Unsqueeze}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.
