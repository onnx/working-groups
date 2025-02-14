# Contents
- `Div` [operator (real)](#real)
- `Div` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `Div` [operator (INT8, INT16, INT32)](#int)



<a id="real"></a>
# `Div` operator (real)

### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:
- Tensors `A`, `B` and `C` must have the same shape.  `[R1]` 

### Signature

`C = Div(A, B)`

where
- `A`: numerator of the division
- `B`: denominator of the division
- `C`: result of the element-wise division of `A` by `B`

#### Informal specification

The `Div` operator divides input tensors `A` and `B` element-wise and place the result in output tensor `C`. Each element `C` is the result of the division of the corresponding element in `A` by the corresponding element in `B`.

The mathematical definition of the operator is given hereafter for a unidimensional tensor, with $i$ covering all valid indexes:

$$
C[i] = 
\begin{cases} 
\frac{A[i]}{B[i]} & \text{if } B[i] \text{ is different from 0} \\
\text{undefined} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples:
- `A` and `B` are tensors holding numerical data

Example 1:
```math
A = \begin{bmatrix}  6 & 9 & 35 \end{bmatrix}
```
```math
B = \begin{bmatrix}  3 & 3 & 5 \end{bmatrix}
```
Result `C` will be: 
```math
C =  \begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
```

Example 2:
```math
A =  \begin{bmatrix} 3 & 4 \\ 16 & 0 \\ 25 & 24 \end{bmatrix}
```
```math
B =  \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```
Result `C` will be:
```math
C =  \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```

#### Inputs and outputs

##### `A`

Tensor `A` is the numerator of the division.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 
  
##### `B`

Tensor `B` is the denominator of the division.

###### Constraints

- (C1) Range 
    - Statement: The operator is only defined for a denominator tensor containing non null values.
- (C2) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise division of `A` by `B`.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 

#### Attributes

The `Div` operator does not require any attributes.

---
<a id="float"></a>
# `Div` operator (FP16, FP32, FP64, BFLOAT16)

### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:
- Tensors `A`, `B` and `C` must have the same shape.  `[R1]` 
- Tensors `A`, `B` and `C` shall have the same numerical type. `[R2]`
- Sparse tensors are not supported. `[RG1]`

### Signature

`C = Div(A, B)`

where
- `A`: numerator of the division
- `B`: denominator of the division
- `C`: result of the element-wise division of `A` by `B`

#### Informal specification

The `Div` operator divides input tensors `A` and `B` element-wise and place the result in `C`. Each element `C` is the result of the division of the corresponding element in `A` by the corresponding element in `B`.

The mathematical definition of the operator is given hereafter for a unidimensional tensor.

$$
C[i] = 
\begin{cases} 
\frac{A[i]}{B[i]} & \text{if } A[i] \text{ and } B[i] \text{ are different from 0} \\
\text{inf} & \text{if } A[i] \neq 0 \text{ and } B[i]=0  \\
\text{nan} & \text{if } A[i]=0 \text{ and } B[i]=0 
\end{cases}
$$

The effect of the operator is illustrated on the following examples:

- `A` does not contain 0 and `B` contains a zero element

```math
A =  \begin{bmatrix} 3 & 4 \\ 16 & 1 \\ 25 & 24 \end{bmatrix}
```
```math
B =  \begin{bmatrix} 3 & 2 \\ 4 & 0 \\ 5 & 4 \end{bmatrix}
```
```math
C =  \begin{bmatrix} 1 & 2 \\ 4 & \text{inf} \\ 5 & 6 \end{bmatrix}
```


- An element of `A` and its corresponding element of `B` are both equal to zero

```math
A =  \begin{bmatrix} 3 & 4 \\ 16 & 0 \\ 25 & 24 \end{bmatrix}
```
```math
B =  \begin{bmatrix} 3 & 2 \\ 4 & 0 \\ 5 & 4 \end{bmatrix}
```
```math
C =  \begin{bmatrix} 1 & 2 \\ 4 & \text{nan} \\ 5 & 6 \end{bmatrix}
```

Examples are available in [google collab.](https://colab.research.google.com/drive/1j9VlF-uYN4AitOglPkTWsvjoRe4L9-qb#scrollTo=rEKyVwTun7hf)

#### Inputs and outputs

##### `A`

Tensor `A` is the numerator of the division.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 
  
##### `B`

Tensor `B` is the denominator of the division.

###### Constraints

- (C1) Range 
    - Statement: The operator is only defined for a denominator tensor containing non null values.
- (C2) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by element-wise division of `A` by `B`.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B` and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]` 

#### Attributes

The `Div` operator does not require any attributes.

---
<a id="int"></a>
# `Div` operator (INT8, INT16, INT32)

*To be completed.*