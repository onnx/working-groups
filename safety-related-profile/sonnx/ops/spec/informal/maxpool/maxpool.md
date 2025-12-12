# Contents

- **MaxPool** operator for type [real](#real)
- **MaxPool** operator for types [float16, float, double](#float)
- **MaxPool** operator for types [int8, uint8](#int)

Based on ONNX [Op version 22](https://onnx.ai/onnx/operators/onnx__MaxPool.html).

<a id="real"></a>
# **MaxPool** (real, real)

## Signature
Definition of operator $\text{MaxPool}$ signature:
$Y = \text{MaxPool}(A, B)$

where:
- $X$: input tensor
- $Y$: output tensor containing max velue selected from $X$
- $Indices$: output tensor containing the indices in $X$ from where the max values are taken.
   
## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **MaxPool** operator:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a> | Input tensor `X` has 2 spatial axes | Transient |
| `[R2]` <a id="R2"></a> | Attribute `auto_pad` is set to `NOTSET`  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value)
| `[R3]` <a id="R3"></a> | Attribute `ceil_mode` is set to 0 ??????  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value)
| `[R4]` <a id="R4"></a> | Attribute `storage_order` is set to 0  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value)

## Informal specification

Operator **MaxPool** consumes an input tensor $X$ and applies max pooling across the tensor according to kernel sizes, stride sizes, and pad lengths, max pooling consisting of computing the max on all values of a subset of the input tensor according to the kernel size and downsampling the data into the output tensor $Y$.

Operator **MaxPool** also stores the indices of input tensor $X$ from which the max values are taken in $Indices$. The index values are those of a flatten 1-D view of $X$  


The effect of the operator is illustrated on the following examples.

### Example 1

graph test-maxpool (
  %x[DOUBLE, 1x1x8x8]
) {
  %y, %Indices = MaxPool[auto_pad = 'NOTSET', dilations = [1, 1], kernel_shape = [3, 3], pads = [0, 0, 0, 0], strides = [1, 1]](%x)
  
  return %y, %Indices

}

$X$ shape: (1, 1, 8, 8)

$X$:

[[[[ 5.67591154 -0.04859958  2.94203104  3.70327292  2.47014306
     4.12455586  5.81838665  1.84118807]

   [-0.05267874  2.75227858  2.16608732  4.03416243  1.28184638
     4.81748948  4.64878412  3.31626988]
    
   [ 3.55427648  0.39997585  4.45761508  4.82722666  0.18843372
     0.49564314  7.96647029  4.82851447]
  
   [ 1.52417623  2.28965587  0.36251913  1.64413983  4.67267459
     3.73167179  2.20052118  2.06720836]
  
   [-1.22446366 -0.86469519  6.01461967 -1.08813165  2.11920055
     0.78561867  0.29834533  1.94499626]
  
   [ 1.57776732  3.64260188  3.47181319  4.83723727  1.49868674
     3.27683692  2.42625178  0.4401565 ]

   [ 6.8972704   5.51113868  5.99293336  4.24088721  1.94993561
    -0.04040625  3.07940675  3.06769141]

   [ 3.1299626   4.5546675   3.5008191   2.06181403  3.27400104
     6.70386189  0.92777015 -1.29092574]]]]

$Y$ shape: (1, 1, 6, 6)

$Y$: 

[[[[5.67591154 4.82722666 4.82722666 4.82722666 7.96647029 7.96647029]
   [4.45761508 4.82722666 4.82722666 4.82722666 7.96647029 7.96647029]
   [6.01461967 6.01461967 6.01461967 4.82722666 7.96647029 7.96647029]
   [6.01461967 6.01461967 6.01461967 4.83723727 4.67267459 3.73167179]
   [6.8972704  6.01461967 6.01461967 4.83723727 3.27683692 3.27683692]
   [6.8972704  5.99293336 5.99293336 6.70386189 6.70386189 6.70386189]]]]

$Indices$ shape: (1, 1, 6, 6)

$Indices$: 

[[[[ 0 19 19 19 22 22]

[18 19 19 19 22 22]

[34 34 34 19 22 22]

[34 34 34 43 28 29]

[48 34 34 43 45 45]

[48 50 50 61 61 61]]]]


## Error conditions
No error conditions.

## Inputs

### $\text{X}$: `real`

`X` is the input tensor from which the max values are selected. 


#### Constraints

 - `[C1]` <a id="C1ia"></a> First constraint on $X$
   - Statement: Description of the first constraint on $X$
    
## Outputs

### $\text{Y}$: `real`



#### Constraints

 - `[C1]` <a id="C1iy"></a> First constraint on $Y$
   - Statement: Description of the first constraint on $Y$

### $\text{Indices}$: `int64`

*Output description*

#### Constraints

 - `[C1]` <a id="C1iy"></a> First constraint on $Indices$
   - Statement: Description of the first constraint on $Indices$


## Attributes

### $\text{auto\_pad}$: `string`

*Attribute description*

### $\text{ceil\_mode}$: `int`

*Attribute description*

### $\text{dilations}$: `list of ints`

*Attribute description*

### $\text{kernel\_shape}$: `list of ints`

*Attribute description*

### $\text{pads}$: `list of ints`

*Attribute description*

### $\text{storage\_order}$: `int`

*Attribute description*

### $\text{strides}$: `list of ints`

*Attribute description*





#### Constraints

 - `[C1]` <a id="C1iattr"></a> [See constraint (C1) on A](#C1ia). First constraint on $ATTR$
   - Statement: Description of the first constraint on $ATTR$
