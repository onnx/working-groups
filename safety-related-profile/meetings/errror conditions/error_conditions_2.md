Error conditions and runtime errors
(Material discussed on 2025-07-16)

## Case 1: floating point computation

### General principles
- No exception is raised during a floating point computation.
- Error values occur and are propagated according to the IEEE 754 standard:

### Example : Softmax

`Softmax(input,axis)=  Exp(input) / ReduceSum(Exp(Input), axis=axis, keepdims=1)`

$$s(z_i) = {e^{z_i} \over \sum_{j=1}^K e^{z_j}} $$

Described using `Exp` (exponential element wise) and `ReduceSum` (computes the sum of the input tensor’s elements along the provided axes).

See the [Google Collab notebook](https://colab.research.google.com/drive/1fFDuuAK_lA3ScDk6I_VplbC5RYBncQD6#scrollTo=BfheCRKub5vl)

Neither the ORT nor the Reference over or underflow.

The ONNX reference implementation computes SoftMax as follows:
class Softmax(OpRunUnaryNum):

```python
    def _run(self, X, axis=None):
        axis = axis or self.axis
        tmp = X - X.max(axis=axis, keepdims=1)
        Y = np.exp(tmp)
        Y /= Y.sum(axis=axis, keepdims=1)
        return (Y.astype(X.dtype),)
```

The operation is not implemented in the naive way exactly the one specified. 

If we use the naive, direct implementation:
```python
output_data_underflow_naive = np.exp(input_data_underflow)
output_data_underflow_naive /= output_data_underflow_naive.sum(axis=0, keepdims=1)
```
we have a nan.  

There can't be a nan for Onnxruntime thanks to normalization, but another implementation could under/overflow.

Shall we simply write :

>**Runtime errors**
>Operator `SoftMax` may overflow (resp. underflow) for large (resp. small) input input values.
> In that case, the operator will return a nan.

## Case 2: Integer computations

### Example 1: `add` over int32 values

**Option 1**: complete the specification with preconditions
- Operator `add` is specified using the standard $+$ operator, i.e, add(x,y) returns $x+y$  and 
	- a precondition is added: $$-2^{31} \leq x+y \leq 2^{31}-1 $$
	- or conservative constraints on $x$ and $y$ are added 
		- If $x > 0$ and  $y>0$ then $y ≤ (2^{31}-1) -x$
		- If $x < 0$ and $y<0$ then $y ≥ -2^{31} - x$

		- those conditions could be checked by the user by adding a dedicated sub-graph. 

**Option 2:** give a rigorous specification of the `add` operator 

$$z=\left\{ 
  \begin{array}{ c l }
    x + y - 2^{32} & \quad \textrm{if } x + y > 2^{31}-1 \\
   x + y + 2^{32} & \quad \textrm{if } x + y < -2^{31} \\
   x+y & \quad \textrm{otherwise}
  \end{array}
\right.$$

**Option 3**
>**Runtime errors**
> Operator `add`may overflow in the positive or negative numbers for large positive of negative input values. 
> In that case the result returned by the operator does not comply with the specification.

