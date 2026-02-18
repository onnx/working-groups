# Contents

- **Pow** operator for type [real](#real)
- **Pow** operator for types [float16, float, double](#float)
- **Pow** operator for types [int32, int64](#int)

Based on ONNX documentation [Pow version 15](https://onnx.ai/onnx/operators/onnx__Pow.html).

<a id="real"></a>

# **Pow** (real, real)

## Signature

$C = \textbf{Pow}(A, B)$

where:

- $A$: base tensor
- $B$: exponent tensor
- $C$: result of the element-wise power of $A$ to $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following restrictions apply to the `Pow` operator for the SONNX profile:
- All input elements in `A` and `B` must be of types that support the power operation `[R1]`
- All input `A` and output element shall be of the same type (not possible to mix integer and real) `[R2]`
- All `B` element of the exponent shall be of the same type (it is not possible to mix integer and real) `[R3]`


## Informal specification

Operator **Pow** computes the element-wise power between input tensors $A$ and $B$ and stores the result in output tensor $C$.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

**pow** is indefined for the value  $A[i] < 0 \text{ and } B[i] \notin \mathbb{Z} ~~or~~ B[i] = \frac{q}{p} \text{ in its simplest form with } q \text{ even}  \ ~~or~~ A[i] = 0 \text{ et } B[i] \leq 0$ , otherwise **pow** is defined by :

$$
C[i] =
\begin{cases}
0.0 & \text{si } A[i] = 0 \text{ et } B[i] > 0 \\
1.0 & \text{si } A[i] \neq 0 \text{ et } B[i] = 0\\
A[i]^{B[i]} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
A = \begin{bmatrix} 9 & 4 & 16 & 8 & 2 \end{bmatrix}
\quad
B = \begin{bmatrix} 2 & 2.5 & \frac{1}{2} & \frac{1}{3} & \frac{3}{2} \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 81 & 32 & 4 & 2 & 2.82842708 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 0 & 0 & 5 & -5 & -25 & -8 \end{bmatrix}
\quad
B = \begin{bmatrix} 0 & 2 & 0 & 0 & \frac{3}{5} & \frac{1}{3} \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 1 & 0 & 1 & 1 & −6.898648307 & -2.0 \end{bmatrix}
```



## Error conditions

No error condition beyond the undefined behavior for out of range inputs in the mathematical model.

## Attributes

Operator **Pow** has no attribute.

## Inputs

### $\text{A}$: real tensor

Base of the power operation.

#### Constraints

- `[C1]` <a id="C1ra_pow"></a> Shape consistency

  - Statement: Tensors $A$, $B$, and $C$ shall have the same shape.

### $\text{B}$: real tensor

Exponent of the power operation.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra_pow) on tensor $A$.

## Outputs

### $\text{C}$: real tensor

Result of the element-wise power of $A$ to $B$.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra_pow) on tensor $A$.

## Formal specification

See the Why3 specification.

<a id="float"></a>

# **Pow** (float, float)

where float is in {float16, float, double}

## Signature

Definition of operator $\text{Pow}$ signature:

$C = \textbf{Pow}(A, B)$

where:

- $A$: base tensor
- $B$: exponent tensor
- $C$: result of element-wise power of $A$ to $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

In more than the additionnal [Restrictions](#restrictions) the input range of $B[i]$ is limited for float :

- Even if it is possible to compute **Pow** in the real space when B$[i] = \frac{q}{p} \text{ in its simplest form with } q \text{ odd}$ this value will be not defined in float and will return a NaN. `[R4]`


## Informal specification

Operator **Pow** computes the element-wise power between input tensors $A$ and $B$ according to IEEE 754 floating-point semantics and stores the result in output tensor $C$.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:





$$
C[i] = \begin{cases}
\text{NaN} & \text{if } (A[i] = \text{NaN} \text{ and } B[i] \neq \pm0) \text{ or } B[i] = \text{NaN} \\
\text{NaN} & \text{if } A[i] \in ]-\infty, +\infty[ \text{ and } B[i] \notin \mathbb{Z}  \text{ and } B[i] \neq \pm0 \\

1.0 & \text{if } B[i] = \pm 0 \\
0.0 & \text{if } A[i] = 0 \text{ and } B[i] > 0 \\
0.0 & \text{if } A[i] = \pm\infty \text{ and } B[i] < 0 \\
0.0 & \text{if } A[i] \in ]-\infty, +\infty[  and A[i] \neq \pm0 \text{ and } B[i] = -\infty \\
+\infty & \text{if } A[i] = +\infty \text{ and } B[i] > 0 \\
+\infty & \text{if } A[i] = \pm0 \text{ and } B[i] < 0 \\
A[i]^{B[i]} & \text{otherwise}
\end{cases}
$$





[HBE revoir la formule, un tableau ? C'est pas fini]

|  A\B   | -inf |$$]-\infty, 0[ \in \mathbb{Z}$$|$$]-\infty, 0[ \notin \mathbb{Z} $$| -0.0 | 0.0  |$$]0,+\infty[ \notin \mathbb{Z} $$ |$$]0,+\infty[ \in \mathbb{Z}$$| inf  | nan  |
|--------|------|----------|---------|------|------|------|-------|------|------|
|  -inf  | 0    |    0     |    0    | 1    | 1    | inf  |  inf  | inf  | nan  |
|]-inf,0[| 0    |    A^B   |    nan  | 1    | 1    | nan  |  A^B  | inf  | nan  |
|  -0.0  | inf  |    inf   |    inf  | 1    | 1    | 0    |  0    | 0    | nan  |
|   0.0  | inf  |    inf   |    inf  | 1    | 1    | 0    |  0    | 0    | nan  |
|]0,inf[ | 0    |    A^B   |    A^B  | 1    | 1    | A^B  |  A^B  | inf  | nan  |
| inf    | 0    |    0     |    0    | 1    | 1    | inf  |  inf  | inf  | nan  |
| nan    | nan  |    nan   |    nan  | 1    | 1    | nan  |  nan  | nan  | nan  |






### Example 1

```math
A = \begin{bmatrix} 9 & 4 & 16 & 8 & 2 \end{bmatrix}
\quad
B = \begin{bmatrix} 2 & 2.5 & \frac{1}{2} & \frac{1}{3} & \frac{3}{2} \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 81 & 32 & 4 & 2 & 2.82842708 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 0 & 0 & 5 & -5 & -25 & -8 \end{bmatrix}
\quad
B = \begin{bmatrix} 0 & 2 & 0 & 0 & \frac{3}{5} & \frac{1}{3} \end{bmatrix}
```

```math
C \approx \begin{bmatrix} 1 & 0 & 1 & 1 & NaN & NaN \end{bmatrix}
```
[HBE exemple float]


## Error conditions

No error condition.
[HBE A ANALYSER]

## Attributes

Operator **Pow** has no attribute.

## Inputs

### $\text{A}$: floating-point tensor

Base of the power operation.

#### Constraints

- `[C1]` <a id="C1fa_pow"></a> Shape consistency

  - Statement: Tensors $A$, $B$, and $C$ must have the same shape.
- `[C2]` <a id="C2fa_pow"></a> Type consistency

  - Statement: Tensors $A$, $B$, and $C$ must have the same floating-point type.

### $\text{B}$: floating-point tensor

Exponent of the power operation.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa_pow) on tensor $A$.
- `[C2]` Type consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa_pow) on tensor $A$.

## Outputs

### $\text{C}$: floating-point tensor

Result of the element-wise power of $A$ to $B$.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa_pow) on tensor $A$.
- `[C2]` Type consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa_pow) on tensor $A$.

## Numeric accuracy

[See the numeric accuracy note](./pow_acc.md).


[HBE A PASSER DEVANT FLOAT ?]
<a id="int"></a>

# **Pow** (int, int)

where int is in {int32, int64}

## Signature

Definition of operator $\text{Pow}$ signature:
$C = \textbf{Pow}(A, B)$

where:

- $A$: base tensor
- $B$: exponent tensor
- $C$: result of element-wise power of $A$ to $B$

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

No specific restrictions apply to the **Pow** operator.
[HBE A ANALYSER]

## Informal specification

Operator **Pow** computes the element-wise integer power between input tensors $A$ and $B$ and stores the result in output tensor $C$.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
C[i] =
\begin{cases}
A[i]^{B[i]} & \text{if } B[i] \ge 0 \
\text{undefined} & \text{otherwise}
\end{cases}
$$

The exponent must be non-negative. The result is the exact integer power, provided no overflow occurs. Overflow behavior is implementation dependent.

### Example 1

```math
A = \begin{bmatrix} 2 & 3 & 4 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 2 & 1 \end{bmatrix}
```

```math
C = \begin{bmatrix} 8 & 9 & 4 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 5 & 2 \\ 3 & 4 \end{bmatrix}
\quad
B = \begin{bmatrix} 0 & 3 \\ 2 & 1 \end{bmatrix}
```

```math
C = \begin{bmatrix} 1 & 8 \\ 9 & 4 \end{bmatrix}
```

## Error conditions

The behaviour is implementation dependent if:

- An exponent is negative.
- An overflow occurs during the computation.
[HBE A ANALYSER]

## Attributes

Operator **Pow** has no attribute.

## Inputs

### $\text{A}$: integer tensor

Base of the power operation.

#### Constraints

- `[C1]` <a id="C1ia_pow"></a> Shape consistency

  - Statement: Tensors $A$, $B$, and $C$ must have the same shape.
- `[C2]` <a id="C2ia_pow"></a> Type consistency

  - Statement: Tensors $A$, $B$, and $C$ must have the same type.

### $\text{B}$: integer tensor

Exponent of the power operation.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia_pow) on tensor $A$.
- `[C2]` Type consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia_pow) on tensor $A$.
- `[C3]` Definition domain

  - Statement: $\forall i, B[i] \ge 0$.

## Outputs

### $\text{C}$: integer tensor

Result of the element-wise power of $A$ to $B$.

#### Constraints

- `[C1]` Shape consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia_pow) on tensor $A$.
- `[C2]` Type consistency

  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia_pow) on tensor $A$.
