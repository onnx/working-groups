# Contents
 - **Sub** operator for type [real](#real)
 - **Sub** operator for types [float16, float, double](#float)
 - **Sub** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation version 14.

---

<a id="real"></a>
# **Sub** (real, real)

## Signature

Definition of operator $\text{Sub}$ signature:

$C = \text{Sub}(A, B)$

where:
- $A$: first operand of the subtraction  
- $B$: second operand of the subtraction  
- $C$: result of the element-wise subtraction of $B$ from $A$
 

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sub** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">
[E_SUB_REAL_FUNC_0010]</br></span>

Operator **Sub** subtracts input tensors $B$ from input tensor $A$ element-wise and stores the result in output tensor $C$. Each element $C[i]$ is the result of subtracting $B[i]$ from $A[i]$ where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The definition of the operator is given hereafter.

For any index i:

$$
C[i] = A[i] - B[i]
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples:

### Example 1 (1D tensors)

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 2 & 3 & 4 \end{bmatrix}
```

```math
C = A - B = \begin{bmatrix} 4.1 & 6.5 & 31.7 \end{bmatrix}
```

---

## Error conditions
No error condition.

## Attributes

The **Sub** operator has no attribute.

## Inputs

### $\text{A}$: real tensor
Tensor $A$ is the first operand of the subtraction.

#### Constraints

<a id="E_SUB_REAL_CONSTR_A_0010"></a>
 - `[E_SUB_REAL_CONSTR_A_0010]` Shape consistency
   - Statement: Tensors $A$, $B$, and $C$ shall have the same shape. 

 
### $\text{B}$: real tensor
Tensor $B$ is the second operand of the subtraction.

#### Constraints

 - `[E_SUB_REAL_CONSTR_B_0010]` Shape consistency
  -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_REAL_CONSTR_A_0010</span></b>](#E_SUB_REAL_CONSTR_A_0010) on tensor $A$.

## Outputs

### $\text{C}$: real tensor

Tensor $C$ is the element-wise result of $A$ Subtiplied by $B$.

#### Constraints

 - `[E_SUB_REAL_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_REAL_CONSTR_A_0010</span></b>](#E_SUB_REAL_CONSTR_A_0010) on tensor $A$.


---

<a id="float"></a>
# **Sub** (float, float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Sub}$ signature:

$C = \text{Sub}(A, B)$

where

 - $A$: first operand tensor
 - $B$: second operand  tensor
 - $C$: output tensor, result of element-wise subtraction of $B$ from $A$ 
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sub** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">
[E_SUB_FLOAT_FUNC_0010]</br></span>

Operator **Sub** subtracts input tensor $B$ from input ensor $A$ element-wise according to IEEE 754 floating-point semantics, placing the result in output tensor $C$. Each element $C[i]$ is computed as follows:

$$
C[i] = A[i] - B[i]
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
C = A - B = \begin{bmatrix} 0.0 & 2.5 \\ 12.0 & 1.0 \\ 20.5 & 20.25 \end{bmatrix}
```
## Error conditions
No error condition.

## Attributes

The **Sub** operator has no attribute.

## Inputs

### $\text{A}$: floating-point tensor
Tensor $A$ is the first operand of the subtraction.

#### Constraints

<a id="E_SUB_FLOAT_CONSTR_A_0010"></a>
 - `[E_SUB_FLOAT_CONSTR_A_0010]` Shape consistency
   - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.
<a id="E_SUB_FLOAT_CONSTR_A_0020"></a>
- `[E_SUB_FLOAT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type.

 
### $\text{B}$: floating-point tensor
Tensor $B$ is the second operand of the subtraction.

#### Constraints

 - `[E_SUB_FLOAT_CONSTR_B_0010]` Shape consistency
  -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_FLOAT_CONSTR_A_0010</span></b>](#E_SUB_FLOAT_CONSTR_A_0010) on tensor $A$.
- `[E_SUB_FLOAT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_FLOAT_CONSTR_A_0020</span></b>](#E_SUB_FLOAT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: floating-point tensor

Tensor $C$ is the element-wise result of $A$ Subtiplied by $B$.

#### Constraints

 - `[E_SUB_FLOAT_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_FLOAT_CONSTR_A_0010</span></b>](#E_SUB_FLOAT_CONSTR_A_0010) on tensor $A$.
- `[E_SUB_FLOAT_CONSTR_C_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_FLOAT_CONSTR_A_0020</span></b>](#E_SUB_FLOAT_CONSTR_A_0020) on tensor $A$.


---

<a id="int"></a>

# **Sub** (int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}

## Signature
Definition of operator $\text{Sub}$ signature:

 $C = \text{Sub}(A,B)$

 where
 - $A$: first operand of the subtraction
 - $B$: second operand of the subtraction
 - $C$: result of the element-wise subtraction of $B$ from $A$ 
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Sub** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">
[E_SUB_INT_FUNC_0010]</br></span>

Operator **Sub** subtracts input tensor $B$ from input tensor $A$ element-wise and stores the result in output tensor $C$. Each element $C[i]$ is the result of subtracting $B[i]$ from $A[i]$ where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The integer subtraction is performed as follows (considering that all tensors have the same type):

For unsigned values (type uint\<n>):

$$
C[i]=
\begin{cases}
  A[i] - B[i] - 2^{n} & \quad \textrm{if }  A[i] - B[i] > 2^{n}-1 \\
  A[i] - B[i] & \quad \textrm{otherwise}
\end{cases}
$$

For signed values (type int\<n>):

$$C[i]= 
\begin{cases}
  A[i] - B[i] - 2^{n} & \quad \textrm{if } A[i] - B[i] > 2^{n-1}-1 \\
  A[i] - B[i] + 2^{n} & \quad \textrm{if } A[i] - B[i] < -2^{n-1} \\
  A[i] - B[i] & \quad \textrm{otherwise}
\end{cases}
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

### Example 1 (1D uint8 tensors)

```math
A = \begin{bmatrix} 6 & 100 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 200 \end{bmatrix}
```
```math
C = \begin{bmatrix} 3 & 44 \end{bmatrix}
```

### Example 2 (1D int8 tensors)

```math
A = \begin{bmatrix} -6 & 10 & 10  \end{bmatrix}
\quad
B = \begin{bmatrix} -3 & 100 & -120  \end{bmatrix}
```
```math
C = \begin{bmatrix} -9 & -90 & -126  \end{bmatrix}
```

## Error conditions
- According to the definition, the result of the subtraction differs from the value that would be expected in $N$ (for unsigned) or $Z$ (for signed) when under- or overflow occur.

## Attributes

The **Sub** operator has no attribute.

## Inputs

### $\text{A}$: integer tensor

Tensor $A$ is the first operand of the subtraction.

#### Constraints
This section gives all constraints applicable to the input.

<a id="E_SUB_INT_CONSTR_A_0010"></a>
- `[E_SUB_INT_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape.
<a id="E_SUB_INT_CONSTR_A_0020"></a>
- `[E_SUB_INT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 


### $\text{B}$: integer tensor

Tensor $B$ is the second operand of the subtraction.

#### Constraints

- `[E_SUB_INT_CONSTR_B_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_INT_CONSTR_A_0010</span></b>](#E_SUB_INT_CONSTR_A_0010) on tensor $A$.
- `[E_SUB_INT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_INT_CONSTR_A_0020</span></b>](#E_SUB_INT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: integer tensor

Tensor $C$ is the element-wise integer subtraction result.

#### Constraints

 - `[E_SUB_INT_CONSTR_C_0010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_INT_CONSTR_A_0010</span></b>](#E_SUB_INT_CONSTR_A_0010) on tensor $A$.
- `[E_SUB_INT_CONSTR_C_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_SUB_INT_CONSTR_A_0020</span></b>](#E_SUB_INT_CONSTR_A_0020) on tensor $A$.








