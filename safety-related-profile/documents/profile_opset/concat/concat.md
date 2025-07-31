
### Contents

- `concat` [operator (heterogeneous: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64, FP16, FP32, FP64, BFLOAT16, STRING, BOOL)](#heterogeneous) 
<a id="heterogeneous"></a>
\
In accordance with ONNX specifications, in the following document, the term **heterogeneous** describes an operator input or output that supports multiple, different data types. This work is based on ONNX description for the `concat` operator in version 13.

## `concat` `(heterogeneous)`

### Signature

`Y = concat(`$X_{0}, \dots, X_{n}$`)`

where

-  `T1` : $X_{0}, \dots ,X_{n}$ : input tensors with $n \in [0, 2^{31}-1[$
-  `Y`: output concatenated tensor

#### Restrictions

The following restriction applies to the `concat` operator for the SONNX profile:


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1`   | Attribute `axis` lower bound is restricted to 0. | Transient | 



#### Informal specification

The  `concat` operator concatenates the input tensors $X_{0}, \dots , X_{n}$ along the `axis` into a single output tensor `Y`. Input tensors are of rank $r$ defined as $r=dim(inputs) \in [1, 2^{31}-1]$. Let $a$ be the concatenation axis and $d_{k,a}$ `T5` the dimension of the $X_{k}$ input tensor $k$ along the axis $a$.

The mathematical definition of the operator `concat` is given hereafter. The formal specification is given in section [**Formal specification**](#formal_spec) below. 


$$\begin{gathered}
 \mathtt{T2:} \text{  } Y[i_{0}, \dots , i_{r-1}] = X_{k}[i_{0}, \dots,  i_{a}', \dots, i_{r-1}], \text{  } \mathtt{ T3:} \text{  if } \text{  } \exists k \in [0, n], \text{  } s_k \le i_a \le s_k + d_{k,a}
\end{gathered}$$


Where
- `Y` shape matches the input shapes, except along the axis dimension $a$, which is the sum of the input dimensions. 
- $i_{0}$ and $i_{r-1}$ are the indices which access respectively the first and last dimensions of a tensor to uniquely identify an element. 
- $k$ `T3` refers to the index of a specific input tensor that satisfies:
```math
\mathtt{T4:} \text{  } s_k \leq i_{a} < s_k + d_{k,a}
``` 
- $i_{a}'$ the local index in a local tensor $X_{k}$ corresponding to the global index $i_{a}$ along dimension $a$, is defined as follows:

```math
  \mathtt{T5:} \text{  } i'_{a} = i_{a} - s_k
```
- with $s_k$ the cumulative offset along axis before input $X_{k}$ defined as:  

```math
\mathtt{T6:} \text{  } s_k= \sum_{j=0}^{k-1} d_{j,a}
```



![Concat example 1](imgs/Concat_example.png)

Let's compute the concatenation illustrated by the example above:
```math
Y = \text{concat}(X_0, X_1, X_2) \quad \text{along axis}=1
```
Now, let's calculate for \( $i_a = 3$ \):
```math
Y[0, 3] = X_k[0, 3 - s_k]
```
According to the inequality:
```math
s_k \leq i_a < s_k + d_{k,a}
```
We check for which \( $k$ \) this holds:
```math
s_1 \leq i_a < s_1 + d_{1,a} \Rightarrow 3 \leq 3 < 3 + 2 = 5
```
Thus,
```math
k = 1
```
So,
```math
Y[0,3] = X_1[0, 3 - s_1] = X_1[0, 3 - 3] = X_1[0, 0]
```

You can find more examples in [tests](./tests/.) folder.


#### Error conditions
No error conditions since there is no computation for `concat` operator. 

#### Inputs


#####  **$X_{0},...,X_{n}$** (variadic, heterogeneous)

`concat` operator accepts a *variadic* list of input tensors defined as multiple input tensors (e.g., $X_{0},...,X_{n}$). The operator `concat` is not commutative so the input tensors order impacts on the output tensor. Its type parameter is *heterogeneous*, please refer to the definition given above (see [heterogeneous](#heterogeneous)). 

`T7`: All inputs must have the same total count of dimensions. Dimension sizes must match on all axes other than the concatenation axis `T8` . 

#####  Constraints

- `C1`: Value range
	- Statement: The number of input tensors must range from [1, $2^{31}-1$] 
- `C2`: Shape consistency
    - Statement: All tensors must have the same shape except for the concatenation axis, i.e, 

```math
 \mathtt{T8:} \text{  } \forall i,k \text{ and all } j \neq a: d_{i,j} = d_{k,j}
```

#### Attributes

##### `axis`: int (required)
Attribute  `axis`  determines the axis along which concatenation should done. 

##### Constraints

-   `C1`: Value domain
    -   Statement: `axis` value ranges from $[0, r-1]$   with $r=dim(inputs)$. The range of the axis value is reduced to positive values regarding our applied specific activity.`R1`  
	
#### Output

##### `Y` (heterogeneous)

Tensor  `Y`  is the output tensor of the concatenation and its type parameters is also *heterogeneous* as input tensors (see the definition of [heterogeneous](#heterogeneous)).

##### Constraints

-   `C1`: Shape consistency
	-	 Statement: Output tensor must have the same shape as input tensors except for the concatenation axis where this dimension is the sum of the dimensions of the inputs i.e,

```math
  \mathtt{T9:} \text{  } shape(Y) = (d_0,d_1, \dots, d_{r-1})
```
```math
d_j = \sum_{i=1}^{n} d_{i,j} \text{ if } j=a \text{ and } d_{j} = d_{1,j} \text{ otherwise }
```      

<a id="formal_spec"></a>

#### Formal specification
The formal specification of the `concat` operator using the Why3 language is provided in the folder [why3](./why3/.). This specification ensures the consistency and desired behavior of the operator within the constraints described.

#### Numerical Accuracy
`concat` operator does not perform numerical operations thus numerical accuracy issues are not considered here. 
