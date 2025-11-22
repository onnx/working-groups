# Contents

- **Max** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)
- **Max** operator for types [bfloat16, float16, float, double](#float)

Based on ONNX documentation version 13.

# Link to ONNX description

https://onnx.ai/onnx/operators/onnx__Max.html

<a id="int"></a>
# **Max** (int, int)

## Signature
Definition of operator $\text{Max}$ signature:
$Y = \text{Max}(X0, ... , XL)$

where:
- $X0$, ... , $XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: result of the element-wise maximum among $X0$, ... , $XL$

## Restrictions

The following restrictions apply to the **Max** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

 ## Informal specification
 
Operator **Max** is applied on $Z0$,... , $ZL$ where $Z0$,..., $ZL$ is the broadcasted form of $X0$,..., $XL$,
i.e. ($Z0$, ... , $ZL$) = Broadcast($X0$, ... , $XL$) cf. [broadcast](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md). 
Thanks to broadcasting, all $Zm$ for $m \in [0, L]$ have a common number of dimensions $nZ$. Moreover, they have in each dimension $j \in [0, nZ-1]$ the same number of elements $dZ_j$.

The maximum is taken element wize among the elements of the different input tensors presenting identical indexes.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$Y[i] = \max_{m \in [0, L] } Zm[i]$$

The maximum shall comply with the mathematical definition of the function denoted $\max$.

## Error conditions

The following error condition applies to **Max** operator:

| Error    | Statement | Origin |
| -------- | ------- | ------- |
| `E1` | $X0$,..., $XL$ not broadcastable | [broadcast](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md)|
| `E2` | Shape of $Y$ is not with $nZ$ dimensions or there is a dimension $j$ with a number of elements diferent to $dZ_j$| Explicit shape `[R2]` combined with broadcast | 

## Inputs

### $\text{X0,...,XL}$: `int tensors`
Tensors among which the maximum is to be taken element-wise.

#### Constraints
No applicable constraints.

## Outputs

### $\text{Y}$: `int tensor`

Tensor $Y$ is the element-wise result of the maximum among $X0$,..., $XL$.

#### Constraints
No applicable constraints.

## Attributes

Operator $\text{Max}$ has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy
Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

Maximum is exact under the defined semantics; error is not introduced by the operator itself:

### Error Propagation
For integer inputs modeled without error symbols, $Y_{\textit{err}}^{\textit{propag}} = [0]$.
### Error Introduction
Error introduction for int arithmetic is null:
 $Y_{\textit{err}}^{\textit{intro}} = [0]$.
### Unit Verification
TODO

<a id="float"></a>
# **Max** (float, float)

## Signature
Definition of operator $\text{Max}$ signature:
$Y = \text{Max}(X0, ... , XL)$

where:
- $X0$, ... , $XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: result of the element-wise maximum among $X0$, ... , $XL$ after broadcasting

## Restrictions

The following restrictions apply to the **Max** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

 ## Informal specification
 
Operator **Max** is applied on $Z0$,... , $ZL$ where $Z0$,..., $ZL$ is the broadcasted form of $X0$,..., $XL$,
i.e. ($Z0$, ... , $ZL$) = Broadcast($X0$, ... , $XL$) cf. [broadcast](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md). 
Thanks to broadcasting, all $Zm$ for $m \in [0, L]$ have a common number of dimensions $nZ$. Moreover, they have in each dimension $j \in [0, nZ-1]$ the same number of elements $dZ_j$.

The maximum is taken element wize among the elements of the different input tensors presenting identical indexes.

For any [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) $i$:

$$Y[i] = \max_{m \in [0, L] } Zm[i]$$

The maximum shall comply with the mathematical definition of the function denoted $\max$.

Note that the types considered here have special values that do not inherit naturally the order defined on the real numbers (>) underlying the maximum function, i.e. Inf, 0+, 0-, NaN. For those values the following order shall be assumed when considering the maximum function:

NaN > Inf > any positive number > 0+ > 0 > 0- > any negative number > -Inf. 

## Error conditions

The following error condition applies to **Max** operator:

| Error    | Statement | Origin |
| -------- | ------- | ------- |
| `E1` | $X0$,..., $XL$ not broadcastable | [broadcast](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md)|
| `E2` | Shape of $Y$ is not with $nZ$ dimensions or there is a dimension $j$ with a number of elements diferent to $dZ_j$| Explicit shape `[R2]` combined with broadcast | 

## Inputs

### $\text{X0,...,XL}$: `float tensors`
Tensors among which the maximum is to be taken element-wise.

#### Constraints
No applicable constraints.

## Outputs

### $\text{Y}$: `float tensor`

Tensor $Y$ is the element-wise result of the maximum among $X0$,..., $XL$ after broadcasting.

#### Constraints
No applicable constraints.

## Attributes

Operator $\text{Max}$ has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy
Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

Maximum is exact under the defined semantics; error is not introduced by the operator itself but the operator propagates errors on its inputs:

### Error Propagation
For all valid indexes $i$,

  $$
  |Y_{\textit{err}}^{\textit{propag}}[i]| \leq \max_{m \in [0, L]} \left|Z_{\textit{err}}[i]\right|
  $$

### Error Introduction
Error introduction for float arithmetic is null:
 $Y_{\textit{err}}^{\textit{intro}} = [0]$.
### Unit Verification
TODO
