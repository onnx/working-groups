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
### Link to ONNX description

https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md

### Purpose

Boroadcasting is the operation consisting in expanding the dimensions of a tensor to make its shape compatible the shape of the other arguments in an element-wise operation (e.g., Add , Mul , etc.).

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

The following constraint applies to boardcasting:

| Constraint    | Statement | Origin |
| -------- | ------- | ------- |
| `C1` | $\forall m \in [1, N], \forall i \in [1, nY]$ either $dYm_i = dY_i$  or $dYm_i = 1$| https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md|

Constraint `C1` indicates that, for each tensor and each dimension, considering a common number of dimensions, the value of a dimension is either equal to the maximum dimension among all tensors or equal to one.

### Functionality description

The description of the functionality relies on two relations:
- the relation between the input tensors and tensors with a common number of dimensions, and
- the relation between the tensors with a common number of dimensions and the output tensors.

#### Relation between input tensors and tensors with a common number of dimensions

The common number of dimensions is the largest number of dimensions among the input tensors:

$$nY = \max_{m \in [1, N]} nXm$$

where $nXm$ is the number of dimensions of $Xm$ the $m$ th input tensor.

The tensors with $nY > nXm$ have their dimensions completed adding dimensions of value 1 for the $nY - nXm$ first dimensions and shifting the other dimensions. That is:

$\forall m \in [1,N] \forall i \in [1,nY] ~~~~~ dYm_i = 1$ if $i \leq nY - nXm$ and $dXm_{i-nY+nXm}$ otherwise.

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

That is when, for a given dimension $dYm_k$ of a tensor $Ym$ $dYm_k = 1$,  $f(i_k,1,.)$ is 1 whatever the value of the index $i_k$ leading to $Zm$ related always to the first element of $Ym$ in the $k$ th dimension.

### Alternate functionality description

The Broadcast operator is commutative, i.e. given any permutation of tensors $\sigma$(.):

$\sigma$(Z1, ..., ZN) = Broadcast($\sigma$(X1, ... , XN))

In consequence the relations above can be described without loss of generality assuming that the input tensors are ordered by increasing number of dimensions.
Moreover, they can be described recursivelly using only the binary broadcast operator Z1,Z2 = Broadcast(X1, X2):

Z1, ..., ZN = Broadcast(Broadcast(X1, ... , XN-1),XN)

Broadcast(X1, ... , XN-1) = Broadcast(Broadcast(X1, ... , XN-2),XN)

...

Broadcast(X1, X2, X3) = Broadcast(Broadcast(X1, X2), X3)

In consequence the relations above can be described in a simpler way.

#### Relation between input tensors and tensors with a common number of dimensions

The common number of dimensions is the largest number of dimensions among the two input tensors:

$$nY = \max (nX1, nX2)$$

where $nX1$ and $nX2$ are reciprocally the number of dimensions of $X1$ and $X2$ input tensors. Because of commutativity, we can assume that the tensor with the lowest number of dimensions is $X1$, i.e. $nX1 \leq nX2 = nY$.

If $nX1 < nY$, $X1$ has its dimensions completed adding dimensions of value 1 for the $nY - nX1$ first dimensions and shifting the other dimensions. That is:

$\forall i \in [1,nY] ~~~~~ dY1_i = 1$ if $i \leq nY - nX1$ and $dX1_{i-nY+nXm}$ otherwise.

Adressing of elements of $X1$ has to be shifted in consequence:

$$\forall i_1 \in [1,dX1_1]... \forall i_{nX1} \in [1,dX1_{nX1}] ~~~~~~~~ Y1[s,i_1,...i_{nX1}] = X1[i_1,...i_{nX1}]$$

where $s$ is a sequence of $nY - nX1$ ones, i.e. 1,...1. The relation can also be written without relying on the sequence $s$:

$$\forall i_1 \in [1,dY1_1]... \forall i_{nY} \in [1,dY1_{nY}] ~~~~~~~~ Y1[i_1,..., i_{nY-nX1+1}, ...i_{nY}] = X1[i_{nY-nX1+1}, ...i_{nY}]$$

The dimensions and addressing of elements of $Y2$ are indentical to the ones of $X2$. That is:

$\forall i \in [1,nY] ~~~~~ dY1_i = dX1_i$

$$\forall i_1 \in [1,dY1_1]... \forall i_{nY} \in [1,dY1_{nY}] ~~~~~~~~ Y1[i_1,...i_{nY}] = X1[i_{1}, ...i_{nY}]$$

#### Relation between tensors with a common number of dimensions and output tensors

This relation relies on the function $f(.,.,.)$ described above assuming constraint `C1` holds.

We define $dY_1$,... $dY_{nY}$ reciprocaly as $dY_1 = \max(dY1_1, dY2_1)$, ...  $dY_{nY} = \max(dY1_{nY}, dY2_{nY})$

Then the relation between elements of boardcasted tensors $Z1,Z2$ and tensors with common number of dimensions $Y1,Y2$ are:

$$\forall i_1 \in [1, dY_1], ... \forall i_{nY} \in [1, dY_{nY}] ~~~~~~~ Z1[i_1,...i_{nY}] = Y1[f(i_1,dY1_1,dY_1),...f(i_{nY},dY1_{nY},dY_{nY})]$$

$$\forall i_1 \in [1, dY_1], ... \forall i_{nY} \in [1, dY_{nY}] ~~~~~~~ Z2[i_1,...i_{nY}] = Y2[f(i_1,dY2_1,dY_1),...f(i_{nY},dY2_{nY},dY_{nY})]$$

That is when, for a given dimension of $dYm_k$ of a tensor $Ym$, with $m$ = 1 or 2, $dYm_k = 1$,  $f(i_k,1,.)$ is 1 whatever the value of the index $i_k$ leading to $Zm$ related always to the first element of $Ym$ in the $k$ th dimension.









