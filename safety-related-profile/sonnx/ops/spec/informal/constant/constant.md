# Preliminary remarks

## Types

- The `Constant` operator produces a constant tensor, which can be of various data types. The supported types for the constant value include `tensor(bfloat16)`, `tensor(bool)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size for the tensor is defined by $N(tensor)$.

# `Constant` operator

### Restrictions

The following restrictions apply to the `Constant` operator for the ONNX profile:
- The operator must have a defined constant value through the attribute `value` `[R1]`
- The operator does not support sparse tensors `[R2]`
- all element of the attribut shall be of the same type `[R3]`

### Signature

`C = Constant(value)` with a fixed value attribut

where
- `C`: output tensor containing the constant value

#### Informal specification

The `Constant` operator generates a tensor that contains a constant value. The value of the tensor is specified by an attribute `value`, which determines both the type and value of the output tensor. The output tensor can be of any shape and data type, as long as they are consistent with the provided `value`.

The mathematical definition of the operator is given hereafter.

$$
C = value
$$

##### Example 1:
```math
\text{value} = 4.5
```
Result `C` will be:
```math
`C` = \begin{bmatrix} 4.5 \end{bmatrix}
```

##### Example 2:
```math
\text{value} = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
```
Result `C` will be:
```math
`C` = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
```

#### Inputs and outputs

##### `C`

Tensor `C` is the output tensor containing the provided constant value.

The shape of tensor `C` and its type are determined by the attribute `value`. `[R1]` & `[R2]` & `[R3]`

###### Constraints

- (C1) Value consistency
    - Statement: The shape and type of `C` are determined by the attribute `value`. 

#### Attributes

##### `value`
- **Description:** The constant value to fill the output tensor.
- **Type:** Any supported tensor type : `tensor(bfloat16, bool, double, float, float16, int16, int32, int64, int8, string, uint16, uint32, uint64, uint8)`.
- **Requirement:** This attribute is required to define the constant value for the output tensor `[R1]`.

### Formal specification

The formal specification of the `Constant` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the described constraints.


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

predicate constant_result (X: tensor, Y: tensor, i: int) =
  Y.data[i] = X.data[i]

val check_constant (X: tensor): tensor
  requires { same_dimensions X.dims X.dims }
  ensures { Y.dims = X.dims }
  ensures { length Y.data = size X }
  ensures { forall i. constant_result X Y i }
```
[^1]: See [Why3 documentation](https://www.why3.org/)