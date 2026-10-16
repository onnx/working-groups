> The format has slightly changed. Please refer to [div](../../div/div.md) for an up to date example;


# `max` operator
### Contents
- `Maximum` operator for a type on which an order is defined.
## `Max`  `(type on which an order is defined, i.e. bfloat16, double, float, float16, int16, int32, int64, int8, uint16, uint32, uint64, uint8)`

### Signature
`Y = max(X^1, ... , X^N)`
where

- `N`: 
- `X^1`: first input tensor
- ...
- `X^N`: last input tensor
- `Y`: output tensor


> Variadic arguments are noted with a subscript $A_i$.

#### Restrictions
The following restrictions apply to the `max` operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | `N` is an integer between 1 and 2147483647 | Transient |
| `R2` | Numpy boardcasting rules shall be applicable to `Y`, `X^1`, ... , `X^N` | https://numpy.org/doc/stable/user/basics.broadcasting.html |

> I think that the restriction on the number of variadic parameters is not a restriction but a constraint. 

 #### Informal specification

> Everywhere: replace "boardcasted" by "broadcasted" ;-)

The result tensor $Y$ is based on the boardcasted values $Z^1$, ... , $Z^N$ of the input tensors $X^1$, ... , $X^N$.

> The meaning of "is based" must be clarified. We could define a broadcast operator $\text{broadcast}$ and define operator max applied on $Z_1, Z_2,...$ where $Z_i=\text{broadcast}(X_i,...)$. Stated differently: $\text{max}(X_1,X_2,...)= \text{max}(\text{broadcast}(X_1), \text{broadcast}(X_2),...)$ and define the $\text{broadcast}$ operator elsewhere.

> In the informal specification of the $\text{broadcast}$ operator, introduce first the opeator in an informal way:
> Boroadcasting is the operation consisting in expanding the dimensions of a tensor to make its shape compatible the shape of the other arguments in an element-wise operation (e.g., $\text{add}$, $\text{mul}$, etc.).

$ Please use the notation $dT_i$ for the it-th dimension of tensor $T$.  

$ Please use the notion of 

Let, $I$, $J$, $K$, $L$... be the common boardcasted dimensions of all tensors, elements $y_{i,j,k,l...}$ of $Y$ shall comply with:

> (Genera) Always give an informal explanation before an equation .

> Here is an alternate formulation...
> 
> Let $Y=\text{broadcast}(X_1,X_2,...,X_n)$ where $Y$ is the broadcasted value of tensor $X1$ with respect to t$X2$, $X3$?...
>
> The broadcast operator is associative, ie.
> $$Y=\text{broadcast}(...\text{broadcast}(\text{broadcast}(\text{broadcast}(X_1,X_2),X_3),...,Xn)$$
 

> When we compute $A+B$ with broadcasting, we actually compute $b(A,B)+b(B,A)$

> Additionaly operator $b$ is commutative in terms of shape: 
> $$\text{shape}(b(A,B)) = \text{shape}(b(B,A))$$ 


> So we can just define $Y=\text{broadcast}(X1,X2)$, 

> The following constraints are applicable:

> (C1) Dimension must be compatible: 
> $$\forall i \in [0,n-1], dX1_i = dX2_i \vee dX1_i = 1 \vee dX2_i = 1$$
> (C2) Dimension of the broadcasted tensor:
>  $$\forall i \in [1,n], dY_i = \max(dX_{1,i}, dX_{2,i})$$ 

> Note 1: I have to state that if a tensor has only $n$ dimensions , then $\forall i>n, dX_i=1$.

> Note 2: that I refer to the max operation here.$\text{max}$ is the $\text{max}$ applied on scalar. We could define broadcast as a special case in order to prevent an infinitely recursive definition or simply say that this $\text{max}$ is the "usual" max.

> Now, I would define the values of $Y$ from the values of $X1$ and $X2$. 

> If tensor T has $nT$ dimensions, then 
> $$\forall i_1,i_2,...,i_n \in [0,dY_1-1]\times[0,dY_2-1]\times [0,dY_n-1] : Y(i_1,i_2,...i_n) = \text{op}(X1(i_1,i_2,i_{nX1}), X2(i_1,i_2,i_{nX2}))$$



$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} = \max_{n \in [1, N] } z^n_{i,j,k,l...}$

> $z^n_{i,j,k,l...}$ => $z_n(i,j,k,l...)$

where $z^n_{i,j,k,l...}$ is an element of $Z^n$.

> I don't understand why the common dimension of the broadcasted tensor would depend on the values of the tensors. I a probably missing the point.   


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


