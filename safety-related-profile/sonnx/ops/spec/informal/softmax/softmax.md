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

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a> | `axis` $\ge 0$   | Transient |
---

## Informal specification
[t1]

The **Softmax** operator computes the normalized exponential function along a specified axis of the input tensor.

Let $r$ be the rank of $X$ and let $\textit{axis}$ be the attribute specifying the dimension along which the normalization is performed.

For any [tensor index](./../common/definitions.md#tensor_index)
$i = (i_0, \dots, i_{r-1})$:


> Rajouter la formulation avec le "-M".


$$
Y[i] =
\frac{e^{X[i]}}
{\sum_{j_{axis}=0}^{dX_{axis}-1}
e^{X[i_0,\dots,j_{axis},\dots,i_{r-1}]}}
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

with `axis = 0`.

Then:

```math
Y = \textbf{Softmax}(X)
=
\begin{bmatrix}
\frac{e^{9.5}}{e^{9.5}+e^{35.7}} &
\frac{e^{35.7}}{e^{9.5}+e^{35.7}}
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

  - Statement: `axis` ≥ 0. `[R4]`

- `[C2]` Consistency with tensor rank

  - Statement: `axis` < r, where $r$ is the rank of $X$.



## Inputs

### $\text{X}$: real

Input tensor.

#### Constraints

- `[C1]` <a id="C1ra"></a> Shape consistency

  - Statement: $X$ and $Y$ shall have the same shape.

- `[C2]` <a id="C2ra"></a> Consistency with `axis`

  - Statement: The rank $r$ of $X$ shall satisfy `axis` < r.

## Outputs

### $\text{Y}$: real

Softmax of tensor $X$.

#### Constraints

- `[C1]` Shape consistency

  - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

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
[t1]

The **Softmax** operator computes the normalized exponential along the specified axis according to IEEE 754 floating-point semantics.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \text{Softmax}(X[i]) =
\begin{cases}
\\
\\
\\
\text{NaN}, &
\begin{aligned}
&\text{if } \exists j_{axis} :  X[i_0,\dots,j_{axis},\dots,i_{r-1}] \in \text{ \{NaN, +inf\} }
\end{aligned}
\\
\\
\\
0, &
\begin{aligned}
&\text{if } X[i]=-\inf \\
&\land \text{if } \nexists j_{axis} :  X[i_0,\dots,j_{axis},\dots,i_{r-1}] \in \text{ \{NaN, +inf\} }
\end{aligned}
\\
\\
\\
\dfrac{e^{X[i]-M}}{\sum_{j_{axis}=0}^{dX_{axis}-1} e^{X[i_0,\dots,j_{axis},\dots,i_{r-1}]-M}} &
\begin{aligned}
& \text{with}~M = \max_{j_{axis}=0}^{dX_{axis}-1} X[i_0,\dots,j_{axis},\dots,i_{r-1}], \text{ otherwise}
\end{aligned}
\end{cases}
$$

[/t1]


> Normalization using $M$ prevents large values for the exponential. 

---

### Example 1

```math
X = \begin{bmatrix} 9.5 & 35.7 \end{bmatrix}
```

```math
Y \approx \begin{bmatrix} 4.182965147 \times 10^{-12} & 0.9999999999958 \end{bmatrix}
```


### Example 2a

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
```

with `axis = 0`.

```math
Y \approx
\begin{bmatrix}
\frac{e^{1-4}}{e^{1-4}+e^{4-4}}=0.04742587 & \frac{e^{2-5}}{e^{2-5}+e^{5-5}}=0.04742587 & \frac{e^{3-6}}{e^{3-6}+e^{6-6}}=0.04742587 \\
\frac{e^{4-4}}{e^{1-4}+e^{4-4}}=0.95257413 & \frac{e^{5-5}}{e^{2-5}+e^{5-5}}=0.95257413 & \frac{e^{6-6}}{e^{3-6}+e^{6-6}}=0.95257413
\end{bmatrix}
```
### Example 2b


```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
```

with `axis = 1`.

```math
Y \approx
\begin{bmatrix}
\frac{e^{1-3}}{e^{1-3}+e^{2-3}+e^{3-3}}=0.09003057 & \frac{e^{2-3}}{e^{1-3}+e^{2-3}+e^{3-3}}=0.24472848 & \frac{e^{3-3}}{e^{1-3}+e^{2-3}+e^{3-3}}=0.66524094 \\
\frac{e^{4-6}}{e^{4-6}+e^{5-6}+e^{6-6}}=0.09003057 & \frac{e^{5-6}}{e^{4-6}+e^{5-6}+e^{6-6}}=0.24472848 & \frac{e^{6-6}}{e^{4-6}+e^{5-6}+e^{6-6}}=0.66524094
\end{bmatrix}
```


### Example with special value :

### Case `+inf`

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & +\inf
\end{bmatrix}
```


```math
Y_{\text{axis=0}} \approx
\begin{bmatrix}
0.04742587 & 0.04742587 & \text{NaN} \\
0.95257413 & 0.95257413 & \text{NaN}
\end{bmatrix}
```

```math
Y_{\text{axis=1}} \approx
\begin{bmatrix}
0.09003057 & 0.24472848 & 0.66524094 \\
\text{NaN} & \text{NaN} & \text{NaN}
\end{bmatrix}
```

### Case `-inf`

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & -\text{inf}
\end{bmatrix}
```


```math
Y_{\text{axis=0}} \approx
\begin{bmatrix}
0.04742587 & 0.04742587 & 1.0 \\
0.95257413 & 0.95257413 & 0.0
\end{bmatrix}
```

```math
Y_{\text{axis=1}} \approx
\begin{bmatrix}
0.09003057 & 0.24472848 & 0.66524094 \\
0.26894143 & 0.73105860 & 0.0
\end{bmatrix}
```

### Case `NaN`

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & \text{NaN}
\end{bmatrix}
```

```math
Y_{\text{axis=0}} \approx
\begin{bmatrix}
0.04742587 & 0.04742587 & \text{NaN} \\
0.95257413 & 0.95257413 & \text{NaN}
\end{bmatrix}
```

```math
Y_{\text{axis=1}} \approx
\begin{bmatrix}
0.09003057 & 0.24472848 & 0.66524094 \\
\text{NaN} & \text{NaN} & \text{NaN}
\end{bmatrix}
```


---

### Example: 3D tensor 2x2x3, softmax along axis=2 (last axis)

```math
X =
\begin{bmatrix}
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \\
\begin{bmatrix} 10 & 20 & 30 \\ 40 & 50 & 60 \end{bmatrix}
\end{bmatrix}
```

- Shape: `(2,2,3)`

```math
Y \approx
\begin{bmatrix}
\begin{bmatrix}
0.09003 & 0.24473 & 0.66524 \\
0.09003 & 0.24473 & 0.66524
\end{bmatrix} \\
\begin{bmatrix}
2.061 \cdot 10^{-9} & 4.539 \cdot 10^{-5} & 0.99995 \\
2.061 \cdot 10^{-9} & 4.539 \cdot 10^{-5} & 0.99995
\end{bmatrix}
\end{bmatrix}
```





## Error conditions

No error condition.

Division by zero cannot occur because the denominator is strictly positive unless all exponentials underflow to zero, in which case IEEE 754 rules apply.



## Attributes

### `axis`: int

See [Softmax (real)](#real).

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
