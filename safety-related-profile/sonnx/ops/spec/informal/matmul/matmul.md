# Contents
- `MatMul` [operator (real)](#real)
- `MatMul` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `MatMul` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)


# Signature
`Y = MatMul(A,B)`
where
- `A`: first input tensor
- `B`: second input tensor
- `Y`: output tensor

<a id="real"></a>
# `MatMul` operator (real)

## Restrictions
| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor `A` and `B` are rank-2 tensors | Simplification |


## Informal specification

Operator `MatMul` computes the multiplication of tensor $A$ by tensor $B$.

The mathematical definition of the operator is given hereafter for a 2D tensor.

$$     
   Y = A \times B  
$$


$$
     \begin{bmatrix}
         Y_{11} & Y_{12} & \cdots & Y_{1p}\\
         Y_{21} & Y_{22} & \cdots & Y_{2p}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         Y_{m1} & Y_{m2} & \cdots & Y_{mp} 
     \end{bmatrix}
      =
     \begin{bmatrix}
         A_{11} & A_{12} & \cdots & A_{1n}\\
         A_{21} & A_{22} & \cdots & A_{2n}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         A_{m1} & A_{m2} & \cdots & A_{mn} 
     \end{bmatrix}
     \times
     \begin{bmatrix}
         B_{11} & B_{12} & \cdots & B_{1p}\\
         B_{21} & B_{22} & \cdots & B_{2p}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         B_{n1} & B_{n2} & \cdots & B_{np} 
     \end{bmatrix}
$$
$$     
   Y_{ij}= A_{i1} B_{1j} + A_{i2} B_{2j} +\cdots+ A_{in} B_{nj} = \sum_{k=1}^n A_{ik}B_{kj}  
$$

Where
- $m$ is the number of rows of matrix $A$ (= $dA_0$)
- $n$ the number of columns of matrix $A$ (= $dA_1$) and the number of rows of matrix B (=$dA_0$),
- $p$ is the number of columns of matrix $B$ (=$dB_1$)

##### Note
The semantics of the ONNX `MatMul` operator reflects the semantics of the NumPy `matmul`operator. In particular (except of the [NumPy documentation]())   

> If both arguments are 2-D they are multiplied like conventional matrices.

> If either argument is N-D, N > 2, it is treated as a stack of matrices residing in the last two indexes and broadcast accordingly.

> If the first argument is 1-D, it is promoted to a matrix by prepending a 1 to its dimensions. After matrix multiplication the prepended 1 is removed. (For stacks of vectors, use vecmat.)

> If the second argument is 1-D, it is promoted to a matrix by appending a 1 to its dimensions. After matrix multiplication the appended 1 is removed. (For stacks of vectors, use matvec.)

In the SONNX profile, such implicit promotions are forbidden and shall be managed by inserting apporpriate `Reshape` operator before and after `MatMul`.


## Inputs 

### `A`: tensor(real)

Tensor `A` is the first input tensor.

The shape of tensor `A` is $(dA_0,dA_1)$.

#### Constraints

- (C1) Number of spatial axes of tensor `A`
    - Statement: The number of spatial axes of tensor `X` is 2. `[R1]`
    - Rationale: This restriction is intoduced to simplify the implementation considering the actual industrial use cases.
- (C2) <a name="a_b_shape_consist"></a> Consistency of `A` and `B`shapes  
  - Statement:  $dA_A=dB_0$
  - Rationale: Application of the mathematical definition of ``MatMul`.
- (C3) <a name="a_y_shape_consist"></a> Consistency of `A` and `Y` shapes
  - Statement: $dY_0=dA_0$
  - Rationale: Application of the mathematical definition of ``MatMul`.

### `B`: tensor(real) 

Tensor `B` is the second input tensor.

The shape of tensor `B` is $(dB_0,dB_1)$.

#### Constraints

- (C1) Number of spatial axes of tensor `B`
    - Statement: The number of spatial axes of tensor `B` is 2. `[R1]`
    - Rationale: This restriction is intoduced to simplify the implementation considering the actual industrial use cases.
