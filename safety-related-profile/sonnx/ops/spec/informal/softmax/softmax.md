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
Y[i] = \text{Softmax}(X[i]) =
\begin{cases}
\\
\\
\\
\text{NaN}, &
\begin{aligned}
&\text{if } \exists j \text{ along axis: } X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}] \in \text{ \{NaN, +inf\} }
\end{aligned}
\\
\\
\\
0, &
\begin{aligned}
&\text{if } X[i]=-\inf \\
&\land \text{if } \nexists j \text{ along axis: } X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}] \in  \text{\{NaN, +inf\} }
\end{aligned}
\\
\\
\\
\dfrac{e^{X[i]-M}}{\sum_{j=0}^{dX_{axis}-1} e^{X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]-M}}, &
\begin{aligned}
&\text{otherwise, with } M = \max_{j=0}^{dX_{axis}-1} X[i_0,\dots,i_{axis-1},j,i_{axis+1},\dots,i_{r-1}]
\end{aligned}
\end{cases}
$$

---


NOTE : With a dimension >=2 the tensor is flatten in 2D matrix in the direction of the axis, then softmax is applyon this 2D matrix, then the matrix is deflatten at it original dimension 



Let ($X \in \mathbb{R}^{a_0 \times a_1 \times \dots \times a_{n-1}}$) be an n-dimensional tensor and let (k) be the axis chosen for softmax. Define:

- Flattened rows: ($L = a_0 \cdot a_1 \cdot \dots \cdot a_{k-1}$)
- Flattened columns: ($C = a_k \cdot a_{k+1} \cdot \dots \cdot a_{n-1}$)

Then we have a **temporary 2D matrix** ($X_{\text{flat}} \in \mathbb{R}^{L \times C}$), on which softmax is applied **row by row**.

The softmax formula becomes:

$$
Y[i] = \text{Softmax}(X[i]) =
\begin{cases}
\text{NaN}, &
\exists j \in {0, \dots, C-1} : X_{\text{flat}}[\ell, j] \in \text{\{NaN, +inf\}} \\
0, &
X_{\text{flat}}[\ell,j_i] = -\inf \land \nexists j \in {0, \dots, C-1} : X_{\text{flat}}[\ell, j] \in \text{\{NaN, +inf\}}  \\
\dfrac{e^{X_{\text{flat}}[\ell,j_i] - M_\ell}}{\sum_{j=0}^{C-1} e^{X_{\text{flat}}[\ell,j] - M_\ell}}, &
\text{otherwise, with } M_\ell = \max_{j=0}^{C-1} X_{\text{flat}}[\ell,j]
\end{cases}
$$

where:

- ($\ell \in {0, \dots, L-1}$) is the **flattened row index** corresponding to the combination ($[i_0, \dots, i_{k-1}]$)
- ($j_i$) corresponds to the position of ($[i_k, \dots, i_{n-1}]$) in the flattened row

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
0.04742587 & 0.04742587 & NaN \\
0.95257413 & 0.95257413 & NaN
\end{bmatrix}
```

```math
Y_{\text{axis=1}} \approx
\begin{bmatrix}
0.09003057 & 0.24472848 & 0.66524094 \\
NaN & NaN & NaN
\end{bmatrix}
```




### Case `-inf`

```math
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & -\infty
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
4 & 5 & NaN
\end{bmatrix}
```

```math
Y_{\text{axis=0}} \approx
\begin{bmatrix}
0.04742587 & 0.04742587 & NaN \\
0.95257413 & 0.95257413 & NaN
\end{bmatrix}
```

```math
Y_{\text{axis=1}} \approx
\begin{bmatrix}
0.09003057 & 0.24472848 & 0.66524094 \\
NaN & NaN & NaN
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
- Axis = 2 (columns of each submatrix)



#### Step 1: flatten along the axis

Flatten everything **before axis 2** into rows:

* Rows (L = 2*2 = 4)
* Columns (C = 3)

```math
X_{\text{flat}} =
\begin{bmatrix}
1 & 2 & 3 \\      % batch0, row0
4 & 5 & 6 \\      % batch0, row1
10 & 20 & 30 \\   % batch1, row0
40 & 50 & 60      % batch1, row1
\end{bmatrix}
```



#### Step 2: apply softmax **row by row**

1. Row `[1,2,3]` → max = 3

$$
\text{softmax} =
\left[\frac{e^{1-3}}{e^{1-3}+e^{2-3}+e^{3-3}}, \frac{e^{2-3}}{...}, \frac{e^{3-3}}{...}\right]
\approx [0.09003, 0.24473, 0.66524]
$$

2. Row `[4,5,6]` → max = 6

$$
\text{softmax} \approx [0.09003, 0.24473, 0.66524]
$$

3. Row `[10,20,30]` → max = 30

$$
e^{10-30} \approx 2.061 \cdot 10^{-9},\quad e^{20-30} \approx 4.539 \cdot 10^{-5},\quad e^{30-30}=1
$$

$$
\text{softmax} \approx [2.061e-9, 4.539e-5, 0.99995]
$$

4. Row `[40,50,60]` → max = 60

$$
\text{softmax} \approx [2.061e-9, 4.539e-5, 0.99995]
$$

---

#### Step 3: reshape back to original 3D shape

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
