# Contents

- **ConvInteger** operator for types [int8, uint8](#int)

Based on ONNX documentation [ConvInteger version 10](https://onnx.ai/onnx/operators/onnx__ConvInteger.html#convinteger-10).

<a id="int"></a>
# **ConvInteger** (int8, uint8)

## Signature

$$
Y = \textbf{ConvInteger}(X,W,[x\_zero\_point],[w\_zero\_point])
$$

where:
- $X$: input tensor
- $W$: convolution kernel
- $x\_zero\_point$: optional zero point of input tensor $X$
- $w\_zero\_point$: optional zero point of kernel $W$
- $Y$: output tensor containing the integer convolution result

The type of $X$ and $x\_zero\_point$ is `T1`, the type of $W$ and $w\_zero\_point$ is `T2`, where `T1` and `T2` are each in {int8, uint8}. The output tensor $Y$ has type `int32`.

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following restrictions apply to the **ConvInteger** operator for the SONNX profile:

| Restriction | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` | Attribute `auto_pad` is set to `NOTSET` | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]` | Attribute `group` is set to 1 (standard convolution) or to the number of channels of the input tensor $X$ (depthwise convolution) | Transient |

## Function

<span style="background: red; color: white; font-size:0.7em;">[E_CONVINTEGER_INT_FUNC_0010]</br></span>
Operator **ConvInteger** computes the convolution of the input tensor $X$ with the kernel $W$ after subtracting their respective zero points. The resulting products are accumulated in the output tensor $Y$, whose elements are `int32`.

Two types of convolution are supported by the SONNX profile: standard convolution and depthwise convolution.

For any valid output index $(b,c,m,n)$, the mathematical definition is:

$$
Y[b,c,m,n]
=
\sum_{i=0}^{dW_1-1}
\sum_{j=0}^{dW_2-1}
\sum_{z=0}^{dW_3-1}
\left(
X_p[b,i,m\cdot\text{strides}[0]+j,n\cdot\text{strides}[1]+z]
-
X_{0}
\right)
\cdot
\left(
W_d[c,i,j,z]
-
W_{0}[c]
\right)
$$

where:
- $b \in [0,dY_0-1]$ is the batch index.
- $c \in [0,dY_1-1]$ is the output-channel index.
- $m \in [0,dY_2-1]$ is the index of the first spatial axis of $Y$.
- $n \in [0,dY_3-1]$ is the index of the second spatial axis of $Y$.
- $dY_0=dX_0$ is the batch size.
- $dY_1=dW_0$ is the number of output channels.
- $dW_1=dX_1/\text{group}$ is the number of input channels processed by one group.
- $dW_2$ and $dW_3$ are the two spatial dimensions of the kernel.
- $X_p=\text{pad}(X,\text{pads})$ is the input tensor after padding.
- $W_d=\text{dilation}(W,\text{dilations})$ is the kernel after dilation.
- $X_0$ is the input zero point. It is 0 when `x_zero_point` is not provided.
- $W_0[c]$ is the zero point associated with output channel $c$. It is 0 when `w_zero_point` is not provided. If `w_zero_point` is scalar, the same value is used for every output channel.
- `strides`, `pads`, `dilations` and `group` will be described in the attribute section.

For standard convolution (`group = 1`), every output channel uses all input channels. For depthwise convolution (`group = dX_1`), each output channel is associated with one input channel and the corresponding kernel has one input-channel value.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

### Standard convolution

A standard convolution applies each output-channel filter to all input channels. This corresponds to `group = 1`. In this case:

$$
dW_1=dX_1
$$

and the summation in the definition above covers every input channel.

### Depthwise convolution

A depthwise convolution applies one filter to each input channel. This corresponds to `group = dX_1`. The number of output channels is therefore equal to the number of input channels:

$$
dY_1=dX_1
$$

and each filter has one input channel:

$$
dW_1=1
$$

For an output channel $c$, the computation can consequently be written as:

$$
Y[b,c,m,n]
=
\sum_{j=0}^{dW_2-1}
\sum_{z=0}^{dW_3-1}
\left(
X_p[b,c,m\cdot\text{strides}[0]+j,n\cdot\text{strides}[1]+z]-X_0
\right)
\cdot
\left(
W_d[c,0,j,z]-W_0[c]
\right)
$$

### Example : standard convolution, single channel
In this example
- shape of $X$ is $(1,1,3,3)$, type `int8`
- shape of $W$ is $(1,1,2,2)$, type `int8`
- `x_zero_point` $=1$ (scalar, type `int8`)
- `w_zero_point` $=1$ (scalar, type `int8`)
- $pads=(0,0,0,0)$, $dilations=(1,1)$, $strides=(1,1)$, $group=1$

$$
X[0,0] = \begin{bmatrix} 2 & 4 & 6 \\ 8 & 10 & 12 \\ 14 & 16 & 18 \end{bmatrix}
\qquad
W[0,0] = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
$$

Since $pads=(0,0,0,0)$, $X_p=X$; since $dilations=(1,1)$, $W_d=W$. With $group=1$, $dW_1=dX_1=1$, so the general formula reduces, for each output position $(m,n)$, to a single term $i=0$:

$$
Y[0,0,m,n] = \sum_{j=0}^{1}\sum_{z=0}^{1} \big(X[0,0,m+j,n+z]-1\big)\cdot\big(W[0,0,j,z]-1\big)
$$

The output shape is $dY_2=dY_3=\left\lfloor\dfrac{3-2}{1}\right\rfloor+1=2$, so $Y[0,0]$ has shape $(2,2)$.

For instance, for $(m,n)=(0,0)$, the $2\times2$ patch of $X$ is $\begin{bmatrix}2&4\\8&10\end{bmatrix}$; subtracting `x_zero_point` gives $\begin{bmatrix}1&3\\7&9\end{bmatrix}$, and subtracting `w_zero_point` from $W$ gives $\begin{bmatrix}0&-1\\-1&0\end{bmatrix}$, so $Y[0,0,0,0]=1\cdot0+3\cdot(-1)+7\cdot(-1)+9\cdot0=-10$.

Applying the same computation to the three remaining output positions gives:

$$
Y[0,0] = \begin{bmatrix} -10 & -14 \\ -22 & -26 \end{bmatrix}
$$

Tensor $Y$ has shape $(1,1,2,2)$ and type `int32`.
## Error conditions
No error condition.

## Attributes

### `auto_pad`: string

The `auto_pad` attribute determines whether padding is automatically computed for the spatial axes of input tensor $X$.

Its value shall be one of `NOTSET`, `VALID`, `SAME_UPPER`, or `SAME_LOWER`.

When `auto_pad` is `NOTSET`, explicit padding is specified by `pads`. In the SONNX profile, `auto_pad` is restricted to `NOTSET` `[R2]`.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_AUTOPAD_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_AUTOPAD_0010]` Value domain
  - Statement: `auto_pad` shall be in the set {`NOTSET`, `VALID`, `SAME_UPPER`, `SAME_LOWER`}.

<a id="E_CONVINTEGER_INT_CONSTR_AUTOPAD_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_AUTOPAD_0020]` Explicit padding
  - Statement: `auto_pad` shall be set to `NOTSET` `[R2]`.
  - Rationale: The SONNX profile imposes explicit padding.

### `dilations`: list of int

The `dilations` attribute specifies the spacing between kernel elements for each spatial axis.

A dilation value of 1 means that consecutive kernel elements are adjacent. A value greater than 1 inserts spacing between consecutive kernel elements.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_DILATIONS_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_DILATIONS_0010]` Value domain
  - Statement: `dilations` is a list of strictly positive integers.
  - Rationale: A dilation is a positive expansion factor.

<a id="E_CONVINTEGER_INT_CONSTR_DILATIONS_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_DILATIONS_0020]` Relation with $W$
  - Statement: The length of `dilations` is equal to the number of spatial axes of $W$.
  - Rationale: A dilation factor is specified for every spatial axis of the kernel.

