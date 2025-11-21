# Contents
- `Exp` [operator (real)](#real)
- `Exp` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `Exp` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)

<a id="real"></a>
# `Exp` operator (real)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

The shape of tensor `A` is $(m \times n)$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Exp(X)`
where
- `X`: input tensor
- `Y`: output tensor
  
#### Informal specification

Operator `Exp` computes the Exp function element-wise.

The mathematical definition of the operator is given hereafter.

$$     
   Y = e^X
$$


<a id="float"></a>
# `Exp` operator (real)

#### Inputs and outputs

##### `X`

Tensor `X` is the first input tensor.

*FP16*: the input range for non +Inf values of `Y` is defined by $[-65500.0, \ln(65500.0)] = [-65500.0, 11.09]$.

*FP32*: the input range for non +Inf values of `Y` is defined by $[-3.4028235e+38, \ln(3.4028235e+38)] = [-3.4028235e+38, 88.72284]$.

*FP64*: the input range for non +Inf values of `Y` is defined by $[-1.7976931348623157e+308, \ln(1.7976931348623157e+308)] = [-1.7976931348623157e+308, 709.782712893384]$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is identical to `X`.

### Signature
`Y = Exp(X)`
where
- `X`: input tensor
- `Y`: output tensor

### Algorithm
Exp is subject to overflow for great X values.

<a id="int"></a>



### Formal specification

The formal specification of the `exp` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Exp operation on tensors.
 *)
module Exp
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Exp
  let function exp (a : tensor real) : tensor real =
    ensures { forall i. result.value[i] = exp a.value[i] }
  {
    shape = a.shape ;
    value = fun i -> exp a.value[i] ;
  }
end
```

[^1]: See [Why3 documentation](https://www.why3.org/)
