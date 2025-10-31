# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Less` operator outputs a boolean tensor representing the comparison of each element in input tensors, the output is of type `tensor(bool)`. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Less` operator

### Restrictions

The following restrictions apply to the `Less` operator for the SONNX profile:
- The tensors `A` and `B` must have the same shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `A` and `B` shall have explicit comparable types `[R3]`
- No broadcasting allowed for the tensors `A` and `B` even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic `[R4]`

### Signature

`C = Less(A, B)`

where
- `A`: input tensor to compare
- `B`: input tensor to compare with `A`
- `C`: output boolean tensor based on element-wise comparison of `A` and `B`

#### Informal specification

The `Less` operator compares two input tensors `A` and `B` element-wise. For each element, if the corresponding entry in `A` is strictly less than the corresponding entry in `B`, the resulting tensor `C` contains the value `True`. Otherwise, the resulting tensor `C` contains the value `False`.

The mathematical definition of the operator is given hereafter.

$$
C[i] = 
\begin{cases} 
\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}
\end{cases}
$$

Where
- $i$ is an index covering all dimensions of the tensors.

The effect of the operator is illustrated on the following examples :
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
`C` =  \begin{bmatrix} \text{True} & \text{False} & \text{False} \end{bmatrix}
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
`C` =  \begin{bmatrix} \text{True} & \text{False} \\ \text{False} & \text{True} \\ \text{False} & \text{False} \end{bmatrix}
```

Note in python is is equivalent to do :
```python
>>> import numpy as np
np.less([[1,2],[0,1],[8,0]],[[2,0],[0,4],[8,4]])
array([[ True, False],
       [False,  True],
       [False,  True]])
```


#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors to be compared.

The shape of tensor `A` should be the same as `B`. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

##### `B`

Tensor `B` is the other input tensor for the comparison.

The shape of tensor `B` should be the same as `A`. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` must be the same. $N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise comparison of `A` and `B`.

`C` will have the resulting shape of `A` and `B` and must be the same. `[R1]` Broadcastable tensor is forbidden.`[R4]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the `A` and `B` shape. $N(C)=N(A)=N(B)$ `[R1]` Broadcastable tensor is forbidden.`[R4]`.

#### Attributes

The `Less` operator does not require any attributes.

### Formal specification

The formal specification of the `Less` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Less operation on tensors.
 *)

module Less
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor

  let function less (a b : tensor 'a) : tensor 'a =
  {
    shape = same a.shape b.shape ;
    value = fun i -> a.value[i] < b.value[i] ;
  }

end
```


[^1]: See [Why3 documentation](https://www.why3.org/)
