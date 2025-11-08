# `broadcast` operator or functionality embeeded in another operator
### Contents
- `Broadcast` operator or functionality for any type.
## `Broadcast`  `(anytype)`

### Signature
`Z1, ..., ZN = Broadcast(X1, ... , XN)`
where

- `N`: The number of input tensors
- `X1`: first input tensor
- ...
- `XN`: last input tensor
- `Z1`: first output tensor
- ...
- `ZN`: last ouput tensor

### Purpose
The purpose of the Broadcast is to produce a set of output tensors presenting a common shape, that is a common number of dimensions $nZ$ and for each dimension $i$ a common size $dZ_i$. The objectives of the operation are:
- to provide to all tensors a number of dimensions equal to the largest number of dimensions among the input tensors and
- for each dimension to provide to all tensors a dimension size equal to the maximum of the dimension sizes of all the input tensors.
When the number of dimensions is increased for a tensor:
- the dimensions to be completed are those of lower indexes,
- those dimensions are set to a dimension size equal to 1 and,
- the indexes allowing access to the elements of the tensor are shifted consequently.
When the dimension size is increased for a tensor:
- the additional elements are equal to the elements with index 1 for this dimension.

### Notations
Let's note the tensors with already a common number of dimensions, $nY$, but with still different dimension sizes $Y1$, ... $YN$.

### Constraints

$dY_1$, ...$dY_{nY}$ are reciprocaly defined as $dY_1 = \max_{m \in [1, N] } dYm_1$, ...  $dY_{nY} = \max_{m \in [1, N] } dYm_{nY}$ where $dYm_1$, ... $dY_{nY}$ are the dimensions of the $m$ th input tensor with already the common number of dimensions.

The following constraint applies to the Numpy boardcasting:

| Constraint    | Statement | Origin |
| -------- | ------- | ------- |
| `C1` | $\forall m \in [1, N], \forall i \in [1, nY]$ either $dYm_i = dY_i$  or $dYm_i = 1$| https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md|
| ...  | ... | ... |

### Functionality

Assuming those restrictions hold, the relation between elements of boardcasted tensors and input tensors are:

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... z^n_{i,j,k,l...} = x^n_{f(i,I_n,I),f(j,J_n,J),f(k,K_n,K),f(l,L_n,L)...}$

Where $f(.,.,.)$ is a function such that:

$f(a,B,C) = a$ if $B=C$ and $f(a,B,C) = 1$ if $B=1$.

Note that other cases, i.e. $B \neq C$ and $B \neq 1$, don't need to be specified because of restrictions `RI`, `RJ`, `RK`, `RL`... 

