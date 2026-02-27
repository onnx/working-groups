# Contents

- **Clip** operator for type [real](#real)
- **Clip** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)
- **Clip** operator for types [float16, float, double](#floats)


Based on ONNX [Clip version 13](https://onnx.ai/onnx/operators/onnx__Clip.html).

<a id="real"></a>
# **Clip** (real, real, real)

## Signature
$Y = \textbf{Clip}(X,L,M)$

where:
- $input$: input tensor (denoted by $X$)
- $min$: minimum value (scalar) (denoted by $L$)
- $max$: maximum value (scalar) (denoted by $M$)
- $output$: output tensor (denoted by $Y$)


## Restrictions
The following restrictions apply to the **Clip** operator for the SONNX profile:

[General restrictions](../general_restrictions.md) are applicable.


## Informal specification

Operator **Clip** limit the given input within an interval.
- If $L$ $\leq$ $M$:

  - if $X[i]$ $\lt$ $L$ then $Y[i]$ = $L$.

  - If $X[i]$ $\gt$ $M$ then $Y[i]$ = $M$.

  - Otherwise, $Y[i]$ = $X[i]$.

- If $L$ $\gt$ $M$:

  - $Y[i] = M$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).


The following **Clip** formula captures the behavior expressed by the previous if-statements:

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
Y = \begin{bmatrix} \min(10, \max(-6.1, 0)) & \min(10, \max(9.5, 0)) & \min(10, \max(35.7, 0)) \end{bmatrix}
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
Y = \begin{bmatrix} \min(10, \max(6.1, 20)) & \min(10, \max(9.5, 20)) & \min(10, \max(35.7, 20)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} 10 & 10 & 10 \end{bmatrix}
```

## Error conditions
No error condition

## Attributes

Operator **Clip** has no attribute.

## Inputs

### $input$: `real tensor`
Tensor $input$ is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $input$ and $output$ must have the same shape.
 
### $min$: `real tensor`
Tensor $min$ is the minimum bound for clipping.


### Constraints
  - `[C1]` Shape consistency
    - Statement: The shape of tensor $min$ must be empty.

### $max$: `real tensor`
Tensor $max$ is the maximum bound for clipping.

### Constraints
  - `[C1]` Shape consistency
    - Statement: The shape of tensor $max$ must be empty.

## Outputs

### $output$: `real tensor`
Tensor $output$ is the element-wise result of clipping $input$ by the interval $[min, max]$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $input$.


## Formal specification
 
See the [Why3 specification](../formal/clip).

## Numerical Accuracy

See the [Numerical accuracy specification](/clip_na.md).

<a id="int"></a>
# **Clip** (int, int, int)
where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

All arguments have the same data type.

See specification for [real numbers](#real).

<a id="float"></a>
# **Clip** (float, float, float)
where float is in {float16, float, double}

All the arguments have the same data type.

## Signature
$Y = \textbf{Clip}(X,L,M)$

where:
- $input$: input tensor (denoted by $X$)
- $min$: minimum value (scalar) (denoted by $L$)
- $max$: maximum value (scalar) (denoted by $M$)
- $output$: output tensor (denoted by $Y$)


## Restrictions
The following restrictions apply to the **Clip** operator for the SONNX profile:

[General restrictions](../general_restrictions.md) are applicable.

## Informal specification

Operator **Clip** limit the given input within an interval.

**Clip** operation can be divided into two steps:

- First step : normalize the boundaries $L$ and $M$ as follows:

  If any of the boundaries is $NaN$ it is readjusted to the respetive extreme value:

    - If $L$ is $NaN$, then $L'$ = $-\infty$

    - If $M$ is $NaN$, then $M'$ = $+\infty$

    - Otherwise, $L'$ = $L$ and $M'$ = $M$

- Second step: perform the clipping as follows:
  - If $L'$ $\leq$ $M'$:

    - if $X[i]$ $\lt$ $L'$ then $Y[i]$ = $L'$.

    - If $X[i]$ $\gt$ $M'$ then $Y[i]$ = $M'$.
    - Otherwise, $Y[i]$ = $X[i]$.

  - If $L'$ $\gt$ $M'$:

    - $Y[i] = M'$

where $i$ is a [tensor index](../common/definitions.md#tensor_index).


The following **Clip** formula captures the behavior expressed of the second step, previously defined:


$$ Y[i] = \min(M, \max(X[i], L))$$

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
Y = \begin{bmatrix} \min(10.1, \max(-6.3, 0.5)) & \min(10.1, \max(9.2, 0.5)) & \min(10.1, \max(35.5, 0.5)) \end{bmatrix}
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
Y = \begin{bmatrix} \min(10.0, \max(6.5, 20.2)) & \min(10.0, \max(9.2, 20.2)) & \min(10.0, \max(35.1, 20.2)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} 10.0 & 10.0 & 10.0 \end{bmatrix}
```

### Example 3

```math
X = \begin{bmatrix} -\infty & 0.0 & +\infty & NaN \end{bmatrix}
```
```math
L = -1.0
\quad
M = NaN
```
```math
M = +\infty
```

```math
Y = \begin{bmatrix} \min(+\infty, \max(-\infty, -1.0)) & \min(+\infty, \max(0.0, -1.0)) & \min(+\infty, \max(+\infty, -1.0)) & \min(+\infty, \max(NaN, -1.0)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} -1.0 & 0.0 & +\infty & NaN \end{bmatrix}
```

### Example 4

```math
X = \begin{bmatrix} -\infty & 0.0 & +\infty & NaN \end{bmatrix}
```
```math
L = NaN
\quad
M = NaN
```
```math
L = - \infty \quad M = +\infty
```

```math
Y = \begin{bmatrix} \min(+\infty, \max(-\infty, -\infty)) & \min(+\infty, \max(0.0, -\infty)) & \min(+\infty, \max(+\infty, -\infty)) & \min(+\infty, \max(NaN, -\infty)) \end{bmatrix}
```

```math
Y = \begin{bmatrix} -\infty & 0.0 & +\infty & NaN \end{bmatrix}
```

## Error conditions
- Values of the output tensor may be IEEE 754 infinity or NaN

## Attributes

Operator **Clip** has no attribute.

## Inputs

### $input$: [<b><span style="font-family: 'Courier New', monospace">float</span></b>](#float)
Tensor $input$ is the input tensor to be clipped within the specified bounds.

### Constraints

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors $input$ and $output$ must have the same shape.
 - `[C2]` <a id="C2ia"></a> Type consistency
   - Statement: Tensors $input$, $min$, $max$ and $output$ must have the same type.
 
### $min$: [<b><span style="font-family: 'Courier New', monospace">float</span></b>](#float)
Tensor $min$ is the minimum bound for clipping.

### Constraints

- `[C1]` Shape consistency
  - Statement: The shape of tensor $min$ must be empty.

- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $input$.


### $max$: [<b><span style="font-family: 'Courier New', monospace">float</span></b>](#float)
Tensor $max$ is the maximum bound for clipping.

### Constraints

- `[C1]` Shape consistency
  - Statement: The shape of tensor $max$ must be empty.

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
