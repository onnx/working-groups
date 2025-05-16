# Contents
- `Sigmoid` [operator (real)](#real)
- `Sigmoid` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `Sigmoid` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)

<a id="real"></a>
# `Sigmoid` operator (real)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

The shape of tensor `A` is $(m \times n)$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Sigmoid(X)`
where
- `X`: input tensor
- `Y`: output tensor
  
#### Informal specification

Operator `Sigmoid` computes the sigmoid function.

The mathematical definition of the operator is given hereafter.

$$     
   Y = \frac{1}{1+e^{-x}} = \frac{e^x}{1+e^x}  
$$


<a id="float"></a>
# `Sigmoid` operator (float32, float64)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Sigmoid(X)`
where
- `X`: input tensor
- `Y`: output tensor

### Algorithm
Sigmoid is subject to exponent overflow for great negative values of `X`.
To remain stable, the algorithm shall split the `X` domain to only compute negative exponent.

```
if X < 0
    Y = exp(x)/(1+exp(x))
else
    Y = 1/(1+exp(-x))
```


### Formal specification

The formal specification of the `sigmoid` operator using the Why3 language is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Sigmoid operation on tensors with real numbers.
 *)
module SigmoidReal
  use int.Int
  use map.Map
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Exp
  (** Define the sigmoid function with piecewise conditions *)
  let function sigmoid (x : real) : real =
    ensures {
      if x < 0.0 then result = exp(x) / (1.0 + exp(x)) 
      else result = 1.0 / (1.0 + exp(-x))
    }
  {
    if x < 0.0 then exp(x) / (1.0 + exp(x))
    else 1.0 / (1.0 + exp(-x))
  }
  (** Define the sigmoid operation on a tensor **)
  let function sigmoid_tensor (a : tensor real) : tensor real =
    ensures { forall i. result.value[i] = sigmoid (a.value[i]) }
  {
    shape = a.shape ;
    value = fun i -> sigmoid (a.value[i]) ;
  }
end
```


<a id="int"></a>
