### RK 1 (status is "NOT ANALYZED")
I have remove the following text:

>  Preliminary remarks
>  Types
> - Operators are first described for values in the domain of real numbers. Because the `Div` operator divides each element in the input tensors element-wise, the output is of the same data type as the inputs. The inputs `A` and `B` can be of various types including `tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, and `tensor(uint8)`. The dimension size of a tensor is defined by $N(tensor)$.


Because this concerns the general structure of all operators : 
- first specify the operator in R
- then specify the operator for specific types

### RK 2 (status is "NOT ANALYZED")
> - if Elements of tensor `B` is zero, as division by zero is not valid the nemeric result will be infinite representation. `[R5]`

This is not a "restriction": this is a actually a contraints on the operator parameters.


### RK 3 (status is "CORRECTED")
> Tensor `A` is one of the two input tensors to be divided.
=>
> Tensor `A` is the numerator of the division

Same remark for `B`.

### RK 4 (status is "CORRECTED")
I have slightly rephrased the condition concerning the range constraint.

I have removed the "formula" : 
 > $\forall B[i] \neq 0$ else the result will be inf `[R5]`
because, we ar only considering values in R.

The formula should be written for a tensor with any dimensions...

### RK 5 (status is "NOT ANALYZED")

> Broadcastable tensor is forbidden. `[R4]`

This is redundant since we have a constraint on the shape of the tensor.
Furthermore, this constraint concern the graph, not the operator.

### RK 6 (status is "CORRECTED")

> The mathematical definition of the operator is given hereafter 

Added : "for a unidimensional tensor."

### RK 7 (status is "CORRECTED")

Slightly edited formula.

### RK 8 (status is "NOT ANALYZED")

>Where
>- $i$ is an index covering all dimensions of the tensors.

Strange formulation... to be discussed... I have modified to say that we are considering a unidimensional tensor.


### RK 9 (status is "NOT ANALYZED")

If we give an example, we should give an example with ONNX. We said that we will provide examples in G collab.

> Note in python it is equivalent to do :
> ```python
> >>> import numpy as np
> np.divide([[1,3],[5,7],[9,12]],[[11,22],[33,-44],[-55,66]])
> array([[ 0.09090909,  0.13636364],
>        [ 0.15151515, -0.15909091],
>        [-0.16363636,  0.18181818]])

> with a division by 0
> np.divide([[6,9,35]],[[3,3,0]])
> array([[ 2.,  3., inf]])

### RK 10 (status is "NOT ANALYZED")

Added section for floating-point implementation types. 
