
# `Gemm` operator (real)

### Restrictions
The following restrictions apply to the `Gemm` operator for the SONNX profile:
- The number of spatial axes of the tensors is restricted to 2 ========TBC======`[R1]`
- alpha, beta, transA, transB ONNX attributes are not supported. A similar behaviour can be optained using `Mul` or `Transpose` operators. ========TBC======`[R2]`
- `Gemm` is not unidirectionnaly broadcastable.  ========TBC======`[R3]`
- `C` input is not optional. `MatMul` shall be used in this case. ========TBC======`[R4]`

### Signature
`Y = Gemm(A,B,C)`
where
- `A`: first input tensor
- `B`: second input tensor
- `C`: bias input tensor
- `Y`: output tensor
  
#### Informal specification

Operator `Gemm` computes the matrix multiplication of the input tensors `A` and `B`, then add the `C` bias tensor into the output tensor `Y`.

The mathematical definition of the operator is given hereafter.

$$     
   Y = (A \times B) + C
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
     +
     \begin{bmatrix}
         c_{11} & c_{12} & \cdots & c_{1p}\\
         c_{21} & c_{22} & \cdots & c_{2p}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         c_{m1} & c_{m2} & \cdots & c_{mp} 
     \end{bmatrix}
$$
$$     
   y_{ij}= a_{i1} b_{1j} + a_{i2} b_{2j} +\cdots+ a_{in} b_{nj} + c_{ij} = \sum_{k=1}^n a_{ik}b_{kj} + c_{ij} 
$$

Where
- $y$ is the output matrix,
- $a$ is the first input matrix,
- $b$ is the second input matrix,
- $c$ is the bias input matrix,
- $m$ the first input matrix number of rows,
- $n$ the first input matrix number of columns and second input matrix number of rows,
- $p$ the second input matrix number of columns

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

##### `C`

Tensor `C` is the bias input tensor.

The shape of tensor `C` is $(m \times p)$.

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is $(m \times p)$.

