# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Neg` operator outputs a tensor representing the negation of each element in the input tensor, the output is of the same type as the input tensor. The input `A` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Neg` operator

### Restrictions

The following restrictions apply to the `Neg` operator for the SONNX profile:
- The tensor `A` must have a defined shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All elements of input `A` shall have explicit numeric types `[R3]`
- No broadcasting is allowed for the tensor `A` `[R4]`

### Signature

`B = Neg(A)`

where
- `A`: input tensor to be negated
- `B`: output tensor containing the negated values of `A`

#### Informal specification

The `Neg` operator computes the negation of each element in the input tensor `A`. For each element, the resulting tensor `B` contains the value that is the negation of the corresponding entry in `A`.

The mathematical definition of the operator is given hereafter.

$$
B[i] = -A[i]
$$

Where
- $i$ is an index covering all dimensions of the tensor.

The effect of the operator is illustrated on the following examples :
- `A` is a tensor holding numerical data

Example 1:
```math
`A` = \begin{bmatrix}  2 & -3 & 7 \end{bmatrix}
```
Result `B` will be: 
```math
`B` =  \begin{bmatrix} -2 & 3 & -7 \end{bmatrix}
```

Example 2:
```math
`A` =  \begin{bmatrix} 1 & -2 \\ 4 & 0 \\ -5 & 6 \end{bmatrix}
```
Result `B` will be:
```math
`B` =  \begin{bmatrix} -1 & 2 \\ -4 & 0 \\ 5 & -6 \end{bmatrix}
```

Note in python is is equivalent to do :
```python
>>> import numpy as np
np.negative([[1,-2],[0,-4],[-8,4]])
array([[-1,  2],
       [ 0,  4],
       [ 8, -4]])
```


#### Inputs and outputs

##### `A`

Tensor `A` is the input tensor to be negated.

The shape of tensor `A` should be predefined and cannot be broadcasted `[R1]` `[R4]`.

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `A` must be predefined. `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Outputs

##### `B`

Tensor `B` is the output tensor formed by element-wise negation of `A`.

`B` will have the same shape as `A`. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `B` will match the `A` shape. $N(B)=N(A)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Attributes

The `Neg` operator does not require any attributes.

### Formal specification

The formal specification of the `Neg` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
use int.Int
use bool.Bool
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

predicate neg_result (A: tensor) (B: tensor) (i: int) =
  B.data[i] = -A.data[i]

val neg (A: tensor): tensor
  requires { same_dimensions A.dims A.dims }
  ensures { B.dims = A.dims }
  ensures { length B.data = size B }
  ensures { forall i. neg_result A B i }
```

[^1]: See [Why3 documentation](https://www.why3.org/)