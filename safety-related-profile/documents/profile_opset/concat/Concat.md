
# Preliminary remarks

## Types

- Operators are initially described for values in the domain of real numbers. For `concat` operator all inputs and output can be of various types including `tensor(bfloat16)`, `tensor(bool)`, `tensor(complex128)`, `tensor(complex64)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, `tensor(uint8)`.**(Version 13)**

# `concat` operator

### Restrictions

The following restriction apply to the `concat` operator for the SONNX profile:


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]`   | Attribute `axis` lower bound is retricted to 0. | Simplification | 


In the following documentation, you will find key points, labeled **(E1)** through **(E9)**, which serve as explanations. These same points also appear in the formal Why3 definition of the selected operator.

### Signature

`Y = concat(`$X_{0}, \dots, X_{n}$`)`

where

-  **E1** : $X_{0}, \dots ,X_{n}$ : input tensors with $n \in [0, 2^{31}-1[$
-  `Y`: output concatenated tensor

#### Informal specification

The  `concat`  operator concatenates the input tensors $X_{0}, \dots , X_{n}$ along the `axis`. Input tensors are of rank $r$ defined as $r=dim(inputs) \in [1, 2^{31}-1]$.


Let $a$ be the concatenation axis and $d_{k,a}$ **(E4)** the dimension of the $X_{k}$ input tensor $k$ along the axis $a$. $s_k$ be the cumulative offset along axis before input $X_{k}$. Then 


```math
 \text{\textbf{E4}: } s_k= \sum_{j=0}^{k-1} d_{j,a}, \text{\textbf{E2}: } Y[i_{0}, \dots , i_{r-1}] = X_{k}[i_{0}, \dots,  i_{a}-s_k, \dots, i_{r-1}] \text{ if \textbf{E5}: } s_k \leq i_{a} < s_k + d_{k,a}
```
with 
```math
 \text{\textbf{E3}: } i'_{a} = i_{a} - s_k
```
With $i_{a}$ the global index along $a$ and be $i_{a}$ **prime** the local index associated with $i_{a}$ for a local tensor $X_{k}$. 

Example 1:
![Concat example 1](imgs/Concat_example_1.jpg)

Let's take three input tensors: 


```math
X_{0}  \in \mathbb{R}^{(2,3)} = \begin{bmatrix} 1 & 2 & 3\\  4 & 5 & 6 \end{bmatrix}, 
X_{1} \in \mathbb{R}^{(4,3)} = \begin{bmatrix} 7 & 8 & 9 \\ 10 & 11 & 12 \\ 13 & 14 & 15 \\ 16 & 17 & 18  \end{bmatrix}, X_{2} \in \mathbb{R}^{(3,3)} = \begin{bmatrix} 20 & 21 & 22 \\ 23 & 24 & 25 \\ 26 & 27 & 28  \end{bmatrix}
``` 

```math
Y = concat(X_{0},X_{1}, X_{2}) \text{ along } axis =0
```
Let's compute the different values of $s_{k}$ as introduced before as 
```math
s_{k} = \sum_{j=0}^{k-1}d_{j,a}
```
so,
```math
 s_{0} = d_{0,0} = 2, s_{1}  = s_{0} + d_{1,0} =  6,  s_{2} =  s_{1}+ d_{2,0} =   9
```

```math
i_a \in [0, (d_{0,0} + d_{1,0} + d_{2,0}-1)], i_{a} \in [0, 8]
```
\
for $i_a=0:$
```math
Y[0, :]=X_{k}[0 - \sum_{j=0}^{k-1}d_{j,a},:]
```
and according the following inequality,
```math
s_k \leq i_{a} < s_k + d_{k,a}
```
the inequality below can be inferred as,

$s_{0} \leq  i_{a} < s_{0} + d_{0,0} \Rightarrow 0\leq 0 <2 \text{ therefor } k=0$

```math
s_0 = \sum_{j=0}^{-1}d_{j,0} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Then, 

```math
Y[0,:]=X_{0}[0 - \sum_{j=0}^{-1}d_{j,0},:] = X_{0}[0 - 0,:] = X_{0}[0,:] = (1, 2, 3)
```


for $i_a=1:$
```math
Y[1,:]=X_{k}[1 - \sum_{j=0}^{k-1}d_{j,0},:]
```
and according the same mathematical property as stated before,
```math
s_k \leq i_{a} < s_k + d_{k,a}
```
the following inequality can be deducted as,

$s_{0} \leq  i_{a} < s_{0} + d_{0,0} \Rightarrow 0\leq 1<2 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}d_{j,0} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Then, 


```math
Y[1,:]=X_{0}[1 - \sum_{j=0}^{-1}d_{j,0},:] = X_{0}[1 - 0,:] = X_{0}[1,:] = (3, 4, 5)
```

for $i_a=2:$

```math
Y[2,:]=X_{k}[2 - \sum_{j=0}^{k-1}d_{j,0},:]
```

the inequality below can be inferred thanks to the property stated above as,

$s_{1} \leq  i_{a} <s_{1} + d_{1,0} \Rightarrow 2\leq 2<6 \text{ therefor } k=1$

```math
Y[2,:]=X_{1}[2 - \sum_{j=0}^{0}d_{j,0},:] = X_{1}[2 - s_{0},:] = X_{1}[0,:] = (7, 8, 9)
```
.
.
.

for $i_a=8:$
```math
Y[8,:]=X_{k}[8 - \sum_{j=0}^{k-1}d_{j,0},:]
```
the inequality below can be inferred thanks to the property stated above as,

$s{2} \leq  i_{a} <s_{2}  + d_{2,0} \Rightarrow 6\leq 8<9 \text{ therefor } k=2$

```math
Y[8,:]=X_{2}[8 - \sum_{j=0}^{1}d_{j,0},:] = X_{2}[8 - 6,:] = X_{2}[2,:] = (26, 27, 28)
```
The output concatenated tensor is, 
```math
Y  \in \mathbb{R}^{(9,3)} = \begin{bmatrix} 1 & 2 & 3\\ 4 & 5 & 6\\7 & 8 & 9 \\ 10 & 11 & 12 \\ 13 & 14 & 15 \\ 16 & 17 & 18 \\20 & 21 & 22 \\ 23 & 24 & 25 \\ 26 & 27 & 28 \end{bmatrix}
```
The example is repeated with 

```math
axis=1
```
Tensor concatenation requires input tensors ($X_{0}, X_{1}, X_{2}$) to share the same dimensions, except along the concatenation axis itself (specified as $axis=0$). The tensors $X_{0}, X_{1}, X_{2}$ did not meet this condition, as their sizes along $axis=0$ were different **(E6)**. Consequently, the concatenation failed and the example cannot proceed. 

You can find the examples above in the Python file located in the "tests" folder.

#### Inputs

##### **$X_{0},...,X_{n}$** 

Tensors  $X_{0},...,X_{n}$  are the inputs for the concatenation. The operator `concat` is not commutative so the input tensors order impacts on the output tensor.

**E8**: All inputs must have the same total count of dimensions. Dimension sizes must match on all axes other than the concatenation axis **(E6)** . 

###### Constraints

- (C1) Value range
	- Statement: The number of input tensors must range from [1, $2^{31}-1$] 
-   (C2) Shape consistency
    -   Statement: All tensors must have the same shape except for the concatenation axis, i.e, 
\
**E6**:
```math
\forall i,k \text{ and all } j \neq a: d_{i,j} = d_{k,j}
```

	
#### Output

##### `Y`

Tensor  `Y`  is the output tensor of the concatenation.

###### Constraints

-   (C1)  Shape consistency
	-	 Statement: Output tensor must have the same shape as input tensors except for the concatenation axis where this dimension is the sum of the dimensions of the inputs i.e,
\
**E7**:
```math
shape(Y) = (d_0,d_1, \dots, d_{r-1})
```
```math
d_j = \sum_{i=1}^{n} d_{i,j} \text{ if } j=a \text{ and } d_{j} = d_{1,j} \text{ otherwise }
```      

#### Attributes

##### `axis`: int
Attribute  `axis`  determines the axis along which concatenation should done. 

###### Constraints

-   (C1) Value domain
    -   Statement: **E9**:  `axis` value ranges from $[0, r-1]$   with $r=dim(inputs)$. The range of the axis value is reduced to positive values regarding our applied specific activity.`[R1]`   
   

### Formal specification
The formal specification of the `concat` operator using the Why3 language is provided in the folder **why3**. This specification ensures the consistency and desired behavior of the operator within the constraints described.


###### Sources
The references used for the writing of this documentation are: 
* [ONNX operator concat](https://onnx.ai/onnx/operators/onnx__Concat.html)
* [NNEF definition for concat](https://registry.khronos.org/NNEF/)
* [OpenXLA concatenate](https://openxla.org/xla/operation_semantics?hl=fr#concatenate)
* [Concat operator analytica](https://docs.analytica.com/index.php/Concat)
* [Concat operator for string type](https://info-llg.fr/option-mp/pdf/03.langages.pdf)
* [Concat operator from Wikipedia](https://en.wikipedia.org/wiki/Concatenation)