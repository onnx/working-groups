# Contents

* **Concat** operator for types [INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64, FP16, FP32, FP64, BFLOAT16, STRING, BOOL](#types)

Based on ONNX documentation [Concat version 13](https://onnx.ai/onnx/operators/onnx__Concat.html#concat-13).

<a id="types"></a>

# **Concat** (INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64, FP16, FP32, FP64, BFLOAT16, STRING, BOOL)

## Signature

$Y = \textbf{Concat}(X_0, \dots, X_n)$

where:

* $X_0, \dots, X_n$: input tensors to concatenate
* $Y$: output tensor resulting from the concatenation

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following specific restriction applies to the **Concat** operator for the SONNX profile:

| Restriction            | Statement                                   | Origin    |
| ---------------------- | ------------------------------------------- | --------- |
| `[R1]` <a id="R1"></a> | Attribute `axis` shall be positive or null. | Transient |

## Informal specification

Operator **Concat** concatenates the input tensors $X_0, \dots, X_n$ along the axis specified by attribute `axis`, and stores the result in output tensor $Y$.

The operator is structural: it does not perform arithmetic or logical computation on tensor values. It only copies input tensor elements into the output tensor according to their position and the selected concatenation axis. Therefore, the behaviour of **Concat** does not depend on the datatype of the tensor elements.

The order of the input tensors is significant. In general:

$$
\textbf{Concat}(X_0, X_1) \neq \textbf{Concat}(X_1, X_0)
$$

Let:

* $a$ be the concatenation axis;
* $r$ be the rank of the input tensors;
* $dX_{k,j}$ be the size of tensor $X_k$ along axis $j$;
* $s_k$ be the cumulative offset before tensor $X_k$ along axis $a$.

For each input tensor $X_k$, the cumulative offset $s_k$ is defined as:

$$
s_k = \sum_{j=0}^{k-1} dX_{j,a}
$$

For any output index $(i_0, \dots, i_{r-1})$, the value of $Y$ is copied from the unique input tensor $X_k$ such that:

$$
s_k \leq i_a < s_k + dX_{k,a}
$$

The local index $i'_a$ inside tensor $X_k$ is then:

$$
i'_a = i_a - s_k
$$

The output value is defined as:

$$
Y[i_0, \dots, i_a, \dots, i_{r-1}]
==================================

X_k[i_0, \dots, i'*a, \dots, i*{r-1}]
$$

The shape of output tensor $Y$ is identical to the input tensor shapes on all axes except the concatenation axis. On the concatenation axis, the output dimension is the sum of the corresponding input dimensions:

$$
dY_j =
\begin{cases}
\sum_{k=0}^{n} dX_{k,j} & \text{if } j = a \
dX_{0,j} & \text{otherwise}
\end{cases}
$$

## Example

Let:

```math
X_0 =
\begin{bmatrix}
1 & 2 & 3
\end{bmatrix}
```

```math
X_1 =
\begin{bmatrix}
4 & 5
\end{bmatrix}
```

```math
X_2 =
\begin{bmatrix}
6 & 7 & 8 & 9
\end{bmatrix}
```

If the concatenation is performed along axis `1`, then:

```math
Y = \textbf{Concat}(X_0, X_1, X_2)
```

and:

```math
Y =
\begin{bmatrix}
1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9
\end{bmatrix}
```

In this example:

* $dX_{0,1} = 3$
* $dX_{1,1} = 2$
* $dX_{2,1} = 4$
* $dY_1 = 3 + 2 + 4 = 9$

For instance, index $i_1 = 3$ in $Y$ belongs to $X_1$, because:

$$
s_1 = dX_{0,1} = 3
$$

and:

$$
3 \leq i_1 < 3 + 2
$$

Therefore:

$$
Y[0,3] = X_1[0,0]
$$

## Error conditions

No error condition is associated with the values stored in the input tensors, because **Concat** does not perform numerical computation.

The operator is undefined if one of the shape, rank, type, or axis constraints is not satisfied.

## Attributes

### `axis`: int

Attribute `axis` determines the axis along which the input tensors are concatenated.

#### Constraints

<a id="C1attr"></a>

* `[C1]` Valid axis domain

  * Statement: `axis` shall identify a valid dimension of the input tensors.

<a id="C2attr"></a>

* `[C2]` SONNX axis restriction

  * Statement: `axis` shall be positive or null. `[R1]`

Formally, for input tensors of rank $r$:

$$
0 \leq axis < r
$$

## Inputs

### $X_0, \dots, X_n$: tensor

Input tensors to concatenate.

All input tensors shall have the same datatype. Supported datatypes are:

`INT8`, `INT16`, `INT32`, `INT64`, `UINT8`, `UINT16`, `UINT32`, `UINT64`, `FP16`, `FP32`, `FP64`, `BFLOAT16`, `STRING`, `BOOL`.

#### Constraints

<a id="C1x"></a>

* `[C1]` Number of inputs

  * Statement: The number of input tensors shall be in the range $[1, 2^{31}-1]$.

<a id="C2x"></a>

* `[C2]` Rank consistency

  * Statement: All input tensors shall have the same rank.

Formally:

$$
\forall i,k,; rank(X_i) = rank(X_k)
$$

<a id="C3x"></a>

* `[C3]` Shape consistency

  * Statement: All input tensors shall have the same shape on every axis except the concatenation axis.

Formally, for all axes $j$ such that $j \neq axis$:

$$
\forall i,k,; dX_{i,j} = dX_{k,j}
$$

<a id="C4x"></a>

* `[C4]` Non-scalar inputs

  * Statement: All input tensors shall be non-scalar tensors.

Formally:

$$
\forall k,; rank(X_k) \geq 1
$$

<a id="C5x"></a>

* `[C5]` Type consistency

  * Statement: All input tensors shall have the same datatype.

## Outputs

### $Y$: tensor

Tensor $Y$ is the result of concatenating input tensors $X_0, \dots, X_n$ along attribute `axis`.

#### Constraints

<a id="C1y"></a>

* `[C1]` Rank consistency

  * Statement: Tensor $Y$ shall have the same rank as the input tensors.

Formally:

$$
rank(Y) = rank(X_0)
$$

<a id="C2y"></a>

* `[C2]` Shape consistency

  * Statement: Tensor $Y$ shall have the same shape as the input tensors on every axis except the concatenation axis.

Formally, for all axes $j$ such that $j \neq axis$:

$$
dY_j = dX_{0,j}
$$

<a id="C3y"></a>

* `[C3]` Concatenation axis dimension

  * Statement: The size of tensor $Y$ on the concatenation axis shall be the sum of the input tensor sizes on this axis.

Formally:

$$
dY_{axis} = \sum_{k=0}^{n} dX_{k,axis}
$$

<a id="C4y"></a>

* `[C4]` Type consistency

  * Statement: Tensor $Y$ shall have the same datatype as the input tensors.

## Formal specification

See the Why3 specification.

## Numerical Accuracy

Operator **Concat** does not perform numerical operations. Therefore, numerical accuracy issues are not applicable.
