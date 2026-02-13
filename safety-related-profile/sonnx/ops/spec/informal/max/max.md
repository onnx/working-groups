# Contents
- **Max** operator for type [real](#real)
- **Max** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)
- **Max** operator for types [float16, float, double](#float)

Based on ONNX documentation [Max version 13](https://onnx.ai/onnx/operators/onnx__Max.html).

<a id="real"></a>
# **Max** (real, ..., real)

## Signature
$Y = \text{Max}(X0, ... , XL)$

where:
- $X0$, ... , $XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: result of the element-wise maximum among $X0$, ... , $XL$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Max** operator.

## Informal specification
 
Operator **Max** is applied on $\dot X0$,... , $\dot XL$ where $\dot X0$,..., $\dot XL$ is the broadcasted form of $X0$,..., $XL$,
i.e. ($\dot X0$, ... , $\dot XL$) = Broadcast($X0$, ... , $XL$), cf. [broadcast](./../common/broadcast/broadcast.md). 

Thanks to broadcasting, all $\dot Xm$ for $m \in [0, L]$ have the same shape.

The maximum is taken element-wise among the elements of the different broadcasted tensors presenting identical indexes.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$Y[i] = \max_{m \in [0, L] } \dot Xm[i]$$

The maximum shall comply with the mathematical definition of the function denoted $\max$.

## Error conditions
No error conditions for **Max**. 

## Inputs

### $\text{X0,...,XL}$: real tensors
Tensors among which the maximum is to be taken element-wise after broadcasting.
#### Constraints

- `[C1]` <a id="C1ra"></a>Broadcasting  
  - Statement: Tensors $X0$,..., $XL$ shall be  broadcastable.  

- `[C2]` <a id="C2ra"></a> Shape consistency  
  - Statement: Tensors $\dot Xm$ and $Y$ shall have the same shape.  

## Outputs

### $\text{Y}$: real tensor

Tensor $Y$ is the element-wise result of the maximum among broadcasted $X0$,..., $XL$.

#### Constraints
 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C2ra) on tensors $\dot Xm$.

## Attributes

Operator $\text{Max}$ has no attribute.


<a id="float"></a>
# **Max** (float, ..., float)
where float is in {float16, float, double}

## Signature
$Y = \text{Max}(X0, ... , XL)$

where:
- $X0$, ... , $XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: result of the element-wise maximum among $X0$, ... , $XL$ after broadcasting

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Max** operator.


 ## Informal specification
 
Operator **Max** is applied on $\dot X0$,... , $\dot XL$ where $\dot X0$,..., $\dot XL$ is the broadcasted form of $X0$,..., $XL$,
i.e. ($\dot X0$, ... , $\dot XL$) = Broadcast($X0$, ... , $XL$), cf. [broadcast](./../common/broadcast/broadcast.md). 

Thanks to broadcasting, all $\dot Xm$ for $m \in [0, L]$ have the same shape.

The maximum is taken element-wise among the elements of the different broadcasted tensors presenting identical indexes.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$Y[i] = \max_{m \in [0, L] } \dot Xm[i]$$

The maximum shall comply with the mathematical definition of the function denoted $\max$.

Note that the types considered here have special values that do not inherit naturally the order defined on the real numbers (>) underlying the maximum function, i.e. Inf, 0, 0-, NaN. For those values the following order shall be assumed when considering the maximum function:

Inf > any positive number > 0 > -0 > any negative number > -Inf. 

NaN is an absorbing element for **Max**. 

Note: In the ONNX runtime implementation, when 0 and -0 are compared, **Max** returns the first value : **Max**(0,-0) = 0 and **Max**(-0,0)=0-.  

## Error conditions
No error conditions for **Max**. 

## Inputs

### $\text{X0,...,XL}$: float tensors
Tensors among which the maximum is to be taken element-wise.

#### Constraints
- `[C1]` <a id="C1fa"></a>Broadcasting  
  - Statement: Tensors $X0$,..., $XL$ shall be  broadcastable.  

- `[C2]` <a id="C2fa"></a> Shape consistency  
  - Statement: Tensors $\dot Xm$ and $Y$ shall have the same shape.  

## Outputs

### $\text{Y}$: float tensor

Tensor $Y$ is the element-wise result of the maximum among among broadcasted $X0$,..., $XL$.

#### Constraints
 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C2fa) on tensors $\dot Xm$.

## Attributes

Operator $\text{Max}$ has no attribute.

<a id="int"></a>
# **Max** (int, ..., int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}

## Signature
$Y = \text{Max}(X0, ... , XL)$

where:
- $X0$, ... , $XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: result of the element-wise maximum among $X0$, ... , $XL$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Max** operator.

## Informal specification
 
Operator **Max** is applied on $\dot X0$,... , $\dot XL$ where $\dot X0$,..., $\dot XL$ is the broadcasted form of $X0$,..., $XL$,
i.e. ($\dot X0$, ... , $\dot XL$) = Broadcast($X0$, ... , $XL$), cf. [broadcast](./../common/broadcast/broadcast.md). 

Thanks to broadcasting, all $\dot Xm$ for $m \in [0, L]$ have the same shape.

The maximum is taken element-wise among the elements of the different broadcasted tensors presenting identical indexes.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$Y[i] = \max_{m \in [0, L] } \dot Xm[i]$$

The maximum shall comply with the mathematical definition of the function denoted $\max$.

## Error conditions
No error conditions for **Max**. 

## Inputs

### $\text{X0,...,XL}$: int tensors
Tensors among which the maximum is to be taken element-wise after broadcasting.
#### Constraints

- `[C1]` <a id="C1ia"></a>Broadcasting  
  - Statement: Tensors $X0$,..., $XL$ shall be  broadcastable.  

- `[C2]` <a id="C2ia"></a> Shape consistency  
  - Statement: Tensors $\dot Xm$ and $Y$ shall have the same shape.  

## Outputs

### $\text{Y}$: int tensor

Tensor $Y$ is the element-wise result of the maximum among broadcasted $X0$,..., $XL$.

#### Constraints
 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C2ia) on tensors $\dot Xm$.

## Attributes

Operator $\text{Max}$ has no attribute.


