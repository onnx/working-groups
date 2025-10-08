# Contents
> - $\text{Div}$ [operator for type real](#real)
> - $\text{Div}$ [operator for types `FP16`, `FP32`, `FP64`, `BFLOAT16`](#float)
> - $\text{Div}$ [operator for types `INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`](#int)

---

<a id="real"></a>
# $\text{div}$ (real, real)

### Signature

Definition of operator $\text{div}$ signature:

$Y = \text{div}(A, B)$

where:
- $A$: numerator of the division  
- $B$: denominator of the division  
- $Y$: result of the element-wise division of `A` by `B`
 
Arguments have different names. For instance 


### Restrictions

The following restrictions apply to the `Div` operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`      | Input and output tensors shall have the same shape          | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[GR1]`     | Sparse tensors are not supported                            | General restrictions ([gen.restrict](../general_restrictions.md))                                  |



#### Informal specification

> Operator $\text{div}$ divides input tensors $A$ and $B$ element-wise and stores the result in output tensor $Y$. Each element $Y[i]$ is the result of dividing $A[i]$ by $B[i]$.

The mathematical definition of the operator is given hereafter for a unidimensional tensor, with $i$ covering all valid indexes:

$$
Y[i] = 
\begin{cases} 
\frac{A[i]}{B[i]} & \text{if } B[i] \text{ is different from 0} \\
\text{undefined} & \text{otherwise}
\end{cases}
$$

The effect of the operator is illustrated on the following examples:
- $A$ and $B$ are tensors holding numerical data





---

### Example 1 (1D tensors, real values with decimals)

```math
A = \begin{bmatrix} 6.1 & 9.5 & 35.7 \end{bmatrix} \in \mathbb{R}^{1 \times 3}
```

```math
B = \begin{bmatrix} 3.0 & 3.3 & 5.1 \end{bmatrix} \in \mathbb{R}^{1 \times 3}
```

```math
Y = \frac{A}{B} = \begin{bmatrix} 2.0333 & 2.8788 & 7.0 \end{bmatrix} \in \mathbb{R}^{1 \times 3}
```

---

### Example 2 (2D tensors, real values with decimals)

```math
A = \begin{bmatrix}
  3.7 & 4.4 \\
  16.2 & 0.5 \\
  25.3 & 24.8
\end{bmatrix} \in \mathbb{R}^{3 \times 2}
```

```math
B = \begin{bmatrix}
  3.0 & 2.2 \\
  4.1 & 1.0 \\
  5.2 & 4.0
\end{bmatrix} \in \mathbb{R}^{3 \times 2}
```

```math
Y = \frac{A}{B} = \begin{bmatrix}
  1.2333 & 2.0 \\
  3.9512 & 0.5 \\
  4.8654 & 6.2
\end{bmatrix} \in \mathbb{R}^{3 \times 2}
```

---



#### Error conditions
- for real computations 
  - division by zero  is undefined

#### Inputs

##### $\text{A}$: `real tensor`
Tensor $A$ is the numerator of the division.

###### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` &lt;Shape consistency&gt;
   - Statement: &lt;Tensors $A$, $B$ and $Y$ must have the same shape.`[R1]`&gt;.


 
##### $\text{B}$: `real tensor`
Tensor $B$ is the denominator of the division.

###### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Range&gt;
   - Statement: &lt;The operator is only defined for a denominator tensor containing non null values.&gt;.

### Outputs

##### $\text{Y}$: `real tensor`

Tensor $Y$ is the element-wise result of $A$ divided by $B$.

##### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.


#### Attributes

The $\text{div}$ operator does not require any attributes.

 #### Formal specification
 
The formal specification of the `div` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Div operation on tensors with real numbers.
 *)

module DivReal
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Inf
  use real.NaN
  use real.Div

  let function div (a : tensor real) (b : tensor real) : tensor real =
    requires { a.shape = b.shape }
    ensures {
      forall i. if a.value[i] <> 0.0 && b.value[i] <> 0.0 then result.value[i] = a.value[i] / b.value[i]
               else if a.value[i] <> 0.0 && b.value[i] = 0.0 then result.value[i] = infinity
               else if a.value[i] = 0.0 && b.value[i] = 0.0 then result.value[i] = nan
    }
  {
    shape = a.shape ;
    value = fun i -> if a.value[i] <> 0.0 && b.value[i] <> 0.0 then a.value[i] / b.value[i]
                     else if a.value[i] <> 0.0 && b.value[i] = 0.0 then infinity
                     else nan ;
  }
  
end
```

#### Numerical Accuracy
Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

###### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of an operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$). For $Y = A/B$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ combines contributions from both $A$ and $B$:

- For every $I$ such that $B[I] \neq 0$ and $B[I]$ does not cross zero under perturbation:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le \left|\frac{A_{\textit{err}}[I]}{B[I]}\right| + \left|\frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]^2}\right|$

- If $B[I]$ and $B[I] + B_{\textit{err}}[I]$ have different signs, the bound may be unbounded (division by a near-zero denominator).

###### Error Introduction
Error introduction for real (ideal) arithmetic is null:
- $Y_{\textit{err}}^{\textit{intro}} = [0]$.



###### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

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


---

<a id="float"></a>
# $\text{div}$ (float, float)
where float could be (`FP16`, `FP32`, `FP64`, `BFLOAT16`)

### Signature

Definition of operator $\text{div}$ signature:

$Y = \text{div}(A, B)$

where

 - $A$: float numerator tensor
 - $B$: float denominator tensor
 - $Y$: output float tensor, result of element-wise division of `A` by `B`
 
Arguments have different names. For instance 

### Restrictions
The following restrictions apply to the `Div` operator for the SONNX profile:

| Restriction | Statement                                                         | Origin                                                                                                          |
| ----------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `[R1]`      | Input and output tensors shall have the same shape                | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]`      | Inputs `A`, `B` and output `Y` shall have the same numerical type | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[GR1]`     | Sparse tensors are not supported                                  | General restrictions ([gen.restrict](../general_restrictions.md))                                                       |

#### Informal specification

> Operator $\text{div}$ divides input tensors $A$ and $B$ element-wise according to IEEE 754 floating-point semantics, placing the result in output tensor $Y$. Each element $Y[i]$ is computed as follows:

$$
Y[i] = 
\begin{cases} 
\frac{A[i]}{B[i]} & \text{if } A[i] \text{ and } B[i] \text{ are different from 0} \\
\text{inf} & \text{if } A[i] \neq 0 \text{ and } B[i]=0  \\
\text{nan} & \text{if } A[i]=0 \text{ and } B[i]=0 
\end{cases}
$$


Examples:


---

### Example 1 (division by zero → inf)

```math
A = \begin{bmatrix} 3.0 & 4.5 \\ 16.0 & 1.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0 & 2.25 \\ 4.0 & \infty \\ 5.1 & 6.0625 \end{bmatrix}
```

---

### Example 2 (zero divided by zero → NaN)

```math
A = \begin{bmatrix} 3.25 & 4.5 \\ 16.0 & 0.0 \\ 25.5 & 24.25 \end{bmatrix}
\quad
B = \begin{bmatrix} 3.0 & 2.0 \\ 4.0 & 0.0 \\ 5.0 & 4.0 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 1.0833 & 2.25 \\ 4.0 & \text{NaN} \\ 5.1 & 6.0625 \end{bmatrix}
```

---





Note in Python it is equivalent to do:
```python
>>> import numpy as np
A = np.array([[3.0, 4.5], [16.0, 1.0], [25.5, 24.25]], dtype=np.float32)
B = np.array([[3.0, 2.0], [4.0, 0.0], [5.0, 4.0]], dtype=np.float32)
np.divide(A, B) # inf/nan appear according to IEEE 754
```

#### Error conditions
- for float computations 
  - Division by zero is defined as IEEE 754 infinity or NaN depending on numerator.

#### Inputs

##### $\text{A}$: `floating-point tensor`
Tensor $A$ is the numerator of the division.

###### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` &lt;Shape consistency&gt;
   - Statement: &lt;Tensors $A$, $B$ and $Y$ shall have the same shape.`[R1]`&gt;.
 - `[C2]` &lt;Type consistency&gt;
   - Statement: &lt;Tensors $A$, $B$, and $C$ share the same floating-point type. `[R2]`&gt;.   
   

 
##### $\text{B}$: `floating-point tensor`
Tensor $B$ is the denominator of the division.

##### Constraints
 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.
 - `[C3]` &lt;Floating-point range and special values&gt;
   - Statement: &lt;Division by zero results in $\infty$ or NaN as defined above.&gt;.

### Outputs

##### $\text{Y}$: `floating-point tensor`

Tensor $Y$ is the element-wise result of $A$ divided by $B$.

##### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.

#### Attributes

The $\text{div}$ operator does not require any attributes.

 #### Formal specification
 
The formal specification of the `div` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Div operation on tensors with floating-point semantics.
 *)

module DivFloat
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor
  use real.Real
  use real.Inf
  use real.NaN
  use real.Div

  let function div (a : tensor real) (b : tensor real) : tensor real
    requires { a.shape = b.shape }
    ensures  { result.shape = a.shape }
    ensures  {
      forall i.
        if a.value[i] <> 0.0 && b.value[i] <> 0.0 then result.value[i] = a.value[i] / b.value[i]
        else if a.value[i] <> 0.0 && b.value[i] = 0.0 then result.value[i] = infinity
        else if a.value[i] = 0.0 && b.value[i] = 0.0 then result.value[i] = nan
        else result.value[i] = 0.0
    }
  {
    shape = a.shape ;
    value = fun i ->
      if a.value[i] <> 0.0 && b.value[i] <> 0.0 then a.value[i] / b.value[i]
      else if a.value[i] <> 0.0 && b.value[i] = 0.0 then infinity
      else if a.value[i] = 0.0 && b.value[i] = 0.0 then nan
      else 0.0 ;
  }
  
end
```

#### Numerical Accuracy

For $Y = A / B$ with numerical errors $A_{\textit{err}}$, $B_{\textit{err}}$:

###### Error Propagation

  For all valid indexes $i$ where $B[i] \neq 0$ and $B[i] + B_{\textit{err}}[i]$ does not cross zero,

  $$
  |Y_{\textit{err}}^{\textit{propag}}[i]| \leq \left|\frac{A_{\textit{err}}[i]}{B[i]}\right| + \left|\frac{A[i] \cdot B_{\textit{err}}[i]}{B[i]^2}\right|
  $$

###### Error Introduction

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

---

<a id="int"></a>

# $\text{div}$ (int, int)
where int could be (`INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`)

### Signature
Definition of operator $\text{div}$ signature:

 $Y = \text{div}(A,B)$

 where
 - $A$: numerator of the division
 - $B$: denominator of the division
 - $Y$: result of the element-wise division of `A` by `B`
 
Arguments have different names. For instance 


### Restrictions
The following restrictions apply to the `Div` operator for the SONNX profile:

| Restriction | Statement                                                         | Origin                                                                                                          |
| ----------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `[R1]`      | Input and output tensors shall have the same shape                | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R2]`      | Inputs `A`, `B` and output `C` shall have the same numerical type | Restriction [Explicit types and shape](../../../deliverables/reqs/reqs.md#req-gr-000-explicit-types-and-shapes) |
| `[R3]`      | Division by zero is undefined                                     | Integer semantics (implementation-dependent handling)                                                           |
| `[GR1]`     | Sparse tensors are not supported                                  | General restrictions ([gen.restrict](../general_restrictions.md))                                                       |

Overflow behavior is implementation-defined.

#### Informal specification

> Operator $\text{div}$ computes element-wise integer division with floor semantics where defined.

For every index $i$:

$$
Y[i] = 
\begin{cases} 
\left\lfloor \frac{A[i]}{B[i]} \right\rfloor & \text{if } B[i] \text{ is different from 0} \\
\text{undefined} & \text{otherwise}
\end{cases}
$$

Note:
- $\left\lfloor X \right\rfloor$ means the floor of $X$.
- "undefined" is implementation-dependent.


Examples:

Example 1:

```math
A = \begin{bmatrix} 6 & 9 & 35 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 3 & 5 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
```

Example 2:

```math
A = \begin{bmatrix} 10 & 10 \\ 21 & 1 \\ 30 & 9 \end{bmatrix}
\quad
B = \begin{bmatrix} 3 & 2 \\ 4 & 1 \\ 5 & 4 \end{bmatrix}
```

```math
Y = \begin{bmatrix} 3 & 5 \\ 5 & 1 \\ 6 & 2 \end{bmatrix}
```

#### Error conditions
- for integer computations 
  - Division by zero is undefined and shall be prevented.

#### Inputs

##### $\text{A}$: `integer tensor`

Tensor $A$ is the numerator of the division.

###### Constraints
This section gives all constraints applicable to the input.

 - `[C1]` &lt;Shape consistency&gt;
   - Statement: &lt;Tensors $A$, $B$ and $Y$ must have the same shape.`[R1]`&gt;.
 - `[C2]` &lt;Type consistency&gt;
   - Statement: &lt;Tensors $A$, $B$, and $C$ share the same integer type. `[R2]`&gt;. 


##### $\text{B}$: `integer tensor`

Tensor $B$ is the denominator of the division.

###### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.
 - `[C3]` &lt;integer range and special values&gt;
   - Statement: &lt; $B$ must not contain zero elements.`[R3]`&gt;.


#### Outputs

##### $\text{Y}$: `integer tensor`

Tensor $Y$ is the element-wise integer division result.

###### Constraints

 - `[C1]` &lt;Shape consistency&gt; : See constraint on $A$.
 - `[C2]` &lt;Type consistency&gt; : See constraint on $A$.

#### Attributes

The $\text{div}$ operator does not require any attributes.

 #### Formal specification
The formal specification of the `div` operator using the Why3 language[^1] is provided below. This specification ensures the consistency and desired behavior of the operator within the constraints described.

```ocaml
(**
    Specification of Div operation on tensors with integer semantics.
 *)

module DivInt
  use int.Int
  use map.Map
  use utils.Same
  use tensor.Shape
  use tensor.Tensor

  let function div (a : tensor int) (b : tensor int) : tensor int
    requires { a.shape = b.shape }
    requires { forall i. b.value[i] <> 0 }
    ensures  { result.shape = a.shape }
    ensures  { forall i. result.value[i] = a.value[i] / b.value[i] }

  {
    shape = a.shape ;
    value = fun i -> if b.value[i] <> 0 then a.value[i] / b.value[i]
                     else assert False; (* Enforces undefined behavior *) ;
  }
end
```

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
  return (B[I].int != 0) ? A[I] / B[I] : /* undefined */ SymbolicDomainError::undef();
};

for (auto I : A.indexes()) {
   auto a = A[I];
   auto b = B[I];
   if (b.int != 0 && b.int + b.err != 0) {
      auto c = result(I);
      double bound = std::abs(a.err / b.int) + std::abs(a.int * b.err / (b.int * b.int));
      assert(std::abs(c.err) <= bound + 0);
   }
}
```
[^1]: See [Why3 documentation](https://www.why3.org/)
