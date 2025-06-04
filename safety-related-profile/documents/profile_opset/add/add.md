# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Add` operator outputs a tensor representing the element-wise addition of values in input tensors, the output is of the same type as the input tensors `A` and `B`. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Add` operator

### Restrictions

The following restrictions apply to the `Add` operator for the SONNX profile:
- The tensors `A` and `B` must have the same shape or be broadcastable to a common shape `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `A` and `B` shall have explicit additive types `[R3]`

### Signature

`C = Add(A, B)`

where
- `A`: input tensor to be added
- `B`: input tensor to be added with `A`
- `C`: output tensor based on element-wise addition of `A` and `B`

#### Informal specification

The `Add` operator performs element-wise addition of two input tensors `A` and `B`. For each element, the corresponding entry in `C` contains the sum of the corresponding entries in `A` and `B`.

The mathematical definition of the operator is given hereafter.

$$
C[i] = A[i] + B[i]
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
`C` = \begin{bmatrix} 5 & 6 & 12 \end{bmatrix}
```

Example 2:
```math
`A` = \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```
```math
`B` = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```
Result `C` will be:
```math
`C` = \begin{bmatrix} 4 & 4 \\ 8 & 1 \\ 10 & 10 \end{bmatrix}
```

Note in Python it is equivalent to do:
```python
>>> import numpy as np
np.add([[1,2],[0,1],[8,0]],[[0,5],[0,8],[8,7]])
array([[ 1,  7],
       [ 0,  9],
       [16,  7]])
```

#### Inputs and outputs

##### `A`

Tensor `A` is one of the two input tensors to be added.

The shape of tensor `A` should be the same as `B` or broadcastable to a common shape. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` shall be compatible for broadcasting. $N(A)$ must be compatible with $N(B)$ `[R1]`.

##### `B`

Tensor `B` is the other input tensor for the addition.

The shape of tensor `B` should be the same as `A` or broadcastable to a common shape. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shapes of `A` and `B` shall be compatible for broadcasting. $N(B)$ must be compatible with $N(A)$ `[R1]`.

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise addition of `A` and `B`.

`C` will have the resulting shape of the broadcasted shape of `A` and `B`. `[R1]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `C` will match the resultant broadcasted shape of `A` and `B`. $N(C)$ will match the broadcasted shape of $N(A)$ and $N(B)$ `[R1]`.

#### Attributes

The `Add` operator does not require any attributes.

### Formal specification

The formal specification of the `Add` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Add operation on tensors.
 *)

module Add
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor

  let function add (a b : tensor 'a) : tensor 'a =
  {
    shape = same a.shape b.shape ;
    value = fun i -> a.value[i] + b.value[i] ;
  }

end
```

[^1]: See [Why3 documentation](https://www.why3.org/)

### Numerical Accuracy

If tensor $A_{\textit{err}}$ is the numerical error of `A`,
tensor $B_{\textit{err}}$ is the numerical error of `B`, let us consider
$Y_{\textit{err}}^{\textit{propag}}$ the propagated error of `Add` and `C`
and $C_{\textit{err}}^{\textit{intro}}$ the introduced error of `Add`.
Hence the numerical error of `C`, $C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

#### Error propagation

For every index $i$, 

- $C_{\textit{err}}^{\textit{propag}}[i] = A_{\textit{err}}[i] + B_{\textit{err}}[i]$

#### Error introduction

The `Add` operation introduces an error bound by the semi-ulp of the addition result for every
tensor component. For a hardware providing $m$ bits for floating-point mantissa, the semi-ulp
of `1.0` is $2^{-(m+1)}$. Hence, for every index $i$,

- $C_{\textit{err}}^{\textit{intro}}[i] \leq (A[i] + B[i] + A_{\textit{err}}[i] + B_{\textit{err}}[i])\times(1.0 + 2^{-(m+1)})$

#### Unit verification

A symbolic inference of the error over the tensor components should ensure the
above properties.

```c++
Tensor<SymbolicDomainError> A, B;

/* X symbolic initialization */

template <typename TypeFloat>
std::function<TypeFloat (int64_t)> result = [&A, &B](int64_t index) {
  return A.value()[index] + B.value()[index];
}

for (int i = 0; i < x.NumElements(); ++i) {
   SymbolicDomainError a = A.value(i);
   SymbolicDomainError b = B.value(i);
   SymbolicDomainError c = result(i);
   assert(std::abs(c.err - a.err - b.err) <= std::abs(a.real + b.real + a.err + b.err)*(1.0LD + pow(2.0LD, -(m+1))));
}
```

