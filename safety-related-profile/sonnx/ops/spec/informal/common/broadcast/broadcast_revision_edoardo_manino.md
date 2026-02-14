**Note 1: all questions and comments are explicitly numbered. Whenever I have suggestions in terms of writing/phrasing, I just changed the text (highlighted in bold capital font).**

# Contents
- **Broadcast** functionality for type [real, float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64, string, boolean](#any).

Based on ONNX documentation version 14, multidirectional broadcasting.
<a id="any"></a>
# **Broadcast**  (type, type, type...)

where type is in {real, float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64, string, boolean}.

## Signature
Definition of functionality $\text{Broadcast}$ signature: $Z0, ..., ZL = \text{Broadcast}(X0, ... , XL)$

where
- $L \in [0, 2^{31}-1[$: number of tensors to be broadcasted minus one **Note 2: it is unclear why L cannot be 2^31-1. Why "minus one"?**
- $X0$, ... , $XL$: tensors to be broadcasted
- $Z0$, ... , $ZL$: broadcasted tensors 

## Link to ONNX description

https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md

## Restrictions

No restriction.

## Informal specification

The broadcasting functionality allows element-wise operations, e.g. **Add** , **Mul** , etc., to take tensors with different shapes, **BY EXPLICITLY NORMALISING THEM TO THE SAME SHAPE.**

Broadcasting consists in producing a set of tensors with the same shape: **I.E. EACH OUTPUT TENSOR WILL HAVE** number of dimensions $nZ$ and for each dimension $i$, size $dZ_i$. TO ACHIEVE THIS GOAL,** each produced tensor $Zi$ contains elements from $Xi$ repeated as necessary.

The shape of a $Zi$ satisfies two conditions.

*Condition 1*: the number of dimensions **OF ALL OUTPUT TENSORS** is the largest number of dimensions among all the input tensors. When the number of dimensions is increased for a tensor:
- the **EXTRA** dimensions to be completed are **PREPENDED BEFORE THE** lower indexes,
- those dimensions are set to a size equal to 1, and
- the access to the tensor data remains possible. **Note 3: this remark is unclear. Is it a statement about copying the data vs accessing by reference? Or is it a subtle reference to the Description fo Step 1 below? Is the meaning something like "during the broadcasting, the data of the input tensor remains in place", where "in place" is to be intended as the technical memory access terminology? In general, it seems the intention here is to say something about the *implementation* of the broadcasting operator, which I am not sure is the desired goal.**

*Condition 2*: the size **OF EACH OUTPUT** dimension is equal to the maximum of the sizes of all the input tensors for that dimension after expansion. **AS A CONSEQUENCE, THE SIZE OF SOME DIMENSIONS IN AN OUTPUT TENSOR MIGHT BE LARGER THAN THAT OF THE CORRESPONDING INPUT TENSOR. IF THAT IS THE CASE, THE MISSING DATA IS FILLED BY COPYING THE ENTRIES AT INDEX 0 OF THE CORRESPONDING DIMENSION.**

The figure **BELOW** shows an **EXAMPLE** of broadcasting two tensors, i.e. $Z0, Z1 = \text{Broadcast}(X0, X1)$.

<img src="assets/imgs/Broadcast.png" alt="drawing" width="100%"/>

The operation can be described in two steps:
- Step 1: make tensors with the same number of dimensions to ensure condition 1
- Step 2: make the tensor dimension sizes equal to ensure condition 2

Let us note $Y0$, ... $YL$ the tensors obtained after step 1, with a common number of dimensions $nY$ but with still different dimension sizes.

### Description of step 1

The common number of dimensions is the largest number of dimensions among the input tensors:

$$nY = \max_{m \in [0, L]} nXm$$

where $nXm$ is the number of dimensions of $Xm$ the $m^{\text{th}}$ input tensor.

The tensors with $nY > nXm$ have their dimensions prepended  with $nY - nXm$ times 1. That is:

$$\forall m \in [0,L] \forall i \in [0,nY-1] ~~~~~ dYm_i = 1 ~~~~~ \text{if} ~~~~~ i < nY - nXm, ~~~~~ dXm_{i-nY+nXm} ~~~~~ \text{otherwise}$$

Concerning the access to data through [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index) we have the following relation:

$$Ym[i]=Xm[i']$$

with $i$ defined from $i'$:

$$i= \underbrace{1,...,1},i'
    \atop nY-nXm$$

### Description of step 2

Now $Y0$, ... $YL$ have a common number of dimensions but different dimension sizes. This common number of dimensions, is the number of dimensions of **ALL** output tensors **Zm**:

$$ nZm = nY $$

In order to **FULLY** define the output we have to set each dimension to its maximum among all tensors and, for tensors with increased dimension, access always to the first element whatever the value of the index in this dimension.

**FOR OUR RUNNING EXAMPLE**, The figure **BELOW** presents the tensors obtained at the end of **STEP** 1.

<img src="assets/imgs/Y.png" alt="drawing" width="100%"/>

#### **SETTING** each dimension to its maximum

**Note 4: the notation was difficult to parse, I have tried to improve it.** The dimensions $dY_0$, ... $dY_{nY-1}$ are defined as the maximum over all tensors, i.e. $dY_i = \max_{m \in [0, L] } dYm_i$ for all $i\in[0,nY-1]$ where $dYm_0$, ... $dYm_{nY-1}$ are the dimensions of tensor $Ym$. Overall, we have:

$$\forall m \in [0,L] \forall i \in [0,nZm-1] ~~~~~ dZm_i = dY_i$$

#### Access to data

Let $f(.,.,.)$ a function that provides an index value of 0 when the dimension size is not the maximum size and the current index of this dimension when the dimension size is equal to the maximum dimension size. This **FUNCTION** is defined as:

$f(a,B,C) = a$ if $B=C$ and $f(a,B,C) = 0$ otherwise where:
- $a$ is the current index,
- $B$ is the **SIZE OF THE INPUT DIMENSION**, and
- $C$ is the **SIZE OF THE OUTPUT DIMENSION**.

When, for a given dimension $dYm_k$ of a tensor $Ym$, $dYm_k \neq dY_k$ then  $f(i_k,dYm_k,dY_k)$ is 0 whatever the value of the index $i_k$. **THIS WAY**, $Zm$ always **RELATES** to the first element of $Ym$ in the $k^{\text{th}}$ dimension.

Then the relation between elements of **BROADCASTED** tensors $Z0,...ZL$ and tensors with common number of dimensions $Y0,...YL$ are:

$$Zm[i]=Ym[i']$$

with: 

$$i=i_0,...i_{nY-1}$$

$$i'=f(i_0,dYm_0,dY_0),...f(i_{nY-1},dYm_{nY-1},dY_{nY-1})$$

**FOR OUR RUNNING EXAMPLE**, The figure **BELOW** presents the way the function $f(.,.,.)$ allows to link elements of $Z0$ and $Z1$ with respectively elements of $Y0$ and $Y1$.

<img src="assets/imgs/f.png" alt="drawing" width="100%"/>

## Error conditions

**Note 5: the link below ("Origin") does not cover the error conditions explicitly. Examples of errors are in the numpy documentation linked therein. Are we happy with the reader having to follow two links to get to the actual information? https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules**

The following error condition applies to **BROADCASTING**:

| Error    | Statement | Origin |
| -------- | ------- | ------- |
| `E1` | $\exists m \in [0, L], \exists i \in [0, nY-1]$ such that $dYm_i \neq dY_i$  and $dYm_i \neq 1$| https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md|

For each tensor and each dimension, the value of a dimension shall be either equal to the maximum dimension among all tensors or equal to one. If not, Error `E1` occurs.

## Inputs

### $Xm$ for $m \in [0,L]$: `type tensor`
**Note 6: for $m \in [0,L]$ means that there are $L+1$ input tensors. This issue is present throughout the document.** $L-1$ input tensors with possibly different shapes.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Type **CONSISTENCY**
   - Statement: For any $m \in [0,L]$ tensors $Xm$ and $Zm$ must have the same type. **Note 7: the shape might change, so is it really the same "type"? Maybe we can say "the entries of Xm and Zm must have the same numerical type"**
 
## Outputs

### $Zm$ for $m \in [0,L]$: `type tensor`

**Note 8: see note 6** $L-1$ output tensors with identical shapes.

#### Constraints

 - `[C1]` Type **CONSISTENCY**
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $Xm$.

## Attributes

No attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

Not applicable. I.e. the data values of the output tensors are stricly equal to the corresponding data values of the input tensors.











