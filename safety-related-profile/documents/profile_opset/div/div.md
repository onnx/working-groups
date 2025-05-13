# Contents
- `Div` [operator (real)](#real)
- `Div` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `Div` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)



<a id="real"></a>
# `Div` operator (real)

### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:
- Tensors `A`, `B` and `C` must have the same shape.  `[R1]` 
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md) 

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
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md) 

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


### Formal specification

The formal specification of the `div` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Div operation on tensors with real numbers.
 *)

module DivReal
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Inf
  use real.NaN
  use real.Div

  let function div (a : tensor real) (b : tensor real) : tensor real =
    requires { a.shape = b.shape }
    ensures {
      forall i. if a.value[i] <> 0.0 && b.value[i] <> 0.0 then result.value[i] = a.value[i] / b.value[i]
               else if a.value[i] <> 0.0 && b.value[i] = 0.0 then result.value[i] = infinity
               else if a.value[i] = 0.0 && b.value[i] = 0.0 then result.value[i] = nan
    }
  {
    shape = a.shape ;
    value = fun i -> if a.value[i] <> 0.0 && b.value[i] <> 0.0 then a.value[i] / b.value[i]
                     else if a.value[i] <> 0.0 && b.value[i] = 0.0 then infinity
                     else nan ;
  }
  
end
```

[^1]: See [Why3 documentation](https://www.why3.org/)



---
<a id="int"></a>
# `Div` operator (INT8, INT16, INT32)

### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:
- Tensors `A`, `B`, and `C` must have the same shape. `[R1]`
- Tensors `A`, `B`, and `C` must have the same numerical type. `[R2]`
- Overflow behavior is implementation-defined.
- Tensors of class `SparseTensor` are not supported [`[GR1]`](../general_restrictions.md)

### Signature

`C = Div(A, B)`

where
- `A`: numerator of the division
- `B`: denominator of the division
- `C`: result of the element-wise division of `A` by `B`

#### Informal specification

The `Div` operator divides input tensors `A` and `B` element-wise and places the result in `C`. Each element `C` is the result of the division of the corresponding element in `A` by the corresponding element in `B`.

The mathematical definition of the operator is given hereafter for a unidimensional tensor, with $i$ covering all valid indexes:

$$
C[i] = 
\begin{cases} 
\left\lfloor \frac{A[i]}{B[i]} \right\rfloor & \text{if } B[i] \text{ is different from 0} \\
\text{undefined} & \text{otherwise}
\end{cases}
$$

Note:
- $\left\lfloor X \right\rfloor$ means the floor of $X$.
- "undefined" is implementation-dependent.


The effect of the operator is illustrated on the following examples:
- `A` and `B` are tensors holding integer data.

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
A =  \begin{bmatrix} 10 & 10 \\ 21 & 1 \\ 30 & 9 \end{bmatrix}
```
```math
B =  \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```
Result `C` will be:
```math
C =  \begin{bmatrix} 3 & 5 \\ 5 & 1 \\ 6 & 2 \end{bmatrix}
```

#### Inputs and outputs

##### `A`

Tensor `A` is the numerator of the division.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B`, and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]`

##### `B`

Tensor `B` is the denominator of the division.

###### Constraints

- (C1) Range 
    - Statement: The operator is only defined for a denominator tensor containing non-null values.
- (C2) Shape consistency
    - Statement: Tensors `A`, `B`, and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]`

#### Outputs

##### `C`

Tensor `C` is the output tensor formed by the element-wise integer division of `A` by `B`.

###### Constraints

- (C1) Shape consistency
    - Statement: Tensors `A`, `B`, and `C` must have the same shape. $N(A)=N(B)=N(C)$ `[R1]`

#### Attributes

The `Div` operator does not require any attributes.

### Formal specification

The formal specification of the `div` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Div operation on tensors with int numbers.
 *)

module DivInt
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use int.Div

  let function div (a : tensor int) (b : tensor int) : tensor int =
    requires { a.shape = b.shape }
    ensures {
      forall i. if b.value[i] <> 0 then result.value[i] = a.value[i] / b.value[i]
               else False (* Represents undefined behavior *)
    }
  {
    shape = a.shape ;
    value = fun i -> if b.value[i] <> 0 then a.value[i] / b.value[i]
                     else assert False; (* Enforces undefined behavior *) ;
  }
  
end
```

[^1]: See [Why3 documentation](https://www.why3.org/)
