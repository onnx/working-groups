
# Preliminary remarks

## Types

- Operators are initially described for values in the domain of real numbers. The `concat` operator concatenates input tensors $A_{0}, \dots, A_{N}$ into a single tensor `concat_result` . The output and inputs  can be of various types including `tensor(bfloat16)`, `tensor(bool)`, `tensor(complex128)`, `tensor(complex64)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, `tensor(uint8)`.
 The dimension size of a tensor, defined by his rank (number of dimensions) is defined by r = $rank(tensor)$ with $r \in  \mathbb{N}$.
**(Version 13)**

# `concat` operator

### Restrictions

The following restrictions apply to the `concat` operator for the SONNX profile:


| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | All inputs $\underbrace{A_{0}, \dots, A_k, \dots, A_{N}}_{n}$ where $n \in \mathbb{N}$  and $n \in [1, 2^{31}-1]$ are indexed starting from 0 up to $N$ and $k$ represents an index within this sequence, so $0 \leq k \leq N$ and $N \in [0, 2^{31}-2]$. These input tensors must be of types that support the concat operation | Simplification |
| `[R2]` | No broadcasting allowed for the input tensors  inputs $A_{0}, \dots, A_{k}, \dots, A_{N}$ even if they are broadcastable to a common shape, the broadcasting is forbidden because dynamic computation time according to the shape is not deterministic   | [Deterministic operators](../../../deliverables/reqs/reqs.md#Deterministic_operators) |
| `[R3]` |All inputs $A_{0}, \dots, A_{k}, \dots, A_{N}$ and output elements shall be of the same type (no shape inference) | [No shape inference ](../../../deliverables/reqs/reqs.md#Explicit_types_and_shapes) | 


In the following documentation, you will find key points, labeled **(E1)** through **(E9)**, which serve as explanations. These same points also appear in the formal Why3 definition of the selected operator.

### Signature

`concat_result = concat(`$\underbrace{A_{0}, \dots, A_{N}}_{n}$`)`

where

-  **E1** : $A_{0}, \dots ,A_{N}$ : input tensors with $N \in [0, 2^{31}-2]$ and $n \in [1, 2^{31}-1]$
-  `concat_result`: output tensor resulting from the concatenation of the inputs  $A_{0}, \dots , A_{N}$

#### Informal specification

The  `concat`  operator computes the concatenation operation from the input tensors $A_{0}, \dots , A_{N}$ along the axis specified as an attribute. Each tensor concatenated result in the output tensor  `concat_result`.

Let $A_{0}, \dots , A_{N}$ input tensors of rank $r$ ( the number of dimensions for the input tensors), where $r \in  \mathbb{N}$.
Let `concat_result` be the output tensor obtained by concatenating $A_{0}, \dots , A_{N}$ along axis $d$,  where $d \in [0,1,...,r−1]$.

The assignment describing how elements from a tensor $A_{k}$ with $0 \leq k \leq N$ are placed into `concat_result` is: 
\
**E2**:
```math
concat\_result[\underbrace{:, ..., :}_{d}, i, \underbrace{:, ..., :}_{r-1-d}] = A_{k}[\underbrace{:, ..., :}_{d}, i', \underbrace{:, ..., :}_{r-1-d}]
```
with 
\
**E3**:
```math
i'= i - \sum_{j=0}^{k-1}D_{j}^{d}
``` 
$i$ is the global index of the ouptut tensor and $i'$ represents the local index associated to $i$ for a specific considedered tensor $A_{k}$. $i'$ is a change of variable and is expressed according $i$ and $k$. 
So that, 

```math
concat\_result[\underbrace{:, ..., :}_{d}, i, \underbrace{:, ..., :}_{r-1-d}] = A_{k}[\underbrace{:, ..., :}_{d},  i - \sum_{j=0}^{k-1}D_{j}^{d} , \underbrace{:, ..., :}_{r-1-d}]
``` 

to simplify the formula, the variable $\sigma_{k}$ has been introduced and is defined by 
\
**E4**:
```math
\sigma_{k} = \sum_{j=0}^{k}D_{j}^{d}
``` 
so,
```math
concat\_result[:, ..., :, i, :, ..., :] = A_{k}[:, ..., :,  i - \sigma_{k-1} , :, ..., :]
``` 

The operator `[]` access the values or elements of tensors when provided with specific indices.
\
The operator `:` selects the entire set of valid indices for an axis different from $d$. 

Where

- The global index of the output concatanated tensor $i \in \mathbb{N}$ along the axis $d$ range from $i \in [0, \sigma_{k}-1]$ and $i' \in [0, D_{k}^{d}-1]$ with $d \in \mathbb{N}, d \in [0, r-1]$ **(E3)**
- $D_{k}^{d}$ represents the dimension of the tensor $A_{k}$ along the axis $d$ **(E4)**
- $\underbrace{:, ..., :}_{d}$ specifies the number of distinct dimensions before the dimension specified by the index $i$. 
- $\underbrace{:, ..., :}_{r-1-d}$ specifies the number of distinct dimensions after the dimension specified by the index $i$.

- The following property  determines which tensor $k$ the element at global index $i$ originates from.
\
**E5**:
```math
\sum_{j=0}^{k-1}D_{j}^{d} \le i  < \sum_{j=0}^{k}D_{j}^{d} \Leftrightarrow \sigma_{k-1} \le i  < \sigma_{k}
```
- Let $\mathbb{S}$ be the set combining reals and boolean values defined by their respective sets as $\mathbb{R}$ and $\mathbb{Z}$, so that $\mathbb{S}$ represents:
```math
\mathbb{S} = \mathbb{R} \cup \mathbb{Z}
```
- **E6**: $A_{0} \in \mathbb{S}^{(D_{0}, D_{1},...,D_{r-1})}, ..., A_{N}  \in \mathbb{S}^{(D_{0'}, D_{1'},...,D_{r-1})}$ $A_{0},...,A_{N}$ are tensors of rank $r$, their dimension match **except along the $axis$ specified** 
- **E7**: `concat_result` $\in \mathbb{S}^{(D_{0}, D_{1},...,D_{d-1},D_{A_{0}}^{d}+...+D_{A_{N}}^{d} ,D_{d+1},..., D_{r-1})}$ `concat_result` output concatenated tensor with **size along the $axis=d$ is the sum** of the size of $A_{0}$ $D_{A_{0}}^{d}$ until the size of $A_{N}$ $D_{A_{N}}^{d}$ along this same axis 

Example 1:
![Concat example 1](imgs/Concat_example_1.jpg)

Let's take three input tensors: 


```math
A_{0}  \in \mathbb{R}^{(2,3)} = \begin{bmatrix} 1 & 1 & 1\\  1 & 1 & 1 \end{bmatrix}, 
A_{1} \in \mathbb{R}^{(4,3)} = \begin{bmatrix} 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2  \end{bmatrix}, A_{2} \in \mathbb{R}^{(3,3)} = \begin{bmatrix} 3 & 3 & 3 \\ 3 & 3 & 3 \\ 3 & 3 & 3  \end{bmatrix}
``` 

```math
concat\_result = concat(A_{0},A_{1}, A_{2}) \text{ along } axis =d =0
```
Let's compute the different values of $\sigma_{k}$ as introduced before as 
```math
\sigma_{k} = \sum_{j=0}^{k}D_{j}^{d}
```
so,
```math
 \sigma_{0} = D_{0}^{d} = 2, \sigma_{1}  = \sigma_{0} + D_{1}^{d} =  6,  \sigma_{2} =  \sigma_{1}+ D_{2}^{d} =   9
```

```math
i \in [0, (D_{0}^{d} + D_{1}^{d} + D_{2}^{d}-1)], i \in [0, 8]
```
\
for $i=0:$
```math
concat\_ result[0,:]=A_{k}[0 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
and according the following inequality,
```math
\sum_{j=0}^{k-1}D_{j}^{d} \le i  < \sum_{j=0}^{k}D_{j}^{d} \Leftrightarrow \sigma_{k-1} \le i  < \sigma_{k}
```
the inequality below can be inferred as,

$0 \leq  i < \sigma_{0} \Rightarrow 0\leq 0 <2 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[0,:]=A_{0}[0 - \sum_{j=0}^{-1}D_{j}^{d},:] = A_{0}[0 - 0,:] = A_{0}[0,:] = (1, 1, 1)
```


for $i=1:$
```math
concat\_ result[1,:]=A_{k}[1 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
and according the same mathematical property as stated before,
```math
\sum_{j=0}^{k-1}D_{j}^{d} \le i  < \sum_{j=0}^{k}D_{j}^{d} \Leftrightarrow \sigma_{k-1} \le i  < \sigma_{k}
```
the following inequality can be deducted as,

$0 \leq  i < \sigma_{0} \Rightarrow 0\leq 1<2 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 


```math
concat\_ result[1,:]=A_{0}[1 - \sum_{j=0}^{-1}D_{j}^{d},:] = A_{0}[1 - 0,:] = A_{0}[1,: ] = (1, 1, 1)
```

for $i=2:$

```math
concat\_ result[2,:]=A_{k}[2 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```

the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 2\leq 2<6 \text{ therefor } k=1$

```math
concat\_ result[2,:]=A_{1}[2 - \sum_{j=0}^{0}D_{j}^{d},:] = A_{1}[2 - \sigma_{0},:] = A_{1}[0,:] = (2, 2, 2)
```

for $i=3:$
```math
concat\_ result[3,:]=A_{k}[3 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 2\leq 3<6 \text{ therefor } k=1$

```math
concat\_ result[3,:]=A_{1}[3 - \sum_{j=0}^{0}D_{j}^{d},:] = A_{1}[3 - 2,:] = A_{1}[1,:] = (2, 2, 2)
```

for $i=4:$
```math
concat\_ result[4,:]=A_{k}[4 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 2\leq 4<6 \text{ so } k=1$

```math
concat\_ result[4,:]=A_{1}[4 - \sum_{j=0}^{1}D_{j}^{d},:] = A_{1}[4 - 2,:] = A_{1}[2,:] = (2, 2, 2)
```

for $i=5:$
```math
concat\_ result[5,:]=A_{k}[5 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 2\leq 5<6 \text{ therefor } k=1$

```math
concat\_ result[5,:]=A_{1}[5 - \sum_{j=0}^{0}D_{j}^{d},:] = A_{1}[5 - 2,:] = A_{1}[3,:] = (2, 2, 2)
```

for $i=6:$
```math
concat\_ result[6,:]=A_{k}[6 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 6\leq 6<9 \text{ so } k=2$

```math
concat\_ result[6,:]=A_{2}[6 - \sum_{j=0}^{1}D_{j}^{d},:] = A_{2}[6 - 6,:] = A_{2}[0,:] = (3, 3, 3)
```

for $i=7:$
```math
concat\_ result[7,:]=A_{k}[7 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 6\leq 7<9 \text{ therefor } k=2$

```math
concat\_ result[7,:]=A_{2}[7 - \sum_{j=0}^{1}D_{j}^{d},:] = A_{2}[7 - 6,:] = A_{2}[1,:] = (3, 3, 3)
```

for $i=8:$
```math
concat\_ result[8,:]=A_{k}[8 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```
the inequality below can be inferred thanks to the property stated above as,

$\sigma_{1} \leq  i <\sigma_{2} \Rightarrow 6\leq 8<9 \text{ therefor } k=2$

```math
concat\_ result[8,:]=A_{2}[8 - \sum_{j=0}^{1}D_{j}^{d},:] = A_{2}[8 - 6,:] = A_{2}[2,:] = (3, 3, 3)
```
The output concatenated tensor is, 
```math
concat\_result  \in \mathbb{R}^{(9,3)} = \begin{bmatrix} 1 & 1 & 1\\ 1 & 1 & 1\\2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\ 2 & 2 & 2 \\3 & 3 & 3 \\ 3 & 3 & 3 \\ 3 & 3 & 3 \end{bmatrix}
```
The example is repeated with 

```math
d=axis=1
```
Tensor concatenation requires input tensors ($A_{0}, A_{1}, A_{2}$) to share the same dimensions, except along the concatenation axis itself (specified as $d=axis=0$). The tensors $A_{0}, A_{1}, A_{2}$ did not meet this condition, as their sizes along $d=axis=0$ were different **(E6)**. Consequently, the concatenation failed and the example cannot proceed. 

Example 2:
\
Let's take two input tensors:
```math
A_0 \in \mathbb{R}^{(2,3,3)} \quad
\left[
  \begin{bmatrix} 
     1 &  2 &  3 & 10 \\
     4 &  5 &  6 & 11 \\
     7 &  8 &  9 & 12 
  \end{bmatrix}
  \quad 
  \begin{bmatrix} 
     11 & 12 & 13 & 20 \\
     14 & 15 & 16 & 21 \\
     17 & 18 & 19 & 22 
  \end{bmatrix}
\right]
```
```math
A_1 \in \mathbb{R}^{(2,3,3)} \quad
\left[
 \begin{bmatrix} 
     101 & 102 & 103 & 110 \\
     104 & 105 & 106 & 120 \\
     107 & 108 & 109 & 130 
  \end{bmatrix}
  \quad 
  \begin{bmatrix} 
     111 & 112 & 113 & 120 \\
     114 & 115 & 116 & 121 \\
     117 & 118 & 119 & 122 
  \end{bmatrix}
\right]
```
```math
concat\_result = concat(A_{0},A_{1}) \text{ along } axis =d =0
```
Let's compute the different values of $\sigma_{k}$ as introduced before as 
```math
\sigma_{k} = \sum_{j=0}^{k}D_{j}^{d}
```
so,
```math
 \sigma_{0} = D_{0}^{d} = 2, \sigma_{1}  = \sigma_{0} + D_{1}^{d} =  4
```

```math
i \in [0, (D_{0}^{d} + D_{1}^{d}) -1)], i \in [0, 3]
```
\
for $i=0:$
```math
concat\_ result[0,:,:]=A_{k}[0 - \sum_{j=0}^{k-1}D_{j}^{d},:,:]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 0<2 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[0,:,:]=A_{0}[0 - \sum_{j=0}^{-1}D_{j}^{d},:,:] = A_{0}[0 - 0,:,:] = A_{0}[0,:,:] =   \begin{bmatrix} 
     1 &  2 &  3 & 10 \\
     4 &  5 &  6 & 11 \\
     7 &  8 &  9 & 12 
  \end{bmatrix}
```
for $i=1:$
```math
concat\_ result[1,:,:]=A_{k}[1 - \sum_{j=0}^{k-1}D_{j}^{d},:,:]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 1<2 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[0,:,:]=A_{0}[1 - \sum_{j=0}^{-1}D_{j}^{d},:,:] = A_{0}[1 - 0,:,:] = A_{0}[1,:,:] =   \begin{bmatrix} 
     11 & 12 & 13 & 20 \\
     14 & 15 & 16 & 21 \\
     17 & 18 & 19 & 22 
  \end{bmatrix}
```
```math
\vdots
```
for $i=3:$
```math
concat\_ result[3,:,:]=A_{k}[3 - \sum_{j=0}^{k-1}D_{j}^{d},:,:]
```

the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 2\leq 3<4 \text{ therefor } k=1$

Thus, 

```math
concat\_ result[3,:,:]=A_{1}[0 - \sum_{j=0}^{0}D_{j}^{d},:,:] = A_{1}[3 - 2,:,:] = A_{1}[1,:,:] =   \begin{bmatrix} 
     111 & 112 & 113 & 120 \\
     114 & 115 & 116 & 121 \\
     117 & 118 & 119 & 122 
  \end{bmatrix}
```

The output concatenated tensor is, 
```math
concat\_result  \in \mathbb{R}^{(4,3,4)} = 
\quad
\left[
  \begin{bmatrix} 
     1 &  2 &  3 & 10 \\
     4 &  5 &  6 & 11 \\
     7 &  8 &  9 & 12 
  \end{bmatrix}
  \quad 
  \begin{bmatrix} 
     11 & 12 & 13 & 20 \\
     14 & 15 & 16 & 21 \\
     17 & 18 & 19 & 22 
  \end{bmatrix}
  \quad 
  \begin{bmatrix} 
     101 & 102 & 103 & 110 \\
     104 & 105 & 106 & 120 \\
     107 & 108 & 109 & 130 
  \end{bmatrix}
  \quad 
  \begin{bmatrix} 
     111 & 112 & 113 & 120 \\
     114 & 115 & 116 & 121 \\
     117 & 118 & 119 & 122 
  \end{bmatrix}
\right]
```
The example is repeated with 

```math
d=axis=1
```
Let's compute the different values of $\sigma_{k}$ as introduced before as 
```math
\sigma_{k} = \sum_{j=0}^{k}D_{j}^{d}
```
so,
```math
 \sigma_{0} = D_{0}^{d} = 3, \sigma_{1}  = \sigma_{0} + D_{1}^{d} =  6
```

```math
i \in [0, (D_{0}^{d} + D_{1}^{d}) -1)], i \in [0, 5]
```
\
for $i=0:$
```math
concat\_ result[:,0,:]=A_{k}[:,0 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 0<3 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[:,0,:]=A_{0}[:,0 - \sum_{j=0}^{-1}D_{j}^{d},:] = A_{0}[:,0 - 0,:] = A_{0}[:,0,:] =  \begin{bmatrix} 
    1 &  2 &  3 & 10  
\end{bmatrix}
\begin{bmatrix} 
    11 & 12 & 13 & 20 
\end{bmatrix}
```
for $i=1:$
```math
concat\_ result[:,1,:]=A_{k}[:,1 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 1<3 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[:,1,:]=A_{0}[:,1 - \sum_{j=0}^{-1}D_{j}^{d},:] = A_{0}[:,1 - 0,:] = A_{0}[:,1,:] =  \begin{bmatrix} 
    4 &  5 &  6 & 11 
\end{bmatrix}
\begin{bmatrix} 
    14 & 15 & 16 & 21
\end{bmatrix}
```
```math
\vdots
```
for $i=5:$
```math
concat\_ result[:,5,:]=A_{k}[:,5 - \sum_{j=0}^{k-1}D_{j}^{d},:]
```

the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 3\leq 5 <6 \text{ therefor } k=1$

Thus, 

```math
concat\_ result[:,5,:]=A_{1}[:,5 - \sum_{j=0}^{0}D_{j}^{d},:] = A_{1}[:,5-3,:] = A_{1}[:,2,:] =  \begin{bmatrix} 
    107 & 108 & 109 & 130 
\end{bmatrix}
\begin{bmatrix} 
    117 & 118 & 119 & 122 
\end{bmatrix}
```
The output concatenated tensor is, 
```math
concat\_result  \in \mathbb{R}^{(2,6,4)} = 
 \quad
\left[
  \begin{bmatrix} 
    1 &  2 &  3 & 10 \\
    4 &  5 &  6 & 11 \\
    7 &  8 &  9 & 12 \\
    101 & 102 & 103 & 110 \\
    104 & 105 & 106 & 120 \\
    107 & 108 & 109 & 130 
  \end{bmatrix}
  \quad
  \begin{bmatrix} 
   11 & 12 & 13 & 20 \\
   14 & 15 & 16 & 21 \\
   17 & 18 & 19 & 22 \\
   111 & 112 & 113 & 120 \\
   114 & 115 & 116 & 121 \\
   117 & 118 & 119 & 122 
  \end{bmatrix}
\right]
```
The example is repeated with 

```math
d=axis=2
```
Let's compute the different values of $\sigma_{k}$ as introduced before as 
```math
\sigma_{k} = \sum_{j=0}^{k}D_{j}^{d}
```
so,
```math
 \sigma_{0} = D_{0}^{d} = 4, \sigma_{1}  = \sigma_{0} + D_{1}^{d} =  8
```

```math
i \in [0, (D_{0}^{d} + D_{1}^{d}) -1)], i \in [0, 7]
```
\
for $i=0:$
```math
concat\_ result[:,:,0]=A_{k}[:,:,0 - \sum_{j=0}^{k-1}D_{j}^{d}]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 0<4 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[:,:,0]=A_{0}[:,:,0 - \sum_{j=0}^{-1}D_{j}^{d}] = A_{0}[:,:,0 - 0] = A_{0}[:,:,0] =  \begin{bmatrix} 
    1 \\
    4 \\
    7
\end{bmatrix}
\begin{bmatrix} 
    11 \\
    14 \\
    17
\end{bmatrix}
```

for $i=1:$
```math
concat\_ result[:,:,1]=A_{k}[:,:,1 - \sum_{j=0}^{k-1}D_{j}^{d}]
```

the inequality below can be inferred thanks to the property stated above as,

$0 \leq  i <\sigma_{0} \Rightarrow 0\leq 1<4 \text{ therefor } k=0$

```math
\sum_{j=0}^{-1}D_{j}^{d} = 0
```
The sum is defined by convention to be the empty sum when the set of indices for a summation is empty (meaning the lower limit is greater than the upper limit). Thus, 

```math
concat\_ result[:,:,1]=A_{0}[:,:,1 - \sum_{j=0}^{-1}D_{j}^{d}] = A_{0}[:,:,1 - 0] = A_{0}[:,:,1] =  \begin{bmatrix} 
    2 \\
    5 \\
    8
\end{bmatrix}
\begin{bmatrix} 
    12 \\
    15 \\
    18
\end{bmatrix}
```
```math
\vdots
```
for $i=6:$
```math
concat\_ result[:,:,6]=A_{k}[:,:,6 - \sum_{j=0}^{k-1}D_{j}^{d}]
```

the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 4\leq 6<8 \text{ therefor } k=1$

Thus, 

```math
concat\_ result[:,:,6]=A_{1}[:,:,6 - \sum_{j=0}^{0}D_{j}^{d}] = A_{1}[:,:,6 - 4] = A_{1}[:,:,2] =  \begin{bmatrix} 
    103 \\
    106 \\
    109
\end{bmatrix}
\begin{bmatrix} 
    113 \\
    116 \\
    119
\end{bmatrix}
```
for $i=7:$
```math
concat\_ result[:,:,7]=A_{k}[:,:,7 - \sum_{j=0}^{k-1}D_{j}^{d}]
```

the inequality below can be inferred thanks to the property stated above as,

$\sigma_{0} \leq  i <\sigma_{1} \Rightarrow 4\leq 7<8 \text{ therefor } k=1$

Thus, 

```math
concat\_ result[:,:,7]=A_{1}[:,:,7 - \sum_{j=0}^{0}D_{j}^{d}] = A_{1}[:,:,7 - 4] = A_{1}[:,:,3] =  \begin{bmatrix} 
    110 \\
    120 \\
    130
\end{bmatrix}
\begin{bmatrix} 
    120 \\
    121 \\
    122
\end{bmatrix}
```
The output concatenated tensor is, 
```math
concat\_result  \in \mathbb{R}^{(2,3,8)} = 
 \quad
\left[
  \begin{bmatrix} 
     1 &  2 &  3 & 10 & 101 & 102 & 103 & 110 \\
     4 &  5 &  6 & 11 & 104 & 105 & 106 & 120 \\
     7 &  8 &  9 & 12 & 107 & 108 & 109 & 130
  \end{bmatrix}
  \quad
  \begin{bmatrix} 
   11 & 12 & 13 & 20 & 111 & 112 & 113 & 120 \\
   14 & 15 & 16 & 21 & 114 & 115 & 116 & 121 \\
   17 & 18 & 19 & 22 & 117 & 118 & 119 & 122
  \end{bmatrix}
\right]
```

Example 3:
\
Let's take four input tensors:


```math
A_{0}  \in \mathbb{R}^{(1,1,3,2)}\begin{bmatrix} \begin{bmatrix} \begin{bmatrix} 3 & 3 \\  3 & 3 \\ 3 & 3 \end{bmatrix} \end{bmatrix}\end{bmatrix}  , A_{1}  \in \mathbb{R}^{(1,3,3,2)} \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}  \end{bmatrix}  , 
```
```math
A_{2}  \in \mathbb{R}^{(1,2,3,2)}  \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix}  \end{bmatrix} , A_{3}  \in \mathbb{R}^{(1,4,3,2)} \begin{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \begin{bmatrix} \begin{bmatrix}  6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \end{bmatrix} 
```


```math
concat\_result= Concat(A_{0}, A_{1}, A_{2}, A_{3}) \text{ along } axis =d= 1
```
```math
concat\_result  \in \mathbb{R}^{(1, 10, 3, 2)} = \begin{bmatrix} \begin{bmatrix} \begin{bmatrix} 3 & 3 \\  3 & 3 \\ 3 & 3 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 4 & 4 \\  4 & 4 \\ 4 & 4 \end{bmatrix} \end{bmatrix}
\\
 \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 5 & 5 \\  5 & 5 \\ 5 & 5 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}  \begin{bmatrix} \begin{bmatrix}  6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix} \begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}\begin{bmatrix}  \begin{bmatrix} 6 & 6 \\  6 & 6 \\ 6 & 6 \end{bmatrix} \end{bmatrix}   \end{bmatrix} 
```
You can find the examples above in the Python file located in the "tests" folder.

#### Inputs

##### **$A_{1},...,A_{N}$** 

Tensors  $A_{1},...,A_{N}$  are the inputs for the concatenation. The operator `concat` is not commutative so the input tensors order impacts on the output tensor.

**E8**: Inputs shapes must be the same. 
\
Specifically, dimension sizes must match on all axes other than the concatenation axis **(E6)** . Broadcastable tensor is forbidden.`[R2]`. 

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
    -   Statement: **E9**:  `axis` value ranges from $[0, r-1]$   with $r=rank(inputs)$. The range of the axis value is reduced to positive values regarding our applied specific activity.   
   

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