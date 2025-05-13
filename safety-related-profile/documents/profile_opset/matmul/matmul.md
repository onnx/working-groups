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



