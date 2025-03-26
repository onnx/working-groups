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
   Y = \frac{1}{1+\epsilon^{-x}} = \frac{\epsilon^x}{1+\epsilon^x}  
$$


<a id="float"></a>
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

### Algorithm
Sigmoid is subject to exponent divergence for great negative values of `X`.
To remain stable, the algorithm shall split the `X` domain to only compute negative exponent.

```
if X < 0
    Y = exp(x)/(1+exp(x))
else
    Y = 1/(1+exp(-x))
```

<a id="int"></a>
