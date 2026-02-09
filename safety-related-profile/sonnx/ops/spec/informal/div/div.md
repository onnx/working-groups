# Contents

- **Div** operator for type [real](#real)
- **Div** operator for types [float16, float, double](#float)
- **Div** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Div version 14](https://onnx.ai/onnx/operators/onnx__Div.html#div-14).

<a id="real"></a>
# **Div** (real, real)

## Signature

$C =\textbf{Div}(A, B)$

where:
- $A$: numerator
- $B$: denominator
- $C$: result of the element-wise division of $A$ by $B$
 

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Informal specification

Operator **Div** divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. If $i$ is a [tensor index](./../common/definitions.md#tensor_index), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] = 
\begin{cases} 
A[i]/B[i] & \text{if } B[i] \text{ is different from 0} \\
\text{ undefined} & \text{otherwise}
\end{cases}
$$




The effect of the operator is illustrated on the following examples.

### Example 1

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3 & 3.3 & 5.1 \end{bmatrix}
```

```math
C = \frac{A}{B} = \begin{bmatrix} 6.1/3 & 9.5/3.3 & 35.7/5.1 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix}
  3.7 & 4.4 \\
  16.2 & 0.5 \\
  25.3 & 24.8
\end{bmatrix}
```

```math
B = \begin{bmatrix}
  3 & 2.2 \\
  4.1 & 1 \\
  5.2 & 4
\end{bmatrix}
```

```math
C = \frac{A}{B} = \begin{bmatrix}
  3.7/3 & 2 \\
  16.2/4.1 & 0.5 \\
  25.3/5.2 & 6.2
\end{bmatrix}
```

## Error conditions
No error condition.

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: real tensor

Numerator of the division.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $A$, $B$, and $C$ shall have the same shape. 
 
### $\text{B}$: real tensor

Denominator of the division.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.
 - `[C2]` Definition domain
   - Statement: $\forall i, B[i] \neq 0$ 

## Outputs

### $\text{C}$: real tensor

Tensor $C$ is the element-wise result of the division of $A$ by $B$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.

## Formal specification
 
See the Why3 specification.

<a id="float"></a>
# **Div** (float, float)
where float is in {float16, float, double}

## Signature
Definition of operator $\text{Div}$ signature:
$C = \textbf{Div}(A, B)$

where

 - $A$: numerator
 - $B$: denominator
 - $C$: result of element-wise division of $A$ by $B$
 
## Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Informal specification

Operator **Div** divides input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics and stores the result in output tensor $C$. If $i$ is a [tensor index](../common/lexicon.md#tensor_index), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] = 
\begin{cases} 
A[i]/B[i] & \text{if } A[i] \text{ and } B[i] \text{ are different from 0} \\
\pm\text{inf} & \text{if } A[i] \neq 0 \text{ and } B[i]= 0  \\
\text{NaN} & \text{if } A[i]=0 \text{ and } B[i]=0 
\end{cases}
$$

In the second case, the sign of $\pm \text{inf}$ is determined from the signs of $A[i]$ and the zero ($\pm 0$) according to the IEEE754 rules.

### Example 1

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 1.0 & 2.25 \\ 4.0 & \text{+inf} \\ 5.1 & 6.0625 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 3.25 & 4.5 \\ 16.0 & 0.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 1.0833 & 2.25 \\ 4.0 & \text{NaN} \\ 5.1 & 6.0625 \end{bmatrix}
```

## Error conditions
  A value in the output tensor is NaN if the numerator and denominator are both 0 (+0.0 or -0.0 according to IEEE754).  

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: floating-point tensor
Numerator of the division.

#### Constraints

- `[C1]` <a id="C1fa"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape. 
- `[C2]` <a id="C2fa"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 

### $\text{B}$: floating-point tensor
Denominator of the division.

#### Constraints
- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa) on tensor $A$.

## Outputs

### $\text{C}$: floating-point tensor

Result of the element-wise division of $A$ by $B$.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa) on tensor $A$.

## Numeric accuracy

[See the numeric accuracy note](./assets/numeric_accuracy/numeric_accuracy.md).


<a id="int"></a>

# **Div** (int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature
Definition of operator $\text{Div}$ signature:
 $C = \textbf{Div}(A,B)$

 where
 - $A$: numerator
 - $B$: denominator
 - $C$: result of the element-wise division of $A$ by $B$

### Restrictions
[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Informal specification

Operator **Div** divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$. 

The result of the division is the algebraic quotient of $A[i]$ by $B[i]$ with any fractional part discarded.

### Example 1

```math
A = \begin{bmatrix} 6 & 5 & -35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 3 & 3 \end{bmatrix}
```
```math
C = \begin{bmatrix} 2 & 1 & -11 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 10 & 10 \\ 21 & 1 \\ 30 & 9 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```

```math
C = \begin{bmatrix} 3 & 5 \\ 5 & 1 \\ 6 & 2 \end{bmatrix}
```

## Error conditions
The behaviour in case of a null denominator is implementation dependent.

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: integer tensor

Numerator of the division.

#### Constraints

- `[C1]` <a id="C1ia"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $C$ must have the same shape. 
- `[C2]` <a id="C2ia"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 
  
### $\text{B}$: integer tensor

Denominator of the division.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $A$.
- `[C3]` Definition domain
  - Statement: $\forall i, B|i]\neq 0$.

## Outputs

### $\text{C}$: integer tensor

Result of the element-wise division of $A$ by $B$.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $A$.











