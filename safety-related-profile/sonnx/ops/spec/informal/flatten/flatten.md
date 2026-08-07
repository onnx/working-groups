# Contents

- **Flatten** operator for [real](#types) and types [float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64](#types)
  
Based on ONNX documentation [Flatten version 25](https://onnx.ai/onnx/operators/onnx__Flatten.html#flatten-25).

<a id="real"></a>
# **Flatten** (type)

where type is real or in {float16, float, double, int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

## Signature
$Y = \textbf{Flatten}(X)$

where:
- $X$: Input tensor 
- $Y$: Output tensor

## Restrictions
[General Restrictions](./../common/general_restrictions.md) are applicable.

## Informal specification

Operator $\text{Flatten}$ reshapes the input tensor $X$ into a 2D tensor $Y$ (i.e., $rY=2$). 

The size of the first dimension of $Y$ is equal to the product of the sizes of the dimensions of $X$ from the start up to (but not including) the dimension specified by $\text{axis}$.

The size of the second dimension of $Y$ is determined by the product of the sizes of the dimensions of $X$ from the dimension specified by $\text{axis}$ to the end.

$$\text{dY}_{0} = \prod_{i=0}^{\text{axis'}-1} \text{dX}_{i}$$
$$\text{dY}_{1} = \prod_{i=\text{axis'}}^{rX-1} \text{dX}_{i}$$

Where 
- $\text{axis'}$ is the normalized $\text{axis}$ and is calculated as follows:

$$ \begin{cases}
      \text{axis'} = \text{axis} & \text{if } \text{axis} \geq 0 \\
      \text{axis'} = \text{axis} + rX & \text{if } \text{axis} < 0
\end{cases}$$

Flatten operation is defined as:

<a id="Y"></a>

$$Y[a, b] = X[j_0, j_1, \ldots, j_{rX-1}]$$


Where:
- $[j_0,...,j_{rX-1}]$ and $[a,b]$ are [tensor indexes](./../common/definitions.md#tensor_index)
- $a = \displaystyle\sum_{z=0}^{\text{axis'}-1} \left( j_z \prod_{k=z+1}^{\text{axis'}-1} dX_k \right)$

- $b = \displaystyle\sum_{z=\text{axis'}}^{rX-1} \left( j_z \prod_{k=z+1}^{rX-1} dX_k \right)$

Note 1: when the start index in a sum or product is greater than the end index then
-  the product is defined to be 1
-  the sum is defined to be 0.

Note 2: if $X$ is a scalar, $dX_i$ is not defined, but the value is given by applying the rule given in note 1.


### Example 1

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 0
```

```math
Y = \begin{bmatrix}\begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}\end{bmatrix}
```
### Example 2

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
\text{axis} = 1
```

```math
Y =  
  \begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 \\
12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 & 22 & 23 \end{bmatrix}

```
### Example 3

```math
X = \begin{bmatrix} 
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix} 
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```
```math
\text{axis} = 2
```
```math
Y = \begin{bmatrix}
  \begin{bmatrix} 0 & 1 & 2 & 3\end{bmatrix} \begin{bmatrix}  4 & 5 & 6 & 7 \end{bmatrix} \begin{bmatrix}  8 & 9 & 10 & 11 \end{bmatrix} \begin{bmatrix}  12 & 13 & 14 & 15 \end{bmatrix} \begin{bmatrix}  16 & 17 & 18 & 19 \end{bmatrix} \begin{bmatrix}  20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

## Error conditions
If any pre-conditions is not satisfied, then the behavior is undefined.

## Attributes

### axis: `integer`
The axis starting from which the input tensor will be flattened into the second dimension of the output.

#### Constraints
 - `[C1]` <a id="C1ra"></a> Value domain
    - Statement: $\text{axis} \in [-rX, rX]$
    - Rationale: Ensures that the attribute `axis` is a valid axis for tensor $X$

## Inputs

### $X$: `real`
Tensor $X$ is the input tensor to be flattened.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Consistency between the shape of tensor $X$ and attribute `axis`
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $X$.

## Outputs

### $Y$: `real tensor`
Tensor $Y$ is the flattened output tensor.

### Constraints

 - `[C1]` Shape consistency
   - Statement: The shape of tensor $Y$ is $(dY_0, dY_1)$, where:
     - $dY_0 = \prod_{i=0}^{\text{axis'}-1} dX_i$

     - $dY_1 = \prod_{i=\text{axis'}}^{rX-1} dX_i$
   
   Where 
   - $dX_i$ is the size of dimension $i$ of tensor $X$

## Numerical Accuracy

The $\text{Flatten}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.
