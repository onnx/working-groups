# Preamble

(This section is for information only. It is *not* part of the
specification.)

### Specification principles

The specification is written with the following *principles* in mind.
Note that these principles will eventually be replaced by the industrial
needs that will be captured in phase 1 of our work.

1.  We are only concerned with the syntactic and semantics elements
    concerning the **inference**. All ONNX constructs dealing with
    training are out of the scope of the Safety-Related Standard.

2.  We distinguish an *informal* and a *formal* specification. The
    *informal* part is aimed at facilitating the understanding of the
    ONNX construct (e.g., operator). It may be incomplete, as far as it
    is clearly indicated. Conversely, the *formal* specification shall
    be absolutely complete and non ambiguous.

3.  Using mathematical formalism shall be avoided if not required. Since
    we are essentially[^1] targeting data and computer scientists, using
    a very cryptic – yet perfectly well defined and mathematically
    grounded – notation may reveal being error prone and, consequently,
    counter effective.

4.  The specification can rely on a formal language, as far as this
    language does not violate rule (2) above.

### Open questions

1.  Can’t we use the ONNX reference implementation and complete it,
    clarify it, rather than writing something completely new? Indeed,
    wouldn’t it be simpler and possibly more efficient and less error
    prone to provide a well-documented (and reviewed) Python
    implementation rather than re-implementing things using a specific
    (possibly formal) language? In particular, the semantics must be
    defined with respect to a actual ONNX model (i.e., a protobuf file).

2.  What do we plan to do with the formal specification?

3.  Would it be wise to define a textual representation of an ONNX model
    in order to simplify specifying the formal semantics?

### References

- About Why3, used to write the formal specification, see
  <https://www.why3.org/>.

