# Contents

- **Less** operator for type [real](#real)
- **Less** operator for types [float16, float, double](#float)
- **Less** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Less version 13](https://onnx.ai/onnx/operators/onnx__Less.html).

<a id="real"></a>
# **Less** (real, real)

## Signature

$C = \textbf{Less}(A, B)$

where
- $A$: real input tensor to compare
- $B$: real input tensor to compare with $A$
- $C$: boolean result tensor of the element-wise comparison of $A$ and $B$
- 
## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Function
<span style="background: red; color: white; font-size:0.7em;">[E_ABS_REAL_LESS_010]</br></span>
Operator **Less** compares two input tensors $A$ and $B$ element-wise.  
For each element, if the corresponding entry in $A$ is strictly less than the corresponding entry in $B$, the corresponding entry in $C$ contains the value $\text{True}$, otherwise it contains the value $\text{False}$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}
\end{cases}
$$
<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

```math
A = \begin{bmatrix} 2.0 & 3.0 & 7.0 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3.0 & 3.0 & 5.0 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix} \text{True} & \text{False} & \text{False} \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 1.1 & 2.0 \\ 4.2 & 0.0 \\ 5.3 & 6.4 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3.5 & 2.0 \\ 4.6 & 1.0 \\ 5.7 & 4.8 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix}
\text{True} & \text{False} \\
\text{True} & \text{True} \\
\text{True} & \text{False}
\end{bmatrix}
```

## Error conditions
No error condition.

## Attributes

Operator **Less** has no attribute.

## Inputs

### $\text{A}$: real tensor

First input tensor to be compared.

#### Constraints

- `[E_LESS_REAL_CONSTR_A_010]` <a id="E_LESS_REAL_CONSTR_A_010"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  
 
### $\text{B}$: real tensor

Second input tensor to be compared with $A$.

#### Constraints

 - `[E_LESS_REAL_CONSTR_B_010]` Shape consistency
   -  Statement: See constraint [E_LESS_REAL_CONSTR_A_010](#E_LESS_REAL_CONSTR_A_010) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

Output tensor formed by the element-wise comparison of $A$ and $B$.

#### Constraints

- `[E_LESS_REAL_CONSTR_C_010]` <a id="E_LESS_REAL_CONSTR_C_010"></a> Shape consistency  
  - Statement: See constraint [E_LESS_REAL_CONSTR_A_010](#E_LESS_REAL_CONSTR_A_010) on tensor $A$.


<a id="float"></a>
# **Less** (float, float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Less}$ signature:  
$C = \textbf{Less}(A, B)$

where
- $A$: float input tensor to compare
- $B$: float input tensor to compare with $A$
- $C$: boolean result tensor of the element-wise comparison of $A$ and $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Function
<span style="background: red; color: white; font-size:0.7em;">[E_ABS_FLOAT_LESS_010]</br></span>
Operator **Less** compares two input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics.  
For each element, if the corresponding entry in $A$ is strictly less than the corresponding entry in $B$, the resulting tensor $C$ contains the value $\text{True}$. Otherwise, the resulting tensor $C$ contains the value $\text{False}$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\begin{cases}
\text{False} & \text{if } A[i]=\text{NaN} & or & B[i]=\text{NaN} \\
\text{False} & \text{if } A[i]=\text{-0.0} & and & B[i]=\text{0.0} \\
\text{False} & \text{if } A[i]=\text{0.0} & and & B[i]=\text{-0.0} \\

\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}

\end{cases}
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

Note: Comparisons involving NaN follow IEEE 754 rules (e.g., $\text{NaN} < x$ or $x < \text{NaN}$  is False for any $x$). 

The effect of the operator is illustrated on the following examples.

### Example 1

```math
A = \begin{bmatrix} 2.5 & 3.7 & 7.9 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3.1 & 3.7 & 5.8 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix} \text{True} & \text{False} & \text{False} \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 1.1 & 2.0 \\ 4.2 & 0.0 \\ 5.3 & 6.4 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3.5 & 2.0 \\ 4.6 & 1.0 \\ 5.7 & 4.8 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix}
\text{True} & \text{False} \\
\text{True} & \text{True} \\
\text{True} & \text{False}
\end{bmatrix}
```

### Example 3

```math
A = \begin{bmatrix} \text{-inf} & \text{-inf} & \text{-inf} & \text{-inf} & 0.0 & 0.0 & 0.0 & 0.0 & \text{+inf} & \text{+inf} & \text{+inf} & \text{+inf} & \text{NaN} & \text{NaN} & \text{NaN} & \text{NaN} \end{bmatrix}
```

```math
B = \begin{bmatrix} \text{-inf} & 0.0 & \text{+inf} & \text{NaN} &  \text{-inf} & 0.0 & \text{+inf} & \text{NaN} & \text{-inf} & 0.0 & \text{+inf} & \text{NaN} & \text{-inf} & 0.0 & \text{+inf} & \text{NaN}  \end{bmatrix}
```

```math
C = \begin{bmatrix} \text{False} & \text{True} & \text{True} &\text{False} &\text{False} &\text{False} & \text{True} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} & \text{False} & \text{False}  \end{bmatrix}
```



## Error conditions

No error condition.

## Attributes

Operator **Less** has no attribute.

## Inputs

### $\text{A}$: floating-point tensor

First input tensor to be compared.

#### Constraints

- `[E_LESS_FLOAT_CONSTR_A_010]` <a id="E_LESS_FLOAT_CONSTR_A_010"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  

- `[E_LESS_FLOAT_CONSTR_A_020]` <a id="E_LESS_FLOAT_CONSTR_A_020"></a> Type consistency  
  - Statement: Tensors $A$ and $B$ shall have the same floating-point type.

### $\text{B}$: floating-point tensor

Second input tensor to be compared with $A$.

#### Constraints
- `[E_LESS_FLOAT_CONSTR_B_010]` Shape consistency
  - Statement: see constraint [E_LESS_FLOAT_CONSTR_A_010](#E_LESS_FLOAT_CONSTR_A_010) on tensor $A$.
- `[E_LESS_FLOAT_CONSTR_B_020]` Type consistency
  - Statement: see constraint [E_LESS_FLOAT_CONSTR_A_020](#E_LESS_FLOAT_CONSTR_A_020) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

Output tensor formed by the element-wise comparison of $A$ and $B$.

#### Constraints

- `[E_LESS_FLOAT_CONSTR_C_010]` <a id="E_LESS_FLOAT_CONSTR_C_010"></a> Shape consistency  
  - Statement: See constraint [E_LESS_FLOAT_CONSTR_A_010](#E_LESS_FLOAT_CONSTR_A_010) on tensor $A$.

## Formal specification
 See Why3 specification.



<a id="int"></a>
# **Less** (int,int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}

## Signature

Definition of operator $\text{Less}$ signature:  
$C = \textbf{Less}(A, B)$

where
- $A$: int input tensor to compare
- $B$: int input tensor to compare with $A$
- $C$: boolean result tensor of the element-wise comparison of $A$ and $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Informal specification
<span style="background: red; color: white; font-size:0.7em;">[E_LESS_INT_FUNC_010]</br></span>
Operator **Less** compares two input tensors $A$ and $B$ element-wise using integer comparison.  
For each element, if the corresponding entry in $A$ is strictly less than the corresponding entry in $B$, the resulting tensor $C$ contains the value $\text{True}$. Otherwise, the resulting tensor $C$ contains the value $\text{False}$.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}
\end{cases}
$$

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The examples given in the real section apply directly when restricted to integer values.
### Example 1

```math
A = \begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3 & 3 & 5 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix} \text{True} & \text{False} & \text{False} \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 1 & 2 \\ 4 & 0 \\ 5 & 6 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```

Result $C$ is:

```math
C = \begin{bmatrix}
\text{True} & \text{False} \\
\text{False} & \text{True} \\
\text{False} & \text{False}
\end{bmatrix}
```


## Error conditions

No error condition.

## Attributes

Operator **Less** has no attribute.

## Inputs

### $\text{A}$: integer tensor

First input tensor to be compared.

#### Constraints

- `[E_LESS_INT_CONSTR_A_010]` <a id="E_LESS_INT_CONSTR_A_010"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  
- `[E_LESS_INT_CONSTR_A_020]` <a id="E_LESS_INT_CONSTR_A_020"></a> Type consistency  
  - Statement: Tensors $A$ and $B$ shall have the same integer type.

### $\text{B}$: integer tensor

Second input tensor to be compared with $A$.

#### Constraints

- `[E_LESS_INT_CONSTR_B_010]` Shape consistency  
  - Statement: See constraint [`E_LESS_INT_CONSTR_A_010`](#E_LESS_INT_CONSTR_A_010) on tensor $A$.
- `[E_LESS_INT_CONSTR_B_020]` Type consistency  
  - Statement: See constraint [`E_LESS_INT_CONSTR_A_020`](#E_LESS_INT_CONSTR_A_020) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

Output tensor formed by the element-wise comparison of $A$ and $B$.

#### Constraints

- `[E_LESS_INT_CONSTR_C_010]` <a id="E_LESS_INT_CONSTR_C_010"></a> Shape consistency  
  - Statement: See constraint [E_LESS_INT_CONSTR_A_010](#E_LESS_INT_CONSTR_A_010) on tensor $A$.



