# Contents
> - $\text{Add}$ [operator for type real](#real)
> - $\text{Add}$ [operator for types `FP16`, `FP32`, `FP64`](#float)
> - $\text{Add}$ [operator for types `INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`](#int)

---

<a id="real"></a>
# $\text{Add}$ (real, real)

## Signature

Definition of operator $\text{Add}$ signature:

$Y = \text{Add}(A, B)$

where:
- $A$: first operand of the addition  
- $B$: second operand of the addition  
- $Y$: result of the element-wise addition of $A$ by $B$
 

## Restrictions

The following restrictions apply to the **Add** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[GR1]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |


## Informal specification

Operator $\text{Add}$ Adds input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. Each element $Y[i]$ is the result of Adding $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/lexicon.md#tensor_index).

The definition of the operator is given hereafter.

For any index i:

$$
Y[i] = A[i] + B[i]
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
Y = A + B = \begin{bmatrix} 8.1 & 12.5 & 39.7 \end{bmatrix}
```

---

## Error conditions
No error condition.

## Inputs

### $\text{A}$: `real tensor`
Tensor $A$ is the first operand of the addition.

#### Constraints

 - `[C1]` <a id="R1"></a> &lt;Shape consistency&gt;
   - Statement: &lt;Tensors $A$, $B$ and $Y$ must have the same shape. 

 
### $\text{B}$: `real tensor`
Tensor $B$ is the second operand of the addition.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1) on tensor $A$.
 - `[C2]` Definition domain
   - Statement: all elements must be non null.

## Outputs

### $\text{Y}$: `real tensor`

Tensor $Y$ is the element-wise result of $A$ Addtiplied by $B$.

#### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1) on tensor $A$.


## Attributes

The $\text{Add}$ operator has no attribute.

## Formal specification
 
See Why3 specification.

## Numerical Accuracy
*(To be completed)*

---

<a id="float"></a>
# $\text{Add}$ (float, float)
where float could be (`FP16`, `FP32`, `FP64`)

## Signature

Definition of operator $\text{Add}$ signature:

$Y = \text{Add}(A, B)$

where

 - $A$: first operand tensor
 - $B$: second operand  tensor
 - $Y$: output tensor, result of element-wise addition of $A$ by $B$
 
## Restrictions
The following restrictions apply to the `Add` operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]` <a id="R2"></a>     | All tensors shall have the same datatype  | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[GR1]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |

 

## Informal specification

Operator $\text{Add}$ Addtiplies input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics, placing the result in output tensor $Y$. Each element $Y[i]$ is computed as follows:

$$
Y[i] = A[i] + B[i]
$$

---

### Example 1 (2D tensors)

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = A + B = \begin{bmatrix} 6.0 & 6.5 \\ 20.0 & 1.0 \\ 30.5 & 28.25 \end{bmatrix}
```
### Error conditions
No error condition.

## Inputs

### $\text{A}$: `floating-point tensor`
Tensor $A$ is the first opearand of the addition.

#### Constraints

- `[C1]` <a id="R1"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $Y$ must have the same shape. 

### $\text{B}$: `floating-point tensor`
Tensor $B$ is the second operand of the addition.

#### Constraints
 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1) on tensor $A$.

## Outputs

### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the element-wise result of $A$ Addtiplied by $B$.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1) on tensor $A$.

## Attributes

The $\text{Add}$ operator has no attribute.

 ## Formal specification
 See Why3 specification.

## Numerical Accuracy

*(To be completed)*

---

<a id="int"></a>

# $\text{Add}$ (int, int)
where int could be (`INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`)

## Signature
Definition of operator $\text{Add}$ signature:

 $Y = \text{div}(A,B)$

 where
 - $A$: first operand of the addition
 - $B$: second operand of the addition
 - $Y$: result of the element-wise addition of `A` by `B`
 
## Restrictions
The following restrictions apply to the `Add` operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>     | The shape of tensors shall be explicit          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[GR1]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |


## Informal specification

Operator $\text{Add}$ adds input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. Each element $Y[i]$ is the result of Adding $A[i]$ by $B[i]$ where $i$ is a [tensor index](../common/lexicon.md#tensor_index).

The integer addition is performed as follows (considering that all tensors have the same type):

For unsigned values (type `UINTn`):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] + B[i]- k.2^{n} & \quad \textrm{if }  A[i] + B[i] > 2^{n}-1 \\
   A[i] + B[i] & \quad \textrm{otherwise}
  \end{array}
\right.$$

with $k \in N$ such that $0 \le A[i] + B[i]- k.2^{n} < 2^n$

For signed values (type `INTn`):
$$Y[i]=\left\{ 
  \begin{array}{ c l }
    A[i] + B[i]- k_1.2^{n} & \quad \textrm{if }  A[i] + B[i] > 2^{n-1}-1 \\
   A[i] + B[i] + k_2.2^{n} & \quad \textrm{if } A[i] + B[i] < -2^{n-1} \\
   A[i] + B[i] & \quad \textrm{otherwise}
  \end{array}
\right\}.$$

with 

$k_1 \in N$ such that $xxx \le A[i] + B[i]-k_1.2^{n} < 2^n$

$k_2 \in N$ such that $xxx \le A[i] + B[i]+k.2^{n} > -2^{n-1}$


### Example 1 (1D UINT8 tensors)

```math
A = \begin{bmatrix} 6 & 200 & 35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 100 & 5 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 9 & 44 & 40 \end{bmatrix}
```

### Example 1 (1D INT8 tensors)

```math
A = \begin{bmatrix} -6 & 100 & -100  \end{bmatrix}
\quad
B = \begin{bmatrix} -3 & 100 & -100  \end{bmatrix}
```
```math
Y = \begin{bmatrix} -9 & -56 & 56  \end{bmatrix}
```

## Error conditions
- According to the definition, the result of the addition differs from the value that would be expected in $N$ (for unsigned) or $Z$ (for signed) when under- or overflow occur.

## Inputs

### $\text{A}$: `integer tensor`

Tensor $A$ is the first operand of the addition.

#### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` &lt;Shape consistency&gt;
   - Statement: &lt;Tensors $A$, $B$ and $Y$ must have the same shape.`[R1]`&gt;.
 - `[C2]` &lt;Type consistency&gt;
   - Statement: &lt;Tensors $A$, $B$, and $C$ share the same integer type. `[R2]`&gt;. 


### $\text{B}$: `integer tensor`

Tensor $B$ is the second operand of the addition.

#### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.

## Outputs

### $\text{Y}$: `integer tensor`

Tensor $Y$ is the element-wise integer addition result.

#### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.

## Attributes

The $\text{Add}$ operator has no attribute.

## Formal specification
See Why3 specification.

## Numerical Accuracy
*(To be completed.)*



