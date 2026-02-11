# Contents

- **Less** operator for type [real](#real)
- **Less** operator for types [float16, float, double](#float)
- **Less** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Less version 13](https://onnx.ai/onnx/operators/onnx__Less.html).

<a id="real"></a>
# **Less** (real, real)

## Signature

Definition of operator $\text{Less}$ signature:  
$C = \textbf{Less}(A, B)$

where
- $A$: input tensor to compare
- $B$: input tensor to compare with $A$
- $C$: output boolean tensor based on element-wise comparison of $A$ and $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Informal specification

Operator **Less** compares two input tensors $A$ and $B$ element-wise.  
For each element, if the corresponding entry in $A$ is strictly less than the corresponding entry in $B$, the resulting tensor $C$ contains the value $\text{True}$. Otherwise, the resulting tensor $C$ contains the value $\text{False}$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}
\end{cases}
$$

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

- `[C1]` <a id="C1ra"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  
 
### $\text{B}$: real tensor

Second input tensor to be compared with $A$.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

*Output tensor formed by the element-wise comparison of $A$ and $B$.*

#### Constraints

- `[C1]` <a id="C1rc"></a> Shape consistency  
  - Statement: See constraint [`[C1]`](#C1ra) on tensor $A$.

## Formal specification

See the Why3 specification.


<a id="float"></a>
# **Less** (float, float)
where float is in {float16, float, double}

## Signature

Definition of operator $\text{Less}$ signature:  
$C = \textbf{Less}(A, B)$

where
- $A$: input tensor to compare
- $B$: input tensor to compare with $A$
- $C$: output boolean tensor based on element-wise comparison of $A$ and $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Informal specification

Operator **Less** compares two input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics.  
For each element, if the corresponding entry in $A$ is strictly less than the corresponding entry in $B$, the resulting tensor $C$ contains the value $\text{True}$. Otherwise, the resulting tensor $C$ contains the value $\text{False}$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
\text{True} & \text{if } A[i] < B[i] \\
\text{False} & \text{otherwise}
\end{cases}
$$

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
A = \begin{bmatrix} -\infty & -\infty & -\infty & -\infty & 0.0 & 0.0 & 0.0 & 0.0 & +\infty & +\infty & +\infty & +\infty & \text{NaN} & \text{NaN} & \text{NaN} & \text{NaN} \end{bmatrix}
```

```math
B = \begin{bmatrix} -\infty & 0.0 & +\infty & \text{NaN} &  -\infty & 0.0 & +\infty & \text{NaN} & -\infty & 0.0 & +\infty & \text{NaN} & -\infty & 0.0 & +\infty & \text{NaN}  \end{bmatrix}
```

```math
C = \begin{bmatrix} \text{False} & \text{True} & \text{True} &\text{False} &\text{False} &\text{False} & \text{True} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} &\text{False} & \text{False} & \text{False}  \end{bmatrix}
```



## Error conditions

Values of the output tensor may be $\text{True}$ or $\text{False}$ according to IEEE 754 comparison semantics. 
Comparisons involving NaN follow IEEE 754 rules (e.g., $\text{NaN} < x$ or $x < \text{NaN}$  is False for any $x$). 

## Attributes

Operator **Less** has no attribute.

## Inputs

### $\text{A}$: floating-point tensor

First input tensor to be compared.

#### Constraints

- `[C1]` <a id="C1fa"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  

- `[C2]` <a id="C2fa"></a> Type consistency  
  - Statement: Tensors $A$ and $B$ shall have the same floating-point type.

### $\text{B}$: floating-point tensor

Second input tensor to be compared with $A$.

#### Constraints
- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

Output tensor formed by the element-wise comparison of $A$ and $B$.

#### Constraints

- `[C1]` <a id="C1fc"></a> Shape consistency  
  - Statement: See constraint [`[C1]`](#C1fa) on tensor $A$.

## Formal specification
 See Why3 specification.



<a id="int"></a>
# **Less** (int,int)
where int is in (int8, int16, int32, int64, uint8, uint16, uint32, uint64)

## Signature

Definition of operator $\text{Less}$ signature:  
$C = \textbf{Less}(A, B)$

where
- $A$: input tensor to compare
- $B$: input tensor to compare with $A$
- $C$: output boolean tensor based on element-wise comparison of $A$ and $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Less** operator.

## Informal specification

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

- `[C1]` <a id="C1ia"></a> Shape consistency  
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.  
- `[C2]` <a id="C2ia"></a> Type consistency  
  - Statement: Tensors $A$ and $B$ shall have the same integer type.

### $\text{B}$: integer tensor

Second input tensor to be compared with $A$.

#### Constraints

- `[C1]` Shape consistency  
  - Statement: See constraint [`[C1]`](#C1ia) on tensor $A$.
- `[C2]` Type consistency  
  - Statement: See constraint [`[C2]`](#C2ia) on tensor $A$.

## Outputs

### $\text{C}$: bool tensor

Output tensor formed by the element-wise comparison of $A$ and $B$.

#### Constraints

- `[C1]` <a id="C1ic"></a> Shape consistency  
  - Statement: See constraint [`[C1]`](#C1ia) on tensor $A$.


## Formal specification
 See Why3 specification.

