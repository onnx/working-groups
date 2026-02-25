# Contents

- **Softmax** operator for type [real](#real)
- **Softmax** operator for types [float16, float, double](#float)

Based on ONNX documentation [Softmax version 13](https://onnx.ai/onnx/operators/onnx__Softmax.html).

<a id="real"></a>
# **Softmax** (real)

## Signature


$Y = \textbf{Softmax}(X)$

where:

- $X$: input tensor
- $Y$: output tensor



## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **Softmax** operator:

| Restriction | Statement                                       | Origin                    |
| ----------- | ----------------------------------------------- | ------------------------- |
| `[R1]`      | Sparse tensors are not supported                | General restriction       |
| `[R2]`      | The shape of tensors shall be explicit          | General restriction       |
| `[R3]`      | Attribute `axis` shall be explicitly defined    | SONNX profile restriction |
| `[R4]`      | Attribute `axis` shall be greater or equal to 0 | SONNX profile restriction |

---

## Informal specification

The **Softmax** operator computes the normalized exponential function along a specified axis of the input tensor.

Let $r$ be the rank of $X$ and let $axis$ be the attribute specifying the dimension along which the normalization is performed.

For any [tensor index](./../common/definitions.md#tensor_index)
$i = (i_0, \dots, i_{r-1})$:

$$
Y[i] =
\frac{e^{X[i]}}
{\sum_{j=0}^{dX_{axis}-1}
e^{X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]}}
$$

where:

* $dX_{axis}$ denotes the size of tensor $X$ along dimension `axis`,
* the summation is performed over the `axis` dimension only,
* all other indices remain fixed.

The operator preserves the shape of the input tensor.



### Example 1

Let:

```math
X = \begin{bmatrix} 9.5 & 35.7 \end{bmatrix}
```

with `axis = 1`.

Then:

```math
Y = \textbf{Softmax}(X)
=
\begin{bmatrix}
\frac{e^{9.5}}{e^{9.5}+e^{35.7}} &
\frac{e^{35.7}}{e^{9.5}+e^{35.7}}
\end{bmatrix}
=
\begin{bmatrix}
\frac{e^{-26.2}}{1 + e^{-26.2}} &
\frac{1}{1 + e^{-26.2}}
\end{bmatrix}
```



## Error conditions

No error condition.

Since exponentials are strictly positive, the denominator is strictly positive and division by zero cannot occur.



## Attributes

### `axis`: int

Specifies the dimension along which the **Softmax** operation is performed.

#### Constraints

- `[C1]` Value domain

  - Statement: `axis ≥ 0`. `[R4]`

- `[C2]` Consistency with tensor rank

  - Statement: `axis < r`, where $r$ is the rank of $X$.



## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

- `[C1]` <a id="C1ra"></a> Shape consistency

  - Statement: $X$ and $Y$ shall have the same shape.

- `[C2]` <a id="C2ra"></a> Axis validity

  - Statement: The rank $r$ of $X$ shall satisfy $axis < r$.



## Outputs

### $\text{Y}$: real

Softmax of tensor $X$.

#### Constraints

- `[C1]` Shape consistency

  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.


## Formal specification

See the Why3 specification.




<a id="float"></a>

# **Softmax** (float)

where float is in {float16, float, double}.


## Signature

Definition of operator $\text{Softmax}$ signature:

$Y = \textbf{Softmax}(X)$

where:

- $X$: floating-point input tensor
- $Y$: floating-point output tensor

---

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

See [Restrictions](#real).



## Informal specification

The **Softmax** operator computes the normalized exponential along the specified axis according to IEEE 754 floating-point semantics.

For numerical stability, the computation is defined as:

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] =
\frac{e^{X[i] - M}}
{\sum_{j=0}^{dX_{axis}-1}
e^{X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}] - M}}
$$

where:

$$
M =
\max_{j=0}^{dX_{axis}-1}
X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]
$$

The subtraction of $M$ improves numerical stability and does not change the mathematical result.

// With float corner case
// NOTE : to be improve and check ... not finish 

$$
Y[i] = \operatorname{Softmax}(X[i]) =
\begin{cases}
\\
\text{NaN}, &
\begin{aligned}
&\text{if } \exists j \text{ along axis: } X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}] = \text{NaN} \\
&\lor (\exists j:X=+\infty \land \exists k:X=\text{NaN}) \\
&\lor (\exists j:X=-\infty \land \exists k:X=\text{NaN})
\end{aligned}
[1em]
\\
1, &
\begin{aligned}
&\text{if } \exists j:X=+\infty \land \forall k\neq j:X\in \mathbb{R}
\end{aligned}
[1em]
\\
0, &
\begin{aligned}
&\text{if } \exists j:X\in\mathbb{R} \land \exists k:X=+\infty \\
&\lor \forall j:X=-\infty
\end{aligned}
[1em]
\\
\dfrac{e^{X[i]-M}}{\sum_{j=0}^{dX_{axis}-1} e^{X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]-M}}, &
\begin{aligned}
&\text{otherwise, with } M = \max_{j=0}^{dX_{axis}-1} X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]
\end{aligned}

\end{cases}
$$




















### Special floating-point cases

For each slice along `axis`:

- If at least one element is `+inf`, the result is:

  - 1.0 for entries equal to `+inf`
  - 0.0 for all finite entries
- If all elements are `-inf`, the result is undefined and may produce `NaN`
- If any element is `NaN`, the result for the corresponding slice is `NaN`



### Example 1

```math
X = \begin{bmatrix} 9.5 & 35.7 \end{bmatrix}
```

```math
Y \approx \begin{bmatrix} 4.21 \times 10^{-12} & 0.9999999999958 \end{bmatrix}
```


### Example 2

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
1 & 2 & 3
\end{bmatrix}
```

with `axis = 1`.

```math
Y \approx
\begin{bmatrix}
0.09003057 & 0.24472847 & 0.66524096 \\
0.09003057 & 0.24472847 & 0.66524096
\end{bmatrix}
```


## Error conditions

No error condition.

Division by zero cannot occur because the denominator is strictly positive unless all exponentials underflow to zero, in which case IEEE 754 rules apply.



## Attributes

### `axis`: int

See [Softmax(real) → Attributes](#real).



## Inputs

### $\text{X}$: floating-point tensor

Input tensor.

#### Constraints

- `[C1]` <a id="C1fx"></a> Shape consistency

  - Statement: $X$ and $Y$ shall have the same shape.

- `[C2]` <a id="C2fx"></a> Type consistency

  - Statement: $X$ and $Y$ shall have the same floating-point type.

- `[C3]` Axis validity

  - Statement: `axis < r`, where $r$ is the rank of $X$.



## Outputs

### $\text{Y}$: floating-point tensor

Softmax of tensor $X$.

#### Constraints

- `[C1]` <a id="C1fy"></a> Shape consistency

  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fx).

- `[C2]` <a id="C2fy"></a> Type consistency

  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fx).



## Numeric accuracy

[See the numeric accuracy note](./softmax_acc.md).
