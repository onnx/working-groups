# Preliminary remarks

## Types

- Operators are first described for values in the domain of real numbers. Because the `Abs` operator outputs a tensor representing the element-wise absolute value of values in an input tensor, the output is of the same type as the input tensor `X`. The input `X` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.

# `Abs` operator

### Restrictions

The following restrictions apply to the `Abs` operator for the ONNX profile:
- The tensor `X` must have a valid numeric type `[R1]`
- The operator does not support sparse tensors `[R2]`
- All input elements `X` shall have explicit numerical types `[R3]`
- No broadcasting allowed for the tensors `X` and `Y` even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic `[R4]`

### Signature

`Y = Abs(X)`

where
- `X`: input tensor whose element-wise absolute values are to be computed
- `Y`: output tensor based on element-wise absolute values of `X`

#### Informal specification

The `Abs` operator performs element-wise absolute value computation of the input tensor `X`. For each element, the corresponding entry in `Y` contains the absolute value of the corresponding entry in `X`.

The mathematical definition of the operator is given hereafter.

$$
Y[i] = |X[i]|
$$

Where
- $i$ is an index covering all dimensions of the tensor.

The effect of the operator is illustrated on the following examples:
- `X` is a tensor holding numerical data

Example 1:
```math
`X` = \begin{bmatrix} -2 & 3 & -7 \end{bmatrix}
```
Result `Y` will be:
```math
`Y` = \begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
```

Example 2:
```math
`X` = \begin{bmatrix} -1 & 0 \\ 4 & -5 \\ 2 & -3 \end{bmatrix}
```
Result `Y` will be:
```math
`Y` = \begin{bmatrix} 1 & 0 \\ 4 & 5 \\ 2 & 3 \end{bmatrix}
```

Note in Python it is equivalent to do:
```python
>>> import numpy as np
np.abs([[-1, 2], [0, -4], [8, -3]])
array([[1, 2],
       [0, 4],
       [8, 3]])
```

#### Inputs and outputs

##### `X`

The shape of tensor `X` should be the same as `Y`. `[R2]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `X` shall be the same than `Y`. $N(X)=N(Y)$ `[R2]` & `[R4]`.

#### Outputs

##### `Y`

Tensor `Y` is the output tensor formed by element-wise computation of the absolute values of `X`.

`Y` will have the same shape as `X`. `[R2]`

###### Constraints

- (C1) Shape consistency
    - Statement: The shape of `Y` shall be the same than `X`. $N(Y)=N(X)$ `[R2]` & `[R4]`.

#### Attributes

The `Abs` operator does not require any attributes.

### Formal specification

The formal specification of the `Abs` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Abs operation on tensors.
 *)

module Abs
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor

  let function abs (a : tensor 'a) : tensor 'a =
  {
    shape = a.shape ;
    value = fun i -> if a.value[i] < 0 then -a.value[i] else a.value[i] ;
  }

end
```

[^1]: See [Why3 documentation](https://www.why3.org/)

### Numerical Accuracy

If tensor $X_{err}$ is the numerical error of `X`, let us consider $Y_{err}^{propag}$ the
propagated error of `Abs` and `Y` and $Y_{err}^{intro}$ the introduced error of `Abs`.
Hence the numerical error of `Y`, $Y_{err} = Y_{err}^{propag} + Y_{err}^{intro}$.

#### Error propagation

For every index $i$, 

- $Y_{err}^{propag}[i] = X_{err}[i]$ if $X[i] \geq 0$ and $X[i]+X_{err}[i] \geq 0$  
- $Y_{err}^{propag}[i] = -X_{err}[i]$ if $X[i] \leq 0$ and $X[i]+X_{err}[i] \leq 0$ 
- $Y_{err}^{propag}[i] \leq |X_{err}[i]|$ if $X[i]$ and $X[i]+X_{err}[i]$ may not have the same sign

#### Error introduction

The `Abs` operation should not introduce any error: $Y_{err}^{intro} = [0]$.

#### Unit verification

A symbolic inference of the error over the tensor components should ensure the
above properties.

```c++
Tensor<SymbolicDomainError> X;

/* X symbolic initialization */

template <typename TypeFloat>
std::function<TypeFloat (int64_t)> result = [&X](int64_t index) {
  return (a.value()[index] < 0) ? -a.value()[index] : a.value()[index];
}

for (int i = 0; i < x.NumElements(); ++i) {
   SymbolicDomainError x = X.value(i);
   SymbolicDomainError y = result(i);
   if (x.value >= 0 && x.value+x.err >= 0)
      assert(y.err == x.err);
   if (x.value <= 0 && x.value+x.err <= 0)
      assert(y.err == -x.err);
   if (x.value >= 0 && x.value+x.err <= 0)
      assert(std::abs(y.err) <= std::abs(x.err));
   if (x.value <= 0 && x.value+x.err >= 0)
      assert(std::abs(y.err) <= std::abs(x.err));
}
```
