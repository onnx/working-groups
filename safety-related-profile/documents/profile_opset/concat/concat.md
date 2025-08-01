
### Contents

- `concat` [operator (INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64, FP16, FP32, FP64, BFLOAT16, STRING, BOOL)](#types) 

<a id="types"></a>

## `concat` `(INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64, FP16, FP32, FP64, BFLOAT16, STRING, BOOL)`

### Signature

`Y = concat(`$X_{0}, \dots, X_{n}$`)`

where

-  `[T1]:` $X_{0}, \dots ,X_{n}$ input tensors with $n \in [0, 2^{31}-1[$
-  `Y`: output concatenated tensor

#### Restrictions

The following restriction applies to the `concat` operator for the SONNX profile:


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]:`   | Attribute `axis` is positive. | Transient | 



#### Informal specification

The  `concat` operator concatenates the input tensors $X_{0}, \dots , X_{n}$ along the `axis` into a single output tensor `Y`. The operator `concat` is not commutative so the input tensors order impacts on the output tensor.

Let $a$ be the concatenation axis and $dX_{k,a}$ `[T5]` the dimension of the $X_{k}$ along the axis $a$. The mathematical definition of the operator `concat` is given hereafter. 


$$\begin{gathered}
 \mathtt{[T2]\mathord{:}} \text{  } Y[i_{0}, \dots , i_{r-1}] = X_{k}[i_{0}, \dots,  i_{a}', \dots, i_{r-1}], \text{  } \mathtt{ [T3]\mathord{:}} \text{  if } \text{  } \exists k \in [0, n], \text{  } s_k \le i_a \le s_k + dX_{k,a}
\end{gathered}$$


Where
- $i_{0}$ and $i_{r-1}$ are the indices which access respectively the first and last dimensions of a tensor to uniquely identify an element. 
- $k$ `[T3]` refers to the unique index of the source input tensor. Since there is always at least one input tensor `[T1]`, $k$ is guaranteed to exist and is found by the condition:
```math
\mathtt{[T4]\mathord{:}} \text{  } s_k \leq i_{a} < s_k + dX_{k,a}
``` 
- $i_{a}'$ the local index in $X_{k}$ corresponding to the global index $i_{a}$ along dimension $a$, is defined as follows:

```math
  \mathtt{[T5]\mathord{:}} \text{  } i'_{a} = i_{a} - s_k
```
- with $s_k$ the cumulative offset along axis before input $X_{k}$ defined as:  

```math
\mathtt{[T6]\mathord{:}} \text{  } s_k= \sum_{j=0}^{k-1} dX_{j,a}
```

The following example illustrates the concept explained above:

![Concat example 1](imgs/Concat_example.png)

Let's compute the concatenation illustrated by the example above:
```math
Y = \text{concat}(X_0, X_1, X_2) \text{ along axis}=1
```
Now, let's calculate for \( $i_a = 3$ \):
```math
Y[0, 3] = X_k[0, 3 - s_k]
```
According to the inequality:
```math
s_k \leq i_a < s_k + dX_{k,a}
```
We check for which \( $k$ \) this holds:
```math
s_1 \leq i_a < s_1 + dX_{1,a} \Rightarrow 3 \leq 3 < 3 + 2 = 5
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

`concat` operator accepts a a variadic list of input tensors. The accepted data types are defined in the [types](#types) section.

`[T7]:` All inputs must have the same total count of dimensions. Dimension sizes must match on all axes other than the concatenation axis `[T8]`. 

#####  Constraints

- `[C1]:` Limit on argument number
	- Statement: The number of input tensors must range from [1, $2^{31}-1$] 
- `[C2]:` Shape consistency
    - Statement: All tensors must have the same shape except for the concatenation axis, i.e, 

```math
 \mathtt{[T8]\mathord{:}} \text{  } \forall i,k \text{ and all } j \neq a: dX_{i,j} = dX_{k,j}
```
- `[C3]:` Limit on scalars
    - Statement: All input tensors must be non-scalar, meaning they must have a number of dimensions of at least one.  

```math
  \forall i,k : \sum dX_{i,j} \in [1, 2^{31}-1]
```

#### Attributes

##### `axis`: int (required)
Attribute  `axis`  determines the axis along which concatenation should done. 

##### Constraints

-   `[C1]:`Valid axis domain
    -   Statement: `axis` must be an integer identifying a valid dimension.
```math
 \forall i,k \text{  axis } \in [0, \sum dX_{i,j}-1]
```

#### Output

##### `Y` (heterogeneous)

Tensor  `Y`  is the output tensor of the concatenation and its type is the same as input tensors (see accepted [types](#types)).

##### Constraints

-   `[C1]:` Dimension of the concatenation axis
	-	 Statement: Output tensor must have the same shape as input tensors except for the concatenation axis where this dimension is the sum of the dimensions of the inputs i.e,

```math
   \forall i,k : r = \sum dX_{i,j}, \text{  } \mathtt{[T9]\mathord{:}} \text{  } shape(Y) = (dX_0,dX_1, \dots, dX_{r-1})
```
```math
dX_j = \sum_{i=1}^{n} dX_{i,j} \text{ if } j=a \text{ and } d_{j} = d_{1,j} \text{ otherwise }
```      

<a id="formal_spec"></a>

#### Formal specification
The formal specification of the `concat` operator using the Why3 language is provided in the folder [why3](./why3/.). This specification ensures the consistency and desired behavior of the operator within the constraints described.

#### Numerical Accuracy
`concat` operator does not perform numerical operations thus numerical accuracy issues are not considered here. 
