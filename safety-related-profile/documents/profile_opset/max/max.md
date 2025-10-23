# `max` operator
### Contents
- `Maximum` operator for any type on which an order is defined.
## `Max`  `(type on which an order is defined)`

### Signature
`Y = max(X^1, ... , X^N)`
where

- `N`: 
- `X^1`: first input tensor
- ...
- `X^N`: last input tensor
- `Y`: output tensor

#### Restrictions
The following restrictions apply to the `max` operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | `N` is an integer between 1 and 2147483647 | Transient |
| `R2` | Numpy boardcasting rules shall be applicable to `Y`, `X^1`, ... , `X^N` | https://numpy.org/doc/stable/user/basics.broadcasting.html |

 #### Informal specification

The result tensor $Y$ is based on the boardcasted values $Z^1$, ... , $Z^N$ of the input tensors $X^1$, ... , $X^N$.

Let, $I$, $J$, $K$, $L$... be the common boardcasted dimensions of all tensors, elements $y_{i,j,k,l...}$ of $Y$ shall comply with:

$\forall i \in \{ 1,...I \}, \forall j \in \{ 1,...J \}, \forall k \in \{ 1,...K \}, \forall l \in \{ 1,...L \}... ~~~~ y_{i,j,k,l...} = \max_{n \in \{ 1,...N \} } z^n_{i,j,k,l...}$

where $z^n_{i,j,k,l...}$ is an element of $Z^n$.

##### Numpy boardcasting
$I$, $J$, $K$, $L$... are reciprocaly defined as $I = \max_{n \in \{ 1,...N \} } I_n$, $J = \max_{n \in \{ 1,...N \} } J_n$, $K = \max_{n \in \{ 1,...N \} } K_n$, $L = \max_{n \in \{ 1,...N \} } L_n$... where $I_n$, $J_n$, $K_n$, $L_n$... are the dimensions of the $n$ th input tensor.

The following restrictions apply to the Numpy boardcasting:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `RI` | $\forall n \in \{ 1,...N \}$ either $I_n = I$  or $I_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RJ` | $\forall n \in \{ 1,...N \}$ either $J_n = J$  or $J_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RK` | $\forall n \in \{ 1,...N \}$ either $K_n = K$  or $K_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| `RL` | $\forall n \in \{ 1,...N \}$ either $L_n = L$  or $L_n = 1$| https://numpy.org/doc/stable/user/basics.broadcasting.html |
| ...  | ... | ... |

Assuming those restrictions hold, the relation between elements of the boardcasted tensor and the input tensor are:

$\forall n \in \{ 1,...N \}, \forall i \in \{ 1,...I \}, \forall j \in \{ 1,...J \}, \forall k \in \{ 1,...K \}, \forall l \in \{ 1,...L \}... z^n_{i,j,k,l...} = x^n_{f(i,I_n,I),f(j,J_n,J),f(k,K_n,K),f(l,L_n,L)...}$
