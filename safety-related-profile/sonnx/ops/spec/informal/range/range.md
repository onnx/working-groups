# Contents

- **Range** operator for type [real](#real)
- **Range** operator for type [FP64, FP32, INT16, INT32, INT64](#types)

Based on ONNX documentation version 11.

<a id="real"></a>
# **Range** (real, real, real)

## Signature
$Y = \text{Range}(S, L, D)$

where:
- $S$: initial position of the range (**scalar** tensor)
- $L$: limit (exclusive) position of the range (**scalar** tensor)
- $D$: delta or step size (**scalar** tensor)

## Restrictions
The following restrictions apply to the $\text{Range}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification

Operator $\text{Range}$ creates a sequence of numbers that begins at the specified $S$ value and extends by increments of $D$ up to, but not including, the specified $L$ value.

$$ Y[i] = S + i \cdot D $$

Where:
- $K = \displaystyle \max \left( \ \left\lceil \frac{L - S}{D} \right\rceil , 0 \right)$

- $i \in [0, K - 1]$

\
Note that if $D$ is positive and $S$ is greater than or equal to $L$, or if $D$ is negative and $S$ is less than or equal to $L$, the output tensor $Y$ will be empty.

Moreover, whenever the interval $[0, K - 1]$ is empty (for instance when $K \leq 0$), the output tensor $Y$ will also be empty.


### Example 1

```math
S = 0  \quad L = 10 \quad D = 1
```

```math
Y = \begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 \end{bmatrix}
```

### Example 2

```math
S = 10  \quad L = 2 \quad D = -3
```

```math
Y = \begin{bmatrix} 10 & 7 & 4 \end{bmatrix}
```

### Example 3

```math
S = 10  \quad L = 10 \quad D = -3
```

```math
Y = \begin{bmatrix} \end{bmatrix}
```

### Example 4

```math
S = 30  \quad L = 10 \quad D = 3
```

```math
Y = \begin{bmatrix} \end{bmatrix}
```


## Error conditions
No error condition.

## Inputs

### $S$: `real tensor`
Tensor $S$ is the first entry for the range of output values.

Tensor $S$ is a scalar real tensor.

### Constraints
Tensor $S$ does not have any specific constraints.

### $L$: `real tensor`
Tensor $L$ is the exclusive upper limit for the range of output values.

Tensor $L$ is a scalar real tensor.

### Constraints
Tensor $L$ does not have any specific constraints.

### $D$: `real tensor`
Tensor $D$ is the delta or step size of the Range.

Tensor $D$ is a scalar real tensor.

### Constraints
  - `[C1]` Non-zero step size
    - Statement: $D \neq 0$
   
    - Rationale: Ensures that the step size is not zero to avoid infinite loops.

## Outputs

### $Y$: `real tensor`
Tensor $Y$ is a 1D tensor containing all values that lie in the range and are spaced by $D$.

### Constraints
Tensor $Y$ does not have any specific constraints.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy
(-- IGNORE --)


<a id="type"></a>
# **Range** (type, type, type)
Where type in in { FP64, FP32, INT64, INT32, INT16 }

## Signature
$Y = \text{Range}(S, L, D)$

where:
- $S$: initial position of the range (**scalar** tensor)
- $L$: limit (exclusive) position of the range (**scalar** tensor)
- $D$: delta or step size (**scalar** tensor)

## Restrictions
The following restrictions apply to the $\text{Range}$ operator for the SONNX profile:

[General Restrictions](../general_restrictions.md) are applicable

## Informal specification

Operator $\text{Range}$ creates a sequence of numbers that begins at the specified $S$ value and extends by increments of $D$ up to, but not including, the specified $L$ value.

$$ Y[i] = S + i \cdot D $$

Where:
- $K = \displaystyle \max \left( \ \left\lceil \frac{L - S}{D} \right\rceil , 0 \right)$

- $i \in [0, K - 1]$

\
Note that if $D$ is positive and $S$ is greater than or equal to $L$, or if $D$ is negative and $S$ is less than or equal to $L$, the output tensor $Y$ will be empty.

Moreover, whenever the interval $[0, K - 1]$ is empty (for instance when $K \leq 0$), the output tensor $Y$ will also be empty.


### Example 1

```math
S = 0  \quad L = 10 \quad D = 1
```

```math
Y = \begin{bmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 \end{bmatrix}
```

### Example 2

```math
S = 10  \quad L = 2 \quad D = -3
```

```math
Y = \begin{bmatrix} 10 & 7 & 4 \end{bmatrix}
```

### Example 3

```math
S = 10  \quad L = 10 \quad D = -3
```

```math
Y = \begin{bmatrix} \end{bmatrix}
```

### Example 4

```math
S = 30  \quad L = 10 \quad D = 3
```

```math
Y = \begin{bmatrix} \end{bmatrix}
```

## Error conditions
No error condition.

## Inputs

### $S$: `type tensor`
Tensor $S$ is the first entry for the range of output values.

Tensor $S$ is a scalar type tensor.

### Constraints
Tensor $S$ does not have any specific constraints.

### $L$: `type tensor`
Tensor $L$ is the exclusive upper limit for the range of output values.

Tensor $L$ is a scalar type tensor.

### Constraints
Tensor $L$ does not have any specific constraints.

### $D$: `type tensor`
Tensor $D$ is the delta or step size of the Range.

Tensor $D$ is a scalar type tensor.

### Constraints
  - `[C1]` Non-zero step size
    - Statement: $D \neq 0$
   
    - Rationale: Ensures that the step size is not zero to avoid infinite loops.

## Outputs

### $Y$: `type tensor`
Tensor $Y$ is a 1D tensor containing all values that lie in the range and are spaced by $D$.

### Constraints
Tensor $Y$ does not have any specific constraints.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy
(-- IGNORE --)
