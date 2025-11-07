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

The maximum is taken element wize among the elements of the different input tensors presenting identical indexes. The maximum shall comply with the mathematical definition of the function denoted $\max$. In consequence, denoting $Zm[i_1,...,i_{nZ}]$ and $Y[i_1,...,i_{nZ}]$ the elements of reciprocally the $m$th broadcasted input tensor $Zm$ and the output tensor $Y$, the following relation shall hold:

$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} = \max_{n \in [1, N] } z^n_{i,j,k,l...}$

where $z^n_{i,j,k,l...}$ is an element of $Z^n$.

##### Numpy boardcasting
$I$, $J$, $K$, $L$... are reciprocaly defined as $I = \max_{n \in [1, N] } I_n$, $J = \max_{n \in [1, N] } J_n$, $K = \max_{n \in [1, N] } K_n$, $L = \max_{n \in [1, N] } L_n$... where $I_n$, $J_n$, $K_n$, $L_n$... are the dimensions of the $n$ th input tensor.

The following restrictions apply to the Numpy boardcasting:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `RI` | $\forall n \in [1, N]$ either $I_n = I$  or $I_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RJ` | $\forall n \in [1, N]$ either $J_n = J$  or $J_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RK` | $\forall n \in [1, N]$ either $K_n = K$  or $K_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RL` | $\forall n \in [1, N]$ either $L_n = L$  or $L_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| ...  | ... | ... |

Assuming those restrictions hold, the relation between elements of boardcasted tensors and input tensors are:

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... z^n_{i,j,k,l...} = x^n_{f(i,I_n,I),f(j,J_n,J),f(k,K_n,K),f(l,L_n,L)...}$

Where $f(.,.,.)$ is a function such that:

$f(a,B,C) = a$ if $B=C$ and $f(a,B,C) = 1$ if $B=1$.

Note that other cases, i.e. $B \neq C$ and $B \neq 1$, don't need to be specified because of restrictions `RI`, `RJ`, `RK`, `RL`... 

#### Properties
From the definition of the maximum we have two properties:

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} \geq z^n_{i,j,k,l...}$

$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... \exists n \in [1, N] ~~| ~~~~ y_{i,j,k,l...} = z^n_{i,j,k,l...}$

The same properties written in function of unboardcasted inputs are:

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} \geq x^n_{f(i,I_n,\max_{m \in [1, N] } I_m),f(j,J_n,\max_{m \in [1, N] } J_m),f(k,K_n,\max_{m \in [1, N] } K_m),f(l,L_n,\max_{m \in [1, N] } L_m)...}$

$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... \exists n \in [1, N] ~~| ~~~~ y_{i,j,k,l...} = x^n_{f(i,I_n,\max_{m \in [1, N] } I_m),f(j,J_n,\max_{m \in [1, N] } J_m),f(k,K_n,\max_{m \in [1, N] } K_m),f(l,L_n,\max_{m \in [1, N] } L_m)...}$


