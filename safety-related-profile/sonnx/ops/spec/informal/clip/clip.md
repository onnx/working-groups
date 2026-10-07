# Contents

- **Clip** operator for type [real](#real)
- **Clip** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)
- **Clip** operator for types [float16, float, double](#float)

Based on ONNX documentation [Clip version 13](https://onnx.ai/onnx/operators/onnx__Clip.html).

<a id="real"></a>
# **Clip** (real, real, real)

## Signature
$Y = \textbf{Clip}(X,L,M)$

where:
- $X$: Input tensor
- $L$: Minimum value (scalar)
- $M$: Maximum value (scalar)
- $Y$: Output tensor

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

## Informal specification

[t1] Operator **Clip** limit the given input within an interval.

[t1.1]
- If $L$ $\leq$ $M$:

  - $Y[i]$ = $L$ if $X[i]$ $\lt$ $L$  

  - $Y[i]$ = $M$ if $X[i]$ $\gt$ $M$  

  - $Y[i]$ = $X[i]$, otherwise.

[/t1.1]

- If $L$ $\gt$ $M$:

  - $Y[i] = M$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).

[/t1]

Note: **Clip** can also be specified as :
$$ Y[i] = \min(M, \max(X[i], L))$$


where $i$ is a [tensor index](../common/definitions.md#tensor_index).


### Example 1

```math
X = \begin{bmatrix} -6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
L = 0
\quad
M = 10
```


```math
Y = \begin{bmatrix} 0 & 9.5 & 10 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
L = 20
\quad
M = 10
```

```math
Y = \begin{bmatrix} 10 & 10 & 10 \end{bmatrix}
```

## Error conditions

If any precondition is not satisfied, the behaviour of the operator is not defined.

## Attributes

Operator **Clip** has no attribute.

## Inputs

### $X$: `real`
Tensor $X$ is the input tensor to be clipped.

### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape.
 
### $L$: `real`
Tensor $L$ is a scalar tensor giving the minimum bound for clipping.

### Constraints
  - `[C1]` Shape consistency
    - Statement: The shape of tensor $L$ must be empty.
    - Rationale: $L$ is a scalar tensor

### $M$: `real`
Tensor $M$ a scalar tensor giving the maximum bound for clipping.

### Constraints
  - `[C1]` Shape consistency
    - Statement: The shape of tensor $M$ must be empty.
    - Rationale: $M$ is a scalar tensor

## Outputs

### $Y$: `real`
Tensor $Y$ is the element-wise result of clipping $X$ by the interval $[L, M]$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.


## Numerical Accuracy

See the [Numerical accuracy specification](/clip_na.md).

<a id="int"></a>
# **Clip** (int, int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

See specification for [real numbers](#real).

<a id="float"></a>
# **Clip** (float, float, float)
where float is in {float16, float, double}

## Signature
$Y = \textbf{Clip}(X,L,M)$

where:
- $X$: Input tensor
- $L$: Minimum value (scalar)
- $M$: Maximum value (scalar)
- $Y$: Output tensor

## Restrictions
[General restrictions](../general_restrictions.md) are applicable.

## Informal specification

Operator **Clip** limit the given input within an interval.

**Clip** operation is specified as follows:

  - If $L'$ $\leq$ $M'$:

    - if $X[i]$ $\lt$ $L'$ then $Y[i]$ = $L'$.

    - If $X[i]$ $\gt$ $M'$ then $Y[i]$ = $M'$.
    - Otherwise, $Y[i]$ = $X[i]$.

  - If $L'$ $\gt$ $M'$:
    - $Y[i] = M'$

where 
- $i$ is a [tensor index](../common/definitions.md#tensor_index).
- $L'$ = -inf if $L$ is NaN otherwise $L'$ = $L$
- $M'$ = +inf if $M$ is NaN otherwise $M'$ = $M$

Note:  **Clip** **does not** behave as 
$$ Y[i] = \min(M', \max(X[i], L'))$$ 
when $L=+0$ and $M=-0$

For instance, $Y[i]=\min(-0,\max(-1.0, +0))=-0$ whereas the expected value from specification according to the IEEE754 rules for $+0$ and $-0$ comparisons is $+0$.

where $i$ is a [tensor index](../common/definitions.md#tensor_index).


### Example 1

```math
X = \begin{bmatrix} -6.3 & 9.2 & 35.5 \end{bmatrix}
```

```math
L = 0.5
\quad
M = 10.1
```

```math
Y = \begin{bmatrix} 0.5 & 9.2 & 10.1 \end{bmatrix}
```

### Example 2

```math
X = \begin{bmatrix} 6.5 & 9.2 & 35.1 \end{bmatrix}
```

```math
L = 20.2
\quad
M = 10.0
```

```math
Y = \begin{bmatrix} 10.0 & 10.0 & 10.0 \end{bmatrix}
```

### Example 3

```math
X = \begin{bmatrix} \text{-inf} & 0.0 & \text{+inf} & \text{NaN} \end{bmatrix}
```
```math
L = -1.0
\quad
M = \text{NaN}
```

```math
Y = \begin{bmatrix} -1.0 & 0.0 & \text{+inf} & \text{NaN} \end{bmatrix}
```

### Example 4

```math
X = \begin{bmatrix} \text{-inf} & 0.0 & \text{+inf} & \text{NaN} \end{bmatrix}
```
```math
L = \text{NaN}
\quad
M = \text{NaN}
```

```math
Y = \begin{bmatrix} \text{-inf} & 0.0 & \text{+inf} & \text{NaN} \end{bmatrix}
```

## Error conditions
If any pre-conditions is not satisfied, then the behavior is undefined.

## Attributes
Operator **Clip** has no attribute.

## Inputs

### $X$: `float`
Tensor $X$ is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors $X$ and $Y$ must have the same shape.
 - `[C2]` <a id="C2ia"></a> Type consistency
   - Statement: Tensors $X$, $L$, $M$ and $Y$ must have the same type.
 
### $L$: `float`
Tensor $L$ is the minimum bound for clipping.

### Constraints

- `[C1]` Shape consistency
  - Statement: The shape of tensor $L$ must be empty.
  - Rationale: $L$ is a scalar tensor.

- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $X$.


### $M$: `float`
Tensor $M$ is the maximum bound for clipping.

### Constraints

- `[C1]` Shape consistency
  - Statement: The shape of tensor $max$ must be empty.
  - Rationale: $M$ is a scalar tensor.
  
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $input$.
## Outputs

### $output$: [<b><span style="font-family: 'Courier New', monospace">float</span></b>](#float)
Tensor $output$ is the element-wise result of clipping $input$ by the interval $[min, max]$.
### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $input$.
 - `[C2]` Type consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">  [C2]</span></b>](#C2ia) on tensor $input$.

## Formal specification
 
See the [Why3 specification](../formal/clip).

## Numerical Accuracy

See the [Numerical accuracy specification](/clip_na.md).
