# `max` operator
### Contents
- `Maximum` operator for a type on which an order is defined.
## `Max`  `(type on which an order is defined, i.e. bfloat16, double, float, float16, int16, int32, int64, int8, uint16, uint32, uint64, uint8)`

### Signature
`Y = Max(X1, ... , XN)`
where

- `N`: 
- `X1`: first input tensor
- ...
- `XN`: last input tensor
- `Y`: output tensor

#### Constraints
The following constraints apply to the `Max` operator for the SONNX profile:

| Constraint    | Statement | Origin |
| -------- | ------- | ------- |
| `C1` | `N` is an integer between 1 and 2147483647 | ONNX documentation: https://onnx.ai/onnx/operators/onnx__Max.html#l-onnx-doc-max |
| `C2` | Numpy broadcasting rules shall be applicable to `Y`, `X1`, ... , `XN` | ONNX documentation: https://onnx.ai/onnx/operators/onnx__Max.html#l-onnx-doc-max and https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md |

 #### Informal specification

The result tensor $Y$ depends on the broadcasted values $Z1$, ... , $ZN$ of the input tensors $X1$, ... , $XN$, cf. https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/broadcast/broadcast.md . Because of broadcasting all $Zi$ for $i \in [1, N]$ have a common number of dimensions $nZ$. Moreover, they have in each dimension $j \in [1, nZ]$ the same number of elements $dZ_j$.

The maximum is taken element wize among the elements of the different input tensors presenting identical indexes. The maximum shall comply with the mathematical definition of the function denoted $\max$. In consequence, denoting $Zm[i_1,...,i_{nZ}]$ and $Y[i_1,...,i_{nZ}]$ the elements, identified by indexes $i_1,...,i_{nZ}$, of reciprocally the $m$ th broadcasted input tensor $Zm$ and the output tensor $Y$, the following relation shall hold:

$$\forall i_1 \in [1, dZ_1], ... \forall i_{nZ} \in [1, dZ_{nZ}] ~~~~ Y[i_1,...,i_{nZ}] = \max_{m \in [1, N] } Zm[i_1,...,i_{nZ}]$$

Note some 


