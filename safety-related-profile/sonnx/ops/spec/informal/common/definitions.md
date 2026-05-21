# Definitions

- <a id="tensor_index"></a> **Tensor index** (or **multi-index**): For an $n$-dimensional tensor $T$, i.e., a tensor of rank $n$, a single element is addressed by an index tuple $i=(i_0,i_1,\dots,i_{n-1})$ where $i_k$ is the index along axis $k$. We have $i_k \in [0,dT_k]$ where $dT_k$ is the number of elements along the $k$-th axis. 

- **Empty tensor (null tensor)**: A tensor with at least one zero dimension. 
A null tensor can be created by operators  such as **Slice** or **Where**. 
    >Nota: If the application of an operator leads to a  tensor with a dimension equal to 0, the tensor is null and its values are no more accessible. In particular, no structural operator can be applied recover access to the tensors values:
    >- Operators **Reshape** and **Flatten** preserve the number of elements of their input tensors, so a null input tensor will generate a null output tensor.
    >- Operator **Squeeze** can only remove dimensions with size 1.
    
    >However, using `keepdims=0`, operators **ReduceSum** (resp. **ReduceProd**) applied (e.g.) on a tensor with shape `[0,X]` will produce a tensor with X zeroes (resp. with `ReduceProd`, the result would be a vector of X ones). Note that the values of the resulting tensor do not depend on the values of the initial tensor. They are the  identity values for the addition (resp. multiplication). Additionally, the multiplication of two null tensors (e.g. using the **Matmul** operator) can also produce a non-null tensor with all values equal to zero.<br/> 
    In practice, this means that, if one dimension of a tensor becomes 0, the tensor cannot be reduced to some canonical null tensor (e.g., a tensor with only one dimension equal to 0) since its shape still matters.  
- **Scalar**: A 0-rank tensor. 
- **Vector**: A 1-rank tensor. 
- **Matrix**: A 2-rank tensor. 
- **Shape of a tensor**: The shape of a tensor is a list of its dimensions. The list is empty for a scalar tensor. 
- Symbol `minfloat16`,  `minfloat`,  `mindouble` (resp. `maxfloat16`, `maxfloat`, `maxdouble`) represent the minimum (resp. maximum) values for `float16`, `float`, `double`, `respectively`.  
- Symbol `minint8`, `minint16`, `minint32`, `minint64`(resp. `maxint8`, `maxint16`, `maxint32`, `maxint64`) represent the minimum (resp. maximum) values for `int8, `int16`, `int32`, `int64. 
- Symbol `minint` (resp. `maxint`)  represent minimum (resp. maximum) values for the integer type considered in the context where it used. 
