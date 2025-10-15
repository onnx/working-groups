# Contents

- **div** operator for type [real](#real)
- **div** operator for types [FP16, FP32, FP64](#float)
- **div** operator for types [INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64](#int)

Based on ONNX documentation version 14.

<a id="real"></a>
# **div** (real)

## Signature
$Y = \text{div}(A, B)$

where:
- $A$: numerator
- $B$: denominator
- $Y$: result of the element-wise division of $A$ by $B$
 

## Restrictions

The following restrictions apply to the **div** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |

## Informal specification

Operator **div** divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. If $i$ is a [tensor index](../common/definitions.md#tensor_index), each element $Y[i]$ is the result of dividing $A[i]$ by $B[i]$.

For any index $i$,

$$
Y[i] = 
\begin{cases} 
A[i]/B[i] & \text{if } B[i] \text{ is different from 0} \\
\text{\it undefined} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples.

### Example 1

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix}
```

```math
B = \begin{bmatrix} 3 & 3.3 & 5.1 \end{bmatrix}
```

```math
Y = \frac{A}{B} = \begin{bmatrix} 6.1/3 & 9.5/3.3 & 35.7/5.1 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix}
  3.7 & 4.4 \\
  16.2 & 0.5 \\
  25.3 & 24.8
\end{bmatrix}
```

```math
B = \begin{bmatrix}
  3 & 2.2 \\
  4.1 & 1 \\
  5.2 & 4
\end{bmatrix}
```

```math
Y = \frac{A}{B} = \begin{bmatrix}
  3.7/3 & 2 \\
  16.2/4.1 & 0.5 \\
  25.3/5.2 & 6.2
\end{bmatrix}
```

## Error conditions
No error condition

## Inputs

### $A$: real
Numerator of the division.

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $A$, $B$, and $Y$ must have the same shape. 
 
### $B$: real
Denominator of the division.

#### Constraints

 - `[C1]` Shape consistency
   -  Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.
 - `[C2]` Definition domain
   - Statement: $\forall i, B[i] \neq 0$ 

## Outputs

### $Y$: real

Tensor $Y$ is the element-wise result of the division of $A$ by $B$.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.

## Attributes

Operator **div** has no attribute.

## Formal specification
 
See the Why3 specification.

## Numerical Accuracy

> Section to be verified...

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of an operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$). For $Y = A/B$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ combines contributions from both $A$ and $B$:

- For every $I$ such that $B[I] \neq 0$ and $B[I]$ does not cross zero under perturbation:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{A_{\textit{err}}[I]}{B[I]}\right| + \left|\frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]^2}\right|$

- If $B[I]$ and $B[I] + B_{\textit{err}}[I]$ have different signs, the bound may be unbounded (division by a near-zero denominator).

### Error Introduction
Error introduction for real (ideal) arithmetic is null:
- $Y_{\textit{err}}^{\textit{intro}} = [0]$.*

### Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> A, B;

/* A, B symbolic initialization */

auto result = [&A,&B](auto I) {
  return (B[I].real != 0) ? A[I] / B[I] : /* undefined */ SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];
   if (b.real != 0 && b.real + b.err != 0) {
      auto c = result(I);
      double bound = std::abs(a.err / b.real) + std::abs(a.real * b.err / (b.real * b.real));
      assert(std::abs(c.err) <= bound + 1e-12);
   }
}
```

<a id="float"></a>
# **div** (float, float)
where float is in {FP16, FP32, FP64}

# Signature

$Y = \text{div}(A, B)$

where

 - $A$: numerator
 - $B$: denominator
 - $Y$: result of element-wise division of $A by $B$
 
## Restrictions
The following restrictions apply to the **div** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1">  | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R2"></a>   | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R3]` <a id="R3"></a>     | All tensors shall have the same datatype  | General restriction [GR3](../general_restrictions.md#GR3) |

## Informal specification

Operator **div** divides input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics and stores the result in output tensor $Y$. If $i$ is a [tensor index](../common/lexicon.md#tensor_index), each element $Y[i]$ is the result of dividing $A[i]$ by $B[i]$
For any index $i$,

$$
Y[i] = 
\begin{cases} 
A[i]/B[i] & \text{if } A[i] \text{ and } B[i] \text{ are different from 0} \\
\text{inf} & \text{if } A[i] \neq 0 \text{ and } B[i]=0  \\
\text{nan} & \text{if } A[i]=0 \text{ and } B[i]=0 
\end{cases}
$$

The sign of inf is determined according to the IEEE754 rules.

### Example 1

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0 & 2.25 \\ 4.0 & +\infty \\ 5.1 & 6.0625 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 3.25 & 4.5 \\ 16.0 & 0.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0833 & 2.25 \\ 4.0 & \text{NaN} \\ 5.1 & 6.0625 \end{bmatrix}
```

## Error conditions
- Values of the output tensor may be IEEE 754 infinity or NaN (case of a null denominator).  
  
## Inputs

### $A$: FP16, FP32, FP64
Numerator of the division.

#### Constraints

- `[C1]` <a id="C1fa"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $Y$ must have the same shape. 
- `[C2]` <a id="C2fa"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 

### $B$: FP16, FP32, FP64
Denominator of the division.

#### Constraints
- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa) on tensor $A$.

