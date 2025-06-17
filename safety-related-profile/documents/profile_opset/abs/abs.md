
# `Abs` operator (all numerical types)

## Restrictions

## Restrictions
The following restrictions apply to the `conv` operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input and output tensors shall have the same shape | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |


## Signature

`Y = Abs(X)`

where
- `X`: input tensor 
- `Y`: output tensor

## Documentation

The `Abs` operator computes the element-wise absolute value of the input tensor `X`.

The mathematical definition of the operator is given hereafter.

$$
Y[i_0,i_1,...,i_n] = |X[i_0,i_1,...,i_n]|
$$

Where
- $i_j$ is the index for dimension $j$.

The effect of the operator is illustrated on the following examples:
- `X` is a tensor holding numerical data

Example 1:
```math
X = \begin{bmatrix} -2.1 & 3.4 & -7 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 2.1 & 3.4 & 7 \end{bmatrix}
```

Example 2:
```math
X = \begin{bmatrix} -1.123 & 0 \\ 4 & -5 \\ 2 & -3 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 1.123 & 0 \\ 4 & 5 \\ 2 & 3 \end{bmatrix}
```

Note in Python it is equivalent to do:
```python
>>> import numpy as np
np.abs([[-1, 2], [0, -4], [8, -3]])
array([[1, 2],
       [0, 4],
       [8, 3]])
```

## Inputs

### `X`

#### Constraints

- (C1)  <a name="shape_consist"></a> Shape consistency
    - Statement: `X` and `Y` shall have the same shape. $ `[R1]`.

## Outputs

### `Y`

#### Constraints

- (C1) Shape consistency
    - Statement: See [constraint (C1) on X](#shape_consist) .

## Attributes

The `Abs` operator has no attribute.

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

If tensor $X_{\textit{err}}$ is the numerical error of `X`, let us consider
$Y_{\textit{err}}^{\textit{propag}}$ the propagated error of `Abs` and `Y`
and $Y_{\textit{err}}^{\textit{intro}}$ the introduced error of `Abs`.
Hence the numerical error of `Y`, $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

#### Error propagation

For every index $i$, 

- $Y_{\textit{err}}^{\textit{propag}}[i] = X_{\textit{err}}[i]$ if $X[i] \geq 0$
  and $X[i]+X_{\textit{err}}[i] \geq 0$  
- $Y_{\textit{err}}^{\textit{propag}}[i] = -X_{\textit{err}}[i]$ if $X[i] \leq 0$
  and $X[i]+X_{\textit{err}}[i] \leq 0$ 
- $Y_{\textit{err}}^{\textit{propag}}[i] \leq |X_{\textit{err}}[i]|$ if $X[i]$
  and $X[i]+X_{\textit{err}}[i]$ may not have the same sign

#### Error introduction

The `Abs` operation should not introduce any error: $Y_{\textit{err}}^{\textit{intro}} = [0]$.

#### Unit verification

A symbolic inference of the error over the tensor components should ensure the
above properties.

```c++
Tensor<SymbolicDomainError> X;

/* X symbolic initialization */

template <typename TypeFloat>
std::function<TypeFloat (int64_t)> result = [&X](int64_t index) {
  return (X.value()[index] < 0) ? -X.value()[index] : X.value()[index];
}

for (int i = 0; i < x.NumElements(); ++i) {
   SymbolicDomainError x = X.value(i);
   SymbolicDomainError y = result(i);
   if (x.real >= 0 && x.real+x.err >= 0)
      assert(y.err == x.err);
   if (x.real <= 0 && x.real+x.err <= 0)
      assert(y.err == -x.err);
   if (x.real >= 0 && x.real+x.err <= 0)
      assert(std::abs(y.err) <= std::abs(x.err));
   if (x.real <= 0 && x.real+x.err >= 0)
      assert(std::abs(y.err) <= std::abs(x.err));
}
```

