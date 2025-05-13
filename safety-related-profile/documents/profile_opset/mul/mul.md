# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Mul` operator multiplies each element in the input tensors element-wise, the output is of the same data type as the inputs. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Mul` operator

### Restrictions

The following restrictions apply to the `Mul` operator for the SONNX profile:
- The tensors `A` and `B` must have the same shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `A` and `B` shall have numerical types `[R3]`
- No broadcasting allowed for the tensors `A` and `B` even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic `[R4]`

### Signature

`C = Mul(A, B)`

where
- `A`: input tensor to be multiplied
- `B`: input tensor to be multiplied with `A`
- `C`: output tensor based on element-wise multiplication of `A` and `B`

#### Informal specification

The `Mul` operator multiplies two input tensors `A` and `B` element-wise. For each element, the corresponding entry in `A` is multiplied by the corresponding entry in `B`, and the resulting tensor `C` contains the result of these multiplications.

The mathematical definition of the operator is given hereafter.

$$
C[i] = A[i] * B[i]
$$

Where
- $i$ is an index covering all dimensions of the tensors.

The effect of the operator is illustrated on the following examples:
- `A` and `B` are tensors holding numerical data

Example 1:
```math
`A` = \begin{bmatrix}  2 & 3 & 7 \end{bmatrix}
```
```math
`B` = \begin{bmatrix}  3 & 3 & 5 \end{bmatrix}
```
Result `C` will be: 
```math
`C` =  \begin{bmatrix} 6 & 9 & 35 \end{bmatrix}
```

Example 2:
```math
`A` =  \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```
```math
`B` =  \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```
Result `C` will be:
```math
`C` =  \begin{bmatrix} 3 & 4 \\ 16 & 0 \\ 25 & 24 \end{bmatrix}
```

Note in python it is equivalent to do :
```python
>>> import numpy as np
np.multiply([[2,1],[0,9],[5,6]],[[1,3],[0,6],[5,6]])
array([[ 2,  3],
       [ 0, 54],
       [25, 36]])
```

#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors to be multiplied.

The shape of tensor `A` should be the same as `B`. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`

##### `B`

Tensor `B` is the other input tensor for the multiplication.

The shape of tensor `B` should be the same as `A`. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise multiplication of `A` and `B`.

`C` will have the resulting shape of `A` and `B` and must be the same. `[R1]` Broadcastable tensor is forbidden. `[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the `A` and `B` shape. $N(C)=N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden. `[R4]`

#### Attributes

The `Mul` operator does not require any attributes.

### Formal specification

The formal specification of the `Mul` operator using the Why3 language is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Mul operation on tensors.
 *)

module Mul
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor

  let function mul (a b : tensor 'a) : tensor 'a =
  {
    shape = same a.shape b.shape ;
    value = fun i -> a.value[i] * b.value[i] ;
  }

end
```