## Outputs

### $Y$: FP16, FP32, FP64

Result of the element-wise division of $A$ by $B$.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1fa) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2fa) on tensor $A$.

#### Attributes

Operator **div** has no attribute.

## Formal specification
 See Why3 specification.

## Numerical Accuracy

For $Y = A / B$ with numerical errors $A_{\textit{err}}$, $B_{\textit{err}}$:

### Error Propagation

  For all valid indexes $i$ where $B[i] \neq 0$ and $B[i] + B_{\textit{err}}[i]$ does not cross zero,

  $$
  |Y_{\textit{err}}^{\textit{propag}}[i]| \leq \left|\frac{A_{\textit{err}}[i]}{B[i]}\right| + \left|\frac{A[i] \cdot B_{\textit{err}}[i]}{B[i]^2}\right|
  $$

### Error Introduction

  Floating-point division introduces rounding error bounded by the unit in the last place (ulp) of $Y[i]$ in the target floating-point format.
- $Y_{\textit{err}}^{\textit{intro}} = ulp(Y[i])$.

### Unit verification (symbolic)

```c++
Tensor<SymbolicDomainError> A, B;

/* Symbolic initialization of A, B */

auto result = [&A,&B](auto i) {
  if (B[i].real != 0) return A[i] / B[i];
  if (A[i].real != 0) return SymbolicDomainError::inf();
  return SymbolicDomainError::nan();
};

for (auto i : A.indexes()) {
   auto a = A[i];
   auto b = B[i];
   auto c = result(i);
   if (std::isfinite(b.real) && b.real != 0 && b.real + b.err != 0) {
      double bound = std::abs(a.err / b.real) + std::abs(a.real * b.err / (b.real * b.real));
      assert(std::abs(c.err) <= bound + ulp(c.real)); // includes intro. rounding
   }
   if (b.real == 0 && a.real != 0) { assert(c.is_inf()); }
   if (b.real == 0 && a.real == 0) { assert(c.is_nan()); }
}
```

<a id="int"></a>

# **div** (int, int)
where int is in {INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64}

## Signature

 $Y = \text{div}(A,B)$

 where
 - $A$: numerator
 - $B$: denominator
 - $Y$: result of the element-wise division of `A` by `B`

### Restrictions
The following restrictions apply to the **div** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1">  | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R2"></a>   | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R3]` <a id="R3"></a>     | All tensors shall have the same datatype  | General restriction [GR3](../general_restrictions.md#GR3) |

#### Informal specification

Operator **div** divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. 

The result of the division is the algebraic quotient of $A[i]$ by $B[i]$ with any fractional part discarded. If the quotient $A[i]/B[i]$ is representable, the expression $(A[i]/B[i])\times B[i] + A[i] \mod B[i]$ shall equal $A[i]$.

### Example 1

```math
A = \begin{bmatrix} 6 & 5 & -35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 3 & 3 \end{bmatrix}
```
```math
Y = \begin{bmatrix} 2 & 1 & -11 \end{bmatrix}
```

### Example 2

```math
A = \begin{bmatrix} 10 & 10 \\ 21 & 1 \\ 30 & 9 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 3 & 5 \\ 5 & 1 \\ 6 & 2 \end{bmatrix}
```

## Error conditions
- The behaviour in case of a null denominator is implementation dependent.

## Inputs

### $A$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64

Numerator of the division.

#### Constraints

- `[C1]` <a id="C1ia"></a> Shape consistency
  - Statement: Tensors $A$, $B$ and $Y$ must have the same shape. 
- `[C2]` <a id="C2ia"></a> Type consistency
  - Statement: Tensors $A$, $B$, and $C$ must have the same type. 
  
### $B$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64

Denominator of the division.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $A$.
- `[C3]` Definition domain
  - Statement: $\forall i, B|i]\neq 0$ 

## Outputs

### $Y$: INT8, INT16, INT32, INT64, UINT8, UINT16, UINT32, UINT64

Result of the element-wise division of $A$ by $B$.

#### Constraints

- `[C1]` Shape consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ia) on tensor $A$.
- `[C2]` Type consistency
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C2ia) on tensor $A$.

#### Attributes

Operator **div** has no attribute.

 #### Formal specification
 See Why3 specification.

#### Numerical Accuracy
Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

Integer division is exact under the defined semantics; error is not introduced by the operator itself:

###### Error Propagation
 For integer inputs modeled without error symbols, $C_{\textit{err}}^{\textit{propag}} = [0]$.
###### Error Introduction
Error introduction for int arithmetic is null:
 $Y_{\textit{err}}^{\textit{intro}} = [0]$.

Division by zero remains undefined and shall be prevented by input constraints.
###### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:


```c++
Tensor<SymbolicDomainError> A, B;

/* A, B symbolic initialization */

auto result = [&A,&B](auto I) {
  return (B[I].int != 0) ? A[I] / B[I] :
         /* undefined */ SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];
   if (b.int != 0 && b.int + b.err != 0) {
      auto c = result(I);
      double bound = std::abs(a.err / b.int) +
          std::abs(a.int * b.err / (b.int * b.int));
      assert(std::abs(c.err) <= bound + 0);
   }
}
```



