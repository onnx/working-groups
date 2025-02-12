# Preliminary remarks

## Types

- Operators are initially described for values in the domain of real numbers. The `Pow` operator computes the element-wise power operation, where each element of the output tensor is derived by raising the corresponding element in the first input tensor `A` to the power given by the corresponding element in the second input tensor `B`. The outputs and inputs `A` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int32)`, `tensor(int64)`. The exponent of the power `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`.
 The dimension size of a tensor is defined by $N(tensor)$.

# `Pow` operator

### Restrictions

The following restrictions apply to the `Pow` operator for the SONNX profile:
- The input tensors `A` and `B` and output must have the same shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements in `A` and `B` must be of types that support the power operation `[R3]`
- No broadcasting allowed for the tensors `A` and `B` even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic `[R4]`
- All input `A` and output element shall be of the same type (not possible to mix integer and real) `[R5]`
- All `B` element of the exponent shall be of the same type (it is not possible to mix integer and real) `[R6]`

### Signature

`C = Pow(A, B)`

where
- `A`: input tensor, base of the power operation
- `B`: input tensor, exponent of the power operation
- `C`: output tensor resulting from the element-wise power operation on `A` and `B`

#### Informal specification

The `Pow` operator computes the power operation element-wise for two input tensors `A` and `B`. Each element in the resulting tensor `C` is calculated by raising the corresponding element in `A` to the power specified by the corresponding element in `B`.

The mathematical definition of the operator is given hereafter.

$$
C[i] = A[i]^{B[i]}
$$

Where
- $i$ is an index covering all dimensions of the tensors.

The effect of the operator is illustrated on the following examples:

Example 1:
```math
`A` = \begin{bmatrix}  2 & 3 & 7 \end{bmatrix}
```
```math
`B` = \begin{bmatrix}  3 & 2 & 1 \end{bmatrix}
```
Result `C` will be:
```math
`C` =  \begin{bmatrix} 8 & 9 & 7 \end{bmatrix}
```

Example 2:
```math
`A` =  \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```
```math
`B` = \begin{bmatrix} 3 & 2 \\ 1 & 4 \\ 2 & 2 \end{bmatrix}
```
Result `C` will be:
```math
`C` =  \begin{bmatrix} 1 & 4 \\ 4 & 0 \\ 25 & 36 \end{bmatrix}
```

Note in python is is equivalent to do :
```python
>>> import numpy as np
np.power([[1,2],[4,0],[5,6]],[[3,2],[1,4],[2,2]])
array([[  1,   4],
       [  4,   0],
       [ 25,  36]])
```

#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors for the power calculation.

The shape of tensor `A` should be the same as `B`. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

##### `B`

Tensor `B` is the other input tensor for the power calculation.

The shape of tensor `B` should be the same as `A`. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise power calculation of `A` and `B`.

`C` will have the resulting shape of `A` and `B`, and must be the same. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the `A` and `B` shape. $N(C)=N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Attributes

The `Pow` operator does not require any attributes.

### Formal specification

The formal specification of the `Pow` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

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

predicate pow_result (A: tensor) (B: tensor) (C: tensor) (i: int) =
  C.data[i] = A.data[i] ^ B.data[i]

val pow (A: tensor) (B: tensor): tensor
  requires { same_dimensions A.dims B.dims }
  ensures { C.dims = A.dims }
  ensures { length C.data = size C }
  ensures { forall i. pow_result A B C i }
```

[^1]: See [Why3 documentation](https://www.why3.org/)