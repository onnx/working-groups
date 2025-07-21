Reviewer: Jean Souyris

# Introduction

This document gives guidelines to be followed when writing an operator's 
- informal specification
- formal specifications. 

# Informal specification

> Remark 1: I propose to change the title "informal specification" to "Guidelines for the informal specification" or "Informal specification guidelines". Same remark for the future guidelines for the formal specification.

> Remark 2: I propose to rename the two level-2 sub-sections "General recommendations" and "Structure" into "General guidelines" and "Structure of the informal specification" and to present them here as follows:
> 
> This section is composed of two sub-sections:
> - "General guidelines", which expresses general recommendations, defines the use of specific fonts, some notations (e.g., for tensor) and tags (e.g., for constraints), and, finally, specifies how to deal with the numerical types involved in the operator at stake.
> - "Structure of the informal specification", which defines the structure and contents of the informal specification of an operator. This section makes use of the guidelines expressed in sub-section "General guidelines".

## General recommendations

### Keep it simple!

> Remark 1: I propose to change the title "Keep it simple" to "General recommendations"

> Remark 2: since we now have precise and detailed guidelines, this section should be adapted. Indeed, the simplicity should come from the strict application of the guidelines. The risk in keeping this section as it is, is to minimize the importance of the informal specification, e.g., part of the verification of the formal one will be performed against it.
> 
> Proposal for the whole contents of this section:
> 
> The informal specification is intended for readers who want to know how to use an operator, as well as for the ones who need to implement and verify a neural network from an ONNX model. For instance, the first kind of readers might be satisfied with one or two sentences about the semantics of an operator whereas the second category of readers would like to get all the details of the semantics.
> 
> More precisely, the informal specification:

> - Is aimed at showing clearly what a given operator is supposed to do,
>   - Without calling on a strict formal, mathematical language,
>   - Knowing that the exact and complete specification is given in the "formal" part.
> - May provide diagrams and examples to make things clear.

> The writer of the informal specification of an operator shall have constantly in mind the following recommendation: "Keep it simple!", while applying the rules expressed in the guidelines.

> Remove the following five bullets.
> 
- Basically, the informal specification is a documentation, an "operator user's manual". 
- It is aimed at showing clearly what a given operator is supposed to do, but without calling on a strict formal, mathematical language. 
- The exact and complete specification is given in the "formal" part.
- The informal specification shall use greek with extreme parsimony ;-)
- The informal specification can provide diagrams and examples to make things clear.
  
> End of proposal.
> 
### Fonts
- Inputs, outputs, and attributes are represented using a non-serif font. For instance, the "pads" attribute is represented by `pads`.

### Notations

> Remark 1: the term "shape" should be used instead of dimensions.

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
- A **constraints tag** expresses a constraint on one or several inputs, output or attribute. They are indicated using `[C<i>]` where `<i>` is a number.
- A **traceability tag** identifies a specific location in the informal specification. These tags are used to establish a traceability between the informal and formal specification. They are indicated using `T<i>` where `<i>` is a number.

> Remark 1: add [] around `T<i>`.
> Remark 2: give an example of the declaration and use of a tag.

### Types
- All operators applicable to numeric values shall be specified for values in the domain of real numbers. 
- Specific description may be given for the other types (``float``, ``double``, etc.).
- A description can be applicable to a set of types as long as its **semantics description** remains the same for all types in the set. A counter example is, for instance, the case of operators applied on ``float`` or ``double`` that may create ``NaNs`` or ``+Inf`` or ``-Inf``. For this reason, they cannot be covered by the specification in $R$.
- Only the sections that need to be modified are repeated.
  
> Remark 1: explicit the above sentence. See MatMul.

## Structure

> Remark 1: I propose to change the title of this section to "Structure of the informal specification"

The specification on an operator is structured as follows. 

> Remark 2: introduce the "Contents" section as in MatMul.
> 
> Proposal:
 
> ### Contents

> *This section lists the various per input set of types informal specifications of the operator at stake. Only the first line below is mandatory, i.e., the one for real inputs. Any subsequent line comes from the necessity to specialize the informal specification for the real to machine types*

