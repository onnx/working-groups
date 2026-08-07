Generated on: 2026-06-08

# Contents

- Div operator for type [real](#real)
- Div operator for types [float16, float, double](#float)
- Div operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

Based on ONNX documentation [Div version 14](https://onnx.ai/onnx/operators/onnx__Div.html#div-14).


<a id="real"></a>
# Specification of operator Div for real values

## Signature

$$
C = \textbf{Div}(A, B)
$$

where:
- $A$ (real): Numerator
- $B$ (real): Denominator
- $C$ (real): Element-wise division of $A$ by $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Function

<a id="E_DIV_REAL_FUNC_0010"></a>
<span style="background: red; color: white; font-size:0.7em;">[E_DIV_REAL_FUNC_0010]</br></span>
Operator Div divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$.

If $i$ is a [tensor index](./../common/defs.md#tensor_index), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/defs.md#tensor_index) $i$:

$$
C[i] = \frac{A[i]}{B[i]}
$$

if $B[i] \neq 0$; otherwise $C[i]$ is not defined.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

$$
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
$$

$$
B = \begin{bmatrix} 3 & 3.3 & 5.1 \end{bmatrix}
$$

$$
C = \frac{A}{B}
  = \begin{bmatrix} 6.1/3 & 9.5/3.3 & 35.7/5.1 \end{bmatrix}
$$
### Example 2

$$
A =
\begin{bmatrix}
  3.7 & 4.4 \\
  16.2 & 0.5 \\
  25.3 & 24.8
\end{bmatrix}
$$

$$
B =
\begin{bmatrix}
  3 & 2.2 \\
  4.1 & 1 \\
  5.2 & 4
\end{bmatrix}
$$

$$
C = \frac{A}{B}
  =
\begin{bmatrix}
  3.7/3 & 2 \\
  16.2/4.1 & 0.5 \\
  25.3/5.2 & 6.2
\end{bmatrix}
$$

## Error conditions

No error condition.

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: real

Numerator

#### Constraints

<a id="E_DIV_REAL_CONSTR_A_0010"></a>
- `[E_DIV_REAL_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.

### $\text{B}$: real

Denominator

#### Constraints

<a id="E_DIV_REAL_CONSTR_B_0010"></a>
- `[E_DIV_REAL_CONSTR_B_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_REAL_CONSTR_A_0010</span></b>](#E_DIV_REAL_CONSTR_A_0010) on tensor $A$.
<a id="E_DIV_REAL_CONSTR_B_0020"></a>
- `[E_DIV_REAL_CONSTR_B_0020]` Avoid undefined behaviour for operator Div
  - Statement: $\forall i,\ B[i] \neq 0$

## Outputs

### $\text{C}$: real

Element-wise division of $A$ by $B$

#### Constraints

<a id="E_DIV_REAL_CONSTR_C_0010"></a>
- `[E_DIV_REAL_CONSTR_C_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_REAL_CONSTR_A_0010</span></b>](#E_DIV_REAL_CONSTR_A_0010) on tensor $A$.

---

<a id="float"></a>
# Specification of operator Div for float values

where float is in {float16, float, double}

## Signature

$$
C = \textbf{Div}(A, B)
$$

where:
- $A$ (float): Numerator
- $B$ (float): Denominator
- $C$ (float): Element-wise division of $A$ by $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Function

<a id="E_DIV_FLOAT_FUNC_0010"></a>
<span style="background: red; color: white; font-size:0.7em;">[E_DIV_FLOAT_FUNC_0010]</br></span>
Operator Div divides input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics and stores the result in output tensor $C$.

If $i$ is a [tensor index](./../common/defs.md#tensor_index), each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/defs.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
A[i]/B[i] & \text{if } A[i] \text{ and } B[i] \text{ are different from } 0 \\
\pm\mathrm{inf} & \text{if } A[i] \neq 0 \text{ and } B[i] = 0 \\
\mathrm{NaN} & \text{if } A[i] = 0 \text{ and } B[i] = 0
\end{cases}
$$

In the second case, the sign of $\pm\mathrm{inf}$ is determined from the signs of $A[i]$ and the zero value ($+0$ or $-0$) according to IEEE 754 rules.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

$$
A =
\begin{bmatrix}
3.0 & 4.5 \\
16.0 & 1.0 \\
25.5 & 24.25
\end{bmatrix}
\quad
B =
\begin{bmatrix}
3.0 & 2.0 \\
4.0 & 0.0 \\
5.0 & 4.0
\end{bmatrix}
$$

$$
C \approx
\begin{bmatrix}
1.0 & 2.25 \\
4.0 & +\mathrm{inf} \\
5.1 & 6.0625
\end{bmatrix}
$$
### Example 2

$$
A =
\begin{bmatrix}
3.25 & 4.5 \\
16.0 & 0.0 \\
25.5 & 24.25
\end{bmatrix}
\quad
B =
\begin{bmatrix}
3.0 & 2.0 \\
4.0 & 0.0 \\
5.0 & 4.0
\end{bmatrix}
$$

$$
C \approx
\begin{bmatrix}
1.0833 & 2.25 \\
4.0 & \mathrm{NaN} \\
5.1 & 6.0625
\end{bmatrix}
$$

## Error conditions

- A value in the output tensor is NaN if the numerator and denominator are both 0 ($+0.0$ or $-0.0$ according to IEEE 754).

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: float

Numerator

#### Constraints

<a id="E_DIV_FLOAT_CONSTR_A_0010"></a>
- `[E_DIV_FLOAT_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same shape.
<a id="E_DIV_FLOAT_CONSTR_A_0020"></a>
- `[E_DIV_FLOAT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type.

### $\text{B}$: float

Denominator

#### Constraints

<a id="E_DIV_FLOAT_CONSTR_B_0010"></a>
- `[E_DIV_FLOAT_CONSTR_B_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_FLOAT_CONSTR_A_0010</span></b>](#E_DIV_FLOAT_CONSTR_A_0010) on tensor $A$.
<a id="E_DIV_FLOAT_CONSTR_B_0020"></a>
- `[E_DIV_FLOAT_CONSTR_B_0020]` Type consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_FLOAT_CONSTR_A_0020</span></b>](#E_DIV_FLOAT_CONSTR_A_0020) on tensor $A$.

## Outputs

### $\text{C}$: float

Element-wise division of $A$ by $B$

#### Constraints

<a id="E_DIV_FLOAT_CONSTR_C_0010"></a>
- `[E_DIV_FLOAT_CONSTR_C_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_FLOAT_CONSTR_A_0010</span></b>](#E_DIV_FLOAT_CONSTR_A_0010) on tensor $A$.
<a id="E_DIV_FLOAT_CONSTR_C_0020"></a>
- `[E_DIV_FLOAT_CONSTR_C_0020]` Type consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_FLOAT_CONSTR_A_0020</span></b>](#E_DIV_FLOAT_CONSTR_A_0020) on tensor $A$.

---

<a id="int"></a>
# Specification of operator Div for int values

where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature

$$
C = \textbf{Div}(A, B)
$$

where:
- $A$ (int): Numerator
- $B$ (int): Denominator
- $C$ (int): Element-wise division of $A$ by $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Div** operator.

## Function

<a id="E_DIV_INT_FUNC_0010"></a>
<span style="background: red; color: white; font-size:0.7em;">[E_DIV_INT_FUNC_0010]</br></span>
Operator Div divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $C$.

For any [tensor index](./../common/defs.md#tensor_index) $i$, the result of the division is the algebraic quotient of $A[i]$ by $B[i]$ with any fractional part discarded.

$$
C[i] = \operatorname{trunc}\left(\frac{A[i]}{B[i]}\right)
$$

where $B[i] \neq 0$.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

$$
A = \begin{bmatrix} 6 & 5 & -35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 3 & 3 \end{bmatrix}
$$

$$
C = \begin{bmatrix} 2 & 1 & -11 \end{bmatrix}
$$
### Example 2

$$
A =
\begin{bmatrix}
10 & 10 \\
21 & 1 \\
30 & 9
\end{bmatrix}
\quad
B =
\begin{bmatrix}
3 & 2 \\
4 & 1 \\
5 & 4
\end{bmatrix}
$$

$$
C =
\begin{bmatrix}
3 & 5 \\
5 & 1 \\
6 & 2
\end{bmatrix}
$$

## Error conditions

- The behaviour in case of a null denominator is implementation dependent.

## Attributes

Operator **Div** has no attribute.

## Inputs

### $\text{A}$: int

Numerator

#### Constraints

<a id="E_DIV_INT_CONSTR_A_0010"></a>
- `[E_DIV_INT_CONSTR_A_0010]` Shape consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same shape.
<a id="E_DIV_INT_CONSTR_A_0020"></a>
- `[E_DIV_INT_CONSTR_A_0020]` Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type.

### $\text{B}$: int

Denominator

#### Constraints

<a id="E_DIV_INT_CONSTR_B_0010"></a>
- `[E_DIV_INT_CONSTR_B_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_INT_CONSTR_A_0010</span></b>](#E_DIV_INT_CONSTR_A_0010) on tensor $A$.
<a id="E_DIV_INT_CONSTR_B_0020"></a>
- `[E_DIV_INT_CONSTR_B_0020]` Type consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_INT_CONSTR_A_0020</span></b>](#E_DIV_INT_CONSTR_A_0020) on tensor $A$.
<a id="E_DIV_INT_CONSTR_B_0030"></a>
- `[E_DIV_INT_CONSTR_B_0030]` Definition domain
  - Statement: $$
    \forall i,\ B[i] \neq 0
    $$

## Outputs

### $\text{C}$: int

Element-wise division of $A$ by $B$

#### Constraints

<a id="E_DIV_INT_CONSTR_C_0010"></a>
- `[E_DIV_INT_CONSTR_C_0010]` Shape consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_INT_CONSTR_A_0010</span></b>](#E_DIV_INT_CONSTR_A_0010) on tensor $A$.
<a id="E_DIV_INT_CONSTR_C_0020"></a>
- `[E_DIV_INT_CONSTR_C_0020]` Type consistency
  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">E_DIV_INT_CONSTR_A_0020</span></b>](#E_DIV_INT_CONSTR_A_0020) on tensor $A$.

