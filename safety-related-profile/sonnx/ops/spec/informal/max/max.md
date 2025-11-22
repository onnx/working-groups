# Contents

- **Max** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)
- **Max** operator for types [bfloat16, float16, float, double](#float)

Based on ONNX documentation version 13.

# Link to ONNX description

https://onnx.ai/onnx/operators/onnx__Max.html

<a id="int"></a>
- `Maximum` operator for a type on which an order is defined.
## `Max`  `type on which an order is defined`

### Signature
$Y = \text{Max}(X0, ... , XL)$

where
- $X0$, ... ,$XL$ input tensors with L $\in [0, 2^{31}-1[$
- $Y$: output tensor

### Link to ONNX description



### Constraints
The following constraints apply to the `Max` operator for the SONNX profile:


 ### Informal specification
> L'opérateur max est appliqué sur Z0,..? ZL où Z0,...,ZL est la "version" broadcasté de X0..XL.

The result tensor $Y$ depends on the broadcasted values $Z0$, ... , $ZL$ of the input tensors $X0$, ... , $XL$, i.e. ($Z0$, ... , $ZL$) = Broadcast($X0$, ... , $XL$) cf. [broadcast](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md). 

Thanks to broadcasting, all $Zi$ for $i \in [0, L]$ have a common number of dimensions $nZ$. Moreover, they have in each dimension $j \in [0, nZ-1]$ the same number of elements $dZ_j$.


The maximum is taken element wize among the elements of the different input tensors presenting identical indexes.

For any tensor index $i$:

$$Y[i] = \max_{m \in [0, L] } Zm[i]$$

 The maximum shall comply with the mathematical definition of the function denoted $\max$.

> Traiter type par type. Donc definir max entier, max flottant,...
Note that some types such as `bfloat16`, `double`, `float`, `float16` have special values that do not inherit naturally the order defined on the real numbers (>) underlying the maximum function, i.e. Inf, 0+, 0-, NaN. For those values the following order shall be assumed when considering the maximum function:

NaN > Inf > any positive number > 0+ > 0 > 0- > any negative number > -Inf. 


| Constraint    | Statement | Origin |
| -------- | ------- | ------- |
| `C1` | Broadcasting rules shall be applicable to `Y`, `X1`, ... , `XN` | ONNX documentation: https://onnx.ai/onnx/operators/onnx__Max.html#l-onnx-doc-max and https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md |


> Il manque la partie inputs et outputs 
