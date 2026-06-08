# Contents
- **MatMul** operator for type [real](#real)
- **MatMul** operator for types [int32, int64, uint32, uint64](#int)
- **MatMul** operator for types [float16, float32, float64](#float)

Based on ONNX [Op version 13](https://onnx.ai/onnx/operators/onnx__MatMul.html).

<a id="real"></a>
# **MatMul** (real, real)

# Signature
$Y = \textbf{MatMul}(A, B)$

where:
- $A$: left-side of the multiplication
- $B$: right-side of the multiplication
- $Y$: result of the multiplication

## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **MatMul** operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Input tensors $A$ and $B$ have 2 dimensions | Transient |

## Informal specification

Operator **MatMul** computes a matrix multiplication. 

The mathematical definition of the operator is given hereafter.

$$
  \forall i \in [0, dA_0 - 1], \forall j \in [0, dB_1 - 1] \quad Y[i,j] = \sum_{k=0}^{dA_1-1} A[i,k]\times B[k,j]
$$

with $dA_1 = dB_0$

### Example 1

$$
  A = \begin{bmatrix}
        1 & 2 \\
        3 & 4
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      5 & 6 \\
      7 & 8
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      19 & 22 \\
      43 & 50
\end{bmatrix}
$$

### Example 2
$$
A = \begin{bmatrix}
      1 & 2 \\
      3 & 4 \\
      5 & 6
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      7 & 8 & 9 \\
      10 & 11 & 12
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      27 & 30 & 33 \\
      61 & 68 & 75 \\
      95 & 106 & 117
\end{bmatrix}
$$

## Error conditions

No error conditions.

## Attributes

Operator **MatMul** has no attributes.

## Inputs 

### $A$: real

Tensor $A$ is the left-side input tensor.

#### Constraints
<a id="E_MATMUL_REAL_CONSTR_A_0010"></a>
- `E_MATMUL_REAL_CONSTR_A_0010` Number of spatial axes of tensor $A$
  - Statement: The number of spatial axes of tensor $A$ is 2.

<a id="E_MATMUL_REAL_CONSTR_A_0020"></a>
- `E_MATMUL_REAL_CONSTR_A_0020` Consistency of $A$ and $B$ shapes  
  - Statement:  $dA_1=dB_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

<a id="E_MATMUL_REAL_CONSTR_A_0030"></a>
- `E_MATMUL_REAL_CONSTR_A_0030` Consistency of $A$ and $Y$ shapes
  - Statement: $dY_0=dA_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

### $B$: real

Tensor $B$ is the right-side input tensor.

#### Constraints
<a id="E_MATMUL_REAL_CONSTR_B_0010"></a>
- `E_MATMUL_REAL_CONSTR_B_0010`  Number of spatial axes of tensor $B$
  - Statement: The number of spatial axes of tensor $B$ is 2.
  
<a id="E_MATMUL_REAL_CONSTR_B_0020"></a>
- `E_MATMUL_REAL_CONSTR_B_0020`  Consistency of $A$ and $B$ shapes  
  - See constraint  [<b><span style="font-family: 'Courier New', monospace">E_MATMUL_REAL_CONSTR_A_0020</span></b>](#E_MATMUL_REAL_CONSTR_A_0020) of A.

<a id="E_MATMUL_REAL_CONSTR_B_0030"></a>
- `E_MATMUL_REAL_CONSTR_B_0030` Consistency of $B$ and $Y$ shapes
  - Statement: $dY_1=dB_1$
  - Rationale: Application of the mathematical definition of matrix multiplication.

## Outputs 

### $Y$: real

Tensor $Y$ is the output tensor.

#### Constraints
<a id="E_MATMUL_REAL_CONSTR_Y_0010"></a>
- `E_MATMUL_REAL_CONSTR_Y_0010` Number of spatial axes of tensor $Y$
  - Statement: The number of spatial axes of tensor $Y$ is 2.

<a id="E_MATMUL_REAL_CONSTR_Y_0020"></a>
- `E_MATMUL_REAL_CONSTR_Y_0020` Consistency of $A$, $B$ and $Y$ shapes
  - See constraint [<b><span style="font-family: 'Courier New', monospace">E_MATMUL_REAL_CONSTR_A_0030</span></b>](#E_MATMUL_REAL_CONSTR_A_0030) of A and constraint [<b><span style="font-family: 'Courier New', monospace">E_MATMUL_REAL_CONSTR_B_0030</span></b>](#E_MATMUL_REAL_CONSTR_B_0030) of B



<a id="float"></a>
# **MatMul** (float, float)

where float is in {float16, float32, float64}

# Signature
$Y = \textbf{MatMul}(A, B)$
where
- $A$: left-side input tensor
- $B$: right-side input tensor
- $Y$: output tensor


## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.


## Informal specification

Operator **MatMul** computes the tensor operation equivalent to a matrix multiplication. 

The mathematical definition of the operator is given hereafter for a bidimensional tensors.

$$     
  Y = AB  
$$


$$
     \begin{bmatrix}
         Y_{00} & Y_{01} & \cdots & Y_{0c_B}\\
         Y_{10} & Y_{11} & \cdots & Y_{1c_B}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         Y_{l_A0} & Y_{l_A1} & \cdots & Y_{l_Ac_B} 
     \end{bmatrix}
      =
     \begin{bmatrix}
         A_{00} & A_{01} & \cdots & A_{0c_A}\\
         A_{10} & A_{11} & \cdots & A_{1c_A}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         A_{l_A0} & A_{l_A1} & \cdots & A_{l_Ac_A} 
     \end{bmatrix}
     \begin{bmatrix}
         B_{00} & B_{01} & \cdots & B_{0c_B}\\
         B_{10} & B_{11} & \cdots & B_{1c_B}\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         B_{l_B0} & B_{l_B1} & \cdots & B_{l_Bc_B} 
     \end{bmatrix}
$$

$$
  \forall i \in [0, l_A], \forall j \in [0, c_B] \quad Y_{ij} = \sum_{k=0}^{n-1} A_{ik}B_{kj}
$$

Where
- $l_A = dA_0 - 1$
- $c_A = dA_1 - 1$
- $l_B = dB_0 - 1$
- $c_B = dB_1 - 1$
- $n = dA_1 = dB_0$

### Example 1
$$
A = \begin{bmatrix}
      1.0 & 2.0 \\
      3.0 & 4.0
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      5.0 & 6.0 \\
      7.0 & 8.0
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      19.0 & 22.0 \\
      43.0 & 50.0
\end{bmatrix}
$$

### Example 2
$$
A = \begin{bmatrix}
      \infty & -\infty & NaN \\
      NaN & \infty & -\infty \\
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      1.0 & 2.0 \\
      4.0 & 5.0 \\
      7.0 & 8.0
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      NaN & NaN \\
      NaN & NaN
\end{bmatrix}
$$

### Example 3

$$
A = \begin{bmatrix}
      \infty & \infty \\
      NaN & \infty \\
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      1.0 & 2.0 & 3.0 & 4.0 \\
      4.0 & 5.0 & 6.0 & 7.0 \\
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      \infty & \infty & \infty & \infty \\
      NaN & NaN & NaN & NaN \\
    \end{bmatrix}
$$

## Error conditions

No error conditions.

## Attributes

Operator **MatMul** has no attributes.

## Inputs 

### $\text{A}$: float

Tensor $A$ is the left-side input tensor.

#### Constraints

- `[C1]` <a id="C1f"></a> Number of spatial axes of tensor $A$
  - Statement: The number of spatial axes of tensor $A$ is 2.

- `[C2]` <a id="C2f"></a> Consistency of $A$ and $B$ shapes  
  - Statement:  $dA_1=dB_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

- `[C3]` <a id="C3f"></a> Consistency of $A$ and $Y$ shapes
  - Statement: $dY_0=dA_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

### $\text{B}$: float

Tensor $B$ is the right-side input tensor.

#### Constraints

- `[C1]` <a id="C1f"></a> Number of spatial axes of tensor $B$
  - Statement: The number of spatial axes of tensor $B$ is 2.
  
- `[C2]` <a id="C2f"></a> Consistency of $A$ and $B$ shapes  
  - [See constraint (C2) of A](#C2f)

- `[C3]` <a id="C4f"></a> Consistency of $B$ and $Y$ shapes
  - Statement: $dY_1=dB_1$
  - Rationale: Application of the mathematical definition of matrix multiplication.

## Outputs 

### $\text{Y}$: float

Tensor $Y$ is the output tensor.

#### Constraints

- `[C1]` <a id="C1f"></a> Number of spatial axes of tensor $Y$
  - Statement: The number of spatial axes of tensor $Y$ is 2.

- `[C2]` <a id="C5f"></a> Consistency of $A$, $B$ and $Y$ shapes
  - [See constraint (C3) of A](#C3f) and [constraint (C3) of B](#C4f)

<a id="int"></a>
# **MatMul** (int, int)

where int is in {int32, int64, uint32, uint64}

# Signature
$Y = \textbf{MatMul}(A, B)$
where
- $A$: left-side of the multiplication
- $B$: right-side of the multiplication
- $Y$: result of the multiplication


[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **MatMul** operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | Input tensors $A$ and $B$ have 2 dimensions | Transient |

## Informal specification

Operator **MatMul** computes a matrix multiplication. 

The mathematical definition of the operator is given hereafter.

$$
  \forall i \in [0, dA_0 - 1], \forall j \in [0, dB_1 - 1] \quad Y[i,j] = \sum_{k=0}^{dA_1-1} A[i,k]\times B[k,j]
$$

with $dA_1 = dB_0$

where 
- $x+y$ = [**Add**](../add/add.md#add-int-int)$(x,y)$
- $x\times y$ = [**Mul**](../mul/mul.md#mul-int-int)$(x,y)$

### Example 1
$$
A = \begin{bmatrix}
      1 & 2 \\
      3 & 4
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      5 & 6 \\
      7 & 8
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      19 & 22 \\
      43 & 50
\end{bmatrix}
$$

### Example 2
$$
A = \begin{bmatrix}
      1 & 2 \\
      3 & 4 \\
      5 & 6
  \end{bmatrix}
$$

$$
B = \begin{bmatrix}
      7 & 8 & 9 \\
      10 & 11 & 12
  \end{bmatrix}
$$

$$
Y = \begin{bmatrix}
      27 & 30 & 33 \\
      61 & 68 & 75 \\
      95 & 106 & 117
\end{bmatrix}
$$

## Error conditions

No error conditions.

## Attributes

Operator **MatMul** has no attributes.

## Inputs 

### $\text{A}$: itype

Tensor $A$ is the left-side input tensor.

#### Constraints

- `[C1]` <a id="C1i"></a> Number of spatial axes of tensor $A$
  - Statement: The number of spatial axes of tensor $A$ is 2.

- `[C2]` <a id="C2i"></a> Consistency of $A$ and $B$ shapes  
  - Statement:  $dA_1=dB_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

- `[C3]` <a id="C3i"></a> Consistency of $A$ and $Y$ shapes
  - Statement: $dY_0=dA_0$
  - Rationale: Application of the mathematical definition of matrix multiplication.

### $\text{B}$: itype

Tensor $B$ is the right-side input tensor.

#### Constraints

- `[C1]` <a id="C1i"></a> Number of spatial axes of tensor $B$
  - Statement: The number of spatial axes of tensor $B$ is 2.
  
- `[C2]` <a id="C2i"></a> Consistency of $A$ and $B$ shapes  
  - [See constraint (C2) of A](#C2i)

- `[C3]` <a id="C4i"></a> Consistency of $B$ and $Y$ shapes
  - Statement: $dY_1=dB_1$
  - Rationale: Application of the mathematical definition of matrix multiplication.

## Outputs 

### $\text{Y}$: itype

Tensor $Y$ is the output tensor.

#### Constraints

- `[C1]` <a id="C1i"></a> Number of spatial axes of tensor $Y$
  - Statement: The number of spatial axes of tensor $Y$ is 2.

- `[C2]` <a id="C5i"></a> Consistency of $A$, $B$ and $Y$ shapes
  - [See constraint (C3) of A](#C3i) and [constraint (C3) of B](#C4i)