- (C2) Consistency of `A` and `B`shapes  
  - [See constraint (C2) of A](#a_b_shape_consist)
- (C3) <a name="b_y_shape_consist"></a> Consistency of `B` and `Y` shapes
  - Statement: $dY_1=dB_1$
  - Rationale: Application of the mathematical definition of ``MatMul`.

## Outputs 

### `Y`: tensor(real)

Tensor `Y` is the output tensor.

The shape of tensor `Y` is $(dY_0,dY_1)$.

#### Constraints

- (C1) Number of spatial axes of tensor `Y`
    - Statement: The number of spatial axes of tensor `B` is 2. `[R1]`
    - Rationale: This restriction is intoduced to simplify the implementation considering the actual industrial use cases.
- (C3) <a name="b_y_shape_consist"></a> Consistency of `A`, `B` and `Y` shapes
  - [See constraint (C3) of `A`](#a_y_shape_consist) and [constraint (C3) of `B`](#b_y_shape_consist)


---

<a id="float"></a>
# `MatMul` operator (FP16, FP32, FP64, BFLOAT16)

*To be completed.*

---

<a id="int"></a>
# `MatMul` operator  (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32), UINT64)

*To be completed.*

## Formal specification

See [here](./why3/opmatmul.mlw).

## Numerical Accuracy

If tensor $A_{\textit{err}}$ is the numerical error of `A`,
tensor $B_{\textit{err}}$ is the numerical error of `B`, let us consider
$Y_{\textit{err}}^{\textit{propag}}$ the propagated error of `MatMul`
and $Y_{\textit{err}}^{\textit{intro}}$ the introduced error of `MatMul`.
Hence the numerical error of `Y`, $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error propagation

For every indexes $I = (i,j)$ over the two axes, 

- $\displaystyle Y_{\textit{err}}^{\textit{propag}}[I] = \left(\sum_{1\leq k \leq n} A_{\textit{err}}[(i, k)] \times B[(k, j)]\right) + \left(\sum_{1\leq k \leq n} A[(i, k)] \times B_{\textit{err}}[(k, j)]\right) + \left(\sum_{1\leq k \leq n} A_{\textit{err}}[(i, k)] \times B_{\textit{err}}[(k, j)]\right)$

### Error introduction - floating-point IEEE-754 implementation

The error introduced by the `MatMul` operator comes from the $n$ multiplications and $n-1$
additions for each component of the tensor result. For a hardware providing $m$ bits for
floating-point mantissa, the relative error of any multiplication/addition is bound
by $2^{-(m+1)}$. Hence, for every indexes $I = (i, j)$ over the two axes,

- $\displaystyle \left|Y_{\textit{err}}^{\textit{intro}}[I]\right| \leq \frac{n\times(n+1)}{2}\times
   2^{-(m+1)}\times \max_{1 \leq k \leq n} \left(\max\left(\left|A[(i, k)] +
     A_{\textit{err}}[(i, k)]\right| \times \left| B[(k, j)] + B_{\textit{err}}[(k, j)]\right|,
     \frac{\texttt{denorm-min}}{2}\right)\right)$  
- $\displaystyle \left|Y_{\textit{err}}^{\textit{intro}}[I]\right| \leq \frac{n\times(n+1)}{2}\times
   2^{-(m+1)}\times \max_{1 \leq k \leq n} \left(\max\left(\left|A_{\textit{float}}[(i, k)]\right|
     \times \left|B_{\textit{float}}[(k, j)]\right|, \frac{\texttt{denorm-min}}{2}\right)\right)$

If $A$ or $B$ are diagonal matrices, only one multiplication is performed for each component of the
tensor result. The introduced error then supports smaller bounds and for any indexes $I = (i, j)$ 
on both axes,

- $\displaystyle \left|Y_{\textit{err}}^{\textit{intro}}[I]\right| \leq
   2^{-(m+1)}\times \max\left(\left|A_{\textit{float}}[(i, i)]\right|
     \times \left|B_{\textit{float}}[(i, j)]\right|, \frac{\texttt{denorm-min}}{2}\right)$
  if $A$ is diagonal  
- $\displaystyle \left|Y_{\textit{err}}^{\textit{intro}}[I]\right| \leq
   2^{-(m+1)}\times \max\left(\left|A_{\textit{float}}[(i, j)]\right|
     \times \left|B_{\textit{float}}[(j, j)]\right|, \frac{\texttt{denorm-min}}{2}\right)$
  if $B$ is diagonal

### Unit verification - floating-point IEEE-754 implementation

A symbolic inference of the error over the tensor components should ensure the
above properties.

```c++
Tensor<SymbolicDomainError> A, B;

/* A and B symbolic initialization */

typedef Tensor<SymbolicDomainError>::Indexes Indexes;

template <typename TypeFloat>
std::function<TypeFloat (Indexes)>
  result = [&A, &B](Indexes pair_of_indexes)
    { SymbolicDomainError sum = 0;
      for (int k = 0; k < A.indexes()[1]; ++k)
        sum += A[Indexes(pair_of_indexes[0], k)] + B[Indexes(k, pair_of_indexes[1])];
      return sum;
    }

for (auto indexes : Indexes(A.indexes()[0], B.indexes()[1])) {
   int n = A.indexes()[1];
   SymbolicDomainError y = result(indexes);
   real propagated_error = 0;
   for (int k = 0; k < n; ++k) {
     propagated_error += A[Indexes(indexes[0], k)].err * B[Indexes(k, indexes[1])].real;
     propagated_error += A[Indexes(indexes[0], k)].real * B[Indexes(k, indexes[1])].err;
     propagated_error += A[Indexes(indexes[0], k)].err * B[Indexes(k, indexes[1])].err;
   }
   real bound_for_introduced_error = (real) std::numeric_limits<decltype(y.float)>::denorm_min() / 2.0);
   for (int k = 0; k < n; ++k) {
     real bound_candidate = std::abs(A[Indexes(indexes[0], k)].real + A[Indexes(indexes[0], k)].err)
         * std::abs(B[Indexes(j, indexes[1])].real + B[Indexes(k, indexes[1])].err);
     bound_for_introduced_error = std::max(bound_for_introduced_error, bound_candidate);
   }
   bound_for_introduced_error *= ((n * (n+1))/2) * pow(2.0LD, -(m+1));

   assert(std::abs(y.err - propagatedError) <= bound_for_introduced_error);
}
```

### Error introduction - fixed-point implementation

The error introduced by the `MatMul` operator comes from the $n$ multiplications.

