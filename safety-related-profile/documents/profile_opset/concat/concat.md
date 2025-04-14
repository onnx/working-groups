
# Preliminary remarks

## Types

- Operators are initially described for values in the domain of real numbers. The `concat` operator concatenates input tensors `A` and `B` into a single tensor `C` . The output and inputs  can be of various types including `tensor(bfloat16)`, `tensor(bool)`, `tensor(complex128)`, `tensor(complex64)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, `tensor(uint8)`.
 The dimension size of a tensor is defined by $N(tensor)$.
**(Version 13)**

# `concat` operator

### Restrictions

The following restrictions apply to the `concat` operator for the SONNX profile:


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | All inputs $A_{1},...,A_{N}$ with $N \in [1, 2^{31}-1]$ must be of types that support the concat operation | Simplification |
| `[R2]` | No broadcasting allowed for the input tensors  inputs $A_{1},...,A_{N}$ even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic   | [Deterministic operators](../../../deliverables/reqs/reqs.md#Deterministic_operators) |
| `[R3]` |All inputs $A_{1},...,A_{N}$ and output elements shall be of the same type (no shape inference) | [No shape inference ](../../../deliverables/reqs/reqs.md#Explicit_types_and_shapes) | 




### Signature

`concat_result = concat(`$A_{1},...,A_{N}$`)`

where

-  $A_{1},...,A_{N}$ : input tensors with $N \in [1, 2^{31}-1]$
-  `concat_result`: output tensor resulting from the concatenation of the inputs  $A_{1},...,A_{N}$

#### Informal specification

The  `concat`  operator computes the concatenation operation from the input tensors $A_{1}$... $A_{N}$ along the axis specified as an attribute. Each tensor concatenated result in the output tensor  `concat_result`.

The mathematical definition of the operator is given hereafter.


```math
concat\_result[\underbrace{:, ..., :}_{d-1}, i, \underbrace{:, ..., :}_{n-d}] = A_{k}[\underbrace{:, ..., :}_{d-1}, i', \underbrace{:, ..., :}_{n-d}]
```
with 

```math
i'= i - \sum_{j=1}^{k-1}D_{j}^{d}
``` 

Where

- $n = N(tensor)$ and $d = axis$
- $k \in [1,..,N] \text{ with } N \in  [1, 2^{31}-1]$ 
- $D_{k}^{d}$ represents the dimension of the tensor $A_{k}$ along the axis $d$ with $d \in [0, r-1]$ with $r=rank(inputs)$
```math
\bullet  i \in [0, \sum_{j=1}^{k}D_{j}^{d} - 1] \text{ and }\sum_{j=1}^{k-1}D_{j}^{d} \le i  < \sum_{j=1}^{k}D_{j}^{d}
```
- $A_{1} \in \mathbb{R}^{(D_{0}, D_{1},...,D_{r-1})}, ..., A_{N}  \in \mathbb{R}^{(D_{0'}, D_{1'},...,D_{r-1})}$
$A_{1},...,A_{N}$ are tensors of rank $r$, their dimension match except along the $axis$ specified
- `concat_result` $\in \mathbb{R}^{(D_{0}, D_{1},...,D_{d-1},D_{A_{1}}^{d}+...+D_{A_{N}}^{d} ,D_{d+1},..., D_{r-1})}$
`concat_result` output concatenated tensor with size along the $axis=d$ is the sum of the size of $A_{1}$ $D_{A_{1}}^{d}$ until the size of $A_{N}$ $D_{A_{N}}^{d}$ along this same axis

Example 1:
![Concat example 1](imgs/Concat_example_1.jpg)
Let's take three input tensors: 


```math
A_{1}  \in \mathbb{R}^{(2,3)} = \begin{bmatrix} 1 & 1 & 1\\  1 & 1 & 1 \end{bmatrix}, 
A_{2} \in \mathbb{R}^{(4,3)} = \begin{bmatrix} 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2  \end{bmatrix}, A_{3} \in \mathbb{R}^{(3,3)} = \begin{bmatrix} 3 & 3 & 3 \\ 3 & 3 & 3 \\ 3 & 3 & 3  \end{bmatrix}
``` 

```math
concat\_result = concat(A_{1},A_{2}, A_{3}) \text{ along } axis =d =0
```

```math
\sigma_{0} = D_{0}^{d} = 0, \sigma_{1}  = \sigma_{0} + D_{1}^{d} =  2,  \sigma_{2} =  \sigma_{1}+ D_{2}^{d} =   6,  \sigma_{3} = \sigma_{2} + D_{3}^{d} = 9
```

```math
i \in [0, (D_{1}^{d} + D_{2}^{d} + D_{3}^{d}-1)], i \in [0, 8]
```
\
for $i=0:$
```math
concat\_ result[0,:]=A_{k}[0 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```

$\sigma_{0} \leq  i < \sigma_{1} \Rightarrow 0\leq 0 <2 \text{ as } k=1$

```math
concat\_ result[0,:]=A_{1}[0 - \sum_{j=1}^{0}D_{j}^{d},:] = A_{1}[0 - \sigma_{0},:] = A_{1}[0,:] = (1, 1, 1)
```

for $i=1:$
```math
concat\_ result[1,:]=A_{k}[1 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```

$\sigma_{0} \leq  i < \sigma_{1} \Rightarrow 0\leq 1<2 \text{ as } k=1$

```math
concat\_ result[1,:]=A_{1}[1 - \sum_{j=1}^{0}D_{j}^{d},:] = A_{1}[1 - \sigma_{0},:] = A_{1}[1,: ] = (1, 1, 1)
```

for $i=2:$

```math
concat\_ result[2,:]=A_{k}[2 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 2\leq 2<6 \text{ as } k=2$

```math
concat\_ result[2,:]=A_{2}[2 - \sum_{j=1}^{1}D_{j}^{d},:] = A_{2}[2 - 2,:] = A_{2}[0,:] = (2, 2, 2)
```

for $i=3:$
```math
concat\_ result[3,:]=A_{k}[3 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 3\leq 2<6 \text{ as } k=2$

```math
concat\_ result[3,:]=A_{2}[3 - \sum_{j=1}^{1}D_{j}^{d},:] = A_{2}[3 - 2,:] = A_{2}[1,:] = (2, 2, 2)
```

for $i=4:$
```math
concat\_ result[4,:]=A_{k}[4 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 3\leq 4<6 \text{ as } k=2$

```math
concat\_ result[4,:]=A_{2}[4 - \sum_{j=1}^{1}D_{j}^{d},:] = A_{2}[4 - 2,:] = A_{2}[2,:] = (2, 2, 2)
```

for $i=5:$
```math
concat\_ result[5,:]=A_{k}[5 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 3\leq 5<6 \text{ as } k=2$

```math
concat\_ result[5,:]=A_{2}[5 - \sum_{j=1}^{1}D_{j}^{d},:] = A_{2}[5 - 2,:] = A_{2}[3,:] = (2, 2, 2)
```

for $i=6:$
```math
concat\_ result[6,:]=A_{k}[6 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{2} \leq  i <\sigma_{3} \Rightarrow 6\leq 6<9 \text{ as } k=3$

```math
concat\_ result[6,:]=A_{3}[6 - \sum_{j=1}^{2}D_{j}^{d},:] = A_{3}[6 - 6,:] = A_{3}[0,:] = (3, 3, 3)
```

for $i=7:$
```math
concat\_ result[7,:]=A_{k}[7 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{2} \leq  i <\sigma_{3} \Rightarrow 6\leq 7<9 \text{ as } k=3$

```math
concat\_ result[7,:]=A_{3}[7 - \sum_{j=1}^{2}D_{j}^{d},:] = A_{3}[7 - 6,:] = A_{3}[1,:] = (3, 3, 3)
```

for $i=8:$
```math
concat\_ result[8,:]=A_{k}[8 - \sum_{j=1}^{k-1}D_{j}^{d},:]
```
$\sigma_{2} \leq  i <\sigma_{3} \Rightarrow 6\leq 8<9 \text{ as } k=3$

```math
concat\_ result[8,:]=A_{3}[8 - \sum_{j=1}^{2}D_{j}^{d},:] = A_{3}[8 - 6,:] = A_{3}[2,:] = (3, 3, 3)
```
Then we have, 
```math
concat\_result  \in \mathbb{R}^{(9,3)} = \begin{bmatrix} 1 & 1 & 1\\ 1 & 1 & 1\\2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\3 & 3 & 3 \\ 3 & 3 & 3 \\ 3 & 3 & 3 \end{bmatrix}
```

Example 2:
\
Let's take four input tensors:


```math
A_{1}  \in \mathbb{R}^{(1,1,3,2)}\begin{bmatrix} \begin{bmatrix} \begin{bmatrix} 3 & 3 \\  3 & 3 \\ 3 & 3 \end{bmatrix} \end{bmatrix}\end{bmatrix}  , A_{2}  \in \mathbb{R}^{(1,3,3,2)} \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}  \end{bmatrix}  , 
```
```math
A_{3}  \in \mathbb{R}^{(1,2,3,2)}  \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix}  \end{bmatrix} , A_{4}  \in \mathbb{R}^{(1,4,3,2)} \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \begin{bmatrix} \begin{bmatrix}  6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \end{bmatrix} 
```


```math
concat\_result= Concat(A_{1}, A_{2}, A_{3}, A_{4}) \text{ along } axis =d= 1
```
```math
concat\_result  \in \mathbb{R}^{(1, 10, 3, 2)} = \begin{bmatrix} \begin{bmatrix} \begin{bmatrix} 3 & 3 \\  3 & 3 \\ 3 & 3 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}
\\
 \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \begin{bmatrix} \begin{bmatrix}  6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}   \end{bmatrix} 
```

#### Inputs

##### **$A_{1},...,A_{N}$** 

Tensors  $A_{1},...,A_{N}$  are the inputs for the concatenation. The operator `concat` is not commutative so the input tensors order impacts on the output tensor.

Their shapes must be the same, except for the dimension size of the axis to concatenate on. Broadcastable tensor is forbidden.`[R2]`. 

###### Constraints

- (C1) Value range
	- Statement: The input number of tensors must range from [1, $2^{31}-1$] 
-   (C2) Shape consistency
    -   Statement: The shapes of   **$A_{1},...,A_{N}$** shapes must be the same, $N(A_{1})=N(A_{2})= ... = N(A_{N})$
   except for the dimension size of the axis to concatenate on. Broadcastable tensor is forbidden.`[R2]`

-   (C3) Type consistency
	-	 Statement: Inputs and output type must be the same. All inputs $A_{1},...,A_{N}$ and output `concat_output ` elements shall be of the same type (no shape inference) `[R3]`
	
#### Output

##### `concat_output`

Tensor  `concat_output`  is the output tensor of the concatenation.

###### Constraints

-   (C1) Type consistency
	-	 Statement: Inputs and output type must be the same. All inputs $A_{1},...,A_{N}$ and output `concat_output ` elements shall be of the same type (no shape inference) `[R3]`

#### Attributes

##### `axis`: int
Attribute  `axis`  determines how the concatenation should be operated (along which axis). 

###### Constraints

-   (C1) Value domain
    -   Statement:  `axis` value ranges from $[0, r-1]$   with $r=rank(inputs)$. The range of the axis value is reduced to positive values regarding our applied specific activity.  
   

### Formal specification

(to be completed)