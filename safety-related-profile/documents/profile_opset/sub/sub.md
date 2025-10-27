# Contents
 - **Sub** operator for type [real](#real)
 - **Sub** operator for types [`FP16`, `FP32`, `FP64`](#float)
 - **Sub** operator for types [`INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`](#int)

---

<a id="real"></a>
# **Sub** (real, real)

## Signature

Definition of operator $\text{Sub}$ signature:

$Y = \text{Sub}(A, B)$

where:
- $A$: first operand of the substraction  
- $B$: second operand of the substraction  
- $Y$: result of the element-wise substraction of *A$ by $B$
 

## Restrictions

The following restrictions apply to the **Sub** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |


## Informal specification

Operator **Sub** Subtiplies input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. Each element $Y[i]$ is the result of Subtiplying $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/lexicon.md#tensor_index).

The definition of the operator is given hereafter.

For any index i:

$$
Y[i] = A[i] - B[i]
$$

The effect of the operator is illustrated on the following examples:

---

### Example 1 (1D tensors)

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 2 & 3 & 4 \end{bmatrix}
```

```math
Y = A + B = \begin{bmatrix} 4.1 & 6.5 & 31.7 \end{bmatrix}
```

---

## Error conditions
No error condition

## Inputs

### $\text{A}$: `real tensor`
Tensor $A$ is the first operand of the substraction.

#### Constraints

 - `[C1]` <a id="C1r"></a> Shape consistency
   - Statement: Tensors $A$, $B$ and $Y$ must have the same shape. 

 
##### $\text{B}$: `real tensor`
Tensor $B$ is the second operand of the substraction.

###### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1r) on tensor $A$.
 - `[C2]` Definition domain
   - Statement: all elements must be non null.

## Outputs

### $\text{Y}$: `real tensor`

Tensor $Y$ is the element-wise result of $A$ Subtiplied by $B$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1r) on tensor $A$.


## Attributes

The **Sub** operator has no attribute.

 ## Formal specification
 
See Why3 specification.

## Numerical Accuracy
*(To be completed)*

---

<a id="float"></a>
# **Sub** (float, float)
where float is in {`FP16`, `FP32`, `FP64`}

## Signature

Definition of operator $\text{Sub}$ signature:

$Y = \text{Sub}(A, B)$

where

 - $A$: first operand tensor
 - $B$: second operand  tensor
 - $Y$: output tensor, result of element-wise substraction of $A$ by $B$
 
## Restrictions
The following restrictions apply to the **Sub** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]` <a id="R2"></a>     | All tensors shall have the same datatype  | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R3]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |

 

## Informal specification

Operator **Sub** Subtiplies input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics, placing the result in output tensor $Y$. Each element $Y[i]$ is computed as follows:

$$
Y[i] = A[i] - B[i]
$$

---

### Example 1 (2D tensors)

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = A + B = \begin{bmatrix} 0.0 & 2.5 \\ 12.0 & 1.0 \\ 20.5 & 20.25 \end{bmatrix}
```
## Error conditions
No error condition.

## Inputs

### $\text{A}$: `floating-point tensor`
Tensor $A$ is the first opearand of the substraction.

#### Constraints

- `[C1]` <a id="C1f"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $Y$ must have the same shape. 

### $\text{B}$: `floating-point tensor`
Tensor $B$ is the second operand of the substraction.

#### Constraints
 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1f) on tensor $A$.

## Outputs

### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the element-wise result of $A$ Subtiplied by $B$.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1f) on tensor $A$.

## Attributes

The **Sub** operator has no attribute.

 ## Formal specification
 See Why3 specification.

## Numerical Accuracy

*(To be completed)*

---

<a id="int"></a>

# **Sub** (int, int)
where int could be {`INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`}

## Signature
Definition of operator $\text{Sub}$ signature:

 $Y = \text{Sub}(A,B)$

 where
 - $A$: first operand of the substraction
 - $B$: second operand of the substraction
 - $Y$: result of the element-wise substraction of $A$ by $B$
 
## Restrictions
The following restrictions apply to the **Sub** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |


## Informal specification

Operator **Sub** Subtiplies input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. Each element $Y[i]$ is the result of Subtiplying $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/lexicon.md#tensor_index).

The integer substraction is performed as follows (considering that all tensors have the same type):

For unsigned values (type `UINTn`):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] - B[i]- k.2^{n} & \quad \textrm{if }  A[i] - B[i] > 2^{n}-1 \\
   A[i] - B[i] & \quad \textrm{otherwise}
  \end{array}
\right.$$

with $k \in N$ such that $0 \le A[i] - B[i]- k.2^{n} < 2^n$

For signed values (type `INTn`):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] - B[i]- k_1.2^{n} & \quad \textrm{if }  A[i] - B[i] > 2^{n-1}-1 \\
   A[i] - B[i] + k_2.2^{n} & \quad \textrm{if } A[i] - B[i] < -2^{n-1} \\
   A[i] - B[i] & \quad \textrm{otherwise}
  \end{array}
\right\}.$$

with 

$k_1 \in N$ such that $xxx \le A[i] - B[i]-k_1.2^{n} < 2^n$

$k_2 \in N$ such that $xxx \le A[i] - B[i]+k.2^{n} > -2^{n-1}$


### Example 1 (1D UINT8 tensors)

```math
A = \begin{bmatrix} 6 & 100 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 200 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 3 & 44 \end{bmatrix}
```

### Example 1 (1D INT8 tensors)

```math
A = \begin{bmatrix} -6 & 10 & 10  \end{bmatrix}
\quad
B = \begin{bmatrix} -3 & 100 & -120  \end{bmatrix}
```
```math
Y = \begin{bmatrix} -9 & -90 & -126  \end{bmatrix}
```

## Error conditions
- According to the definition, the result of the substraction differs from the value that would be expected in $N$ (for unsigned) or $Z$ (for signed) when under- or overflow occur.

## Inputs

### $\text{A}$: `integer tensor`

Tensor $A$ is the first operand of the substraction.

#### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` <a id="C1ia"></a> Shape consistency
   - Statement: Tensors $A$, $B$ and $Y$ must have the same shape.`[R1]`.
 - `[C2]` <a id="C2ia"></a> Type consistency
   - Statement: Tensors $A$, $B$, and $C$ share the same integer type. `[R2]`. 


### $\text{B}$: `integer tensor`

Tensor $B$ is the second operand of the substraction.

#### Constraints

 - `[C1]` Shape consistency : See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on $A$.
 - `[C2]` Type consistency : See constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on $A$.

## Outputs

### $\text{Y}$: `integer tensor`

Tensor $Y$ is the element-wise integer substraction result.

#### Constraints

 - `[C1]` Shape consistency : See constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on $A$.
 - `[C2]` Type consistency : See constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on $A$.

## Attributes

The **Sub** operator has no attribute.

## Formal specification
See Why3 specification.

## Numerical Accuracy
*(To be completed.)*


