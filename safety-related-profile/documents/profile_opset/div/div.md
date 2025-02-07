# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Div` operator divides each element in the input tensors element-wise, the output is of the same data type as the inputs. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Div` operator

### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:
- The tensors `A` and `B` must have the same shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `A` and `B` shall have numerical types `[R3]`
- No broadcasting allowed for the tensors `A` and `B` even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic `[R4]`
- if Elements of tensor `B` is zero, as division by zero is not valid the nemeric result will be infinite representation. `[R5]`

### Signature

`C = Div(A, B)`

where
- `A`: input tensor to be divided
- `B`: input tensor to divide `A` by
- `C`: output tensor based on element-wise division of `A` by `B`

#### Informal specification

The `Div` operator divides two input tensors `A` and `B` element-wise. For each element, the corresponding entry in `A` is divided by the corresponding entry in `B`, and the resulting tensor `C` contains the result of these divisions.

The mathematical definition of the operator is given hereafter.

$$
C[i] = 
\begin{cases} 
\frac{A[i]}{B[i]} & \text{if } B[i] & \text{is different of 0.0} \\
inf & \text{otherwise}
\end{cases}
$$

Where
- $i$ is an index covering all dimensions of the tensors.

The effect of the operator is illustrated on the following examples:
- `A` and `B` are tensors holding numerical data

Example 1:
```math
`A` = \begin{bmatrix}  6 & 9 & 35 \end{bmatrix}
```
```math
`B` = \begin{bmatrix}  3 & 3 & 5 \end{bmatrix}
```
Result `C` will be: 
```math
`C` =  \begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
```

Example 2:
```math
`A` =  \begin{bmatrix} 3 & 4 \\ 16 & 0 \\ 25 & 24 \end{bmatrix}
```
```math
`B` =  \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```
Result `C` will be:
```math
`C` =  \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```

Note in python it is equivalent to do :
```python
>>> import numpy as np
np.divide([[1,3],[5,7],[9,12]],[[11,22],[33,-44],[-55,66]])
array([[ 0.09090909,  0.13636364],
       [ 0.15151515, -0.15909091],
       [-0.16363636,  0.18181818]])

## with a division by 0
np.divide([[6,9,35]],[[3,3,0]])
array([[ 2.,  3., inf]])
```

#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors to be divided.

The shape of tensor `A` should be the same as `B`. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`

##### `B`

Tensor `B` is the other input tensor for the division.

The shape of tensor `B` should be the same as `A`. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`
- (C2) No zero elements for defined division
    - Statement: All elements of tensor `B` must be non-zero to avoid division by zero. $\forall B[i] \neq 0$ else the result will be inf `[R5]`

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise division of `A` by `B`.

`C` will have the resulting shape of `A` and `B` and must be the same. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the `A` and `B` shape. $N(C)=N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`

#### Attributes

The `Div` operator does not require any attributes.

### Formal specification

The formal specification of the `Div` operator using the Why3 language is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

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

predicate div_result (A: tensor, B: tensor, C: tensor, i: int) =
  B.data[i] <> 0 /\
  C.data[i] = A.data[i] / B.data[i]

val div (A: tensor, B: tensor): tensor
  requires { same_dimensions A.dims B.dims }
  ensures { C.dims = A.dims }
  ensures { length C.data = size C }
  ensures { forall i. div_result A B C i }
```