# Introduction

This document gives the guidelines to be followed when writing an operator's **informal** and **formal** specification.

Nota: as of July 2025, guidelines are limited to the *informal* specification. 

# Informal specification guidelines
This section is composed of two sub-sections:
- *General guidelines*, which defines the use of fonts, notations (e.g., for tensor) and tags (e.g., for constraints), and, finally, specifies how to deal with the numerical types involved in the operator at stake.
- *Structure of the informal specification*, which defines the structure and contents of the informal specification of an operator. This section applies the general guidelines.

## General guidelines  
The informal specification is intended for both users *and* implementers  of operators who both need to understand what an operator does and how to use it. For instance, the first kind of readers might be satisfied with one or two sentences about the semantics of an operator whereas the second category of readers would like to get all the details of the semantics.

More precisely, the informal specification:
- Is aimed at showing clearly what a given operator is supposed to do,
- Without calling on a strict formal, mathematical language,
- Knowing that the exact and complete specification is given in the "formal" part.
- May provide diagrams and examples to make things clear.

The writer of the informal specification must take care to keep it readable and understandable by a ML developer. The recommendations given in the following guidelines target this objective.

### Fonts
- Inputs, outputs, and attributes are represented using a non-serif font. For instance, the "pads" attribute is represented by `pads`.

### Notations
#### Tensors
- A tensor is always represented in uppercase letters (e.g., $A, B,...,X, Y, Z$).
- In cases where this naming convention does not match the one used by ONNX, a correspondence table may be established (e.g., $dX_2$ corresponds to the "width" of tensor $X$).
- Output tensor is usually named $Y$
- In the case of a variadic operator (e.g., "concat"), the tensor parameters are designated by an index: $A_0$, $A_1$, etc. Indexes start at 0 to be consistent with the other use of indexes. 
- The shape of a tensor $A$ is denoted by a vector $(dA_0, ..., dA_i, ..., dA_n)$ where $dA_i$ refers to the dimension along axis $i$. The index of the first axis is 0.
- For a tensor used as a variadic parameter (denoted $A_i$), the shape is denoted by $(dA_{i,0}, dA_{i,1}, ...)$.
#### Errors
- The numerical errors of a tensor $A$ are always represented by a tensor $A_{\textit{err}}$ that is the difference between the tensor $A_{\textit{impl}}$ computed by some implementation and the infinitely accurate tensor $A_{\textit{real}}$ expressed by the formal specification for real numbers.
  - In the section on numerical accuracy, the notation $A_{\textit{real}}$ is replaced by $A$ unless it introduces ambiguity.

#### Tags
The informal specification makes use of three different types of tags:
- A **restrictions tag** expresses a restriction with respect to the ONNX standard (see the section about restriction below). They are indicated by tag `[R<i>]` where `<i>` is a number.\
A synthesis of all restrictions is given in section "Restrictions" (see below).
- A **constraints tag** expresses a constraint on one or several inputs, outputs, or attributes. They are indicated using `[C<i>]` where `<i>` is a number.
- A **traceability tag** identifies a specific location in the informal specification. These tags are used to establish traceability between the informal and formal specifications. They are indicated by `[T<i>]` where `<i>` is a number. For instance, here is a tag introducing a constraint relating the input and output tensors for the `Abs` operator:
>`[C1]` Shape consistency \
> Statement: Tensor $A$ and $Y$ shall have the same shape.
  
When part of the documentation refers to a tag, an hyperlink is used. This is achieved using the following elements: 
```
  `[T1]`<a name="my_tag_name"></a>
```
   to declare the location of the tagged element and 
  ```
  [`[T1]`](#my_tag_name).
```
to refer to the tagged element. 

Here is an example: <br>
`[T1]` <a name="my_tag_name"></a> This is a tagged paragraph.

