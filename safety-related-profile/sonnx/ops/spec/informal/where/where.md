# Contents

- **where** operator for types [BFLOAT16,BOOL,COMPLEX128, COMPLEX64,DOUBLE, FLOAT, FLOAT16, INT16, INT32, INT64, INT8, STRING, UINT16, UINT32, UINT64, UINT8]

<a id="any type"></a>
# **where** (any type)

## Signature
$output = \text{where}(condition, X, Y)$

where:
- $condition$: tensor of boolean values used to select values from $X$ or $Y$ 
- $X$: first input tensor 
- $Y$: second input tensor
- $output$: result of the selection of $X$ and $Y$ elements according to $condition$.
 
## Restrictions

The following restrictions apply to the **where** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

#### Informal specification

The **Where** operator selects elements from two input tensors $X$ and $Y$ based on the values of the $condition$ tensor according to the following formula:
$$
output[i] = 
\begin{cases} 
X[i] & \text{if } condition[i] & \text{is true} \\
Y[i] & \text{otherwise}
\end{cases}
$$

Where
- $i$ is an index covering all dimensions of the tensors.


Example 1:
```math
condition = \begin{bmatrix} True & False & True \end{bmatrix}
```
```math
`X` = \begin{bmatrix}  9 & 8 & 7 \end{bmatrix}
```
```math
`Y` = \begin{bmatrix}  6 & 5 & 4 \end{bmatrix}
```
Result `Z` will be : 
```math
`Z` =  \begin{bmatrix} 9 & 5 & 7 \end{bmatrix}
```


Example 2:
```math
condition =  \begin{bmatrix} True & True \\ True & False \\ False & True \end{bmatrix}
```
```math
`X` = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}
```
```math
`Y` =  \begin{bmatrix} 12 & 11 \\ 10 & 9 \\ 8 & 7 \end{bmatrix}
```
Result `Z` will be  :
```math
`Z` =  \begin{bmatrix} 1 & 2 \\ 3 & 9 \\ 8 & 6 \end{bmatrix}
```

#### Inputs and outputs

##### $condition$

$condition$ is a tensor of boolean values indicating whether an element is selected from $X$ or $Y$.


###### Constraints

- `[C1]`  <a id="C1a"></a> Shape consistency
   - Statement: Tensors $condition$, $X$, $Y$, and $output$ must have the same shape. 

##### $X$

Tensor whose values are selected where condition is True.

###### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1a) on tensor $condition$.

##### $Y$

Tensor whose values are selected where condition is False.


###### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1a) on tensor $condition$.

#### Outputs

##### $output$

Tensor formed by selecting values from $X$ and $Y$ based on $condition$.

###### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1a) on tensor $condition$.

#### Attributes
The `Where` operator has no attribute.

### Formal specification
See the Why3 specification.