<a id="E_CONVINTEGER_INT_CONSTR_DILATIONS_0030"></a>
- `[E_CONVINTEGER_INT_CONSTR_DILATIONS_0030]` Consistency between $X$, $W$, $Y$, `pads`, `dilations` and `strides`
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_STRIDES_0020</span></b>](#E_CONVINTEGER_INT_CONSTR_STRIDES_0020) on attribute `strides`.

### `group`: int

The `group` attribute specifies the number of groups into which the input and output channels are divided.

When `group = 1`, a standard convolution is performed. When `group = dX_1`, a depthwise convolution is performed.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_GROUP_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_GROUP_0010]` Value domain
  - Statement: `group` is a strictly positive integer.
  - Rationale: `group` represents the number of channel groups.

<a id="E_CONVINTEGER_INT_CONSTR_GROUP_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_GROUP_0020]` Consistency between channels and groups
  - Statement:
    - $dX_1 \bmod \text{group}=0$
    - $dW_0 \bmod \text{group}=0$
  - Rationale: Input and output channels must be evenly distributed between groups.

<a id="E_CONVINTEGER_INT_CONSTR_GROUP_0030"></a>
- `[E_CONVINTEGER_INT_CONSTR_GROUP_0030]` Support for standard and depthwise convolutions
  - Statement: `group = 1` or `group = dX_1` `[R3]`.
  - Rationale: The SONNX profile supports standard and depthwise convolution.

