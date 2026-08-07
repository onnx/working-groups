# Contents
- **Reshape** operator for type [real](#real)
- **Reshape** operator for type [bool, string, float16, float32, float64, int2, int4, int8, int16, int32, int64, uint2, uint4, uint8, uint16, uint32, uint64](#types)
 
Based on ONNX [Op version 25](https://onnx.ai/onnx/operators/onnx__Reshape.html).
 
# **Reshape**
 
# Signature
$Y = \textbf{Reshape}(X, S)$

where:
- $data$: input tensor (denoted by $X$)
- $shape$: desired shape (denoted by $S$)

## Restrictions
[General Restrictions](../general_restrictions.md) are applicable
 
## Informal specification

Operator **Reshape** transforms the input tensor into an output tensor with the shape specified in $S$.

The reshape operation depends on the attribute `allowzero`. If:

- `allowzero = 0`: Any dimension **equal to $0$** in $S$ means copying the respective dimension from the input tensor $X$.
 
- `allowzero = 1`: Any dimension **equal to $0$** in $S$ means that the respective dimension in the output tensor $Y$ should be null.

It is possible to have **at most one dimension in $S$ with value -1**. In such case that dimension is inferred from the size of the input tensor $X$ and the remaining dimensions in $S$.
 
The operation is performed in two steps.

### 1. Compute a the flattened index for the output tensor $Y$:

$$\mathit{flat\_y} = \operatorname{offset}\!\left(\,Y_{\mathit{coords}},\; Y_{\mathit{shape}}\,\right)$$
 
where:
- $Y_{\text {coords}}$ are the coordinates of an element in the output tensor $Y$.
- $Y_{\text {shape}}$ is the shape of the output tensor $Y$.
- $\text{offset}$ is defined [here](../common/definitions).
 
### 2. Compute the corresponding $X$ coordinates from the flattened index:
$$X_{\mathit{coords}} = index \left(\mathit{flat\_y}, X_{\mathit{shape}}\right)$$

where:
- $flat\_y$ is the flattened index computed in step 1.

- $X_shape$ is the shape of the input tensor $X$.

- $index$ is defined [here](../common/definitions).

---

Reshape operation can then be expressed as:
 
$$Y[i_0, i_1, \ldots, i_{rY-1}] = X[\displaystyle index \left(offset([i_0, i_1, \ldots, i_{rY-1}], Y_{\mathit{shape}}), X_{\mathit{shape}}\right)] $$
 
Where:
- $i_n \in [0, dY_n - 1]$
 
- $X_{\mathit{shape}}$ is the shape of the input tensor $X$

- $Y_{\mathit{shape}}$ is the shape of the output tensor $Y$
 
 
### Example 1
 
```math
X = \begin{bmatrix}
      \begin{bmatrix} 0 & 1 & 2 & 3 & 4 \end{bmatrix}
      \begin{bmatrix} 5 & 6 & 7 & 8 & 9 \end{bmatrix}
    \end{bmatrix}
```

```math
allowzero = 0
```

```math
\text{S} = [5, 2]
```

```math
Y_\mathit{shape} = [5, 2]
```
 
```math
Y = \begin{bmatrix}
      \begin{bmatrix} 
        0 & 1 \\ 2 & 3 \\ 4 & 5 \\ 6 & 7 \\ 8 & 9 
      \end{bmatrix}
    \end{bmatrix}
```

### Example 2
 
```math
X = \begin{bmatrix}
  \begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \\ 8 & 9 & 10 & 11 \end{bmatrix}
  \begin{bmatrix} 12 & 13 & 14 & 15 \\ 16 & 17 & 18 & 19 \\ 20 & 21 & 22 & 23 \end{bmatrix}
\end{bmatrix}
```

```math
allowzero = 0
```
 
```math
\text{S} = [0, 6, -1]
```

```math
Y_\mathit{shape} = [2, 6, 2]
```

```math
Y = \begin{bmatrix}
      \begin{bmatrix}
        0 & 1 \\
        2 & 3 \\
        4 & 5 \\
        6 & 7 \\
        8 & 9 \\
        10 & 11
      \end{bmatrix}
      \begin{bmatrix}
        12 & 13 \\
        14 & 15 \\
        16 & 17 \\
        18 & 19 \\
        20 & 21 \\
        22 & 23
      \end{bmatrix}
    \end{bmatrix}
```

### Example 3
 
```math
X = \begin{bmatrix}
      \begin{bmatrix} 
        0 & 1 & 2 & 3 & 4 \\
        5 & 6 & 7 & 8 & 9 
      \end{bmatrix}
    \end{bmatrix}
```

```math
allowzero = 1
```
 
```math
\text{S} = [0, -1]
```

```math
Y_\mathit{shape} = [2, 5]
```
 
```math
Y = \begin{bmatrix}
      \begin{bmatrix} 
        0 & 1 & 2 & 3 & 4 \\
        5 & 6 & 7 & 8 & 9 
      \end{bmatrix}
    \end{bmatrix}
 
```
### Example 4
 
```math
X = \begin{bmatrix}
      \
    \end{bmatrix}
```

```math
X_\text{shape} = [0, 3, 8]
```

```math
allowzero = 1
```
 
```math
\text{S} = [1, 2, 0]
```

```math
Y_\mathit{shape} = [1, 2, 0]
```

```math
Y = \begin{bmatrix}
      \
    \end{bmatrix}
```

## Error conditions

No error conditions.

## Attributes
 
### allowzero: integer
If set to 0, dimensions in $S$ with value 0 will copy the size from the corresponding dimension of the input tensor $X$.
 
If set to 1, any 0 in $S$ means that the size of that dimension should be 0.

For any value other than 0 in $S$, the respective value will be kept (regardless of the value of `allowzero`).


#### Constraints

  - `[C1]` Value domain
    - Statement: 
      - $\text{allowzero} \in \{0, 1\} $
 
  - `[C2]` <a id="C1ra"></a> Dimension size copying from input tensor $X$
    - Statement: With `allowzero = 0` only valid dimensions can be copied from the input tensor $X$:
      - $\forall i \in [0, dS - 1]. \quad S[i] = 0 \implies i < rX$
 
    - Rationale: Only valid dimensions in $X$ can be copied to the output.
  
  - `[C3]` <a id="C2ra"></a> Value domain in $S$
    - Statement:
      - If `allowzero = 0`:

        $$\forall i \in [0, dS_0 - 1] . \quad S[i] >= -1 \quad \land \quad $$
        $$(\exists j \in [0, dS_0 - 1]. \quad S[j] = -1) \implies (\forall d \in [0, rX - 1]. \quad dX_d \neq 0)$$
      <br>

      - If `allowzero = 1`: 
      
        $$\forall i \in [0, dS_0 - 1]. \quad S[i] > 0 \quad \lor\\$$
        $$(S[i] = 0 \implies ((\exists d \in [0, rX - 1]. \quad dX_d = 0) \quad \land \quad (\forall  z \in [0, dS_0 - 1]. \quad S[z] \neq -1) )) \quad \lor\\$$
        $$(S[i] = -1 \quad \implies (\forall  z \in [0, dS_0 - 1]. \quad S[z] \neq 0))$$
 
    - Rationale:
      - `allowzero = 0`: Auto inference is not compatible with null tensors (division by 0).
      
      - `allowzero = 1`: Dimensions equal to `0` or `1` are mutually incompatible. Null tensors are only feasible ate output if the input is also null.
 
## Inputs
 
### $X$: real
Tensor $X$ is the input tensor to be reshaped.
 
### Constraints
 
  - `[C1]` <a id="C3ra"></a> Consistency between the shapes of tensor $X$ and the output tensor $Y$.
   - Statement: $size_X = size_Y$
      
      where:
        - $size$ is defined [here](../common/definitions.md)
 
### $S$: int64 tensor
Tensor $S$ is a 1D tensor that specifies the desired shape of the output tensor $Y$.
 
### Constraints
  - `[C1]` <a id="C4ra"></a> Automatic shape inference
    - Statement: 
      - $\forall i,j \in [0, dS_0 - 1]. \quad S[i] = -1 \land S[j] = -1 \implies i = j$
    - Rationale: Ensures that the at most one dimenson can be automatically inferred.
 
  - `[C2]` <a id="C1ra"></a> Dimension size copying from input tensor $X$
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C1ra) on attribute $\text{allowzero}$.
  
  - `[C3]` <a id="C4ra"></a> Value domain
    - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C3]</span></b>](#C2ra) on attribute $\text{allowzero}$.

 
## Outputs
 
### $Y$: real tensor
Tensor $Y$ is the reshaped output tensor.
 
### Constraints
 - `[C1]` Shape consistency
   - Statement: See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C3ra) on tensor $X$.
   
## Formal specification
See the Why3 specification.
 
## Numerical Accuracy
The $\text{Reshape}$ operator does not introduce any numerical error. Hence, for all valid indices the output values are exactly equal to the corresponding input values.