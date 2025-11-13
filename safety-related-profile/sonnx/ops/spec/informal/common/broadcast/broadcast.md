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

$dY_1$, ... $dY_{nY}$ are reciprocaly defined as $dY_1 = \max_{m \in [1, N] } dYm_1$, ...  $dY_{nY} = \max_{m \in [1, N] } dYm_{nY}$ where $dYm_1$, ... $dYm_{nY}$ are the dimensions of the $m$ th input tensor with already the common number of dimensions.

The following constraint applies to the Numpy boardcasting:

| Constraint    | Statement | Origin |
| -------- | ------- | ------- |
| `C1` | $\forall m \in [1, N], \forall i \in [1, nY]$ either $dYm_i = dY_i$  or $dYm_i = 1$| https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md|
| ...  | ... | ... |

### Functionality

The description of the functionality relies on two relations:
- the relation between the input tensors and tensors with a common number of dimensions, and
- the relation between the tensors with a common number of dimensions and the output tensors.

#### Relation between input tensors and tensors with a common number of dimensions

The common number of dimensions is the largest number of dimensions among the input tensors:

$$nY = \max_{m \in [1, N]} nXm$$

where $nXm$ is the number of dimensions of $Xm$ the $m$ th input tensor.

The tensors with $nY > nXm$ have their dimensions completed adding dimensions of value 1 for the $nY - nXm$ first dimensions and shifting the other dimensions. That is:

$\forall m \in [1,N] \forall i \in [1,nY] ~~~~~ dYm_i = 1$ if $i < nY - nXm$ and $dXm_{i-nY+nXm}$ otherwise.

Adressing of elements has to be shifted in consequence:

$$\forall m \in [1,N] \forall i_1 \in [1,dXm_1]... \forall i_{nXm} \in [1,dXm_{nXm}] ~~~~~~~~ Ym[s,i_1,...i_{nXm}] = Xm[i_1,...i_{nXm}]$$

where $s$ is a sequence of $nY - nXm$ ones, i.e. 1,...1. The relation can also be written without relying on the sequence $s$:

$$\forall m \in [1,N] \forall i_1 \in [1,dYm_1]... \forall i_{nY} \in [1,dYm_{nY}] ~~~~~~~~ Ym[i_1,..., i_{nY-nXm+1}, ...i_{nY}] = Xm[i_{nY-nXm+1}, ...i_{nY}]$$

#### Relation between tensors with a common number of dimensions and output tensors

This relation relies on a function $f(.,.,.)$ providing the first element of a dimension when the dimension size is 1 and the current element of this dimension when the dimension size is equal to the target dimension size. This fonction is defined as:

$f(a,B,C) = a$ if $B=C$ and $f(a,B,C) = 1$ if $B=1$ where:
- $a$ is the current element,
- $B$ is the dimension size, and
- $C$ is the target dimension size.

Note that assuming constraint `C1` holds, other cases, i.e. $B \neq C$ and $B \neq 1$, don't need to be specified.

Then the relation between elements of boardcasted tensors $Z1,...ZN$ and tensors with common number of dimensions $Y1,...YN$ are:

$$\forall m \in [1, N], \forall i_1 \in [1, dY_1], ... \forall i_{nY} \in [1, dY_{nY}] ~~~~~~~ Zm[i_1,...i_{nY}] = Ym[f(i_1,dYm_1,dY_1),...f(i_{nY},dYm_{nY},dY_{nY})]$$

That is when, for a given dimension $dYm_k$ of a tensor $Ym$ $dYm_k = 1$,  $f(i_k,1,.)$ is 1 whatever the value of the index $i_k$ leading to $Zm$ reated always the first element of $Ym$ in the $k$ th dimension. 