> - `<Name of the operator>` [operator (real)](#real)
> - `<Name of the operator>` [operator (comma-separated list of types)]
> - `<Name of the operator>` [operator (other comma-separated list of types)]
> - etc

> Example (MatMul):
>
> Contents
- `MatMul` [operator (real)](#real)
- `MatMul` [operator (FP16, FP32, FP64, BFLOAT16)](#float)
- `MatMul` [operator (INT4, INT8, INT16, INT32, INT64, UINT4, UINT8, UINT16, UINT32, UINT64)](#int)

> End of proposal.

### Signature
*Definition of the operator's signature:*

 `<O> = <op>(<I1>,<I2>,...<In>)`

 where
 - `<In>`: &lt;Brief description of the nth input &gt;
 - `<O>`: &lt;Brief description of output &gt; 

### `<operator name>`  `(<list of types for which this description is applicable>)`

> Remark 1: an introductory text should describe the contents of this kind of section by relating it to the Contents section above.

#### Restrictions
*This section lists all restrictions applicable to the operator. A restriction is a limit with respect to the normal usage domain of the ONNX operator. A restriction may concern the dimension of tensors, values of attributes, etc. They are introduced to simplify the implementation of operators, ensure resource usage predictability, enforce explicitness, etc.*

> Remark 1: the verb "simplify" and, later in this section, the notion of "simplification" appear either inside the notion of "restriction" or aside this notion. Furthermore, the term "simplification" might be misinterpreted by the readers. Therefore I propose not to talk about "simplification" as a category but to split the notion of restriction into two categories:
> - "Dependability restrictions": the restrictions for dependability reasons.
> - "Other restrictions": the restrictions that aim at limiting the operator specification effort for the first delivery of SONNX. The restrictions of this second category are acceptable only if they do not prevent the operator at stake from being used in a sufficiently large domain.   


*An example is given hereafter*

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor `X` has 2 spatial axes | Simplification |
| `[R2]` | Attribute `auto_pad` is restricted to `NOTSET`  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

*We discriminate **simplifications** from **restrictions*** as follows:
- Simplifications are introduced to reduce the amount of work for the workgroup and is aimed at being eventually removed. They are not traceable to a requirement.
  
> Remark 2: see remark 1 in this section. I propose to "merge" the text into the Remark 1 proposal.
>
> Remark 3: give an example of "Other restrictions".

- Restrictions are introduced to comply with some requirement. The requirement is identified using an hyperlink.

   
 ##### Informal specification
 
 *This section contains the informal specification of the operator. By "informal", we mean that the description does not rely on a formal language, even though it will usually include mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include figures if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.*

> Remark 1: a more precise template should be proposed for this section. Indeed, some of the remarks and exchanges we had about the informal specification of concat, including the ones with Loïc, should be introduced here.

> Proposal:
> 
> The informal specification shall be composed of the following parts:

> - One or two sentences that give a synthesis of what the operator does

    Example: "Operator conv computes the convolution of the input tensor X with the kernel W and adds bias B to the result. Two types of convolutions are supported: standard convolution and depthwise convolution."

> - The mathematical description that:
>   - Uses the notations proposed in section Notations of these guidelines
>   - Implements the traceability tags proposed in Section Tag of these guidelines
>   - Structures the mathematical formulae according to the following pattern: the complete formula is first given and its atomic elements and sub-expressions are defined afterward, by introducing them with "Where" or "In which"
        
> Example of mathematical description (convolution):

$$\begin{gathered}
    Y[b, c, m, n] = \sum_{i=0}^{fm(W)-1} \sum_{j=0}^{h(W)-1} \sum_{z=0}^{w(W)-1} (X[b,i,m \cdot strides[0]+ j \cdot dilations[0], n \cdot strides[1]+ z \cdot dilations[1]] \cdot W[c, i, j, z]) + B[c]
\end{gathered}$$

> Where
- >$b$ is the batch index, $b \in [0,b(Y)-1]$, $b(Y)$ is the batch size of output `Y`
- > $c$ is the data channel, $c \in [0,c(Y)-1]$, $c(Y)$ is the number of data channels of output `Y`
- > etc

 
##### Error conditions

*This section identifies the errors that may occur during the execution of the operator (or *runtime errors*).*

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

##### Inputs

This section describes the operator's inputs.
 
###### `<name>`: `<type>`

where `<name>` is the name of the input and `<type>` is the type of the input.

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



