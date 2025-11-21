# Contents
- `Tanh` [operator (real)](#real)
- `Tanh` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `Tanh` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)

<a id="real"></a>
# `Tanh` operator (real)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

The shape of tensor `A` is $(m \times n)$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Tanh(X)`
where
- `X`: input tensor
- `Y`: output tensor
  
#### Informal specification

Operator `Tanh` computes the Tanh function.

The mathematical definition of the operator is given hereafter.

$$     
   Y = \frac{e^x-e^{-x}}{e^x+e^{-x}} = \frac{e^{2x}-1}{e^{2x}+1} = \frac{1 - e^{-2x}}{1 + e^{-2x}}
$$


<a id="float"></a>
# `Tanh` operator (real)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Tanh(X)`
where
- `X`: input tensor
- `Y`: output tensor

### Algorithm
Tanh is subject to exponent overflow for great negative values of `X`.
To remain stable, the algorithm shall split the `X` domain to only compute negative exponent.

```
if X < 0
    Y = (exp(2x) - 1) / (exp(2x) + 1)
else
    Y = (1 - exp(-2x)) / (1 + exp(-2x))
```

### Formal specification

The formal specification of the `Tanh` operator using the Why3 language is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Tanh operation on tensors with real numbers.
 *)
module Tanh
  use int.Int
  use map.Map
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Exp
  (** Define the tanh function with piecewise conditions *)
  let function tanh (x : real) : real =
    ensures {
      if x < 0.0 then result = (exp(2.0 * x) - 1.0) / (exp(2.0 * x) + 1.0) 
      else result = (1.0 - exp(-2.0 * x)) / (1.0 + exp(-2.0 * x))
    }
  {
    if x < 0.0 then (exp(2.0 * x) - 1.0) / (exp(2.0 * x) + 1.0)
    else (1.0 - exp(-2.0 * x)) / (1.0 + exp(-2.0 * x))
  }
  (** Define the tanh operation on a tensor **)
  let function tanh_tensor (a : tensor real) : tensor real =
    ensures { forall i. result.value[i] = tanh (a.value[i]) }
  {
    shape = a.shape ;
    value = fun i -> tanh (a.value[i]) ;
  }
end
```




<a id="int"></a>
