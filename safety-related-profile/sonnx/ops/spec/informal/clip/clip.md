# Contents

- **clip** operator for type [real](#real)
- **clip** operator for types [INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64](#int)
- **clip** operator for types [FP16, FP32, FP64, BFLOAT16](#floats)

Based on ONNX documentation version 13.

<a id="real"></a>
# **clip** (real)

## Signature
$Y = \text{clip}(X,L,M)$

where:
- `X`: input tensor
- `L`: minimum tensor (empty shape tensor - scalar)
- `M`: maximum tensor (empty shape tensor - scalar)

## Restrictions
The following restrictions apply to the **clip** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Input L must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]`     | Input M must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]`     | Sparse tensors are not supported              | General restriction [GR1](../general_restrictions.md#GR1) |
| `[R4]`     <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **clip** limit the given input within an interval. For each element in the input tensor `X`: 
- If `L` $\leq$ `M`:
  - if $X[i]$ < `L` then $Y[i]$ = `L`.
  - If $X[i]$ > `M` then $Y[i]$ = `M`.
  - Otherwise, $Y[i]$ = $X[i]$.
- If `L` $\gt$ `M`:
  - $\forall i,\ Y[i] = M$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The result is stored in output tensor `Y`.

Clip operation can be expressed as:

$$\forall i,\ Y[i] = \min(M, \max(X[i], L))$$
where $i$ is a [tensor index](../common/definitions.md#tensor_index).


### Example 1

```math
A = \begin{bmatrix} -6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
L = 0
\quad
M = 10
```

```math
Y = \begin{bmatrix} 0 & 9.5 & 10 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
L = 20
\quad
M = 10
```

```math
Y = \begin{bmatrix} \min(10, \max(6.1, 20)) & \min(10, \max(9.5, 20)) & \min(10, \max(35.7, 20)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} 10 & 10 & 10 \end{bmatrix}
```

## Error conditions
No error condition

## Inputs

### $X$: real
Tensor `X` is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors `X` and `Y` must have the same shape.
 
### $L$: real
Tensor `L` is the minimum bound for clipping.

The shape of tensor `L` must be empty (scalar).

### Constraints
Tensor `L` has no constraints.

### $M$: real
Tensor `M` is the maximum bound for clipping.

The shape of tensor `M` must be empty (scalar).

### Constraints
Tensor `M` has no constraints.

## Outputs

### $Y$: real
Tensor `Y` is the element-wise result of clipping `X` by the interval $[L, M]$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor `X`.


## Attributes

Operator **clip** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **clip** does not introduce any numerical error. Hence, for all valid indexes $i$,

<a id="int"></a>
# **clip** (int, int, int)
where int is in {INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64}

## Signature
$Y = \text{clip}(X,L,M)$

where:
- `X`: input tensor
- `L`: minimum tensor (empty shape tensor - scalar)
- `M`: maximum tensor (empty shape tensor - scalar)

## Restrictions
The following restrictions apply to the **clip** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Input L must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]`     | Input M must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]`     | Sparse tensors are not supported              | General restriction [GR1](../general_restrictions.md#GR1) |
| `[R4]`     <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R5]` <a id="R5"></a>     | All tensors shall have the same datatype  | General restriction [GR3](../general_restrictions.md#GR3) |
## Informal specification

Operator **clip** limit the given input within an interval. For each element in the input tensor `X`: 
- If `L` $\leq$ `M`:
  - if $X[i]$ < `L` then $Y[i]$ = `L`.
  - If $X[i]$ > `M` then $Y[i]$ = `M`.
  - Otherwise, $Y[i]$ = $X[i]$.
- If `L` $\gt$ `M`:
  - $\forall i,\ Y[i] = M$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The result is stored in output tensor `Y`.

Clip operation can be expressed as:

$$\forall i,\ Y[i] = \min(M, \max(X[i], L))$$
where $i$ is a [tensor index](../common/definitions.md#tensor_index).

### Example 1

```math
A = \begin{bmatrix} -6 & 9 & 35 \end{bmatrix}
```

```math
L = 0
\quad
M = 10
```

```math
Y = \begin{bmatrix} 0 & 9 & 10 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 6 & 9 & 35 \end{bmatrix}
```

```math
L = 20
\quad
M = 10
```

```math
Y = \begin{bmatrix} \min(10, \max(6, 20)) & \min(10, \max(9, 20)) & \min(10, \max(35, 20)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} 10 & 10 & 10 \end{bmatrix}
```

## Error conditions
No error condition

## Inputs

### $X$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64
Tensor `X` is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors `X` and `Y` must have the same shape.
 - `[C2]` <a id="C2ia"></a> Type consistency
   - Statement: Tensors `X`, `L`, `M` and `Y` must have the same type.
 
### $L$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64
Tensor `L` is the minimum bound for clipping.

The shape of tensor `L` must be empty (scalar).

### Constraints
- `[C1]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor `X`.

### $M$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64
Tensor `M` is the maximum bound for clipping.

The shape of tensor `M` must be empty (scalar).

### Constraints
- `[C1]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor `X`.

## Outputs

### $Y$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64
Tensor `Y` is the element-wise result of clipping `X` by the interval $[L, M]$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor `X`.
 - `[C2]` Type consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">  [C2]</span></b>](#C2ia) on tensor `X`.

## Attributes

Operator **clip** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **clip** does not introduce any numerical error. Hence, for all valid indexes $i$,


<a id="float"></a>
# **clip** (float, float, float)
where float is in {FP16, FP32, FP64, BFLOAT16}

## Signature
$Y = \text{clip}(X,L,M)$

where:
- `X`: input tensor
- `L`: minimum tensor (empty shape tensor - scalar)
- `M`: maximum tensor (empty shape tensor - scalar)

## Restrictions
The following restrictions apply to the **clip** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Input L must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]`     | Input M must be set                           | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]`     | Sparse tensors are not supported              | General restriction [GR1](../general_restrictions.md#GR1) |
| `[R4]`     <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R5]` <a id="R5"></a>     | All tensors shall have the same datatype  | General restriction [GR3](../general_restrictions.md#GR3) |
## Informal specification

Operator **clip** limit the given input within an interval. For each element in the input tensor `X` (discarding `nan` values in `L` or `M`, for more details see the definition below):
- If `L` $\leq$ `M`:
  - if $X[i]$ < `L` then $Y[i]$ = `L`.
  - If $X[i]$ > `M` then $Y[i]$ = `M`.
  - Otherwise, $Y[i]$ = $X[i]$.
- If `L` $\gt$ `M`:
  - $\forall i,\ Y[i] = M$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The result is stored in output tensor `Y`.

Clip operation can be expressed as:

$$\forall i,\ Y[i] = 
\begin{cases} 
\min(X[i], M) & \text{ if } L = \text{nan} \\
\max(X[i], L) & \text{ if } M = \text{nan} \\
X[i] & \text{ if } L = \text{nan} \text{ and } M = \text{nan} \\
\min(M, \max(X[i], L)) & \text{ otherwise }  \\
\end{cases}$$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).


### Example 1

```math
A = \begin{bmatrix} -6.3 & 9.2 & 35.5 \end{bmatrix}
```

```math
L = 0.5
\quad
M = 10.1
```

```math
Y = \begin{bmatrix} 0.5 & 9.2 & 10.1 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 6.5 & 9.2 & 35.1 \end{bmatrix}
```

```math
L = 20.2
\quad
M = 10.0
```

```math
Y = \begin{bmatrix} \min(10.0, \max(6.5, 20.2)) & \min(10.0, \max(9.2, 20.2)) & \min(10.0, \max(35.1, 20.2)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} 10.0 & 10.0 & 10.0 \end{bmatrix}
```

### Example 3

```math
A = \begin{bmatrix} -\infty & 0.0 & \infty & NaN \end{bmatrix}
```
```math
L = -1.0
\quad
M = NaN
```

```math
Y = \begin{bmatrix} \max(-\infty, -1.0) & \max(0.0, -1.0) & \max(\infty, -1.0) & \max(NaN, -1.0) \end{bmatrix}
```

```math
Y = \begin{bmatrix} -1.0 & 0.0 & \infty & NaN \end{bmatrix}
```

### Example 4

```math
A = \begin{bmatrix} -\infty & 0.0 & \infty & NaN \end{bmatrix}
```
```math
L = NaN
\quad
M = NaN
```

```math
Y = \begin{bmatrix} -\infty & 0.0 & \infty & NaN \end{bmatrix}
```

## Error conditions
- Values of the output tensor may be IEEE 754 infinity or NaN

## Inputs

### $X$: FP16, FP32, FP64, BFLOAT16
Tensor `X` is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors `X` and `Y` must have the same shape.
 - `[C2]` <a id="C2ia"></a> Type consistency
   - Statement: Tensors `X`, `L`, `M` and `Y` must have the same type.
 
### $L$: FP16, FP32, FP64, BFLOAT16
Tensor `L` is the minimum bound for clipping.

The shape of tensor `L` must be empty (scalar).

### Constraints
- `[C1]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor `X`.

### $M$: FP16, FP32, FP64, BFLOAT16
Tensor `M` is the maximum bound for clipping.

The shape of tensor `M` must be empty (scalar).

### Constraints
- `[C1]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor `X`.

## Outputs

### $Y$: FP16, FP32, FP64, BFLOAT16
Tensor `Y` is the element-wise result of clipping `X` by the interval $[L, M]$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor `X`.
 - `[C2]` Type consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">  [C2]</span></b>](#C2ia) on tensor `X`.

## Attributes

Operator **clip** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Operator **clip** does not introduce any numerical error. Hence, for all valid indexes $i$,