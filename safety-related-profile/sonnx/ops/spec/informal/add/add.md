# Contents
- **Add** operator for type [real](#real)
- **Add** operator for types [float16, float32, double](#float)
- **Add** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Add version 14](https://onnx.ai/onnx/operators/onnx__Add.html#l-onnx-doc-add).

---

<a id="real"></a>
# **Add** (real, real)

## Signature

Definition of operator $\text{Add}$ signature:

$Y = \text{Add}(A, B)$

where:
- $A$: first operand of the addition  
- $B$: second operand of the addition  
- $Y$: result of the element-wise addition of $A$ to $B$
 

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Add** operator.

## Function

For any index i:

<span style="background: red; color: white; font-size:0.7em;">[E_ADD_REAL_FUNC_010]</br></span>
Operator **ADD** divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. If $i$ is a [tensor index](./../common/definitions.md), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] = A[i] + B[i]
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>


The effect of the operator is illustrated on the following examples:

---

### Example 1 (1D tensors)

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 2 & 3 & 4 \end{bmatrix}
```

```math
Y = A + B = \begin{bmatrix} 8.1 & 12.5 & 39.7 \end{bmatrix}
```

---

## Error conditions
No error condition.

## Attributes
Operator **Add** has no attribute.

## Inputs

### $\text{A}$: real tensor
Tensor $A$ is the first operand of the addition.

#### Constraints

 - `[E_ADD_REAL_CONSTR_A_010]` <a id="E_ADD_REAL_CONSTR_A_010"></a> Shape consistency
   - Statement: Tensors $A$, $B$, and $C$ shall have the same shape. 

 
### $\text{B}$: real tensor
Tensor $B$ is the second operand of the addition.

#### Constraints

 - `[E_ADD_REAL_CONSTR_B_010]` Shape consistency
  -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_REAL_CONSTR_A_010</span></b>](#E_ADD_REAL_CONSTR_A_010) on tensor $A$.


## Outputs

### $\text{Y}$: real tensor

Tensor $C$ is the element-wise result of $A$ Added by $B$.

#### Constraints

 - `[E_ADD_REAL_CONSTR_C_010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_REAL_CONSTR_A_010</span></b>](#E_ADD_REAL_CONSTR_A_010) on tensor $A$.


<a id="float"></a>
# **Add** (float, float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Add}$ signature:

$C = \text{Add}(A, B)$

where

 - $A$: first operand tensor
 - $B$: second operand  tensor
 - $C$: output tensor, result of element-wise addition of $A$ to $B$
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Add** operator.


## Function

<span style="background: red; color: white; font-size:0.7em;">[E_ADD_FLOAT_FUNC_010]</br></span>
Operator **ADD** divides input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics and stores the result in output tensor $C$. If $i$ is a [tensor index](../common/lexicon.md#tensor_index), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = A[i] + B[i]
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

### Example 1 (2D tensors)

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = A + B = \begin{bmatrix} 6.0 & 6.5 \\ 20.0 & 1.0 \\ 30.5 & 28.25 \end{bmatrix}
```
### Error conditions
No error condition.

## Attributes

Operator **ADD** has no attribute.

## Inputs

### $\text{A}$: floating-point tensor
First opearand of the addition.

#### Constraints

- `[E_ADD_FLOAT_CONSTR_A_0010]` <a id="E_ADD_FLOAT_CONSTR_A_0010"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape.
- `[E_ADD_FLOAT_CONSTR_A_0020]` <a id="E_ADD_FLOAT_CONSTR_A_0020"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type.

### $\text{B}$: floating-point tensor
Tensor $B$ is the second operand of the addition.

#### Constraints
- `[E_ADD_FLOAT_CONSTR_B_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_FLOAT_CONSTR_A_0010</span></b>](#E_ADD_FLOAT_CONSTR_A_0010) on tensor $A$.
- `[E_ADD_FLOAT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_FLOAT_CONSTR_A_0020</span></b>](#E_ADD_FLOAT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: floating-point tensor

Result of the element-wise result of $A$ Added to $B$.

#### Constraints

 - `[E_ADD_FLOAT_CONSTR_C_010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_FLOAT_CONSTR_A_010</span></b>](#E_ADD_FLOAT_CONSTR_A_010) on tensor $A$.
- `[E_ADD_FLOAT_CONSTR_C_020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_FLOAT_CONSTR_A_0020</span></b>](#E_ADD_FLOAT_CONSTR_A_020) on tensor $A$.

<a id="int"></a>

# **Add** (int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature
Definition of operator $\text{Add}$ signature:

 $C = \text{add}(A,B)$

 where
 - $A$: first operand of the addition
 - $B$: second operand of the addition
 - $C$: result of the element-wise addition of $A$ to $B$
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Add** operator.

## Function

<span style="background: red; color: white; font-size:0.7em;">[E_ADD_INT_FUNC_010]</br></span>
Operator **Add** adds input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. Each element $C[i]$ is the result of Adding $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/definitions.md#tensor_index).

The integer addition is performed as follows (considering that all tensors have the same type):

For unsigned values (type uint\<n>):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] + B[i]- k.2^{n} & \quad \textrm{if }  A[i] + B[i] > 2^{n}-1 \\
   A[i] + B[i] & \quad \textrm{otherwise}
  \end{array}
\right.$$

with $k \in N$ such that $0 \le A[i] + B[i]- k.2^{n} < 2^n$

For signed values (type int\<n>):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] + B[i]- k_1.2^{n} & \quad \textrm{if }  A[i] + B[i] > 2^{n-1}-1 \\
   A[i] + B[i] + k_2.2^{n} & \quad \textrm{if } A[i] + B[i] < -2^{n-1} \\
   A[i] + B[i] & \quad \textrm{otherwise}
  \end{array}
\right\}.$$

with 

$k_1 \in N$ such that $xxx \le A[i] + B[i]-k_1.2^{n} < 2^n$

$k_2 \in N$ such that $xxx \le A[i] + B[i]+k.2^{n} > -2^{n-1}$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

### Example 1 (1D uint8 tensors)

```math
A = \begin{bmatrix} 6 & 200 & 35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 100 & 5 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 9 & 44 & 40 \end{bmatrix}
```

### Example 1 (1D int8 tensors)

```math
A = \begin{bmatrix} -6 & 100 & -100  \end{bmatrix}
\quad
B = \begin{bmatrix} -3 & 100 & -100  \end{bmatrix}
```
```math
Y = \begin{bmatrix} -9 & -56 & 56  \end{bmatrix}
```

## Error conditions
- According to the definition, the result of the addition differs from the value that would be expected in $N$ (for unsigned) or $Z$ (for signed) when under- or overflow occur.

## Attributes

The $\text{Add}$ operator has no attribute.

## Inputs

### $\text{A}$: `integer tensor`

Tensor $A$ is the first operand of the addition.

#### Constraints

- `[E_ADD_INT_CONSTR_A_0010]` <a id="E_ADD_INT_CONSTR_A_0010"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape.
- `[E_ADD_INT_CONSTR_A_0020]` <a id="E_ADD_INT_CONSTR_A_0020"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type.



### $\text{B}$: `integer tensor`

Tensor $B$ is the second operand of the addition.

#### Constraints

- `[E_ADD_INT_CONSTR_B_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_INT_CONSTR_A_0010</span></b>](#E_ADD_INT_CONSTR_A_0010) on tensor $A$.
- `[E_ADD_INT_CONSTR_B_0020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_INT_CONSTR_A_0020</span></b>](#E_ADD_INT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{Y}$: `integer tensor`

Tensor $Y$ is the element-wise integer addition result.

#### Constraints

 - `[E_ADD_INT_CONSTR_C_010]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_INT_CONSTR_A_010</span></b>](#E_ADD_INT_CONSTR_A_010) on tensor $A$.
- `[E_ADD_INT_CONSTR_C_020]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_ADD_INT_CONSTR_A_0020</span></b>](#E_ADD_INT_CONSTR_A_020) on tensor $A$.










