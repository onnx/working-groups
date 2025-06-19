# Contents
- `MatMul` [operator (real)](#real)
- `MatMul` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `MatMul` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64, )](#int)

<a id="real"></a>
# `MatMul` operator (real)

#### Inputs and outputs

##### `A`

Tensor `A` is the first input tensor.

The shape of tensor `A` is $(m \times n)$.

###### Constraints

- (C1) Number of spatial axes of tensor `A`
    - Statement: The number of spatial axes of tensor `X` is 2. `[R1]`
    - Rationale: This restriction is intoduced to simplify the implementation considering the actual industrial use cases.

##### `B`

Tensor `B` is the second input tensor.

The shape of tensor `B` is $(n \times p)$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is $(m \times p)$.

### Restrictions
The following restrictions apply to the `MatMul` operator for the SONNX profile:
- The number of spatial axes of the tensors is restricted to 2 ========TBC======`[R1]`

### Signature
`Y = MatMul(A,B)`
where
- `A`: first input tensor
- `B`: second input tensor
- `Y`: output tensor
  
#### Informal specification

Operator `MatMul` computes the matrix multiplication of the input tensors `A` and `B` into the output matrix `Y`.

The mathematical definition of the operator is given hereafter.

$$     
   Y = A \times B  
$$


$$
     \begin{bmatrix}
         y_{11} & y_{12} & \cdots & y_{1p}\\
         y_{21} & y_{22} & \cdots & y_{2p}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         y_{m1} & y_{m2} & \cdots & y_{mp} 
     \end{bmatrix}
      =
     \begin{bmatrix}
         a_{11} & a_{12} & \cdots & a_{1n}\\
         a_{21} & a_{22} & \cdots & a_{2n}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         a_{m1} & a_{m2} & \cdots & a_{mn} 
     \end{bmatrix}
     \times
     \begin{bmatrix}
         b_{11} & b_{12} & \cdots & b_{1p}\\
         b_{21} & b_{22} & \cdots & b_{2p}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         b_{n1} & b_{n2} & \cdots & b_{np} 
     \end{bmatrix}
$$
$$     
   y_{ij}= a_{i1} b_{1j} + a_{i2} b_{2j} +\cdots+ a_{in} b_{nj} = \sum_{k=1}^n a_{ik}b_{kj}  
$$

Where
- $y$ is the output matrix,
- $a$ is the first input matrix,
- $b$ is the second input matrix,
- $m$ the first input matrix number of rows,
- $n$ the first input matrix number of columns and second input matrix number of rows,
- $p$ the second input matrix number of columns

##### Note
The behavior depends on the arguments in the following way.

- If both input are 2-D they are multiplied like conventional matrices.
```
These particularities are linked to numpy specification referenced by ONNX MatMul.

The assumption for SONNX is that the following is managed by splitting matrices and duplicating call to MatMul.

- If either input is N-D, N > 2, it is treated as a stack of matrices residing in the last two indexes and broadcast accordingly.

The assumption for SONNX is that the following is managed by insterting Reshape before and after MatMul.

- If the first input is 1-D, it is promoted to a matrix by prepending a 1 to its dimensions. After matrix multiplication the prepended 1 is removed.

- If the second input is 1-D, it is promoted to a matrix by appending a 1 to its dimensions. After matrix multiplication the appended 1 is removed.
```

<a id="float"></a>

### Formal specification

The formal specification of the `matmul` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of MatMul operation on tensors with real numbers.
 *)
module MatMulReal
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  let function matmul (a : tensor real) (b : tensor real) : tensor real =
    ensures { result.shape = [nth a.shape 0; nth b.shape 1] }
  {
    shape = [nth a.shape 0; nth b.shape 1] ;
    value = fun i j -> sum (fun k -> a.value[i][k] * b.value[k][j]) (nth a.shape 1)
  }
end
```


<a id="int"></a>


### Numerical Accuracy

If tensor $A_{\textit{err}}$ is the numerical error of `A`,
tensor $B_{\textit{err}}$ is the numerical error of `B`, let us consider
$Y_{\textit{err}}^{\textit{propag}}$ the propagated error of `MatMul`
and $Y_{\textit{err}}^{\textit{intro}}$ the introduced error of `MatMul`.
Hence the numerical error of `Y`, $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

#### Error propagation

For every indexes $I = (i,j)$ over the two axes, 

- $\displaystyle Y_{\textit{err}}^{\textit{propag}}[I] = \left(\sum_{1\leq k \leq n} A_{\textit{err}}[(i, k)] \times B[(k, j)]\right) + \left(\sum_{1\leq k \leq n} A[(i, k)] \times B_{\textit{err}}[(k, j)]\right) + \left(\sum_{1\leq k \leq n} A_{\textit{err}}[(i, k)] \times B_{\textit{err}}[(k, j)]\right)$

#### Error introduction - floating-point IEEE-754 implementation

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

#### Unit verification - floating-point IEEE-754 implementation

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

#### Error introduction - fixed-point implementation

The error introduced by the `MatMul` operator comes from the $n$ multiplications.

