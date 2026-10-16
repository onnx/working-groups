# Contents

- **QuantizeLinear** operator for types [float, uint8](#float-uint8)

Based on ONNX documentation [QuantizeLinear version 28](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html).

<a id="float-uint8"></a>
# **QuantizeLinear** (float, uint8)

## Signature

$Y = \textbf{QuantizeLinear}(X, y\_scale, y\_zero\_point)$

where:
- $X$: input tensor to be quantized, of type float
- $y\_scale$: scale of the quantization, a scalar of type float
- $y\_zero\_point$: zero point of the quantization, a scalar of type uint8
- $Y$: the quantized tensor, of type uint8

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **QuantizeLinear** operator, in this specification:

| Restriction | Statement                                                                                                                              | Origin    |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| `[R1]` <a id="R1"></a> | Attribute `axis` is restricted to its default value. Since $y\_scale$ and $y\_zero\_point$ are scalars, only per-tensor quantization is specified; `axis` has no effect. | Transient |
| `[R2]` <a id="R2"></a> | Attribute `block_size` is restricted to its default value `0`. Blocked quantization is not specified.                                    | Transient |
| `[R3]` <a id="R3"></a> | Attribute `output_dtype` is restricted to its default value. The output type is fixed to uint8, determined by the type of $y\_zero\_point$.  | Transient |
| `[R4]` <a id="R4"></a> | Attribute `precision` is restricted to its default value. The division $X[i] / y\_scale$ is performed using the type of $y\_scale$ (float). | Transient |
| `[R5]` <a id="R5"></a> | Attribute `saturate` is not applicable: it only affects quantization to float8 types.                                                      | Transient |

## Function

<span style="background: red; color: white; font-size:0.7em;">[E_QUANTIZELINEAR_UINT8_FUNC_0010]</br></span>
Operator **QuantizeLinear** linearly quantizes the floating-point tensor $X$ into the uint8 tensor $Y$, using scale $y\_scale$ and zero point $y\_zero\_point$, and stores the result in $Y$. If $i$ is a [tensor index](./../common/definitions.md#tensor_index), each element $Y[i]$ is computed as follows.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \text{clamp}\Big(\text{round}\Big(\frac{X[i]}{y\_scale}\Big) + y\_zero\_point,\ 0,\ 255\Big)
$$

where
- the division $X[i] / y\_scale$ is performed according to IEEE 754 floating-point semantics (float),
- $\text{round}$ is the round-to-nearest, ties-to-even function (the default IEEE 754 rounding mode),
- $\text{clamp}(v, lo, hi)$ saturates $v$ into the range $[lo, hi]$, i.e., $\text{clamp}(v,lo,hi) = \min(\max(v,lo),hi)$.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 6.1 & -3.5 & 130.2 \end{bmatrix}
```

```math
y\_scale = 2.0
\quad
y\_zero\_point = 10
```

```math
Y = \begin{bmatrix} 13 & 8 & 75 \end{bmatrix}
```

Here, $6.1/2.0 = 3.05$ rounds to $3$, so $Y[0] = 3+10=13$. $-3.5/2.0=-1.75$ rounds (ties-to-even) to $-2$, so $Y[1]=-2+10=8$.  $130.2/2.0=65.1$ rounds to $65$, so $Y[2]=65+10=75$.

### Example 2 (saturation)

```math
X = \begin{bmatrix} 300.0 & -50.0 \end{bmatrix}
\quad
y\_scale = 1.0
\quad
y\_zero\_point = 0
```

```math
Y \approx \begin{bmatrix} 255 & 0 \end{bmatrix}
```

Here, $300/1.0 + 0 = 300$ is saturated (clamped) to $255$, and $-50/1.0+0=-50$ is saturated to $0$.

## Error conditions
- If $y\_scale = 0$, the division $X[i]/y\_scale$ is not defined (see the constraint on $y\_scale$ below, which prevents this).
- If $X[i]$ is $\pm\text{inf}$ or $\text{NaN}$, then $X[i]/y\_scale$ is respectively $\pm\text{inf}$ or $\text{NaN}$, and the result of rounding and saturating this value is implementation-dependent.

## Attributes

### `axis`: int
Default value: `1`.

(Only used for per-axis and blocked quantization, see restriction [<b><span style="font-family: 'Courier New', monospace">R1</span></b>](#R1).)

#### Constraints
- `[C1]` <a id="C1axis"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R1</span></b>](#R1).

### `block_size`: int
Default value: `0`.

(Only used for blocked quantization, see restriction [<b><span style="font-family: 'Courier New', monospace">R2</span></b>](#R2).)

#### Constraints
- `[C1]` <a id="C1blocksize"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R2</span></b>](#R2).

### `output_dtype`: int
Default value: `0` (unspecified; the output type is then inferred from the type of $y\_zero\_point$, i.e., uint8).

#### Constraints
- `[C1]` <a id="C1outputdtype"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R3</span></b>](#R3).

### `precision`: int
Default value: unspecified (the division is performed using the type of $y\_scale$, i.e., float).

#### Constraints
- `[C1]` <a id="C1precision"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R4</span></b>](#R4).

### `saturate`: int
Default value: `1`. Not applicable, see restriction [<b><span style="font-family: 'Courier New', monospace">R5</span></b>](#R5).

## Inputs

### $\text{X}$: float tensor

Input tensor to be quantized.

#### Constraints
<a id="E_QUANTIZELINEAR_UINT8_CONSTR_X_0010"></a>
- `[E_QUANTIZELINEAR_UINT8_CONSTR_X_0010]` Shape consistency
  - Statement: Tensors $X$ and $Y$ shall have the same shape.

### $\text{y\_scale}$: float scalar

Scale factor for the quantization of $X$.

#### Constraints
<a id="E_QUANTIZELINEAR_UINT8_CONSTR_YSCALE_0010"></a>
- `[E_QUANTIZELINEAR_UINT8_CONSTR_YSCALE_0010]` Avoid undefined behaviour
  - Statement: $y\_scale \neq 0$

### $\text{y\_zero\_point}$: uint8 scalar

Zero point for the quantization of $X$. Determines the output type (uint8).

## Outputs

### $\text{Y}$: uint8 tensor

Tensor $Y$ is the linearly quantized value of $X$, with scale $y\_scale$ and zero point $y\_zero\_point$, rounded to the nearest even integer and saturated into $[0,255]$.

#### Constraints

- `[E_QUANTIZELINEAR_UINT8_CONSTR_Y_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_QUANTIZELINEAR_UINT8_CONSTR_X_0010</span></b>](#E_QUANTIZELINEAR_UINT8_CONSTR_X_0010) on tensor $X$.
- `[E_QUANTIZELINEAR_UINT8_CONSTR_Y_0020]` Value range
  - Statement: $\forall i,\ 0 \le Y[i] \le 255$
