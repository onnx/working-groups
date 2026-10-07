# Contents

- **BatchNormalization** operator for type [real](#real)
- **BatchNormalization** operator for types [float16, float, double](#float)

Based on ONNX documentation [BatchNormalization version 15](https://onnx.ai/onnx/operators/onnx__BatchNormalization.html).

<a id="real"></a>
# **BatchNormalization** (real)

## Signature
$Y = \textbf{BatchNormalization}(X, scale,B,input\_mean,input\_var)$

where:
- $X$: Input tensor to be normalized
- $scale$: per-channel scaling factor $\gamma$
- $B$: per-channel bias $\beta$
- $input\_mean$: per-channel mean used for normalization
- $input\_var$: per-channel variance used for normalization
- $Y$: normalized, scaled, and shifted output tensor

<a id="restrictions"></a> 
## Restrictions
[General restrictions](../common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **BatchNormalization** operator:
| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a> | Only inference mode is specified (training_mode = 0). Training mode is out of scope. | Transient |

<a id="Informal_spec"></a>
## Informal specification

Operator **BatchNormalization**  normalizes the input tensor $X$ along the channel axis using the pre-computed per-channel statistics $input\_mean$
and $input\_var$, then applies a per-channel affine transformation using $scale$ and bias $B$
and stores the result in output tensor $Y$.

The tensor $X$ has shape $(N, C, d_2, \ldots, d_{rX-1})$ where $N = dX_0$
is the batch size and $C = dX_1$
is the number of channels. When $X$ is a $1-D$ tensor of size $N$, the number of channels $C$ is implicitly assumed to be $1$.

The parameters $scale$, $B$,$input\_mean$, and
$input\_var$ are $1-D$ tensors of size $C$, each indexed by the channel index $c \in [0, C-1]$

For any element of the input tensor, the output is computed as follows:
$Y[n, c, d_2, \ldots] = \text{scale}[c] \cdot \frac{X[n, c, d_2, \ldots] - \text{input\_mean}[c]}{\sqrt{\text{input\_var}[c] + \varepsilon}} + B[c]$

where:
- $n \in [0,N−1]$ is the batch index
- $c \in [0, C-1]$ is the channel index
- $d_k​ \in [0,dX_k​−1]$ for $k \in [2,rX−1]$ are the spatial indices
- $\epsilon$ is the value of attribute epsilon

### Examples
 
#### Example 1
 
Single-channel 1-D input ($N=1$, $C=1$, scalar parameters):
 
```math
X = \begin{bmatrix} 2.0 & 4.0 & 6.0 \end{bmatrix}
\quad
input\_mean = \begin{bmatrix} 4.0 \end{bmatrix}
\quad
input\_var = \begin{bmatrix} 2.0 \end{bmatrix}
```
 
```math
scale = \begin{bmatrix} 1.0 \end{bmatrix}
\quad
B = \begin{bmatrix} 0.0 \end{bmatrix}
\quad
\varepsilon = 10^{-5}
```
 
```math
Y = \begin{bmatrix}
  \frac{2.0 - 4.0}{\sqrt{2.0 + 10^{-5}}} &
  \frac{4.0 - 4.0}{\sqrt{2.0 + 10^{-5}}} &
  \frac{6.0 - 4.0}{\sqrt{2.0 + 10^{-5}}}
\end{bmatrix}
\approx
\begin{bmatrix} -1.4142 & 0.0 & 1.4142 \end{bmatrix}
```
 
#### Example 2
 
Two-channel 2-D input ($N=2$, $C=2$, spatial dimension $H=2$):
 
```math
X = \begin{bmatrix}
  [[1.0,\ 2.0],\ [3.0,\ 4.0]] \\
  [[5.0,\ 6.0],\ [7.0,\ 8.0]]
\end{bmatrix}
\quad\text{(shape: } 2 \times 2 \times 2 \text{)}
```
 
```math
input\_mean = \begin{bmatrix} 2.0 \\ 6.0 \end{bmatrix}
\quad
input\_var = \begin{bmatrix} 1.0 \\ 1.0 \end{bmatrix}
\quad
scale = \begin{bmatrix} 2.0 \\ 1.0 \end{bmatrix}
\quad
B = \begin{bmatrix} 0.5 \\ -0.5 \end{bmatrix}
\quad
\varepsilon = 10^{-5}
```
 
For channel $c=0$ (mean = 2.0, var = 1.0, scale = 2.0, B = 0.5):
 
```math
Y[\cdot,0,\cdot] \approx \begin{bmatrix} -1.5 & 0.5 \\ 2.5 & 4.5 \end{bmatrix}
```
 
For channel $c=1$ (mean = 6.0, var = 1.0, scale = 1.0, B = −0.5):
 
```math
Y[\cdot,1,\cdot] \approx \begin{bmatrix} -1.5 & -0.5 \\ 0.5 & 1.5 \end{bmatrix}
```
 
 
## Error conditions
 
No error condition applies in inference mode (`training_mode = 0`). In particular, division by zero is prevented by the `epsilon` attribute, which ensures $input\_var[c] + \varepsilon > 0$ for any non-negative variance.
 
<a id="real_attributes"></a>
## Attributes
 
### `epsilon`: float
 
A small positive value added to the variance before taking the square root, to avoid division by zero.
 
Default value: $10^{-5}$
 
#### Constraints
 
- `[C1]` <a id="C1eps_r"></a> Positivity
  - Statement: `epsilon` shall be strictly positive: $\varepsilon > 0$.
### `momentum`: float
 
Factor used when computing running mean and running variance during training. This attribute is irrelevant in inference mode ([R1](#R1)) and shall be ignored.
 
Default value: $0.9$
 
#### Constraints
 
No constraint applies to `momentum` in inference mode.
 
### `training_mode`: int
 
Flag indicating whether the operator is used in training mode. Per restriction [R1](#R1), only inference mode is in scope.
 
Default value: $0$ (inference)
 
#### Constraints
 
- `[C1]` Inference mode only
  - Statement: `training_mode` shall be $0$.
## Inputs
 
### $X$: real tensor
 
Input tensor to be normalized.
 
#### Constraints
 
- `[C1]` <a id="C1X_r"></a> Shape consistency
  - Statement: Tensors $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2X_r"></a> Rank
  - Statement: $X$ shall have rank $rX \geq 1$. When $rX = 1$, the number of channels $C$ is implicitly 1.
### $scale$: real tensor
 
Per-channel scaling factor $\gamma$, applied after normalization.
 
#### Constraints
 
- `[C1]` <a id="C1sc_r"></a> Shape
  - Statement: $scale$ shall be a 1-D tensor of size $C = dX_1$ (or size 1 when $rX = 1$).
### $B$: real tensor
 
Per-channel bias $\beta$, added after scaling.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_r) on $scale$.
### $input\_mean$: real tensor
 
Per-channel estimated mean used for normalization.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_r) on $scale$.
### $input\_var$: real tensor
 
Per-channel estimated variance used for normalization.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_r) on $scale$.
- `[C2]` Non-negativity
  - Statement: $\forall c,\ input\_var[c] \geq 0$.
## Outputs
 
### $Y$: real tensor
 
Output tensor, result of the normalization and affine transformation applied to $X$.
 
#### Constraints
 
- `[C1]` Shape consistency
  - Statement: see constraint [**[C1]**](#C1X_r) on $X$.
## Formal specification
 
See the Why3 specification.
 
---

<a id="float"></a>
# **BatchNormalization** (float)
where float is in {float16, float, double}
 
## Signature
 
$Y = \textbf{BatchNormalization}(X, scale, B, input\_mean, input\_var)$
 
where:
- $X$: input floating-point tensor to be normalized
- $scale$: per-channel scaling factor $\gamma$
- $B$: per-channel bias $\beta$
- $input\_mean$: per-channel estimated mean
- $input\_var$: per-channel estimated variance
- $Y$: normalized, scaled, and shifted output tensor
## Restrictions
 
[General restrictions](../common/general_restrictions.md) are applicable.
 
The following specific restrictions apply to the **BatchNormalization** operator:
 
| Restriction | Statement | Origin |
|-------------|-----------|--------|
| `[R1]` | Only inference mode is specified (`training_mode = 0`). Training mode is out of scope. | Transient |
 
## Informal specification
 

Operator **BatchNormalization** normalizes the input floating-point tensor $X$ along the channel axis using the pre-computed per-channel statistics $input\_mean$ and $input\_var$, then applies a per-channel affine transformation using $scale$ and bias $B$, and stores the result in output tensor $Y$. Computations are performed according to IEEE 754 floating-point semantics.
 
The tensor $X$ has shape $(N, C, d_2, \ldots, d_{rX-1})$ where $N = dX_0$ is the batch size and $C = dX_1$ is the number of channels. When $X$ is a 1-D tensor of size $N$, the number of channels $C$ is implicitly assumed to be 1.
 
The parameters $scale$, $B$, $input\_mean$, and $input\_var$ are 1-D tensors of size $C$, each indexed by the channel index $c \in [0, C-1]$.
 
For any element of the input tensor, the output is computed as follows:
 
$$
Y[n, c, d_2, \ldots] = scale[c] \cdot \frac{X[n, c, d_2, \ldots] - input\_mean[c]}{\sqrt{input\_var[c] + \varepsilon}} + B[c]
$$
 
where:
- $n \in [0, N-1]$ is the batch index
- $c \in [0, C-1]$ is the channel index
- $d_k \in [0, dX_k - 1]$ for $k \in [2, rX-1]$ are the spatial indices
- $\varepsilon$ is the value of attribute `epsilon`

### Examples
 
#### Example 1
 
```math
X = \begin{bmatrix} 1.0 & 2.0 \\ 3.0 & 4.0 \end{bmatrix}
\quad
input\_mean = \begin{bmatrix} 2.0 \\ 3.0 \end{bmatrix}
\quad
input\_var = \begin{bmatrix} 1.0 \\ 1.0 \end{bmatrix}
```
 
```math
scale = \begin{bmatrix} 1.0 \\ 2.0 \end{bmatrix}
\quad
B = \begin{bmatrix} 0.0 \\ 1.0 \end{bmatrix}
\quad
\varepsilon = 10^{-5}
```
 
```math
Y \approx \begin{bmatrix} -1.0 & 1.0 \\ -3.0 & 3.0 \end{bmatrix}
\quad\text{(with B added: } \begin{bmatrix} -1.0 & 1.0 \\ -1.0 & 3.0 \end{bmatrix}\text{)}
```
 
#### Example 2
 
```math
X = \begin{bmatrix}
  3.0 & 4.5 \\
  16.0 & 1.0 \\
  25.5 & 24.25
\end{bmatrix}
\quad
input\_mean = \begin{bmatrix} 3.0 \\ 4.5 \end{bmatrix}
\quad
input\_var = \begin{bmatrix} 4.0 \\ 2.25 \end{bmatrix}
```
 
```math
scale = \begin{bmatrix} 1.0 \\ 1.0 \end{bmatrix}
\quad
B = \begin{bmatrix} 0.0 \\ 0.0 \end{bmatrix}
\quad
\varepsilon = 10^{-5}
```
 
```math
Y \approx \begin{bmatrix}
  0.0 & 0.0 \\
  6.5 & -2.333 \\
  11.25 & 13.167
\end{bmatrix}
```
 
## Error conditions
 
No error condition applies in inference mode. Division by zero is prevented by the `epsilon` attribute, which ensures the denominator $\sqrt{input\_var[c] + \varepsilon}$ is strictly positive for any non-negative variance.
 
## Attributes
 
### `epsilon`: float
 
A small positive value added to the variance before taking the square root, to avoid division by zero.
 
Default value: $10^{-5}$
 
#### Constraints
 
- `[C1]` <a id="C1eps_f"></a> Positivity
  - Statement: `epsilon` shall be strictly positive: $\varepsilon > 0$.
### `momentum`: float
 
Factor used when computing running mean and running variance during training. This attribute is irrelevant in inference mode ([R1](#R1)) and shall be ignored.
 
Default value: $0.9$
 
#### Constraints
 
No constraint applies to `momentum` in inference mode.
 
### `training_mode`: int
 
Flag indicating whether the operator is used in training mode. Only inference mode is in scope.
 
Default value: $0$ (inference)
 
#### Constraints
 
- `[C1]` Inference mode only
  - Statement: `training_mode` shall be $0$.
## Inputs
 
### $X$: floating-point tensor
 
Input tensor to be normalized.
 
#### Constraints
 
- `[C1]` <a id="C1X_f"></a> Shape consistency
  - Statement: Tensors $X$ and $Y$ shall have the same shape.
- `[C2]` <a id="C2X_f"></a> Type consistency
  - Statement: Tensors $X$ and $Y$ shall have the same type (float16, float, or double).
- `[C3]` <a id="C3X_f"></a> Rank
  - Statement: $X$ shall have rank $rX \geq 1$.
### $scale$: floating-point tensor
 
Per-channel scaling factor $\gamma$, applied after normalization.
 
#### Constraints
 
- `[C1]` <a id="C1sc_f"></a> Shape
  - Statement: $scale$ shall be a 1-D tensor of size $C = dX_1$ (or size 1 when $rX = 1$).
- `[C2]` <a id="C2sc_f"></a> Type consistency
  - Statement: $scale$ and $B$ shall have the same type (float16, float, or double).
### $B$: floating-point tensor
 
Per-channel bias $\beta$, added after scaling.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_f) on $scale$.
- `[C2]` Type consistency
  - Statement: see constraint [**[C2]**](#C2sc_f) on $scale$.
### $input\_mean$: floating-point tensor
 
Per-channel estimated mean used for normalization.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_f) on $scale$.
- `[C2]` <a id="C2mean_f"></a> Type consistency
  - Statement: $input\_mean$ and $input\_var$ shall have the same type (float16, float, or double).
### $input\_var$: floating-point tensor
 
Per-channel estimated variance used for normalization.
 
#### Constraints
 
- `[C1]` Shape
  - Statement: see constraint [**[C1]**](#C1sc_f) on $scale$.
- `[C2]` Type consistency
  - Statement: see constraint [**[C2]**](#C2mean_f) on $input\_mean$.
- `[C3]` Non-negativity
  - Statement: $\forall c,\ input\_var[c] \geq 0$.
## Outputs
 
### $Y$: floating-point tensor
 
Output tensor, result of the normalization and affine transformation applied to $X$.
 
#### Constraints
 
- `[C1]` Shape consistency
  - Statement: see constraint [**[C1]**](#C1X_f) on $X$.
- `[C2]` Type consistency
  - Statement: see constraint [**[C2]**](#C2X_f) on $X$.
## Numeric accuracy
 
[See the numeric accuracy note](./batchnorm_acc.md).
 
## Formal specification
 
See the Why3 specification.