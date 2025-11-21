# Contents

- **Broadcast** operator for type...

<a id="real"></a>
# **Div** (real, real)

## Signature
$Z0, ..., ZL = \text{Broadcast}(X0, ... , XL)$

where
- L $\in [0, 2^{31}-1[$
- $X0$, ... ,$XL$ input tensors  
- $Z0$, ... ,$ZL$ output tensors 
 
### Link to ONNX description

https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md

## Restrictions

No restriction.

## Informal specification

The broadcasting operator allows element-wise operations to take tensors with different shapes (e.g., **Add** , **Mul** , etc.).

Broadcasting consists in producing a set of tensors with the same shape. Each produced tensor $Zi$ contains elements from $Xi$ repeated as necessary.

The shape of $Zi$ satisfies two conditions.

Condition 1: the number of dimensions is the largest number of dimensions among the $Xi$. When the number of dimensions is increased for a tensor:
- the dimensions to be completed are those of lower indexes,
- those dimensions are set to a size equal to 1

Condition 2: the size for a dimension is equal to the maximum of the sizes of all the input tensors for that dimension after expansion

> Schema à rajouter

The operation can be described in two steps:
- Step 1: make the tensors the same number of dimensions to ensure condition 1
- Step 2: make the tensor dimension sizes equal to ensure condition 2

Let us note $Y0$, ... $YL$ the tensors obtained after step 1, with a common number of dimensions $nY$ but with still different dimension sizes.

##### Description of step 1

The common number of dimensions is the largest number of dimensions among the input tensors:

$$nY = \max_{m \in [0, L]} nXm$$

where $nXm$ is the number of dimensions of $Xm$ the $m^{\text{th}}$ input tensor.

The tensors with $nY > nXm$ have their dimensions prepended  with $nY - nXm$ times 1. That is:

> faire référence au multiindex.

Considering the multi-indexes $i$ and $i'$, we have the following relation:

$Y[i]=X[i']$ with 
$i=(1,...,1,i')$
     nY-nXm

##### Description of step 2
> Petite explication de ce qu'on cherche à faire + dessin

When, for a given dimension $dYm_k$ of a tensor $Ym$ $dYm_k = 1$,  $f(i_k,1,.)$ is 1 whatever the value of the index $i_k$ leading to $Zm$ related always to the first element of $Ym$ in the $k$ th dimension.

Let $f(.,.,.)$ a function that provides the first index value in a dimension when the dimension size is not the maximum size and the current index of this dimension when the dimension size is equal to the maximum dimension size. This fonction is defined as:

$f(a,B,C) = a$ if $B=C$ and $f(a,B,C) = 1$ otherwise where:
- $a$ is the current element,
- $B$ is the dimension size, and
- $C$ is the target dimension size.

Then the relation between elements of boardcasted tensors $Z1,...ZN$ and tensors with common number of dimensions $Y1,...YN$ are:

> Exprimer la relation entre multiindexes
> > Modifier les index : 1 => 0, N => L

$$Zm[i]=Ym[i']$$ with 

$$i=i_1,...i_{nY}$$

$$i'=f(i_1,dYm_1,dY_1),...f(i_{nY},dYm_{nY},dY_{nY})$$




## Error conditions
XXXXX

## Inputs

### $\text{Xi}$: XXXX
XXXX

#### Constraints

 - `[C1]` <a id="C1ra"></a> XXXXX
   - Statement: XXXX
 


## Outputs

### $\text{Z}$: XXXX

XXXX

#### Constraints

 - `[C1]` XXXX
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.

## Attributes

No attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Not applicable.