- About the ONNX semantics, see the “[Open Neural Network Exchange
  Intermediate Representation
  Specification](https://onnx.ai/onnx/repo-docs/IR.html)”. This document
  does not really explain in details how the graph is executed, but the
  execution semantics is basically to (i) sort the operators
  topologically, (ii) execute each operator.

# Conventions

- Notation $X.H$ (resp. $X.W$) denotes the *height* (resp. *width*) of
  tensor $X$.

- “height” (resp. “width”) denotes the first (resp. second) spatial
  axis.

- inputs, outputs and attributes are represented using a non-serif font
  (e.g., `pads`).

# `conv` operator

### Restrictions

The following limitations apply to the `conv` operator of the
safety-related profile:

- the number of spatial axes of the tensors is equal to 2.

- there is no grouping (i.e., $\mbox{\texttt{group}}=1$), so the `conv`
  operator does a standard convolution.

In the rest of the document, restrictions with respect to the ONNX
standard `conv` operator are indicated in the text with the tag.

### Signature

`Y = conv(X,W,[B])`

where

- `Y` is the output tensor of the convolution

- `X` is the input tensor to be convoluted with the convolution kernel
  `W`

- `W` is the convolution kernel

- `B` is the optional bias to be added to the result of the convolution.

### Specification for data types: `Y` : real, `X`: real, `W`: real, `B`: real

#### Informal specification

The `conv` operator computes the convolution of the input tensor `X`
with the “filter”, or “kernel”, `W` and adds bias `B` to the result.

A simplified mathematical definition of the operator is given hereafter
for the 2D case, without padding and with $\mbox{\texttt{group}}=1$ .
The formal specification is given in
Section <a href="#sec:conv_formal" data-reference-type="ref"
data-reference="sec:conv_formal">3.5</a>. When considering padding, the
same formula applies, in which `X` is represents the padded version of
the actual input `X`.

$$\begin{gathered}
    \mbox{\texttt{Y}}[b, c, m, n] = \sum_{c_i=0}^{W.C_{in}-1} \sum_{k_h=0}^{W.H-1} \sum_{k_w=0}^{W.W-1} \\ (\mbox{\texttt{X}}[b,c_i,m \cdot \mbox{\texttt{strides[0]}}+k_h\cdot \mbox{\texttt{dilation[0]}}, n \cdot \mbox{\texttt{strides[1]}}+k_w\cdot \mbox{\texttt{dilations[1]}}] \times \mbox{\texttt{W}}[c, c_i, k_h, k_w]) \\ + \mbox{\texttt{B}}[c_i]
\end{gathered}$$

Where

- $b$ is the batch index, $b \in [0,Y.B-1]$ and $Y.B$ is the batch size of
  the output `Y`

- $c$ is the data channel, $c \in [0,Y.C-1]$ and $Y.C$ is the number of data
  channels of the output `Y`

- $m \in [0,Y.H-1]$ (resp. $n \in [0,Y.W-1]$) is the index of the
  first (resp. second) spatial axis of the output `Y`

- $W.C_{in}$ is the number of input channels of kernel `W`

- $W.H$ and $W.W$ are the sizes of the two spatial axis of tensor `W`

- attributes `strides` and `dilations` are described later in this
  section.

The effect of the operator is depicted on the following picture.
![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/conv.png)


#### Inputs and outputs

##### `X`

`X` is the input tensor on which convolution with kernel `W` is
computed.

The shape of tensor `X` is $(X.B \times X.C \times X.H \times X.W)$
where

- $X.B$ is the batch size

- $X.C$ is the number of data channels

- $X.H$ and $X.W$ are the sizes of the tensor for the two spatial axis

###### Constraints

1.  Axis of tensor `X`

    - Statement: The number of spatial axis of tensor `X` is 2.

    - Rationale: We only consider 2 spatial axes.

2. <a name="channel_consist"></a> Consistency between the number of channels of `X`, `W`, `B`, and
    `Y`.  

    - Statement: $X.C=Y.C=W.C_{in}=B.C$

    - Rationale: This is a particular case of the more general relation
      $X.C=Y.C=W.C_{in}\cdot\mbox{\texttt{groups}}$ when
      $\mbox{\texttt{groups}}=1$.

3. <a name="shape_consist"></a> Consistency between the shape of tensors `X`, `W`, `Y` and
    attributes `pads`, `dilations` and `strides`
   
    - Statement: If parameter `pads` is not empty
 
       *  $$\lfloor{\frac{L.H-(\mbox{\texttt{dilations[0]}} \times W.H-1)}{\mbox{\texttt{stride[0]}}}} \rfloor +1 = \mbox{\texttt{Y.H}} \mbox{ with }  L.H=X.H+\mbox{\texttt{pads[0]}}+\mbox{\texttt{pads[2]}}$$
  
      and
 
       * $$\lfloor{\frac{L.W-(\mbox{\texttt{dilations[1]}} \times W.W-1)}{\mbox{\texttt{stride[1]}}}} \rfloor +1 = \mbox{\texttt{Y.W}}  \mbox{ with } L.W=X.W+\mbox{\texttt{pads[1]}}+\mbox{\texttt{pads[3]}}$$

    - Rationale: The size of the output is determined by the number of
      times the kernel can be applied on a given spatial axis.

4.  Axis denotations

    - Statement: If axis denotation is in effect, the operation expects
      input data tensor to arrive with the axis denotation of
      \[`DATA_BATCH`, `DATA_CHANNEL`, `DATA_FEATURE`, `DATA_FEATURE`\].

    - Rationale: Denotation convention

##### `W`

Tensor `W` is the convolution kernel. The shape of the kernel is
$(W.C_{out} \times W.C_{in} \times W.H \times W.W)$, where

- $W.C_{out}$ is the number of output channels or number of feature maps

- $W.C_{in}$ is the number of input channels,

- $W.H$ and $W.W$ are the sizes of the kernel for the two spatial axis.

Optionally,

###### Constraints

1.  Consistency between the number of channels of `X`, `W`,`B`, and `Y`,
     [see constraint (2) of X](#channel_consist)

2.  Consistency between the shape of tensors `X`, `W`, `Y` and
    attributes `pads`, `dilations` and `strides`. [See constraint (3) of X](#shape_consist)
   

3.  Axis denotations

    - Statement: If axis denotation is in effect, the operation expects
      the weight tensor to arrive with the axis denotation of
      \[`FILTER_OUT_CHANNEL`, `FILTER_IN_CHANNEL`, `FILTER_SPATIAL`,
      `FILTER_SPATIAL`\].

    - Rationale: Denotation convention

##### `B`, optional

Tensor `B` is the optional bias. The shape of the bias tensor is
$(B.C \times 1)$.


###### Constraints

1.  Consistency between the number of channels of `X`, `W`,`B`, and `Y`,
    [see constraint (2) of X](#channel_consist)
#### Attributes

##### `strides`: integer (optional, default value 1)

The `strides` attributes determines how the kernel is moved on the input
tensor `X` during the convolution.

For instance, with $\mbox{\texttt{strides}}[0]=1$ and
$\mbox{\texttt{strides}}[1]=2$, the kernel is moved of 1 unit in the
first spatial axis and 2 units in the second spatial axis at each step
of the convolution.

This effect is illustrated on the following figure:

![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/conv_stride.png)

###### Constraints

1.  Size of `strides`

    - Statement: If non empty, the number of elements in the `strides`
      attribute must be equal to 2.

    - Rationale: Striding is done on each spatial axis.

2.  Consistency between the shape of tensors `X`, `W`, `Y` and
    attributes `pads`, `dilations` and `strides`. [See constraint (3) of X](#shape_consist)

##### `auto_pad` : string (default is `NOTSET`)

The `auto_pad` attribute determines if and how automatic padding is done
for the input tensor X.

If it is not set or set to `NOTSET`, padding is determined by the pads
attribute (see below). Otherwise, padding is done according to the
`auto_pad` value, as follows:

- if auto\_pad = VALID: no padding is done.

- if auto\_pad = NOTSET: padding is done according to the `pads` attribute. If attribute `pads` is not
  set, it takes its default value, i.e., $(0,0,0,0)$. In that case, the result is identical to the one that would be obtained if
  auto\_pad = VALID (i.e., no padding
  is done).

- if auto\_pad = SAME\_UPPER: for each axis, padding must be added so that [constraint (3) of X](#shape_consist) holds.
     * $$\lfloor {\frac{L.H-W.H}{\mbox{\texttt{stride[0]}}}} \rfloor +1 = \mbox{\texttt{Y.H}} \mbox{ with }  L.H=X.H+pad_h$$
   
  and
  
     * $$\lfloor {\frac{L.W-W.W}{\mbox{\texttt{stride[1]}}}} \rfloor +1 = \mbox{\texttt{Y.W}} \mbox{ with }  L.W=X.W+pad_w$$

  If the total padding $pad_h$ (resp. $pad_w$) is even then padding shall be

  - $pad_h/2$ (resp. $pad_w/2$) at the beginning
  
   and

  - $pad_h/2$ (resp. $pad_w/2$) at the end.

  otherwise padding shall be

  - $\lfloor{pad_h/2} \rfloor$ (resp. $\lfloor{pad_w/2} \rfloor$) at the beginning
  
    and

  - $\lfloor{pad_h/2}\rfloor+1$ (resp. $\lfloor{pad_w/2}\rfloor+1$) at the end.

- auto\_pad = SAME\_LOWER: For each axis, padding must be added so that [constraint (3) of X](#shape_consist) holds.
     * $$\lfloor {\frac{L.H-W.H}{\mbox{\texttt{stride[0]}}}} \rfloor +1 = \mbox{\texttt{Y.H}} \mbox{ with }  L.H=X.H+pad_h$$
   
  and
  
     * $$\lfloor {\frac{L.W-W.W}{\mbox{\texttt{stride[1]}}}} \rfloor +1 = \mbox{\texttt{Y.W}} \mbox{ with }  L.W=X.W+pad_w$$

  If the total padding $pad_h$ (resp. $pad_w$) is even then padding shall be

  - $pad_h/2$ (resp. $pad_w/2$) at the beginning

    and

  - $pad_h/2$ (resp. $pad_w/2$) at the end.

  otherwise padding shall be

  - $\lfloor{pad_h/2+1} \rfloor$ (resp. $\lfloor{pad_w/2+1} \rfloor$) at the beginning
  
    and

  - $\lfloor{pad_h/2} \rfloor$ (resp. $\lfloor{pad_w/2} \rfloor$) at the end.

The effect of the `auto_pad` attribute is illustrated on the following figure:

![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/autopad.png)

###### Constraints

1.  Value domain

    - Statement: The value of attribute `auto_pad` shall be in
      `"NOTSET"`, `"SAME_UPPER"`, `"SAME_LOWER"`, `"VALID"`.

2. <a name="pads_autopad_consist"></a> Consistency between `pads` and `auto_pad`

    - Statement: If attribute `pads` is not empty, attribute `auto_pad`
      shall be either empty or set to `NOTSET`.

    - Rationale: Padding is either defined by attribute `pads` or
      computed automatically, in an exclusive manner.

##### `pads`: list of int (optional, default value is 0 along start and end of each spatial axis).

The `pads` attribute determines the padding at the beginning and ending
along each spatial axis of the input tensor `X`.

The value represents the number of elements added to the beginning and
end part of the corresponding axis. The `pads` is a list of the form
(`x1_begin`, `x2_begin`,..., `x1_end`, `x2_end`,...), where `xi_begin`
is the number of elements added at the beginning of axis $i$ and
`xi_end` is the number of elements added at the end of axis $i$. If not
present, the padding defaults to 0 for the beginning and end of each
spatial axis.

The value of the elements added by the padding is 0.

The effect of padding illustrated on the following figure:

![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/pad.png)


###### Constraints.

1.  Consistency between `pads` and `auto_pad`, see [constraint (2)](#pads_autopad_consist)
    
2.  Value domain

    - Statement: Each element of the `pads` list shall be greater or
      equal to 0

    - Rationale: A padding value gives a number of elements to be added
      to some spatial axis. This is strictly positive[^2].

3.  Consistency between the shape of `X` and the length of `pads`

    - Statement: The length of the `pads` list shall be equal to 2 times
      the number of spatial axes

    - Rationale: If padding is given, it shall be given for all spatial
      axes.

4.  Length of `pads`

    - Statement: The length of the `pads` list shall be a multiple of 2

    - Rationale: For each axis, two values must be given: one for the
      beginning and one for the end.

5.  Consistency between the shape of tensors `X`, `W`, `Y` and
    attributes `pads`, `dilations` and `strides`. [See constraint (3) of X](#shape_consist)

##### `dilations`: list of ints (default is 1 along each spatial axis)

The `dilations` attribute specifies the spacing between the kernel
elements for each spatial axis of the filter `W`. It is a list of
non-null integer values where each value gives the dilation factor for
spatial axis $i$. If the dilation factor is greater than 1 for a axis
$i$, then the kernel points are spaced out by the dilation factor.

The effect of the `dilations` attribute for a tensor with two spatial axes is depicted on the following figure:

![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/dilation.png)

###### Constraints

1.  (C1) Domain of `dilations` values

    - Statement: All values in the `dilation` attribute shall be an
      integer value strictly greater than 0

    - Rationale: ONNX accepts dilations equal to 0 or negative...

    

2.  (C2) Relation between `dilations` and `W`

    - Statement: If the `dilations` attribute is not empty, its length
      shall be equal to the number of spatial axes of `W`.

    - Rationale: [NOTE:] Dilations shall be defined for all spatial axes of `W`.

3.  Consistency between the shape of tensors `X`, `W`, `Y` and
    attributes `pads`, `dilations` and `strides`. [See constraint (3) of X](#shape_consist)

##### `group`: int (default value is 1) 

This parameter specifies the number of groups input channels and output
channels are divided into. When group is set to 1, this is the standard
convolution operation.

For information, when group is greater than 1, convolution is computed
for each group separately with a specific set of filters.


[NOTE:] I have kept the following text for it may be possible that we allow
`group` greater than 1... This limitation has been chosen to simplify
this first specification work. This constraint may be relaxed in the
actual Safety-Related Profile.</span>


The effect of the `group` attribute for a tensor with two spatial axes is depicted on the following figure:

![](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example/imgs/grouped_convolution.png)

(Taken from https://eli.thegreenplace.net/2018/depthwise-separable-convolutions-for-machine-learning)

  
For example, with `group` set to 2 and an input `X` and an output `Y`
with 6 channels, the input and output channels will be divided into 2
groups of 3 channels.

###### Constraints

1.  : Value domain

    - Statement: The number of groups shall be equal to 1.

    - Rationale: Only standard convolutions are considered in the SRP
      profile,

##### `kernel_shape`: list of ints (optional, default value is the list of sizes of the spatial axis of W 

This parameter specifies the shape of the convolution kernel `W`.

###### Constraints.

1.  Value domain

    - Statement: All elements of `kernel_shape` must be integers greater
      or equal to 1

    - Rationale: A size is always positive.

2.  Consistency between `W` and `[`kernel_shape

    - Statement: If set, the values of `kernel_shape` for a given axis
      must be equal to the size of `W` for that axis.

    - Rationale: `kernel_shape` represents the shape of `W`.

#### Outputs

##### `Y`

The size of the output `Y` will be
$(Y.B \times Y.C \times Y.H \times Y.W)$ where

- $Y.B$ is the number of batches

- $Y.C$ is the number of channels,

- $Y.H$ and $Y.W$ are the sizes of the output for the two spatial axis.

###### Constraints.

1.  Consistency between the shape of tensors `X`, `W`, `Y`, attributes
    `pads` and `strides`, [see constraint (3) of X](#shape_consist)

#### Formal specification

The following code specifies the `conv` operator using the Why3
language[^3].

###### Nota: the specification does not cover all attributes values. Currently, there is no padding (`pads` is not set and `auto_pad = NOTSET`) and `dilations` is not set.

``` ocaml
module Conv
  use int.Int
  use real.RealInfix
  use array.Array
  use int.ComputerDivision
  use real.Truncate
  use real.FromInt

  type input_tensor = {
    x: array real;
    x_h: int;
    x_w: int;
    x_b: int;
    x_c: int;
  }

    type convolution_kernel = {
    w: array real;
    w_h: int;
    w_w: int;
    w_c_in: int;
    w_c_out: int;
  }
  
  type bias_tensor = {
  b: array real;
  b_c: int;
  }
  
  type attributes = {
  stride: array int;
  pads: array int;
  auto_pad: int;
  dilations: array int; 
  }

  type output_tensor = {

   y_b: int;
   y_c: int;
   y_h: int;
   y_w: int;

  }

  function conv_size (out: output_tensor) : int =
    out.y_b * out.y_c * out.y_h * out.y_w

  predicate conv_result
    (inp: input_tensor)
    (kernel: convolution_kernel)
    (bias: bias_tensor)
    (attr: attributes)
    (out: output_tensor)
    (res: array real)
    (bi ci hi wi: int)
    (ci_in ki_h ki_w: int) =
     let y_idx = bi * (out.y_c * out.y_h * out.y_w) + ci * (out.y_h * out.y_w) + hi * out.y_w + wi in
     let x_h_idx = hi * attr.stride[0] + ki_h * attr.dilations[0] - attr.pads[0] in
     let x_w_idx = wi * attr.stride[1] + ki_w * attr.dilations[1] - attr.pads[1] in
                                
     (0 <= x_h_idx < inp.x_h /\ 0 <= x_w_idx < inp.x_w) ->
        let x_idx = bi * (inp.x_c * inp.x_h * inp.x_w) + ci_in * (inp.x_h * inp.x_w) + x_h_idx * inp.x_w + x_w_idx in
        let w_idx = ci * (kernel.w_c_in * kernel.w_h * kernel.w_w) + ci_in * (kernel.w_h * kernel.w_w) + ki_h * kernel.w_w + ki_w in
        res.elts (y_idx) = bias.b[ci] +. (inp.x[x_idx] *. kernel.w[w_idx])

  val conv (inp: input_tensor)(kernel: convolution_kernel)(bias: bias_tensor)(attr: attributes)(out: output_tensor): array real
    requires{inp.x_c = out.y_c = kernel.w_c_in = bias.b_c} 
    requires{out.y_h = (div (inp.x_h + attr.pads[0] + attr.pads[2] - (attr.dilations[0] * kernel.w_h)) attr.stride[0]) + 1}
    requires{out.y_w = (div (inp.x_w + attr.pads[1] + attr.pads[3] - (attr.dilations[1] * kernel.w_w)) attr.stride[1]) +1}
    requires { inp.x_h > 0 /\ inp.x_w > 0 /\ inp.x_c > 0 /\ inp.x_b > 0}
    requires{kernel.w_h > 0 /\ kernel.w_w > 0 /\ kernel.w_c_in > 0 /\ kernel.w_c_out > 0}
    requires { out.y_b > 0 /\ out.y_c > 0 /\ out.y_h > 0 /\ out.y_w > 0}
    requires { length inp.x = inp.x_h * inp.x_w * inp.x_c * inp.x_b}
    requires{length kernel.w = kernel.w_h * kernel.w_w * kernel.w_c_in * kernel.w_c_out}
    requires{inp.x_h >= kernel.w_h}
    requires{inp.x_w >= kernel.w_w}
    requires{length bias.b = bias.b_c}
    requires{length attr.stride = 2}
    requires{length attr.dilations = 2}
    requires{length attr.pads = 4}
    requires{forall i. 0 <= i < length attr.pads -> attr.pads[i] = 0}
    requires{forall j. 0 <= j < length attr.dilations -> attr.dilations[j] >= 1}
    requires{forall k. 0 <= k < length attr.stride -> attr.stride[k] >= 1}
    ensures { length result = conv_size out }
    ensures { forall bi ci hi wi ci_in ki_h ki_w: int.
              0 <= bi < out.y_b ->
              0 <= ci < out.y_c ->
              0 <= hi < out.y_h ->
              0 <= wi < out.y_w ->
              0 <= ci_in < kernel.w_c_in ->
              0 <= ki_h < kernel.w_h ->
              0 <= ki_w < kernel.w_w -> conv_result inp kernel bias attr out result bi ci hi wi ci_in ki_h ki_w }

end


module Test_conv
  use int.Int
  use real.RealInfix
  use array.Array
  use int.ComputerDivision
  use real.Truncate
  use real.FromInt
  use Conv

let test_conv () =
  let inp_x = Array.make 9 1.0 in
  let inp = { x = inp_x; x_h = 3; x_w = 3; x_b = 1; x_c = 1 } in
  
  let kernel_w = Array.make 4 0.0 in  
  let kernel = { w = kernel_w; w_h = 2; w_w = 2; w_c_in = 1; w_c_out = 1 } in
  
  let bias_b = Array.make 1 0.5 in 
  let bias = { b = bias_b; b_c = 1 } in
  let stride = Array.make 2 1 in  (* Stride of 1 *)
  let pads = Array.make 4 0 in  (* No padding *)
  let dilations = Array.make 2 1 in  (* Dilation of 1 *)
  let attr = { stride = stride; pads = pads; auto_pad = 0; dilations = dilations } in
  let out_h = (div (inp.x_h + pads[0] + pads[2] - (dilations[0] * kernel.w_h)) stride[0]) + 1 in
  let out_w = (div (inp.x_w + pads[1] + pads[3] - (dilations[1] * kernel.w_w)) stride[1]) + 1 in
  let out = { y_b = 1; y_c = 1; y_h = out_h ; y_w = out_w  } in
  (* Call the conv function *)
  let result = conv inp kernel bias attr out in
  let actual_result = result.elts 0 in
  assert { conv_result inp kernel bias attr out result 0 0 0 0 0 0 0} ;
  assert { actual_result =  0.5 } ;
  ()

end
```

Another formal specification of the `conv` operator using Frama-C
language[^4] is presented below.

``` objectivec
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Data Structures */
typedef struct {
    float *x;
    int x_h, x_w, x_b, x_c;
} input_tensor;

typedef struct {
    float *w;
    int w_h, w_w, w_c_in, w_c_out;
} convolution_kernel;

typedef struct {
    float *b;
    int b_c;
} bias_tensor;

typedef struct {
    int *stride;
    int *pads;
    int *dilations;
} attributes;

typedef struct {
    float *y;
    int y_b, y_c, y_h, y_w;
} output_tensor;
/*@
 requires \valid_read(pads + (0 .. 3));
 requires \valid_read(stride + (0 .. 1));
 requires \valid_read(result + (0 .. 3));
 requires x_h > 0 && x_w > 0 && w_h > 0 && w_w > 0 && y_h > 0 && y_w > 0;
 assigns result[0 .. 3];
 behavior empty_or_notset:
    assumes (auto_pad == "")  || (auto_pad == "NOTSET");
    ensures \forall integer i; 0 <= i < 4 ==> result[i] == pads[i];

behavior valid:
    assumes (auto_pad == "VALID") ;
    ensures \forall integer i; 0 <= i < 4 ==> result[i] == 0;

behavior same_upper:
    assumes (auto_pad == "SAME_UPPER") ;
    ensures \let pad_h = (y_h - 1) * stride[0] + w_h - x_h;
            \let pad_w = (y_w - 1) * stride[1] + w_w - x_w;
            ((pad_h  % 2 == 0) && (pad_w  % 2 == 0)) ==> 
                (result[0] == (pad_w / 2) && result[1] == (pad_h / 2) && result[2] == (pad_w / 2) && result[3] == (pad_h / 2)) &&
            (pad_h % 2 != 0) && (pad_w % 2 != 0) ==> 
            (result[0] == (pad_w / 2) && result[1] == (pad_h / 2) && result[2] == ((pad_w / 2) + 1) && result[3] == ((pad_h / 2) + 1));   

behavior same_lower:
    assumes (auto_pad == "SAME_LOWER");
    ensures \let pad_h = (y_h - 1) * stride[0] + w_h - x_h;
            \let pad_w = (y_w - 1) * stride[1] + w_w - x_w;
            ((pad_h % 2 == 0) && (pad_w % 2 == 0)) ==> 
                (result[0] == (pad_w / 2) &&  result[2] == (pad_w / 2) && result[1] == (pad_h / 2) && result[3] == (pad_h == 2)) &&
            ((pad_h % 2 != 0) && (pad_w % 2 != 0)) ==> 
                (result[0] == ((pad_w / 2) + 1) && result[1] == ((pad_h / 2) + 1) && result[2] == (pad_w / 2) && result[3] == (pad_h / 2));
complete behaviors empty_or_notset, valid, same_upper, same_lower;
disjoint behaviors empty_or_notset, valid, same_upper, same_lower;            
*/
void compute_pad(const char* auto_pad, int pads[4], int stride[2], int x_h, int x_w, int w_h, int w_w, int y_h, int y_w, int result[4]) {
    int pad_h, pad_w;

    if ((auto_pad == "")  || (auto_pad == "NOTSET")) {
        for (int i = 0; i < 4; i++) {
            result[i] = pads[i];
        }
    } else if ((auto_pad == "VALID")) {
        for (int i = 0; i < 4; i++) {
            result[i] = 0;
        }
    } else if ((auto_pad == "SAME_UPPER")) {
        pad_h = (y_h - 1) * stride[0] + w_h - x_h;
        pad_w = (y_w - 1) * stride[1] + w_w - x_w;

        if ((pad_h % 2 == 0) && (pad_w % 2 == 0)) {
            result[0] = result[2] = pad_w / 2;
            result[1] = result[3] = pad_h / 2;
        } else if ((pad_h % 2 != 0) && (pad_w % 2 != 0)) {
            result[0] = pad_w / 2;
            result[1] = pad_h / 2;
            result[2] = (pad_w / 2) + 1;
            result[3] = (pad_h / 2) + 1;
        }
    } else if ((auto_pad == "SAME_LOWER")) {
        pad_h = (y_h - 1) * stride[0] + w_h - x_h;
        pad_w = (y_w - 1) * stride[1] + w_w - x_w;

        if ((pad_h % 2 == 0) && (pad_w % 2 == 0)) {
            result[0] = result[2] = pad_w / 2;
            result[1] = result[3] = pad_h / 2;
        } else if ((pad_h % 2 != 0) && (pad_w % 2 != 0)) {
            result[0] = (pad_w / 2) + 1;
            result[1] = (pad_h / 2) + 1;
            result[2] = pad_w / 2;
            result[3] = pad_h / 2;
        }
    }
}

/* Function to compute the convolution */
//void compute_pad(int auto_pad, int *pads, int *stride, int x_h, int x_w, int w_h, int w_w, int y_h, int y_w, int *result);

/*@
  requires \valid_read(inp.x + (0..(inp.x_h*inp.x_w*inp.x_b*inp.x_c)-1));
  requires \valid_read(kernel.w + (0..(kernel.w_h*kernel.w_w*kernel.w_c_in*kernel.w_c_out)-1));
  requires \valid_read(bias.b + (0..bias.b_c-1));
  requires \valid_read(attr.stride+(0..1));
  requires \valid_read(attr.pads+(0..3));
  requires \valid_read(attr.dilations+(0..1));
  requires inp.x_c == out.y_c;
  requires out.y_c == kernel.w_c_in;
  requires kernel.w_c_in == bias.b_c;
  requires out.y_h == ((inp.x_h + attr.pads[0] + attr.pads[2] - (attr.dilations[0] * kernel.w_h )) / attr.stride[0]) + 1;
  requires out.y_w == ((inp.x_w + attr.pads[1] + attr.pads[3] - (attr.dilations[1] * kernel.w_w )) / attr.stride[1]) + 1;
  requires inp.x_h > 0 && inp.x_w > 0 && inp.x_c > 0 && inp.x_b > 0;
  requires kernel.w_h > 0 && kernel.w_w > 0 && kernel.w_c_in > 0 && kernel.w_c_out > 0;
  requires bias.b_c > 0;
  requires out.y_h > 0 && out.y_w > 0 && out.y_c > 0 && out.y_b > 0;
  requires inp.x_h >= kernel.w_h;
  requires inp.x_w >= kernel.w_w;
  requires \forall integer i; 0 <= i < 4 ==> attr.pads[i] >= 0;
  requires \forall integer i; 0 <= i < 2 ==> attr.dilations[i] >= 1;
  requires \forall integer i; 0 <= i < 2 ==> attr.stride[i] >= 1;


  assigns out.y[0..(out.y_b * out.y_c * out.y_h * out.y_w)-1];

  ensures \forall integer bi, ci, hi, wi, ci_in, ki_h, ki_w; 
            0 <= bi < out.y_b ==>
                0 <= ci < out.y_c ==>
                    0 <= hi < out.y_h ==>
                        0 <= wi < out.y_w ==>  
                            0 <= ci_in <kernel.w_c_in ==>
                                0 <= ki_h < kernel.w_h ==>
                                    0 <= ki_w < kernel.w_w ==> 
                                        (0 <= hi * attr.stride[0] + ki_h * attr.dilations[0] - attr.pads[0]) && 
                                        (hi * attr.stride[0] + ki_h * attr.dilations[0] - attr.pads[0]  < inp.x_h) && 
                                        (0 <= wi * attr.stride[1] + ki_w * attr.dilations[1] - attr.pads[1]) && 
                                        (wi * attr.stride[1] + ki_w * attr.dilations[1] - attr.pads[1] < inp.x_w) ==>
                                            out.y[bi * (out.y_c * out.y_h * out.y_w) + ci * (out.y_h * out.y_w) + hi * out.y_w + wi] == inp.x[bi * (inp.x_c * inp.x_h * inp.x_w) + ci_in * (inp.x_h * inp.x_w) + (hi * attr.stride[0] + ki_h * attr.dilations[0] - attr.pads[0]) * inp.x_w + ( wi * attr.stride[1] + ki_w * attr.dilations[1] - attr.pads[1])] * kernel.w[ci * (kernel.w_c_in * kernel.w_h * kernel.w_w) + ci_in * (kernel.w_h * kernel.w_w) + ki_h * kernel.w_w + ki_w] + bias.b[ci];
                          
              
                          
                           
                                


  */
float* conv(input_tensor inp, convolution_kernel kernel, bias_tensor bias, attributes attr, output_tensor out) {
    
    out.y_h = ((inp.x_h + attr.pads[0] + attr.pads[2] - (attr.dilations[0] * kernel.w_h )) / attr.stride[0]) + 1;
    out.y_w = ( (inp.x_w + attr.pads[1] + attr.pads[3] - (attr.dilations[1] * kernel.w_w )) / attr.stride[1]) +1;
    int y_size = out.y_b * out.y_c * out.y_h * out.y_w;
    out.y = (float *)malloc(y_size * sizeof(float));

    if (out.y == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    // Compute padding
   // compute_pad(attr.auto_pad, attr.pads, attr.stride, inp.x_h, inp.x_w, kernel.w_h, kernel.w_w, out.y_h, out.y_w, attr.pads);

    // Initialize result tensor to bias values
    for (int bi = 0; bi < out.y_b; ++bi) {
        for (int ci = 0; ci < out.y_c; ++ci) {
            for (int hi = 0; hi < out.y_h; ++hi) {
                for (int wi = 0; wi < out.y_w; ++wi) {
                    int y_idx = bi * (out.y_c * out.y_h * out.y_w) + ci * (out.y_h * out.y_w) + hi * out.y_w + wi;
                    out.y[y_idx] = bias.b[ci];
                }
            }
        }
    }

    // Convolution computation
    for (int bi = 0; bi < out.y_b; ++bi) {
        for (int ci = 0; ci < out.y_c; ++ci) {
            for (int hi = 0; hi < out.y_h; ++hi) {
                for (int wi = 0; wi < out.y_w; ++wi) {
                    int y_idx = bi * (out.y_c * out.y_h * out.y_w) + ci * (out.y_h * out.y_w) + hi * out.y_w + wi;

                    for (int ci_in = 0; ci_in < kernel.w_c_in; ++ci_in) {
                        for (int ki_h = 0; ki_h < kernel.w_h; ++ki_h) {
                            for (int ki_w = 0; ki_w < kernel.w_w; ++ki_w) {
                                int x_h_idx = hi * attr.stride[0] + ki_h * attr.dilations[0] - attr.pads[0];
                                int x_w_idx = wi * attr.stride[1] + ki_w * attr.dilations[1] - attr.pads[1];

                                if (x_h_idx >= 0 && x_h_idx < inp.x_h && x_w_idx >= 0 && x_w_idx < inp.x_w) {
                                    int x_idx = bi * (inp.x_c * inp.x_h * inp.x_w) + ci_in * (inp.x_h * inp.x_w) + x_h_idx * inp.x_w + x_w_idx;
                                    int w_idx = ci * (kernel.w_c_in * kernel.w_h * kernel.w_w) + ci_in * (kernel.w_h * kernel.w_w) + ki_h * kernel.w_w + ki_w;

                                    if (x_idx < inp.x_h * inp.x_w * inp.x_c * inp.x_b && w_idx < kernel.w_h * kernel.w_w * kernel.w_c_in * kernel.w_c_out) {
                                        out.y[y_idx] += inp.x[x_idx] * kernel.w[w_idx];
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return out.y;
}
```

# Graph execution semantics

<div class="note">

[NOTE:] Elements of the execution semantics is given on the [IR (Intermediate
Representation) page](https://onnx.ai/onnx/repo-docs/IR.html) of the
ONNX web site. In addition, a Python “reference implementation” is also
provided (see <https://onnx.ai/onnx/api/reference.html>). The source
code of this implementation can be found at
<https://github.com/onnx/onnx/tree/main/onnx/reference>.

Very informally, the semantics is pretty simple: each operator (or
function) is called according to its position in the topological sorting
of the operators. The topological order is a partial order that ensures
that an operator is executed only when its inputs are available. Being a
partial order, it means that several valid orders exist for a given
graph. Normally (?) each order should generate the same result, even in
the presence of floating point operations.

The Python code to execute a graph is given in class
[`ReferenceEvaluator`](https://github.com/onnx/onnx/blob/main/onnx/reference/reference_evaluator.py)).
After having processed the inputs and the initializers (i.e., fed the
`results` dictorionary with these data), the nodes are executed in
sequence. For each operator, the interpretor checks that its inputs are
in the `results` dictionary. If they are not, an error is raised (if the
operators are listed in topological order, this situation should not
occur). Otherwise, the operator is simply executed (method `run`) with
or without a context (composed of the current results) depending on the
type of operators. (Check that this does not create a dependency to the
total order of operators.)

</div>

### Informal specification

<div class="note">

[NOTE:] The semantics of an ONNX model is given in Section "Model Semantics" of
the [Intermediate
Representation](https://github.com/onnx/onnx/blob/main/docs/IR.md) page.
Basically, an inference-model is a stateless function (except possibly
for some specific nodes such as a random-generation node) represented by
an acyclic `graph` of nodes. The `graph` is mainly represented by a set
of inputs and outputs and a topologically sorted list of nodes. Each
node represents a call to an operator or a function. A `function` is
itself a graph.

Note that the types of inputs and outputs are not systematically
required because they can be inferred. In our case, I guess that we will
forbib shape inference and rely on static tensor shapes (or, at least,
shape inference can be bone before serializing the model). The proecss
of shape inference is described in Section  [ONNX Shape
Inference](https://onnx.ai/onnx/repo-docs/ShapeInference.html).

</div>

### Formal specification

*To be completed.*

[^1]: At least in a first phase...

[^2]: Note: in the ONNX runtime implementation, the padding value may be
    negative, which corresponds to reducing the size of the tensor.

[^3]: See [Why3 documentation](https://www.why3.org/)

[^4]: See [Frama-C
    documentation](https://www.frama-c.com/html/documentation.html)
