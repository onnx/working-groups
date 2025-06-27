# Introduction

This document gives guidelines to be followed when writing an operator's 
- informal specification
- formal specifications. 

# Informal specification

## General recommendations  

### Keep it simple!

- Basically, the informal specification is a documentation, an "operator user's manual". 
- It is aimed at showing clearly what a given operator is supposed to do. 
- The exact and complete specification is given in the "formal" part.
- The informal specification shall use greek with extreme parsimony ;-)
- The informal specification can provide diagrams and examples to make things clear.

### Fonts
- Inputs, outputs, and attributes are represented using a non-serif font. For instance, the "pads" attribute is represented by `pads`.

### Notations
- Tensors: 
  - A tensor is always represented in uppercase name (e.g., A, B,...,X, Y, Z).
  - Input tensors are usually $A$, $B$,...
  - Output tensor is $Y$
  - In the case of a variadic operator (e.g., "concat"), the tensor parameters are designated by an index: $X_0$, $X_1$, etc. Indexes start at 0 to be consistent with the other use of indexes. 
  - The dimensions of a tensor $X$ are denoted by a vector $(dX_0, ..., dX_i, ..., dX_n)$ where $dX_i$ refers to the dimension along axis $i$. The index of the first axis is 0.
  - The numerical errors of a tensor $X$ are always represented by a tensor $X_{\textit{err}}$.
    It is the difference between the tensor $X_{\textit{impl}}$ computed by an implementation
    and the infinitly accurate tensor $X_{\textit{real}}$ expressed by the formal specification.
    In the section on numerical accuracy, the notation $X_{\textit{real}}$ is replaced by $X$ unless it introduces ambiguity.
  - For a tensor used as a variadic parameter (denoted $X_i$), the dimensions become $(dX_{i,0}, dX_{i,1}, ...)$. This notation is consistent with the way tensor dimensions are encoded in Why3.
  - In cases where this naming convention does not match the one used by ONNX, a correspondence table may be established (e.g., $dX_2$ corresponds to the "width" of tensor $X$).

### Tags
The informal specification makes use of three different types of tags:
- A **restrictions tag** expresses a restriction with respect to the ONNX standard (see the section about restriction below). They are indicated in the text with the tag `[R<i>]` where `<i>` is a number.\
A synthesis of all restrictions is given in section "Restrictions" (see below).
- A **constraints tag** expresses a constraint on one or several inputs, ouptu or attrinute. They are indicated using `C<i>` where `<i>` is a number.
- A **traceability tag** identifies a specific location in the informal specificarespecification. These tags are used to establish a traceability between the informal and formal specification. They are indicated using `T<i>` where `<i>` is a number.

### Types
- All operators applicable to numeric values shall be specified for values in the domain of real numbers. 
- Specific description may be given for the other types (``float``, ``double``, etc.).
- A description can be applicable to as et of types as long as its **semantics description** remains the same for all types in the set. A counter example is, for instance, the case of operators applied on ``float`` or ``double`` that may create ``NaNs`` or ``+Inf`` or ``-Inf``. For this reason, they cannot be covered by the specification in $R$.
- Only the scetions that need to be modified are repeated.

## Structure

The specification on an operator is structured as follows. 


### Signature
*Definition of the operator's signature:*

 `<O> = <op>(<I1>,<I2>,...<In>)`

 where
 - `<In>`: &lt;Brief description of the nth input &gt;
 - `<O>`: &lt;Brief description of output &gt; 

### `<operator name>`  `(<list of types for which this description is applicable>)`

 
#### Restrictions
*This section lists all restrictions applicable to the operator. A restriction is a limit with respect to the normal usage domain of the ONNX operator. restriction may concern the dimension of tensors, values of attributes, etc. They are introduced to simplify the implementation of operators, ensure resource usage predictability, enforce explicitness, etc.*  

*An example is given hereafter*

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor `X` has 2 spatial axes | Simplification |
| `[R2]` | Attribute `auto_pad` is restricted to `NOTSET`  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

*We discriminate **simplifications** from **restrictions*** as follows:
- Simplifications are introduced to reduce the amount of work for the workgroup and is aimed at being eventually removed. They are not traceable to a requirement.
- Restrictions are introduced to comply with some requirement. The requirement is identified using an hyperlink.

   
 ##### Informal specification
 
 This section contains the informal specification of the operator. By "informal", we mean that the description does not rely on a formal language, even though it will usually include mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include figures if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.
 
##### Inputs

This section describes the operator's inputs.
 
###### `<name>`: `<type>`

where `<name>` is the attribute's name and `<type>` is the type of the attribute.

##### Attributes

- This section describes the operator's attributes.
- It also gives all constraints applicable to the input/output/attribute (if any). 
- When a constraint involves several inputs/outputs/attributes, it is only be described for the first one and will be cross-referenced in the "constraint" section of the other ones..\
The description is structured as follows:*

 - (C&lt;i&gt;) &lt;Title of constraint&gt;
   - Statement: &lt;Expression of the constraint&gt;
   - Rationale: &lt;Justification for the constraint&gt;

###### `<name>`: `<type>`

where `<name>` is the attribute's name and `<type>` is the attribute's type.

 ###### Constraints

*(same as above)*

 ##### Output
 
 This section describes the operator output.

 ###### `<name>`: `<type>`

where `<name>` is the output's name and `<type>` is the output's type.

 
 ###### Constraints

 *(same as above)*
 
 ##### Formal specification
 
This section contains a link to the formal specification expressed in Why3.
 
##### Numerical Accuracy
 
This section provides a tight and verifiable specification of the numerical error
on the operator's results. It decomposes the error into two parts:
the first, the propagated error, depends on the numerical error and the
numerical values of the inputs ; the second part, the introduced error,
depends only on the numerical value of the inputs.

The provided specification results from an over-approximated semantics (ex: IEEE-754) of the
numerical error of native computer operations approximating real number
operations. In order to preserve the readability of the formulas, the general specification
introduces additional (conservative) simplifications compared to the original spectifiations.
However, this general specification may be too over-approximated for some specific inputs
(ex tensor representing diagonal matrices). In this case, more precise specific specifications
are provided alongside the general specification.

The error specification comes with unit verification scenarios to verify the implementation's
conformity. In the absence of value ranges for the inputs, the unit verification scenarios
operate on symbolic values and errors to propagate correct formulas throughout the scenario
and thus provide a proof for the assertions. In particular, the C implementation generated
from the Why3 formal specification must be verified using these scenarios, for example
by using symbolic instrumentation libraries.

###### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the
propagated error, where $Y$ is the tensor result of an operator.

###### Error Introduction

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$, the
introduced error, where $Y$ is the tensor result of an operator.

Hence $Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

###### Unit Verification

This section contains a verification scenario to verify the above specification
for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each
real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitly precise) C/C++ floating-point
  (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference
  between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference
  between the possible values of `float` and `real` divided by `real`.



