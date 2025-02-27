# Contents
- `Sqrt` [operator (real)](#real)
- `Sqrt` [operator (FP16, FP32, FP64, BFLOAT16)](#float)

<a id="real"></a>
# `Sqrt` operator (real)

### Restrictions
The following restrictions apply to the `Sqrt` operator for the SONNX profile:
- The input tensor `X` must contain non-negative values, as the square root is undefined for negative values. `[R1]`
- Tensors `X`, `Y` must have the same shape. `[R2]`
- The input tensor `X` must be of floating-point types. `[R3]`
- No broadcasting is allowed for the tensor `X`. `[R4]`
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md)

### Signature

`Y = Sqrt(X)`

where
- `X`: input tensor containing real numbers.
- `Y`: output tensor where each element is the square root of the corresponding element in `X`.

#### Informal specification

The `Sqrt` operator computes the square root for each element of the input tensor `X`. Each element in the resulting tensor `Y` is the square root of the corresponding element in `X`.

The mathematical definition of the operator is given hereafter for an element $i$, covering all valid indexes of the tensor:

$$
Y[i] =
\begin{cases}
\sqrt{X[i]} & \text{if } X[i] \geq 0 \\
\text{undefined} & \text{if } X[i] < 0
\end{cases}
$$

The effect of the operator is illustrated on the following examples:
- `X` and `Y` are tensors holding numerical data.

Example 1:
```math
X = \begin{bmatrix}  1 & 4 & 9 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix}  1 & 2 & 3 \end{bmatrix}
```

Example 2:
```math
X =  \begin{bmatrix} 2.25 & 16 \\ 0.01 & 0.25 \\ 100 & 0 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix} 1.5 & 4 \\ 0.1 & 0.5 \\ 10 & 0 \end{bmatrix}
```

#### Inputs and outputs

##### `X`

Tensor `X` is the input tensor containing real numbers for which the square root needs to be computed.

###### Constraints

- (C1) Non-negative values
    - Statement: The tensor `X` must contain non-negative values. $X[i] \geq 0$ for all results $i$. `[R1]`
- (C2) Floating-point types
    - Statement: The tensor `X` must be of floating-point types. `[R3]`
- (C3) Shape consistency
    - Statement: Tensors `X`, `Y` must have the same shape. $N(X)=N(Y)$ `[R2]` and `[R4]`

##### `Y`

Tensor `Y` is the output tensor containing the computed square root values for each element in `X`.

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `Y` must be the same as `X`. $N(Y)=N(X)$ `[R2]` and `[R4]`

#### Attributes

The `Sqrt` operator does not require any attributes.

---
<a id="float"></a>
# `Sqrt` operator (FP16, FP32, FP64, BFLOAT16)

### Restrictions
The following restrictions apply to the `Sqrt` operator for the SONNX profile:
- The input tensor `X` must contain non-negative values, as the square root is undefined for negative values. For negative inputs, nan will be returned. `[R1]`
- Tensors `X`, `Y` must have the same shape. `[R2]`
- The input tensor `X` must be of floating-point types. `[R3]`
- No broadcasting is allowed for the tensor `X`. `[R4]`
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md)

### Signature

`Y = Sqrt(X)`

where
- `X`: input tensor containing real numbers.
- `Y`: output tensor where each element is the square root of the corresponding element in `X`.

#### Informal specification

The `Sqrt` operator computes the square root for each element of the input tensor `X`. Each element in the resulting tensor `Y` is the square root of the corresponding element in `X`.

The mathematical definition of the operator is given hereafter for an element $i$, covering all valid indexes of the tensor:

$$
Y[i] =
\begin{cases}
\sqrt{X[i]} & \text{if } X[i] \geq 0 \\
\text{nan} & \text{if } X[i] < 0
\end{cases}
$$

#### Examples

Example 1:
```math
X = \begin{bmatrix} 1 & 4 & 9 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix} 1 & 2 & 3 \end{bmatrix}
```

Example 2:
```math
X = \begin{bmatrix} 2.25 & -16 \\ 0 & 0.25 \\ 100 & -1 \end{bmatrix}
```
Result `Y` will be:
```math
Y = \begin{bmatrix} 1.5 & \text{nan} \\ 0 & 0.5 \\ 10 & \text{nan} \end{bmatrix}
```

Note in Python, this is equivalent to:
```python
>>> import numpy as np
np.sqrt([[2.25, -16], [0, 0.25], [100, -1]])
array([[ 1.5,  nan],
       [ 0. ,  0.5],
       [10. ,  nan]])
```

#### Inputs and outputs

##### `X`

Tensor `X` is the input tensor containing real numbers for which the square root needs to be computed.

###### Constraints

- (C1) Non-negative values
    - Statement: The tensor `X` must contain non-negative values. $X[i] \geq 0$ for all results $i$. For $X[i] < 0$, the result will be $\text{nan}$. `[R1]`
- (C2) Floating-point types
    - Statement: The tensor `X` must be of floating-point types. `[R3]`
- (C3) Shape consistency
    - Statement: Tensors `X`, `Y` must have the same shape. $N(X)=N(Y)$ `[R2]` and `[R4]`

##### `Y`

Tensor `Y` is the output tensor containing the computed square root values for each element in `X`.

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `Y` must be the same as `X`. $N(Y)=N(X)$ `[R2]` and `[R4]`

#### Attributes

The `Sqrt` operator does not require any attributes.

### Formal specification

The formal specification of the `Sqrt` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
use int.Int
use real.Real
use array.Array

type tensor = {
  data: array real;
  dims: array int;
}

function size (t: tensor) : int =
  product t.dims 0
  where rec product (a: array int) (i: int) : int =
    if i = length a then 1 else a[i] * product a (i + 1)

predicate same_dimensions (dims1: array int) (dims2: array int) : bool =
  length dims1 = length dims2 /\ (forall i. dims1[i] = dims2[i])

predicate sqrt_result (X: tensor) (Y: tensor) (i: int) =
  (X.data[i] >= 0 -> Y.data[i] = sqrt X.data[i])
  /\ (X.data[i] < 0 -> Y.data[i] = nan)

val sqrt (X: tensor): tensor
  requires { forall i. X.data[i] >= 0 }
  requires { same_dimensions X.dims X.dims }
  ensures { same_dimensions result.dims X.dims }
  ensures { length result.data = size X }
  ensures { forall i. sqrt_result X result i }
```

[^1]: See [Why3 documentation](https://www.why3.org/)