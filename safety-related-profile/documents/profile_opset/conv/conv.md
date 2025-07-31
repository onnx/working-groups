# `conv` operator
### Contents
- `Convolution` operator for type real.

## `<Conv>`  `(<real>)`

### Signature
`Y = conv(X,W,[B])`
where
- `X`: input tensor
- `W`: convolution kernel
- `B`: optional bias
- `Y`: output tensor

#### Restrictions
The following restrictions apply to the `conv` operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor `X` has 2 spatial axes | Simplification |
| `[R2]` | Attribute `auto_pad` is restricted to `NOTSET`  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]` | Attribute `group` is restricted to 1 (standard convolution) or to the number of channels of the input tensor (depthwise convolution) | Simplification | 

 #### Informal specification
  
Operator `conv` computes the convolution of the input tensor `X` with the kernel `W` and adds bias `B` to the result. Two types of convolutions are supported: _standard convolution_ and _depthwise convolution_.

##### Standard convolution
A _standard convolution_ applies a kernel (also called "filter") to the input tensor, aggregating information accross both spatial axes and channels. For a given output channel, the kernel operates accross all input channels and all contributions are summed to produce the output. This corresponds to the case where `group`= 1. 

The mathematical definition of the operator is given hereafter.
For the sake of simplification, we assume that padding and dilation are handled by separate operators, `Pad` (ONNX operator) , `Dilation` and `Broadcast`.
Concretely, we consider the convolution to be applied to a transformed version of the input tensor, the kernel and the bias:

- $X_{eff} = Pad(X)$
- $W_{eff} = Dilation(W)$
- $B_{eff} = Broadcast(B)$

where
- $X_{eff}$ is the padded version of the input tensor `X`.
- $W_{eff}$ is the dilated version of the kernel `W`.
- $B_{eff}$ is the Bias `B` added using the `Broadcast` operator.
- The `Pad` operator applies zero-padding as specified by the pads attribute (see ONNX Pad operator).
- The `Dilation` operator simulates the effect of spacing between kernel elements, based on the dilations attribute. Its implementation will be defined later.
- The `Broadcast` operator replicates the bias value across the spatial dimensions and batch dimension of the output `Y`. (`Broadcast` operator will be defined later).


$$\begin{gathered}
    Y[b, c, m, n] = \sum_{i=0}^{fm(W)-1} \sum_{j=0}^{h(W)-1} \sum_{z=0}^{w(W)-1} \\ (X_{\text{eff}}[b,i,m \cdot strides[0]+ j , n \cdot strides[1]+ z ] \cdot W_{\text{eff}}[c, i, j, z]) \\ + B_{\text{eff}}[c]
\end{gathered}$$

Where
- $b$ is the batch index, $b \in [0,b(Y)-1]$, $b(Y)$ is the batch size of output `Y`
- $c$ is the data channel, $c \in [0,c(Y)-1]$, $c(Y)$ is the number of data channels of output `Y`
- $m \in [0,h(Y)-1]$ is the index of the first spatial axis of output `Y`
- $n \in [0,w(Y)-1]$ is the index of the second spatial axis of output `Y`
- $fm(W)$ is the number of feature maps of kernel `W`
- $h(W)$ is the size of the first spatial axis of kernel `W`
- $w(W)$ is the sizes of the second spatial axis of kernel `W`
`strides` is an attribute of the operator. It will be described later in this section.

The effect of the operator is illustrated on the following figure. In this example
- shape of `Y` is ($1, 1, 4, 4$) (batch size is 1, number of data channels is 1)
- shape of `X` is ($1, 1, 8, 8$) (batch size is 1, number of data channels is 1)
- shape of `W` is ($1, 1, 3, 2$)  (number of data channels is 1)
- shape of `B` is ($1$)
- `pads` is  set to (1,2,2,2) (1 column on the left, 2 columns on the right, 2 rows on the top, 2 rows on the bottom)
- `dilations` is set to (2,2)
- `strides` is set to (2,3)

![](./imgs/conv-std.png)

The following figure shows the case where the number of channels of `X` is 3. In this example:
- shape of `Y` is ($1, 1, 4, 4$) 
- shape of `X` is ($1, 1, 8, 8$)
- shape of `W` is ($1, 1, 3, 2$) 
- shape of `B` is $1$
- `groups` is  set to 1 
- the other attributes have the same values as in the previous figure.

![](./imgs/conv-std-3-channels.png) 


##### Depthwise convolution
A _depthwise convolution_ applies a specific kernel (or "filter") to each input channels. The number of output channels is equal to the number of input channels.  This corresponds to the case where `group`= $c(X)$. 

The mathematical definition is given hereafter:

$$\begin{gathered}
    Y[b, c, m, n] = \sum_{j=0}^{h(W)-1} \sum_{z=0}^{w(W)-1}\\ (X_{\text{eff}}[b, c, m \cdot strides[0] + j , n \cdot strides[1] + z \cdot ] \cdot W_{\text{eff}}[c, 0, j , z] ) + B_{\text{eff}}[c]
\end{gathered}$$

Variables are defined as for the standard convolution.
The effect of the operator is illustrated on the following figure. In this example,
- shape of `Y` is ($1, 3, 4, 4$) 
- shape of `X` is ($1, 3, 8, 8$)
- shape of `W` is ($3, 1, 3, 2$)
- shape of `B` is $3$
- `groups` is  set to 3
- the other attributes have the same values as in the previous figure.

![](./imgs/conv-dep-3-channels.png)

#### Error conditions
No error conditions can occur.

#### Inputs

##### `X`: tensor of real

Tensor `X` is the input tensor on which convolution with kernel `W` is computed.

The shape of tensor `X` is $(b(X) , c(X) , h(X) , w(X))$.

###### Constraints

- (C1) Number of spatial axes of tensor `X`
    - Statement: The number of spatial axes of tensor `X` is 2. `[R1]`
    - Rationale: This restriction is introduced to simplify the implementation considering the actual industrial use cases.
- (C2) <a name="channel_consist"></a> Consistency between the number of channels of `X` and `W` 
    - Statement:  $c(X)=fm(W)$
- (C3) <a name="shape_consist"></a> Consistency between the shape of tensors `X`, `W`, `Y` and attributes `pads`, `dilations` and `strides`
    <span id="it:shape_consist" label="it:shape_consist"></span>
    - Statement: 
       *  $$\left\lfloor{\frac{alpha-(dilations[0] \cdot h(W)-1)}{strides[0]}} \right\rfloor +1 = h(Y) \mbox{ with }  alpha=h(X)+pads[0]+pads[2]$$
         
      and
      
       * $$\left\lfloor{\frac{beta-(dilations[1] \cdot w(W)-1)}{strides[1]}} \right\rfloor +1 = w(Y)  \mbox{ with } beta=w(X)+pads[1]+pads[3]$$
    - Rationale: The size of the output is determined by the number of times the kernel can be applied on a given spatial axis.   
- (C4) Axis denotations
    - Statement: If axis denotation is in effect, the operation expects input data tensor to have axis denotation \[`DATA_BATCH`, `DATA_CHANNEL`, `DATA_FEATURE`, `DATA_FEATURE`\].
    - Rationale: Denotation convention

##### `W`: tensor of real

Tensor `W` is the convolution kernel.

The shape of tensor `W`is $(c(W) , fm(W) , h(W) , w(W))$, where
- $c(W)$ is the number of output channels or number of feature maps
- $fm(W)$ is the number of input channels
- $h(W)$ and $w(W)$ are the sizes of the kernel for the two spatial axes.

###### Constraints
- (C1) Consistency between the number of channels of `X` and `W`
   - Statement: [See constraint (C2) of X](#channel_consist).
- (C2) Consistency between the shape of tensors `X`, `W`, `Y` and attributes `pads`, `dilations` and `strides`.
   - Statement: [See constraint (C3) of X](#shape_consist).
- (C3) <a name="kernel_shape_w"></a> Consistency between `W` and `kernel_shape`
    <span id="it:kernel_shape_w" label="it:kernel_shape_w"></span> 
   - Statement:  The size of `W` for an axis must bve equal to the value of `kernel_shape` for that axis
   - Rationale: `kernel_shape` represents the shape of `W`, where `kernel_shape[0]` = $w(W)$ and `kernel_shape[1]` = $h(W)$.
- (C4) Axis denotations
    - Statement: If axis denotation is in effect, the operation expects the weight tensor to have axis denotation \[`FILTER_OUT_CHANNEL`, `FILTER_IN_CHANNEL`, `FILTER_SPATIAL`, `FILTER_SPATIAL`\].
    - Rationale: Denotation convention

##### `B` : tensor of real

Tensor `B` is the bias. 

The shape of tensor `B`is $c(B)$.

###### Constraints
- (C1) Consistency between the number of channels of `B` and `W`
    - Statement:  $c(B) = fm(W)$.

#### Attributes

##### `strides`: list of int

Attribute `strides` determines how the kernel is applied on tensor `X` during the convolution.

For instance, with $\mbox{\texttt{stride}}[0]=2$ and $\mbox{\texttt{stride}}[1]=3$, the kernel is applied to data 2 units on right in the first spatial axis and to data 3 units down in the second spatial axis at each step of the convolution.

The effect of the `strides` attribute is illustrated on the following figure. In this example, `strides`=(2,3).

<img src="./imgs/conv_stride.png" width="300" />

###### Constraints
- (C1) Value domain
    - Statement: `strides` is a list of strictly positive integers.
    - Rationale: Stride values are used in the denominator of expression in [constraint (C3) of X](#shape_consist) 
- (C2) Consistency between the shape of tensors `X`, `W`, `Y` and attributes `pads`, `dilations` and `strides`.
    - Statement: [See constraint (C3) of X](#shape_consist)

##### `auto_pad` : string

The `auto_pad` attribute determines if and how automatic padding is done for the input tensor X.

###### Constraints
- (C1) Explicit padding
    - Statement: `auto_pad` shall be set to `NOTSET` `[R2]`
    - Rationale: The SONNX profile imposes explicit padding.

##### `pads`: list of int

Attribute `pads` determines the padding at the beginning and end along each spatial axis of the input tensor `X`.

`pads` is a list of the form (`x1_begin`, `x2_begin`,..., `x1_end`, `x2_end`,...), where `xi_begin` is the number of elements (possibly zero) added at the beginning of axis $i$ and `xi_end` is the number of elements added at the end of axis $i$.

The padding value is 0.

The effect of the `pads` attribute is illustrated on the following figure. In this example,  `pads`=(1,3,2,2).

<img src="./imgs/conv_pad.png" width="300" />

###### Constraints
- (C1) Value domain
    - Statement: `pads` is a list of positive or null integers.
    - Rationale: A padding value gives a number of elements to be added to some spatial axis. This is positive[^2].
- (C2) Consistency between the shape of `X` and the length of `pads`
    - Statement: The length of the `pads` list is two times the number of spatial axes of `X`
    - Rationale: Padding shall be given for all spatial axes, and a beggining value and an end value must be given for each axis.
- (C3) Consistency between the shape of tensors `X`, `W`, `Y` and attributes `pads`, `dilations` and `strides`.
    - Statement: [See constraint (C3) of X](#shape_consist)

##### `dilations`: list of int

Attribute `dilations` specifies the spacing between the kernel elements for each spatial axis of the filter `W`. It is a list of non-null integer values where each value gives the dilation factor for spatial axis $i$. If the dilation factor is greater than 1 for axis $i$, then the kernel points are spaced out by the dilation factor for that axis. 

The spacing value is 0.

The effect of the `dilations` attribute for a tensor with two spatial axes is depicted on the following figure. In this example, `dilations`=(2,2). 

<img src="./imgs/dilation.png" width="300" />


###### Constraints
- (C1) Value domain
    - Statement: `dilations` is a list of strictly positive integers
- (C2) Relation between `dilations` and `W`
    - Statement: The length of the `dilations` list is equal to number of spatial axes of `W`.
    - Rationale: Dilation is defined for all spatial axes of `W`.
- (C3) Consistency between the shape of tensors `X`, `W`, `Y` and  attributes `pads`, `dilations` and `strides`.
    - Statement: [See constraint (C3) of X](#shape_consist)

##### `group`: int 

This attribute specifies the number of groups the input channels and output channels are divided into. When `group`=1, a standard convolution is performed.
When group is greater than 1, convolution is computed for each group separately with a specific set of filters.

The effect of the `group` attribute for a tensor with two spatial axes is depicted on the following figure. In this example `group`=3.

<img src="./imgs/grouped_convolution.png" width="300" />

(Taken from https://eli.thegreenplace.net/2018/depthwise-separable-convolutions-for-machine-learning)

In the example, with `group` set to 3 and an input `X` and an output `Y` with 3 channels, the input and output channels will be divided into 3 groups of 1 channel.

###### Constraints
- (C1) Support for standard and depthwise convolutions
    - Statement: `group`=1 or `group`$=c(X)$ `[R3]`
    - Rationale: SONNX only supports the most usual types of convolutions: standard (`group`=1) and depthwise convolutions `group`$=c(X)$ 

##### `kernel_shape`: list of int

This parameter specifies the shape of the convolution kernel `W`.

###### Constraints.

- (C1) Value domain
    - Statement: `kernel_shape` is a list of strictly positive integers
    - Rationale: A dimension is always positive and cannot be null.
- (C2) Consistency between `W` and `kernel_shape`
    - Statement: [See constraint (C3) of W](#kernel_shape_w)

#### Outputs

##### `Y` : tensor of real

The size of the output `Y` will be $(b(Y) , c(Y) , h(Y) , w(Y))$ where
- $b(Y)$ is the number of batches
- $c(Y)$ is the number of channels
- $h(Y)$ and $w(Y)$ are the sizes of the output for the two spatial axes

###### Constraints.
- (C1) Consistency between the shape of tensors `X`, `W`, `Y`, attributes `pads` and `strides`,
    - Statement: [see constraint (C3) of X](#shape_consist)

#### Formal specification

*(to be completed)*

