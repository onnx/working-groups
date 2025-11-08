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
The purpose of the Broadcast is to produce a set of output tensors presenting a common shape, that is a common number of dimensions $nZ$ and for each dimension $i$ a common size $dZ_i$.

#### Constraints

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