This is a reference to the tagged paragraph  [`[T1]`](#my_tag_name).


### Types
- All operators applicable to numeric values shall be specified for values in the domain of real numbers. 
- Specific description may be given for the other types (`float`, `double`, etc.).
- A description can be applicable to multiple types as long as its **semantics description** remains the same for all types. A counter example is, for instance, the case of operators applied on `float` or `double` that may create `NaNs` or `Infs`. For this reason, they cannot be covered by the specification in $\mathbb R$.
- In order to reduce the size and complexity of the specifications, the description of the semantics of an operator for type T may refer explicitly to the semantics of the same operator for another type T' (typically: the semantics in $\mathbb R$).  

## Structure of the informal specification

The specification on an operator is structured as follows. 

### Contents

This section gives the list of all informal specifications of the operator, for each of the applicable types. 

- $\text{op}$ operator for type real
- $\text{op}$ operator for types &lt;T1&gt;, &lt;T2&gt;,...
- $\text{op}$ operator for types &lt;T1&gt;, &lt;T2&gt;,...
- etc

Here is an example for operator $\text{MatMul}$:
> Contents
>- $\text{MatMul}$ operator for type real
>- $\text{MatMul}$ operator for types `FP16`, `FP32`, `FP64`, `BFLOAT16`
>- $\text{MatMul}$ operator for types `INT4`, `INT8`, `INT16`, `INT32`, `INT64`, `UINT4`, `UINT8`, `UINT16`, `UINT32`, `UINT64`

The following section must be repeated for each set of types for which the semantics is the same. One section corresponds to one entry in the "Contents" list. 

## $\text{op}$  (`<type 1>`, `<type 2>`,...)

### Signature

Definition of operator $\text{op}$ signature:

 $O = \text{op}(X,Y,...,Z)$

 where
 - $X$: Brief description of argument $X$
 - $Y$: Brief description of argument $Y$
 - ...
 - $O$: Brief description of output 
 
Arguments have different names. For instance 

$Y = \text{add}(X, Y)$

When the same name is used for different arguments such as in 

 $Y = \text{concat}(X_1,X_2,...,X_n)$

 this means that the operator is **variadic**, i.e., it accepts a variable number of arguments. In this example, there are n arguments that are discriminated by their index.  

#### Restrictions
This section lists all restrictions applicable to the operator. A restriction is a limit with respect to the normal usage domain of the ONNX operator. A restriction may concern the dimension of tensors, values of attributes, etc. 

Restrictions marked as "Transient" are introduced by the working group in order to reduce the specification effort. Such restrictions, which are not traceable to a need, are normally aimed at being eventually relaxed. However, in the meantime, both transient and non-transient restrictions are applicable by the operator user or implementer. 

Restrictions not marked as "transient" are traceable to some requirement. The requirement is identified using an hyperlink.
 
An example is given hereafter

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` | Attribute `auto_pad` is restricted to `NOTSET`  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

 #### Informal specification
 
 This section contains the informal specification of the operator. By "informal", we mean that the description does not rely on a formal language, even though it usually uses some mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include figures if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.
 
The informal specification shall be composed of the following parts:
- A short description of the operator. For instance, for the $conv$ operator: 

> Operator $\text{conv}$ computes the convolution of the input tensor $A$ with the kernel $W$ and adds bias $B$ to the result. Two types of convolutions are supported: standard convolution and depthwise convolution.

- A detailed description that:
  - Uses the notations proposed in section "Notations" of these guidelines
  - Implements the traceability tags proposed in Section "Tags" of these guidelines
  - Presents the mathematical formulae, if necessary, according to the following pattern: the complete formula is first given and its atomic elements and sub-expressions are defined afterward, by introducing them with "Where" or "In which".
        
For instance, for the $\text{conv}$ operator:

> $$\begin{gathered}
    Y[b, c, m, n] = \sum_{i=0}^{dW_1-1} \sum_{j=0}^{dW_2-1} \sum_{z=0}^{dW_3-1} \\ (X_p[b,i,m \cdot \text{strides}[0]+ j , n \cdot \text{strides}[1]+ z ] \cdot W_d[c, i, j, z]) \\ + B_b[c]
\end{gathered}$$

> Where
>- $b \in [0,dY_0-1]$ is the batch index. $dY_0$ is the batch size of output $Y$
>- $c \in [0,dY_1-1]$ is the data channel. $dY_1$ is the number of data channels of output $Y$
>- $m \in [0,dY_2-1]$ is the index of the first spatial axis of output $Y$
>- $n \in [0,dY_3-1]$ is the index of the second spatial axis of output $Y$
>- etc.

#### Error conditions

This section identifies the errors that may occur during the execution of the operator (or *runtime errors*).

When writing a specification, the writer must identify the conditions where the following conditions may occur:
- for floating point computations 
  - an invalid operation as defined in IEEE 754 section 7.2, i.e.
    - multiplication $(0, \infty)$ or multiplication $(\infty, 0)$ 
    - addition or subtraction or fusedMultiplyAdd: magnitude subtraction of infinities, such as addition $(+\infty, -\infty)$ 
    - division $(0, 0)$ or division ($\infty, \infty)$
    - remainder(x, y), when y is zero or x is infinite and neither is a NaN
    - square root if the operand is less than zero
    - etc. Refer to the standard for a complete list of error conditions.
- for integer computations 
  - division by zero,
  - operations leading to a value out of the range (e.g., addition of two large `int32` values non representable in `int32`)

This section shall indicate if an operator can potentially return a `NaN` or `Inf`. It is is the case, the condition that might lead to this situation must be described.

If the section is left empty, it means that **not error condition can occur**.

#### Inputs

This section describes the operator's inputs.
 
##### $\text{name}$: `<type>`

where $\text{name}$ is the name of the input and `<type>` is the type of the input.

###### Constraints
This section gives all constraints applicable to the input.

- When a constraint involves several inputs/outputs/attributes, it is only described once when the first input or attribute concerned by the constraint is described. Then, for the other inputs, attributes, or outputs concerned by the same constraint, a cross-reference is given. 
The description is structured as follows:*

 - `[C<i>]` &lt;Title of constraint&gt;
   - Statement: &lt;Expression of the constraint&gt; or cross-reference to the previous location where this constraint was first introduced.
   - Rationale: &lt;Justification for the constraint&gt;. When the title and/or the statement of the constraint are sufficiently explicit, the rationale may be omitted. 

#### Attributes
This section describes the operator's attributes. 

##### $\text{name}$: `<type>`
where $\text{name}$ is the attribute's name and `<type>` is the attribute's type.

 ##### Constraints
Same as for the inputs.

 #### Output
 This section describes the operator output.

##### $\text{name}$: `<type>`
where $\text{name}$ is the output's name and `<type>` is the output's type.

 ##### Constraints
Same as for the inputs.
 
 #### Formal specification
 
This section contains a link to the formal specification expressed in Why3.
 
#### Numerical Accuracy
 
This section provides a tight and verifiable specification of the numerical error
on the operator's results. It decomposes the error into two parts:
the first, the propagated error, depends on the numerical error and the
numerical values of the inputs ; the second part, the introduced error,
depends only on the numerical value of the inputs.

The provided specification results from an over-approximated semantics (ex: IEEE-754) of the
numerical error of native computer operations approximating real number
operations. In order to preserve the readability of the formulas, the general specification introduces additional (conservative) simplifications compared to the original specifications.
However, this general specification may be too over-approximated for some specific inputs (ex tensor representing diagonal matrices). In this case, more precise specific specifications are provided alongside the general specification.

The error specification comes with unit verification scenarios to verify the implementation's conformity. In the absence of value ranges for the inputs, the unit verification scenarios operate on symbolic values and errors to propagate correct formulas throughout the scenario and thus provide a proof for the assertions. In particular, the C implementation generated from the Why3 formal specification must be verified using these scenarios, for example by using symbolic instrumentation libraries.

###### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of an operator.

###### Error Introduction

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$, the introduced error, where $Y$ is the tensor result of an operator.

Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

###### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

# Formal specification guidelines

*To be completed.*
