# Contents

* **ArgMax** operator for type [real](#real)
* **ArgMax** operator for types [float16, float, double](#float)
* **ArgMax** operator for integer types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#integer)

Based on ONNX documentation [ArgMax version 13](https://onnx.ai/onnx/operators/onnx__ArgMax.html).

<a id="real"></a>

# **ArgMax** (real)

## Signature

$Y = \textbf{ArgMax}(X)$

where:

* $X$: input tensor
* $Y$: output tensor containing the indices of the maximum values of $X$ along a given axis

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

| Restriction            | Statement                                                   | Origin                                                                   |
| ---------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| `[R1]` <a id="R1"></a> | Attribute `axis` must be set                                | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R2]` <a id="R2"></a> | Attribute `keepdims` must be set                            | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R3]` <a id="R3"></a> | Attribute `select_last_index` must be set                   | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |
| `[R4]` <a id="R4"></a> | `axis` $\ge 0$                                              | Transient                                                                |
| `[R5]` <a id="R5"></a> | The dimension of $X$ along `axis` must be strictly positive | Mathematical definition                                                  |

---

## Informal specification

The **ArgMax** operator computes the index of the maximum value of the input tensor $X$ along a specified axis.

Let:

$$
r = \operatorname{rank}(X)
$$

where $r$ is the rank of the input tensor $X$.

Let `axis` be the dimension along which the maximum value is searched.

Let:

$$
dX_k
$$

be the size of tensor $X$ along dimension $k$.

The size of the reduced dimension is:

$$
dX_{\mathrm{axis}}
$$

For every output position $k$, all indices of $X$ are fixed except the index along the `axis` dimension.

This varying index is denoted by $j$.

It satisfies:

$$
0 \leq j < dX_{\mathrm{axis}}
$$

For a fixed output position $k$, let:

$$
S_k(j)
$$

denote the value of $X$ at the same fixed coordinates as $k$, with the coordinate $j$ inserted along the `axis` dimension.

In other words, $S_k(j)$ represents the slice of $X$ being inspected by **ArgMax** for one output position.

The maximum value of this slice is:

$$
M_k =
\max_{0 \leq j < dX_{\mathrm{axis}}}
S_k(j)
$$

The output value $Y[k]$ is an index $j$ where this maximum value is reached.

If `select_last_index = 0`, the first occurrence of the maximum value is selected.

In other words, $Y[k]$ is the smallest index $j$ such that:

$$
S_k(j) = M_k
$$

If `select_last_index = 1`, the last occurrence of the maximum value is selected.

In other words, $Y[k]$ is the greatest index $j$ such that:

$$
S_k(j) = M_k
$$

The output tensor contains integer indices in the range:

$$
0 \leq Y[k] < dX_{\mathrm{axis}}
$$

The shape of the output tensor depends on the value of `keepdims`.

If `keepdims = 1`, the output tensor keeps the same rank as $X$, and the reduced dimension is replaced by $1$.

If `keepdims = 0`, the reduced dimension is removed from the output tensor.

---

### Example 1: 1D tensor

Let:

$$
X =
\begin{bmatrix}
1 & 5 & 3 & 2
\end{bmatrix}
$$

with:

$$
axis = 0
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum value is $5$.

It is located at index $1$.

Therefore:

$$
Y =
\begin{bmatrix}
1
\end{bmatrix}
$$

The shape of $X$ is $(4)$.

The shape of $Y$ is $(1)$.

---

### Example 2: 2D tensor with `axis = 0`

Let:

$$
X =
\begin{bmatrix}
1 & 9 & 3 \
4 & 2 & 6
\end{bmatrix}
$$

with:

$$
axis = 0
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum is computed column by column.

For column $0$:

$$
\max(1,4)=4
$$

The selected index is $1$.

For column $1$:

$$
\max(9,2)=9
$$

The selected index is $0$.

For column $2$:

$$
\max(3,6)=6
$$

The selected index is $1$.

Therefore:

$$
Y =
\begin{bmatrix}
1 & 0 & 1
\end{bmatrix}
$$

The shape of $X$ is $(2,3)$.

The shape of $Y$ is $(1,3)$.

---

### Example 3: 2D tensor with `axis = 1`

Let:

$$
X =
\begin{bmatrix}
1 & 9 & 3 \
4 & 2 & 6
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum is computed row by row.

For row $0$:

$$
\max(1,9,3)=9
$$

The selected index is $1$.

For row $1$:

$$
\max(4,2,6)=6
$$

The selected index is $2$.

Therefore:

$$
Y =
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

The shape of $X$ is $(2,3)$.

The shape of $Y$ is $(2,1)$.

---

### Example 4: `keepdims = 0`

Let:

$$
X =
\begin{bmatrix}
1 & 9 & 3 \
4 & 2 & 6
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 0
$$

$$
select_last_index = 0
$$

The maximum is computed row by row.

The reduced dimension is removed.

Therefore:

$$
Y =
\begin{bmatrix}
1 & 2
\end{bmatrix}
$$

The shape of $X$ is $(2,3)$.

The shape of $Y$ is $(2)$.

---

### Example 5: repeated maximum with first index selected

Let:

$$
X =
\begin{bmatrix}
1 & 5 & 5 & 2
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum value is $5$.

It appears at indices $1$ and $2$ along the reduced axis.

Since `select_last_index = 0`, the first occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
1
\end{bmatrix}
$$

---

### Example 6: repeated maximum with last index selected

Let:

$$
X =
\begin{bmatrix}
1 & 5 & 5 & 2
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 1
$$

The maximum value is $5$.

It appears at indices $1$ and $2$ along the reduced axis.

Since `select_last_index = 1`, the last occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
2
\end{bmatrix}
$$

---

### Example 7: 3D tensor

Let:

$$
X =
\begin{bmatrix}
\begin{bmatrix}
1 & 3 & 2 \
4 & 0 & 6
\end{bmatrix}
\
\begin{bmatrix}
7 & 5 & 9 \
2 & 8 & 1
\end{bmatrix}
\end{bmatrix}
$$

The shape of $X$ is:

$$
shape(X) = (2,2,3)
$$

with:

$$
axis = 2
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum is computed along the last dimension.

For the first inner matrix:

$$
\begin{bmatrix}
1 & 3 & 2 \
4 & 0 & 6
\end{bmatrix}
$$

the selected indices are:

$$
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

For the second inner matrix:

$$
\begin{bmatrix}
7 & 5 & 9 \
2 & 8 & 1
\end{bmatrix}
$$

the selected indices are:

$$
\begin{bmatrix}
2 \
1
\end{bmatrix}
$$

Therefore:

$$
Y =
\begin{bmatrix}
\begin{bmatrix}
1 \
2
\end{bmatrix}
\
\begin{bmatrix}
2 \
1
\end{bmatrix}
\end{bmatrix}
$$

The shape of $Y$ is:

$$
shape(Y) = (2,2,1)
$$

---

## Error conditions

The operator is undefined if one of the following conditions holds:

* `axis < 0`
* `axis >= r`, where $r$ is the rank of $X$
* $dX_{\mathrm{axis}} = 0$
* `keepdims` is not equal to `0` or `1`
* `select_last_index` is not equal to `0` or `1`

## Attributes

### `axis`: int

Specifies the dimension along which the maximum index is computed.

#### Constraints

* `[C1]` Value domain

  * Statement: `axis >= 0`. `[R4]`

* `[C2]` Consistency with tensor rank

  * Statement: `axis < r`, where $r$ is the rank of $X$.

### `keepdims`: int

Specifies whether the reduced dimension is kept in the output tensor.

If `keepdims = 1`, the reduced dimension is kept with size $1$.

If `keepdims = 0`, the reduced dimension is removed.

#### Constraints

* `[C1]` Value domain

  * Statement: `keepdims` must be equal to `0` or `1`.

### `select_last_index`: int

Specifies how ties are resolved when the maximum value appears more than once along the reduced axis.

If `select_last_index = 0`, the first index of the maximum value is selected.

If `select_last_index = 1`, the last index of the maximum value is selected.

#### Constraints

* `[C1]` Value domain

  * Statement: `select_last_index` must be equal to `0` or `1`.

## Inputs

### $\text{X}$: real tensor

Input tensor.

#### Constraints

* `[C1]` <a id="C1rx"></a> Axis consistency

  * Statement: The rank $r$ of $X$ shall satisfy `axis < r`.

* `[C2]` <a id="C2rx"></a> Non-empty reduced dimension

  * Statement: The dimension of $X$ along `axis` shall be strictly positive.

## Outputs

### $\text{Y}$: int64 tensor

Output tensor containing the indices of the maximum values of $X$ along `axis`.

#### Constraints

* `[C1]` <a id="C1ry"></a> Output type

  * Statement: $Y$ shall have type `int64`.

* `[C2]` <a id="C2ry"></a> Output shape consistency

  * Statement: If `keepdims = 1`, the shape of $Y$ shall be equal to the shape of $X$, except that the dimension `axis` shall be replaced by $1$.

  * Statement: If `keepdims = 0`, the shape of $Y$ shall be equal to the shape of $X$ with the dimension `axis` removed.

* `[C3]` <a id="C3ry"></a> Output value range

  * Statement: For every output index $k$:

$$
0 \leq Y[k] < dX_{\mathrm{axis}}
$$

<a id="float"></a>

# **ArgMax** (float)

where float is in {float16, float, double}.

## Signature

$Y = \textbf{ArgMax}(X)$

where:

* $X$: floating-point input tensor
* $Y$: int64 output tensor containing the indices of the maximum values of $X$ along a given axis

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

See [Restrictions](#real).

---

## Informal specification

The **ArgMax** operator computes the index of the maximum floating-point value of the input tensor $X$ along a specified axis according to IEEE 754 floating-point semantics.

The output tensor contains integer indices and not floating-point values.

For finite values, the behavior is the same as for real numbers.

For every output position $k$, all indices of $X$ are fixed except the index along the `axis` dimension.

This varying index is denoted by $j$.

It satisfies:

$$
0 \leq j < dX_{\mathrm{axis}}
$$

For a fixed output position $k$, let:

$$
S_k(j)
$$

denote the value of $X$ at the same fixed coordinates as $k$, with the coordinate $j$ inserted along the `axis` dimension.

If the reduced slice contains no `NaN`, then:

* `+inf` is greater than all finite values.
* Finite values are ordered according to the usual floating-point order.
* `-inf` is smaller than all finite values.
* If the maximum appears several times, the selected index depends on `select_last_index`.

If the reduced slice contains one or more `NaN` values, the result is defined deterministically as follows:

* if `select_last_index = 0`, the index of the first `NaN` along the reduced axis is returned;
* if `select_last_index = 1`, the index of the last `NaN` along the reduced axis is returned.

This convention gives priority to `NaN` values over finite and infinite values in the reduced slice.

If the reduced slice contains at least one `NaN`, then `NaN` values have priority over all other values.

If `select_last_index = 0`, the selected output value is the first index of a `NaN` value along the reduced axis.

In other words, $Y[k]$ is the smallest index $j$ such that:

$$
S_k(j) = \text{NaN}
$$

If `select_last_index = 1`, the selected output value is the last index of a `NaN` value along the reduced axis.

In other words, $Y[k]$ is the greatest index $j$ such that:

$$
S_k(j) = \text{NaN}
$$

If the reduced slice contains no `NaN`, then the maximum value is computed normally.

Let:

$$
M_k =
\max_{0 \leq j < dX_{\mathrm{axis}}}
S_k(j)
$$

If `select_last_index = 0`, the selected output value is the first index where the maximum value is reached.

In other words, $Y[k]$ is the smallest index $j$ such that:

$$
S_k(j) = M_k
$$

If `select_last_index = 1`, the selected output value is the last index where the maximum value is reached.

In other words, $Y[k]$ is the greatest index $j$ such that:

$$
S_k(j) = M_k
$$

The output shape is defined in the same way as in [ArgMax (real)](#real).

---

### Example 1: finite floating-point values

Let:

$$
X =
\begin{bmatrix}
1.0 & 9.5 & 3.0 \
4.0 & 2.0 & 6.5
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum is computed row by row.

Therefore:

$$
Y =
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

---

### Example 2: `+inf`

Let:

$$
X =
\begin{bmatrix}
1.0 & +\inf & 3.0 \
4.0 & 2.0 & 6.5
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

For the first row, `+inf` is the maximum value, located at index $1$.

For the second row, $6.5$ is the maximum value, located at index $2$.

Therefore:

$$
Y =
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

---

### Example 3: `-inf`

Let:

$$
X =
\begin{bmatrix}
-\inf & -4.0 & -2.0 \
-\inf & -\inf & -\inf
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

For the first row, $-2.0$ is the maximum value, located at index $2$.

For the second row, all values are equal to $-\inf$.

Since `select_last_index = 0`, the first occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
2 \
0
\end{bmatrix}
$$

---

### Example 4: `NaN` with first index selected

Let:

$$
X =
\begin{bmatrix}
1.0 & \text{NaN} & 3.0 \
4.0 & 2.0 & 6.5
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The first row contains `NaN` at index $1$.

Since `select_last_index = 0`, the first `NaN` index is selected.

The second row contains no `NaN`, so the maximum value $6.5$ is selected.

Therefore:

$$
Y =
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

---

### Example 5: `NaN` with last index selected

Let:

$$
X =
\begin{bmatrix}
\text{NaN} & 1.0 & \text{NaN} & 3.0
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 1
$$

The row contains two `NaN` values at indices $0$ and $2$.

Since `select_last_index = 1`, the last `NaN` index is selected.

Therefore:

$$
Y =
\begin{bmatrix}
2
\end{bmatrix}
$$

---

### Example 6: repeated maximum with floating-point values

Let:

$$
X =
\begin{bmatrix}
1.0 & 7.0 & 7.0 & 2.0
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum value is $7.0$.

It appears at indices $1$ and $2$.

Since `select_last_index = 0`, the first occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
1
\end{bmatrix}
$$

With the same input and:

$$
select_last_index = 1
$$

the last occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
2
\end{bmatrix}
$$

---

## Error conditions

The operator is undefined if one of the following conditions holds:

* `axis < 0`
* `axis >= r`, where $r$ is the rank of $X$
* $dX_{\mathrm{axis}} = 0$
* `keepdims` is not equal to `0` or `1`
* `select_last_index` is not equal to `0` or `1`

The operator does not return `NaN`, because the output tensor contains integer indices.

## Attributes

### `axis`: int

See [ArgMax (real)](#real).

### `keepdims`: int

See [ArgMax (real)](#real).

### `select_last_index`: int

See [ArgMax (real)](#real).

## Inputs

### $\text{X}$: floating-point tensor

Input tensor.

#### Constraints

* `[C1]` <a id="C1fx"></a> Axis consistency

  * Statement: The rank $r$ of $X$ shall satisfy `axis < r`.

* `[C2]` <a id="C2fx"></a> Non-empty reduced dimension

  * Statement: The dimension of $X$ along `axis` shall be strictly positive.

## Outputs

### $\text{Y}$: int64 tensor

Output tensor containing the indices of the maximum values of $X$ along `axis`.

#### Constraints

* `[C1]` <a id="C1fy"></a> Output type

  * Statement: $Y$ shall have type `int64`.

* `[C2]` <a id="C2fy"></a> Output shape consistency

  * Statement: See constraint [C2](#C2ry) on tensor $Y$ in [ArgMax (real)](#real).

* `[C3]` <a id="C3fy"></a> Output value range

  * Statement: See constraint [C3](#C3ry) on tensor $Y$ in [ArgMax (real)](#real).

## Numeric accuracy

No numeric accuracy note is required for the output, since **ArgMax** returns integer indices.

The only floating-point aspects concern value comparison along the reduced axis, including the handling of `NaN`, `+inf`, and `-inf`.

<a id="integer"></a>

# **ArgMax** (integer)

where integer is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature

$Y = \textbf{ArgMax}(X)$

where:

* $X$: integer input tensor
* $Y$: int64 output tensor containing the indices of the maximum values of $X$ along a given axis

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

See [Restrictions](#real).

---

## Informal specification

The **ArgMax** operator computes the index of the maximum integer value of the input tensor $X$ along a specified axis.

For every output position $k$, all indices of $X$ are fixed except the index along the `axis` dimension.

This varying index is denoted by $j$.

It satisfies:

$$
0 \leq j < dX_{\mathrm{axis}}
$$

For a fixed output position $k$, let:

$$
S_k(j)
$$

denote the value of $X$ at the same fixed coordinates as $k$, with the coordinate $j$ inserted along the `axis` dimension.

The maximum value of this slice is:

$$
M_k =
\max_{0 \leq j < dX_{\mathrm{axis}}}
S_k(j)
$$

If `select_last_index = 0`, the first occurrence of the maximum value is selected.

In other words, $Y[k]$ is the smallest index $j$ such that:

$$
S_k(j) = M_k
$$

If `select_last_index = 1`, the last occurrence of the maximum value is selected.

In other words, $Y[k]$ is the greatest index $j$ such that:

$$
S_k(j) = M_k
$$

The output tensor contains integer indices of type `int64`.

The output shape is defined in the same way as in [ArgMax (real)](#real).

---

### Example 1: integer tensor

Let:

$$
X =
\begin{bmatrix}
1 & 9 & 3 \
4 & 2 & 6
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum is computed row by row.

Therefore:

$$
Y =
\begin{bmatrix}
1 \
2
\end{bmatrix}
$$

---

### Example 2: repeated maximum

Let:

$$
X =
\begin{bmatrix}
2 & 8 & 8 & 1
\end{bmatrix}
$$

with:

$$
axis = 1
$$

$$
keepdims = 1
$$

$$
select_last_index = 0
$$

The maximum value is $8$.

It appears at indices $1$ and $2$.

Since `select_last_index = 0`, the first occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
1
\end{bmatrix}
$$

With the same input and:

$$
select_last_index = 1
$$

the last occurrence is selected.

Therefore:

$$
Y =
\begin{bmatrix}
2
\end{bmatrix}
$$

---

## Error conditions

The operator is undefined if one of the following conditions holds:

* `axis < 0`
* `axis >= r`, where $r$ is the rank of $X$
* $dX_{\mathrm{axis}} = 0$
* `keepdims` is not equal to `0` or `1`
* `select_last_index` is not equal to `0` or `1`

## Attributes

### `axis`: int

See [ArgMax (real)](#real).

### `keepdims`: int

See [ArgMax (real)](#real).

### `select_last_index`: int

See [ArgMax (real)](#real).

## Inputs

### $\text{X}$: integer tensor

Input tensor.

#### Constraints

* `[C1]` <a id="C1ix"></a> Axis consistency

  * Statement: The rank $r$ of $X$ shall satisfy `axis < r`.

* `[C2]` <a id="C2ix"></a> Non-empty reduced dimension

  * Statement: The dimension of $X$ along `axis` shall be strictly positive.

## Outputs

### $\text{Y}$: int64 tensor

Output tensor containing the indices of the maximum values of $X$ along `axis`.

#### Constraints

* `[C1]` <a id="C1iy"></a> Output type

  * Statement: $Y$ shall have type `int64`.

* `[C2]` <a id="C2iy"></a> Output shape consistency

  * Statement: See constraint [C2](#C2ry) on tensor $Y$ in [ArgMax (real)](#real).

* `[C3]` <a id="C3iy"></a> Output value range

  * Statement: See constraint [C3](#C3ry) on tensor $Y$ in [ArgMax (real)](#real).

## Numeric accuracy

No numeric accuracy note is required, since **ArgMax** returns integer indices.