### `kernel_shape`: list of int

The `kernel_shape` attribute specifies the spatial shape of the convolution kernel $W$.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_KERNELSHAPE_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_KERNELSHAPE_0010]` Value domain
  - Statement: `kernel_shape` is a list of strictly positive integers.
  - Rationale: A kernel dimension is positive.

<a id="E_CONVINTEGER_INT_CONSTR_KERNELSHAPE_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_KERNELSHAPE_0020]` Consistency between $W$ and `kernel_shape`
  - Statement: The size of $W$ along each spatial axis shall be equal to the corresponding value of `kernel_shape`.
  - Rationale: `kernel_shape` represents the spatial shape of $W$.

### `pads`: list of int

The `pads` attribute specifies the number of elements added before and after each spatial axis of $X$.

For two spatial axes, `pads` has the form:

$$
(\text{x1\_begin},\text{x2\_begin},\text{x1\_end},\text{x2\_end}).
$$

The padding value is 0.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_PADS_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_PADS_0010]` Value domain
  - Statement: `pads` is a list of positive or null integers.
  - Rationale: A padding value represents a number of elements added to an axis.

<a id="E_CONVINTEGER_INT_CONSTR_PADS_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_PADS_0020]` Consistency with the shape of $X$
  - Statement: The length of `pads` is two times the number of spatial axes of $X$.
  - Rationale: Both the beginning and the end of every spatial axis must be specified.

<a id="E_CONVINTEGER_INT_CONSTR_PADS_0030"></a>
- `[E_CONVINTEGER_INT_CONSTR_PADS_0030]` Consistency between $X$, $W$, $Y$, `pads`, `dilations` and `strides`
  - Statement:  see constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_STRIDES_0020</span></b>](#E_CONVINTEGER_INT_CONSTR_STRIDES_0020) on attribute `strides`.

### `strides`: list of int

The `strides` attribute determines the displacement of the kernel between two consecutive applications along each spatial axis.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_STRIDES_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_STRIDES_0010]` Value domain
  - Statement: `strides` is a list of strictly positive integers.
  - Rationale: A stride represents the displacement of the kernel.

<a id="E_CONVINTEGER_INT_CONSTR_STRIDES_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_STRIDES_0020]` Consistency between $X$, $W$, $Y$, `pads`, `dilations` and `strides`
  - Statement:

$$
\left\lfloor
\frac{\alpha-\left((\text{dilations}[0]\cdot dW_2-1)+1\right)}
{\text{strides}[0]}
\right\rfloor+1=dY_2
$$

with

$$
\alpha=dX_2+\text{pads}[0]+\text{pads}[2]
$$

and

$$
\left\lfloor
\frac{\beta-\left((\text{dilations}[1]\cdot dW_3-1)+1\right)}
{\text{strides}[1]}
\right\rfloor+1=dY_3
$$

with

$$
\beta=dX_3+\text{pads}[1]+\text{pads}[3].
$$

  - Rationale: The output spatial dimensions are determined by the input dimensions, padding, dilation, kernel size and stride.

## Inputs

### $X$: int8 or uint8 tensor

Tensor $X$ is the input tensor on which the integer convolution is computed.

The shape of $X$ is:

$$
(dX_0,dX_1,dX_2,dX_3)
$$

where:
- $dX_0$ is the batch size.
- $dX_1$ is the number of input channels.
- $dX_2$ and $dX_3$ are the sizes of the two spatial axes.

#### Constraints


<a id="E_CONVINTEGER_INT_CONSTR_X_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_X_0010]` Number of spatial axes
  - Statement: The number of spatial axes of $X$ is 2 `[R1]`.
  - Rationale: This restriction limits the SONNX specification to two-dimensional image convolutions.

<a id="E_CONVINTEGER_INT_CONSTR_X_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_X_0020]` Consistency between the number of channels of $X$ and $W$
  - Statement: $dW_1=dX_1/\text{group}$.
  - Rationale: Each filter processes the number of input channels assigned to one group.

