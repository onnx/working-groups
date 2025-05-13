# Contents
- `Log` [operator (real)](#real)
- `Log` [operator (FP16, FP32, FP64, BFLOAT16)](#float)



<a id="real"></a>
# `Log` operator (real)

### Restrictions
The following restrictions apply to the `Log` operator for the SONNX profile:
- The input tensor `X` must contain only positive values, as the logarithm is undefined for non-positive values. `[R1]`
- Tensors `X`, `Y` must have the same shape.  `[R2]`
- The input tensor `X` must be of floating-point types. `[R3]`
- No broadcasting is allowed for the tensor `X`. `[R4]`

- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md) 

### Signature

`Y = Log(X)`

where
- `X`: input tensor containing real numbers.
- `Y`: output tensor where each element is the natural logarithm of the corresponding element in `X`.

#### Informal specification

The `Log` operator computes the natural logarithm for each element of the input tensor `X`. Each element in the resulting tensor `Y` is the natural logarithm of the corresponding element in `X`.

The mathematical definition of the operator is given hereafter for an element $i$, covering all valid indexes of the tensor:

$$
Y[i] =
\begin{cases}
\log(X[i]) & \text{if } X[i] > 0 \\
\text{undefined} & \text{if } X[i] <= 0
\end{cases}
$$

The effect of the operator is illustrated on the following examples:
- `X` and `Y` are tensors holding numerical data

Example 1:
```math
X = \begin{bmatrix}  1 & 2 & 4 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix}  0 & 0.693147 & 1.386294 \end{bmatrix}
```

Example 2:
```math
X =  \begin{bmatrix} 2.718 & 7.389 \\ 0.01 & 0.1 \\ 10 & 1000 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix} 0.999896 & \text{1.999992} \\ \text{-4.605170} & -2.302585 \\ 2.302585 & \text{6.907755} \end{bmatrix}
```


#### Inputs and outputs

##### `X`

Tensor `X` is the input tensor containing real numbers for which the natural logarithm needs to be computed.

###### Constraints

- (C1) Positive values
    - Statement: The tensor `X` must contain only positive values. $X[i] > 0$ for all non-zero results $i$. `[R1]`
- (C2) Floating-point types
    - Statement: The tensor `X` must be of floating-point types. `[R3]`
- (C3) Shape consistency
    - Statement: Tensors `X`, `Y` must have the same shape. $N(X)=N(Y)$ `[R2]` and `[R4]` 

##### `Y`

Tensor `Y` is the output tensor containing the computed logarithmic values for each element in `X`.

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `Y` must be the same as `X`. $N(Y)=N(X)$ `[R2]` and `[R4]`

#### Attributes

The `Log` operator does not require any attributes.






---
<a id="float"></a>
# `Log` operator (FP16, FP32, FP64, BFLOAT16)

### Restrictions
The following restrictions apply to the `Log` operator for the SONNX profile:
- The input tensor `X` must contain only positive values, as the logarithm is undefined for non-positive values. But nan or inf will be return otherwise`[R1]`
- Tensors `X`, `Y` must have the same shape.  `[R2]`
- The input tensor `X` must be of floating-point types. `[R3]`
- No broadcasting is allowed for the tensor `X`. `[R4]`
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md) 

### Signature

`Y = Log(X)`

where
- `X`: input tensor containing real numbers.
- `Y`: output tensor where each element is the natural logarithm of the corresponding element in `X`.

#### Informal specification

The `Log` operator computes the natural logarithm for each element of the input tensor `X`. Each element in the resulting tensor `Y` is the natural logarithm of the corresponding element in `X`.

The mathematical definition of the operator is given hereafter for an element $i$, covering all valid indexes of the tensor:

$$
Y[i] =
\begin{cases}
\log(X[i]) & \text{if } X[i] > 0 \\
\text{-inf} & \text{if } X[i] = 0 \\
\text{nan} & \text{if } X[i] < 0
\end{cases}
$$


#### Examples

Example 1:
```math
X = \begin{bmatrix}  1 & 2 & 4 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix}  0 & 0.693147 & 1.386294 \end{bmatrix}
```

Example 2:
```math
X =  \begin{bmatrix} 2.718 & -7.389 \\ 0 & 0.1 \\ 10 & -1000 \end{bmatrix}
```
Result `Y` will be:
```math
Y =  \begin{bmatrix} 0.999896 & \text{nan} \\ \text{inf} & -2.302585 \\ 2.302585 & \text{nan} \end{bmatrix}
```

Note in Python, this is equivalent to:
```python
>>> import numpy as np
np.log([[2.718, -7.389], [0, 0.1], [10, -1000]])
array([[ 0.99989632,         nan],
       [       -inf, -2.30258509],
       [ 2.30258509,         nan]])
```

#### Inputs and outputs

##### `X`

Tensor `X` is the input tensor containing real numbers for which the natural logarithm needs to be computed.

###### Constraints

- (C1) Positive values
    - Statement: The tensor `X` must contain only positive values. $X[i] > 0$ for all non-zero results $i$. For $X[i] = 0$ or $X[i] < 0$, the result will be $\text{inf}$ or $\text{nan}$, respectively. `[R1]`
- (C2) Floating-point types
    - Statement: The tensor `X` must be of floating-point types. `[R3]`
- (C3) Shape consistency
    - Statement: Tensors `X`, `Y` must have the same shape. $N(X)=N(Y)$ `[R2]` and `[R4]` 

##### `Y`

Tensor `Y` is the output tensor containing the computed logarithmic values for each element in `X`.

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `Y` must be the same as `X`. $N(Y)=N(X)$ `[R2]` and `[R4]`

#### Attributes

The `Log` operator does not require any attributes.

### Formal specification

The formal specification of the `Log` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(** 
    Specification of Log operation on tensors.
 *)
module Log
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Log
  let function log (a : tensor real) : tensor real =
    ensures { 
      forall i. if a.value[i] > 0.0 then result.value[i] = log a.value[i]
                else if a.value[i] = 0.0 then result.value[i] = -infinity
                else result.value[i] = nan 
    }
  {
    shape = a.shape ;
    value = fun i -> if a.value[i] > 0.0 then log a.value[i]
                     else if a.value[i] = 0.0 then -infinity
                     else nan ;
  }
end
```

[^1]: See [Why3 documentation](https://www.why3.org/)
