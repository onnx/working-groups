# Contents
 - **Mul** operator for type [real](#real)
 - **Mul** operator for types [float16, float, double](#float)
 - **Mul** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation version 14.

---

<a id="real"></a>
# **Mul** (real, real)

## Signature

Definition of operator $\text{Mul}$ signature:

$C = \text{Mul}(A, B)$

where:
- $A$: first operand of the multiplication  
- $B$: second operand of the multiplication  
- $C$: result of the element-wise multiplication of $A$ by $B$
 

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Mul** operator.
## Informal specification

<span style="background: red; color: white; font-size:0.7em;">
[E_MUL_REAL_FUNC_0010]</br></span>

Operator **Mul** multiplies input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. Each element $C[i]$ is the result of multiplying $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The definition of the operator is given hereafter.

For any index i:

$$
C[i] = A[i] \times B[i]
$$

The effect of the operator is illustrated on the following examples:
<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

---

### Example 1 (1D tensors)

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 2 & 3 & 4 \end{bmatrix}
```

```math
C = A \times B = \begin{bmatrix} 12.2 & 28.5 & 142.8 \end{bmatrix}
```

---

## Error conditions
No error condition.

## Inputs

### $\text{A}$: real tensor
Tensor $A$ is the first operand of the multiplication.

#### Constraints

<a id="E_MUL_REAL_CONSTR_A_0010"></a>
 - `[E_MUL_REAL_CONSTR_A_0010]` Shape consistency
   - Statement: Tensors $A$, $B$, and $C$ shall have the same shape. 

 
### $\text{B}$: real tensor
Tensor $B$ is the second operand of the multiplication.

#### Constraints

 - `[E_MUL_REAL_CONSTR_B_0010]` Shape consistency
  -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_REAL_CONSTR_A_0010</span></b>](#E_MUL_REAL_CONSTR_A_0010) on tensor $A$.


## Outputs

### $\text{C}$: real tensor

Tensor $C$ is the element-wise result of $A$ multiplied by $B$.

#### Constraints

 - `[E_MUL_REAL_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_REAL_CONSTR_A_0010</span></b>](#E_MUL_REAL_CONSTR_A_0010) on tensor $A$.


## Attributes

The **Mul** operator has no attribute.


---

<a id="float"></a>
# **Mul** (float, float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{mul}$ signature:

$C = \text{Mul}(A, B)$

where

 - $A$: first operand tensor
 - $B$: second operand  tensor
 - $C$: output tensor, result of element-wise multiplication of $A$ by $B$
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Mul** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">[E_MUL_FLOAT_FUNC_0010]</br></span>
Operator **Mul** multiplies input tensors $A$ by $B$ element-wise according to IEEE 754 floating-point semantics and stores the result in output tensor $C$. If $i$ is a [tensor index](../common/definitions.md#tensor_index), each element $C[i]$ is the result of multiplying $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] = A[i] \times B[i]
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

---

### Example 1 (2D tensors)

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
C = A \times B = \begin{bmatrix} 9.0 & 9.0 \\ 64.0 & 0.0 \\ 127.5 & 97.0 \end{bmatrix}
```
## Error conditions
No error condition.

## Inputs

### $\text{A}$: floating-point tensor
Tensor $A$ is the first operand of the multiplication.

#### Constraints

<a id="E_MUL_FLOAT_CONSTR_A_0010"></a>
- `[E_MUL_FLOAT_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape.
<a id="E_MUL_FLOAT_CONSTR_A_0020"></a>
- `[E_MUL_FLOAT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 

### $\text{B}$: floating-point tensor
Tensor $B$ is the second operand of the multiplication.

#### Constraints
- `[E_MUL_FLOAT_CONSTR_B_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_FLOAT_CONSTR_A_0010</span></b>](#E_MUL_FLOAT_CONSTR_A_0010) on tensor $A$.
- `[E_MUL_FLOAT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_FLOAT_CONSTR_A_0020</span></b>](#E_MUL_FLOAT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: floating-point tensor

Tensor $C$ is the element-wise result of $A$ multiplied by $B$.

#### Constraints

 - `[E_MUL_FLOAT_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_FLOAT_CONSTR_A_0010</span></b>](#E_MUL_FLOAT_CONSTR_A_0010) on tensor $A$.
- `[E_MUL_FLOAT_CONSTR_C_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_FLOAT_CONSTR_A_0020</span></b>](#E_MUL_FLOAT_CONSTR_A_0020) on tensor $A$.

## Attributes

The **Mul** operator has no attribute.

---

<a id="int"></a>

# **Mul** (int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}

## Signature
Definition of operator $\text{mul}$ signature:

 $C = \text{Mul}(A,B)$

 where
 - $A$: first operand of the multiplication
 - $B$: second operand of the multiplication
 - $C$: result of the element-wise multiplication of $A$ by $B$
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Mul** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">
[E_MUL_INT_FUNC_0010]</br></span>
Operator **Mul** multiplies input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. Each element $C[i]$ is the result of multiplying $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The integer multiplication is performed as follows (considering that all tensors have the same type):

For unsigned values (type uint<n>):
$$C[i]=\left\{ 
\begin{array}{ c l }
A[i] \times B[i]- k.2^{n} & \quad \textrm{if }   A[i] \times B[i] > 2^{n}-1 
\\
A[i] \times B[i] & \quad \textrm{otherwise}
\end{array}
\right\}.$$
with $k \in \mathbb{N}$ such that $0 \le A[i] \times B[i]- k.2^{n} \le 2^n-1$

For signed values (type int<n>):$$C[i]=\left\{ 
\begin{array}{ c l }
A[i] \times B[i]- k_1.2^{n} & \quad \textrm{if }   A[i] \times B[i] > 2^{n-1}-1 \\
A[i] \times B[i] + k_2.2^{n} & \quad \textrm{if } A[i] \times B[i] < -2^{n-1} \\
A[i] \times B[i] & \quad \textrm{otherwise}
\end{array}
\right\}.$$
with: 
$k_1 \in \mathbb{N}$ such that $-2^{n-1} \le A[i] \times B[i]-k_1.2^{n} \le 2^{n-1}-1$
$k_2 \in \mathbb{N}$ such that $-2^{n-1} \le A[i] \times B[i]+k_2.2^{n} \le 2^{n-1}-1$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

### Example 1 (1D uint8 tensors)

```math
A = \begin{bmatrix} 6 & 9 & 35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 100 & 5 \end{bmatrix}
```
```math
C = \begin{bmatrix} 18 & 132 & 175 \end{bmatrix}
```

### Example 2 (1D int8 tensors)

```math
A = \begin{bmatrix} -6 & -9 & -9 & 9 \end{bmatrix}
\quad
B = \begin{bmatrix} -3 & 100 & -100 & 100 \end{bmatrix}
```
```math
C = \begin{bmatrix} 18 & 124 & -124 & -124 \end{bmatrix}
```

## Error conditions
- According to the definition, the result of the multiplication differs from the value that would be expected in $\mathbb{N}$ (for unsigned) or $\mathbb{Z}$ (for signed) when under- or overflow occur.

## Inputs

### $\text{A}$: integer tensor

Tensor $A$ is the first operand of the multiplication.

#### Constraints
This section gives all constraints applicable to the input.

<a id="E_MUL_INT_CONSTR_A_0010"></a>
- `[E_MUL_INT_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape.
<a id="E_MUL_INT_CONSTR_A_0020"></a>
- `[E_MUL_INT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 


### $\text{B}$: integer tensor

Tensor $B$ is the second operand of the multiplication.

#### Constraints

- `[E_MUL_INT_CONSTR_B_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_INT_CONSTR_A_0010</span></b>](#E_MUL_INT_CONSTR_A_0010) on tensor $A$.
- `[E_MUL_INT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_INT_CONSTR_A_0020</span></b>](#E_MUL_INT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: integer tensor

Tensor $C$ is the element-wise integer multiplication result.

#### Constraints

 - `[E_MUL_INT_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_INT_CONSTR_A_0010</span></b>](#E_MUL_INT_CONSTR_A_0010) on tensor $A$.
- `[E_MUL_INT_CONSTR_C_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_MUL_INT_CONSTR_A_0020</span></b>](#E_MUL_INT_CONSTR_A_0020) on tensor $A$.

## Attributes

The **Mul** operator has no attribute.










