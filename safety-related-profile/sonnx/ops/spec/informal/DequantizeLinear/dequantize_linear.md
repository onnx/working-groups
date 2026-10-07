# Contents

- **DequantizeLinear** operator for types [int32, float](#int32-float)

Based on ONNX documentation [DequantizeLinear version 28](https://onnx.ai/onnx/operators/onnx__DequantizeLinear.html).


<a id="int32-float"></a>
# **DequantizeLinear** (int32, float)

## Signature

$Y = \textbf{DequantizeLinear}(X, x\_scale, x\_zero\_point)$

where:
- $X$: quantized input tensor, of type int32
- $x\_scale$: scale of the dequantization, a scalar of type float
- $x\_zero\_point$: zero point of the dequantization, a scalar of type int32
- $Y$: the dequantized tensor, of type float

<span style="font-size:0.7em;">[info]</br></span>
For int32 inputs, $x\_zero\_point$ is usually left at its default value $0$ (in the common case of a symmetrically-quantized int32 tensor, no zero point is needed). This specification nevertheless defines the operator for any value of $x\_zero\_point$, since the ONNX formula is the same in every case.
<span style="font-size:0.7em;">[/info]</br></span>

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **DequantizeLinear** operator, in this specification:

| Restriction | Statement                                                                                                                                 | Origin    |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| `[R1]` <a id="R1"></a> | Attribute `axis` is restricted to its default value. Since $x\_scale$ and $x\_zero\_point$ are scalars, only per-tensor dequantization is specified; `axis` has no effect. | Transient |
| `[R2]` <a id="R2"></a> | Attribute `block_size` is restricted to its default value `0`. Blocked dequantization is not specified.                                        | Transient |
| `[R3]` <a id="R3"></a> | Attribute `output_dtype` is restricted to its default value. The output type is then determined by the type of $x\_scale$, i.e., float.          | Transient |

## Function

<span style="background: red; color: white; font-size:0.7em;">[E_DEQUANTIZELINEAR_FLOAT_FUNC_0010]</br></span>
Operator **DequantizeLinear** linearly dequantizes the int32 tensor $X$ into the float tensor $Y$, using scale $x\_scale$ and zero point $x\_zero\_point$, and stores the result in $Y$. If $i$ is a [tensor index](./../common/definitions.md#tensor_index), each element $Y[i]$ is computed as follows.

The mathematical definition of the operator is given hereafter.

For any [tensor index](./../common/definitions.md#tensor_index) $i$:

$$
Y[i] = \big(\text{float}(X[i] -_{(\text{i32})} x\_zero\_point)\big) \cdot x\_scale
$$

where
- $-_{(\text{i32})}$ is the subtraction of 32-bit signed integers, i.e., $X[i]$ and $x\_zero\_point$ are subtracted as int32 values (see the Error conditions section below for the case where this subtraction overflows),
- $\text{float}(\cdot)$ converts (casts) the resulting int32 value into a float value,
- $\cdot$ is the IEEE 754 floating-point multiplication.

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

The effect of the operator is illustrated on the following examples.

### Example 1

```math
X = \begin{bmatrix} 0 & 10 & 50 & 100 & 128 & 255 \end{bmatrix}
\quad
x\_scale = 0.02
\quad
x\_zero\_point = 128
```

```math
Y \approx \begin{bmatrix} -2.56 & -2.36 & -1.56 & -0.56 & 0.0 & 2.54 \end{bmatrix}
```

### Example 2 (int32 overflow of the subtraction)

```math
X = \begin{bmatrix} -2147483648 & 2147483647 \end{bmatrix}
\quad
x\_scale = 1.0
\quad
x\_zero\_point = 100
```

```math
Y = \begin{bmatrix} 2147483548 & -2147483749 \end{bmatrix}
```

Here $X[1] -_{(\text{i32})} x\_zero\_point = 2147483647 - 100$, whose exact mathematical value ($2147483547$) is representable in int32 and does not overflow, so $Y[1] = 2147483547.0$. In contrast, $X[0] -_{(\text{i32})} x\_zero\_point = -2147483648 - 100$ is not representable as an int32 value: its exact mathematical value ($-2147483748$) is below the int32 minimum ($-2147483648$), so the subtraction wraps around, giving $2147483548$, and $Y[0] = 2147483548.0$.

## Error conditions
- If the exact mathematical value of $X[i] - x\_zero\_point$ is not representable as an int32 value (i.e., is outside $[-2147483648,\ 2147483647]$), the int32 subtraction wraps around (two's complement arithmetic), producing an unexpected result (see Example 2 above). This is an overflow condition, as discussed in the general guidelines on error conditions for integer computations.
- $x\_scale$ or the wrapped difference may be such that the floating-point multiplication overflows, producing $\pm\text{inf}$ in $Y[i]$.

## Attributes

### `axis`: int
Default value: `1`.

(Only used for per-axis and blocked dequantization, see restriction [<b><span style="font-family: 'Courier New', monospace">R1</span></b>](#R1).)

#### Constraints
- `[C1]` <a id="C1axis"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R1</span></b>](#R1).

### `block_size`: int
Default value: `0`.

(Only used for blocked dequantization, see restriction [<b><span style="font-family: 'Courier New', monospace">R2</span></b>](#R2).)

#### Constraints
- `[C1]` <a id="C1blocksize"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R2</span></b>](#R2).

### `output_dtype`: int
Default value: `0` (unspecified; the output type is then inferred from the type of $x\_scale$, i.e., float).

#### Constraints
- `[C1]` <a id="C1outputdtype"></a> Restricted to default value
  - Statement: see restriction [<b><span style="font-family: 'Courier New', monospace">R3</span></b>](#R3).

## Inputs

### $\text{X}$: int32 tensor

Quantized input tensor to be dequantized.

#### Constraints
<a id="E_DEQUANTIZELINEAR_FLOAT_CONSTR_X_0010"></a>
- `[E_DEQUANTIZELINEAR_FLOAT_CONSTR_X_0010]` Shape consistency
  - Statement: Tensors $X$ and $Y$ shall have the same shape.

### $\text{x\_scale}$: float scalar

Scale factor used to dequantize $X$.

### $\text{x\_zero\_point}$: int32 scalar

Zero point used to dequantize $X$. Must have the same type as $X$ (int32).

## Outputs

### $\text{Y}$: float tensor

Tensor $Y$ is the full-precision (dequantized) value of $X$, with scale $x\_scale$ and zero point $x\_zero\_point$.

#### Constraints

- `[E_DEQUANTIZELINEAR_FLOAT_CONSTR_Y_0010]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">E_DEQUANTIZELINEAR_FLOAT_CONSTR_X_0010</span></b>](#E_DEQUANTIZELINEAR_FLOAT_CONSTR_X_0010) on tensor $X$.
