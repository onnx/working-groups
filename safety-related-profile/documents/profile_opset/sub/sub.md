# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Sub` operator outputs a tensor representing the element-wise subtraction of values in input tensors, the output is of the same type as the input tensors `A` and `B`. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Sub` operator

### Restrictions

The following restrictions apply to the `Sub` operator for the SONNX profile:
- The tensors `A` and `B` must have the same shape or be broadcastable to a common shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `A` and `B` shall have explicit subtractive types `[R3]`

### Signature

`C = Sub(A, B)`

where
- `A`: input tensor to be subtracted
- `B`: input tensor to be subtracted from `A`
- `C`: output tensor based on element-wise subtraction of `B` from `A`

#### Informal specification

The `Sub` operator performs element-wise subtraction of one input tensor `B` from another input tensor `A`. For each element, the corresponding entry in `C` contains the difference of the corresponding entries in `A` and `B`.

The mathematical definition of the operator is given hereafter.

$$
C[i] = A[i] - B[i]
$$

Where
- $i$ is an index covering all dimensions of the tensors.

The effect of the operator is illustrated on the following examples:
- `A` and `B` are tensors holding numerical data

Example 1:
```math
`A` = \begin{bmatrix} 4 & 7 & 10 \end{bmatrix}
```
```math
`B` = \begin{bmatrix} 1 & 5 & 3 \end{bmatrix}
```
Result `C` will be:
```math
`C` = \begin{bmatrix} 3 & 2 & 7 \end{bmatrix}
```

Example 2:
```math
`A` = \begin{bmatrix} 9 & 5 \\ 3 & 8 \\ 6 & 2 \end{bmatrix}
```
```math
`B` = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 1 \end{bmatrix}
```
Result `C` will be:
```math
`C` = \begin{bmatrix} 6 & 3 \\ -1 & 7 \\ 1 & 1 \end{bmatrix}
```

Note in Python it is equivalent to do:
```python
>>> import numpy as np
np.subtract([[1,2],[3,4],[5,6]],[[11,22],[33,-44],[-55,0]])
array([[-10, -20],
       [-30,  48],
       [ 60,   6]])
```

#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors and serves as the minuend in the subtraction.

The shape of tensor `A` should be the same as `B` or broadcastable to a common shape. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` shall be compatible for broadcasting. $N(A)$ must be compatible with $N(B)$ `[R1]`.

##### `B`

Tensor `B` is the other input tensor and serves as the subtrahend in the subtraction.

The shape of tensor `B` should be the same as `A` or broadcastable to a common shape. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` shall be compatible for broadcasting. $N(B)$ must be compatible with $N(A)$ `[R1]`.

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise subtraction of `B` from `A`.

`C` will have the resulting shape of the broadcasted shape of `A` and `B`. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the resultant broadcasted shape of `A` and `B`. $N(C)$ will match the broadcasted shape of $N(A)$ and $N(B)$ `[R1]`.

#### Attributes

The `Sub` operator does not require any attributes.

### Formal specification

The formal specification of the `Sub` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

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

predicate sub_result (A: tensor, B: tensor, C: tensor, i: int) =
  C.data[i] = A.data[i] - B.data[i]

val sub (A: tensor, B: tensor): tensor
  requires { same_dimensions A.dims B.dims }
  ensures { C.dims = A.dims }
  ensures { length C.data = size C }
  ensures { forall i. sub_result A B C i }
```

[^1]: See [Why3 documentation](https://www.why3.org/)