<a id="E_CONVINTEGER_INT_CONSTR_X_0030"></a>
- `[E_CONVINTEGER_INT_CONSTR_X_0030]` Consistency between $X$, $W$, $Y$, `pads`, `dilations` and `strides`
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_STRIDES_0020</span></b>](#E_CONVINTEGER_INT_CONSTR_STRIDES_0020) on attribute `strides`.

<a id="E_CONVINTEGER_INT_CONSTR_X_0040"></a>
- `[E_CONVINTEGER_INT_CONSTR_X_0040]` Type of $X$ and `x_zero_point`
  - Statement: $X$ and `x_zero_point` shall have type `int8` or `uint8`.
  - Rationale: These are the types allowed for ONNX ConvInteger input data and its zero point.

### $W$: int8 or uint8 tensor

Tensor $W$ is the convolution kernel.

Its shape is:

$$
(dW_0,dW_1,dW_2,dW_3)
$$

where:
- $dW_0$ is the number of output channels.
- $dW_1$ is the number of input channels per group.
- $dW_2$ and $dW_3$ are the sizes of the two spatial axes of the kernel.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_W_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_W_0010]` Consistency between the number of channels of $X$ and $W$
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_X_0020</span></b>](#E_CONVINTEGER_INT_CONSTR_X_0020) on tensor $X$.

<a id="E_CONVINTEGER_INT_CONSTR_W_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_W_0020]` Consistency between $X$, $W$, $Y$, `pads`, `dilations` and `strides`
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_X_0030</span></b>](#E_CONVINTEGER_INT_CONSTR_X_0030) on tensor $X$.

<a id="E_CONVINTEGER_INT_CONSTR_W_0030"></a>
- `[E_CONVINTEGER_INT_CONSTR_W_0030]` Consistency between $W$ and `kernel_shape`
  - Statement: The spatial size of $W$ shall be equal to `kernel_shape`.
  - Rationale: `kernel_shape` describes the spatial dimensions of $W$.

<a id="E_CONVINTEGER_INT_CONSTR_W_0040"></a>
- `[E_CONVINTEGER_INT_CONSTR_W_0040]` Output channels and groups
  - Statement: $dW_0\bmod\text{group}=0$.
  - Rationale: Output channels must be evenly distributed among groups.

<a id="E_CONVINTEGER_INT_CONSTR_W_0050"></a>
- `[E_CONVINTEGER_INT_CONSTR_W_0050]` Type of $W$ and `w_zero_point`
  - Statement: $W$ and `w_zero_point` shall have type `int8` or `uint8`.
  - Rationale: These are the types allowed for ONNX ConvInteger weights and their zero point.

### $x\_zero\_point$: optional int8 or uint8 tensor

The tensor `x_zero_point` specifies the zero point used to center the values of $X$ before multiplication.

It is optional and, when absent, its value is 0.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_XZEROPOINT_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_XZEROPOINT_0010]` Scalar shape
  - Statement: `x_zero_point` is a scalar.
  - Rationale: Input zero-point quantization is per tensor.
<a id="E_CONVINTEGER_INT_CONSTR_XZEROPOINT_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_XZEROPOINT_0020]` Type consistency
  - Statement: `x_zero_point` has the same type as $X$.
  - Rationale: The zero point is subtracted from values of $X$ before multiplication.

### $w\_zero\_point$: optional int8 or uint8 tensor

The tensor `w_zero_point` specifies the zero point used to center the values of $W$ before multiplication.

It is optional and, when absent, its value is 0.

It may be either a scalar or a one-dimensional tensor with one element for each output channel.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_WZEROPOINT_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_WZEROPOINT_0010]` Shape 
  - Statement: `w_zero_point` is either a scalar or a one-dimensional tensor with $dW_0$ elements.
  - Rationale: Weight zero-point quantization may be per tensor or per output channel.
<a id="E_CONVINTEGER_INT_CONSTR_WZEROPOINT_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_WZEROPOINT_0020]` Type consistency
  - Statement: `w_zero_point` has the same type as $W$.
  - Rationale: The zero point is subtracted from values of $W$ before multiplication.


## Outputs

### $Y$: int32 tensor

Tensor $Y$ contains the result of the integer convolution.

Its shape is:

$$
(dY_0,dY_1,dY_2,dY_3)
$$

where:
- $dY_0=dX_0$ is the batch size.
- $dY_1=dW_0$ is the number of output channels.
- $dY_2$ and $dY_3$ are the spatial dimensions determined by the kernel shape, padding, dilation and stride.

#### Constraints

<a id="E_CONVINTEGER_INT_CONSTR_Y_0010"></a>
- `[E_CONVINTEGER_INT_CONSTR_Y_0010]` Shape consistency
  - Statement: $dY_0=dX_0$, $dY_1=dW_0$, and $dY_2,dY_3$ satisfy the output-dimension equations defined by constraint [<b><span style="font-family: 'Courier New', monospace">E_CONVINTEGER_INT_CONSTR_STRIDES_0020</span></b>](#E_CONVINTEGER_INT_CONSTR_STRIDES_0020) on attribute `strides`.

<a id="E_CONVINTEGER_INT_CONSTR_Y_0020"></a>
- `[E_CONVINTEGER_INT_CONSTR_Y_0020]` Type
  - Statement: $Y$ has type `int32`.
  - Rationale: ConvInteger produces a 32-bit integer output.

## Formal specification

See the Why3 specification.