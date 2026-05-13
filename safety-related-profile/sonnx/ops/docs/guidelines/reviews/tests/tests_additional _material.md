
#### Testing against shapes
For each operator, there shall be at least one test showing the correct behaviour of the operator for the following tensor shapes (when applicable): 
- scalar tensor (rank-0 tensor)
- 1D  tensor
- 2D tensor
- 3D tensor
- one nD- tensor with n>3
- For each of the previous tensor shapes, there shall be at least one test in which at least  one dimension of the tensor is null (null tensor)
#### Testing against indexes
- For a given shape, each index 
#### Selection of values
- A test must be designed to as to discriminate correct behaviours from incorrect ones. This concern both the mathematical operation itself (e.g. using zeroes or infinities for the two arguments of a $+$  and a $\times$ ) and the values of indexes. So the value of the tensor must be chosen so that using an incorrect index $i_\textit{err}$ instead of $i$ lead to a result that can be discriminated from the correct one.  A necessary condition is that the value at multi-index $j$ in the output can only be computed from a unique combination of input values at index $i_1$, $i_2$, ... , $i_n$ for an opertor with $n$ arguments. 
  For instance, when doing the pointwise addition `[[1 2][3 4]] + [[1 2][3 4]]=[[2 4][6 8]]`, values 4 can be obtained by adding 1+3 or 2+2. A better test would be `[[1 2][3 4]] + [[100 200][300 400]]=[[101 202][303 404]]`
  For the **Mult** operator, if one value in the first argument is zero, then the value of the result will be zero whatever the value of the second argument.

>[!Note]   Those tests do not prevent bad implementation to pass the test. They just prevent badly chose input values to mask errors. 

- There shall be one test showing the correct behaviour of the operator with respect to the IEEE special values (-inf, -0, +0, +Inf, NaN), for all combinations.
#### Test of pooling
When an operator uses pooling, test shall be done
- for pooling values null and non null in all dimensions :
	- for kernel sizes such that the dilated kernel is smaller and equal to the size of the padded argument (\*) : 
		- for values of the argument and kernel showing the use of correct padding values. For instance,  for the **MaxPool** operator, the padding value should (conceptually) be -inf. So a test shall be done with values of the argument equal to -inf and a padded argument in all dimensions (e.g., for a 2D tensor: padding is (1,1,1,1)) 

(\*) Other cases are covered by the pre-condition tests
#### Test of striding
When an operator uses striding, test shall be done at least 
- for all dimensions :
	- for  striding value equal to 1 and to the dimension of the tensor on which striding is performed

### Test of Structural operators
A "structural operator" is an operator that does not computes new values from the input arguments but reorganizes the values given in input to build the output tensor.  Operators **Flatten** or **Reshape** is are examples of structural tensors. 

The test of structural operator much show that the value of the output tensor for a given multi-index $j$ actually comes from the correct entry $i$ in the input tensor. Such operator implement a relation between $i$ and $j$ and tests must show that this relation is correct (for the operator). 
But, the relation between multi-indexes is not  since the operator only manipulates values, the multi-indexes relation is not observable. For instance, if all the entries of the input tensor contains the same value, all mappings between $i$ and $j$ are undistinguishable (hence, non testable). 

Therefore, to test structural tensor, each entry of the input tensor must hold a value that can be traced to a unique entry in the output tensor. 

For instance, for an 2x3x4 inputs tensor,  of the **Flatten** operator, 
```
Axis=0
Shape of input tensor: (2, 3, 4)
X=[[[ 0, 1, 2, 3],  [ 4, 5, 6, 7],  [ 8, 9,10,11]], [[12,13,14,15],  [16,17,18,19],  [20,21,22,23]]]
Shape of output tensor: (1, 24)
Result = [[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]]
```

Each entry of the result can be traced to a specific entry in the input and the correct begaviour of the operator can be assessed.

### Tests against constraints

- For each constraint (Ci) taken separately, and each variable $v$ appearing in the constraint, there shall be at least one showing the effect of the variable on the satisfaction/violation of each constraint **if the behaviour of the operator is described for those  violations**. If the behaviour is not decsribed, thi smeans that the beaviour of the operator is undefined  and no test can be described. 
  For instance, in the case of **MaxPool** operator, the following constraints are applicable (2D case):
	- padding values must be positive: $$\forall i \in {0,1,2,3}: \textit{pad\_shape}[i] \ge 0$$
	- striding values must be strictly positive: $$\forall i \in {0,1}: \textit{stride}[i] \gt 0$$
	- for each spatial dimension, the dilated kernel must fit within the padded input, i.e.:  $$dX2+\textit{pad\_shape}[0]+\textit{pad\_shape}[2] \ge \textit{dilations}[0]×(\textit{kernel\_shape}[0]−1)+1$$ and $$dX3+\textit{pad\_shape}[1]+\textit{pad\_shape}[3] \ge \textit{dilations}[1]×(\textit{kernel\_shape}[1]−1)+1$$
	- the size of the left (resp. top) and right (resp. bottom) padding must be strictly smaller than the size of the dilated kernel, e.g., for a tensor with two spatial dimensions  $$\forall i \in {0,1,2,3}: \textit{pad\_shape}[i] \lt \textit{dilations}[0]×(\textit{kernel\_shape}[i]−1)+1$$ 
	- the $\textit{pad\_shape}$ argument shall provide padding values for the beginning and end of each spatial dimensions, i.e. $$d\textit{pad\_shape}0=2\times (dX1+dX2+\ldots+dXi+\ldots+dXn)$$
	- The shape of the dilation tensor shall be compatible with the shape of the kernel: $$s\textit{dilation}=sW$$
	- The shape of the output tensor shall comply with the shape of the computed max pool, i.e. $$dY2​=⌊(dX2​+\textit{pad\_shape}[0]−\textit{dilations}[0]×(\textit{kernel\_shape[0]}−1)−1)/(\textit{strides}[0]+1)⌋$$ and $$dY3=⌊(dX3+pad_shape[1]−dilations[1]×(kernel_shape[1]−1)−1)/(strides[1]+1)⌋$$
	 