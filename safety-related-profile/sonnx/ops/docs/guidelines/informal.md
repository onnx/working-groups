# Introduction

This document gives the guidelines to be followed when writing an operator's non-formal specification. Guidelines for the development of formal specification are given in a [dedicated document](./formal.md).

# Rationales

The non-formal specification is first an entry-point for any *user* of the SONNX profile. Towards that goal, it must explain clearly the purpose of the operator, i.e., the relation between its inputs (arguments and attributes) and its outputs. Towards that goal, it may use whatever means deemed useful including text description, mathematical formulae, graphics, examples. 

It must also provide a clear statement about:
- the usage restrictions for the operator imposed by SONNX,
- the constraints on the arguments and attributes of the operator (or pre-conditions") that must be satisfied for the operator to be applicable, 
- the possible errors that may raise during the execution of the operator.

In the following paragraphs, we express some of the "principles" that we applied to eleborate the  guidelines.

#### About the level of formalization
The non-formal specifications aims at providing a clear and complete description of the behavior of the subset of operators considered in the SONNX profile. Understandability is favored over formalization, accordingly, the non-formal specification essentially relies on natural language, with mathematical formulae when deemed necessary. In addition, for each operator, a formal specification expressed using a formal language (Why3) is provided separately.  

#### About data types
The non-formal specification is given for all data types considered in SONNX i.e.: int8, uint8, int16, uint16, int32, uint32, int64, uint64, float, double and float64. In addition, SONNX also provides a specification of each (mathematical) operator for real numbers. This is aimed at facilitating the understanding of the core function of the operator without dealing with implementation-specific issues such as the effect of overflows (for ints and uints) or the handling of special float values (+Inf, -Inf, NaN, 0+, 0-).   

#### About floating point numbers

Floating point operations are specified in compliance with the the IEEE 754 standards (IEEE Standard for Floating-Point Arithmetic, IEEE Std 754 2019, IEEE). In particular, care is taken to describe the expected behaviour of mathematical operator when dealing with IEEE special values (+Inf, -Inf, +0+, -0, and NaN).

#### About the compliance with implementation standards

SONNX is essentially a specification effort. As such, it must remain independent from any specific implementation and, instead, must simply express the intended behavior of each operator according to some usual and/or consensual understanding of its semantics. However, tests realized by the SONNX WG on the implementations of some operators (e.g., **MaxPool**) show that the actual behavior sometimes differs significantly from the expected one, due to implementation choices or, sometimes, implementation bugs. 

Even if we consider that the SONNX specification shall not "reflect" a specific implementation, it shall preferably stick to the ONNX Runtime implementation when choices have to be made. When, for a given operator, the usual/consensual semantics and the ONNRtime implementation diverge, the SONNX WG choose to indicate this discrepancy. This is for instance the case for the **MaxPool** operator. 
Note also that the semantics of an operator in ONNX runtime may depend on the execution backend (CPU, GPU,...). 

#### About error conditions

An error condition is a condition leading to an unexpected result. Obviously, if the specification is clear and complete, all possible behaviour should be "expected". However, we consider worth being mentioned any result leading to 
- an "unexpected result", such as a division by zero in the  integer domain
- a NaN in the floating point domain *when this NaN is not simply the propagation of a NaN in the operator inputs*

In some cases, a pre-condition may be stated on the inputs so that, if the pre-condition is satisfied, then no error -- NaN, division by zero, etc. -- can occur. For instance, no division by zero can occur if the condition stating that "the denominator shall not be null" is satisfied.  Nevertheless, the possibility for an error to occur will still be signaled to the reader.

Systematically providing pre-conditions on the inputs to prevent error conditions was not considered useful for the end-user since operators are generally used in complex graphs for which verifying the preconditions to prevent the occurrence of error is not achievable in practice. 

#### About accuracy

The SONNX profile does not specify the accuracy of operators, instead, it provides guidance on how to analyze the propagation and introduction of errors on a given implementation and illustrates the approach on SONNX' reference implementation.

The analysis is carried out in two steps: 
- During step 1, an analysis is carried out to specify bounds on propagated and introduced errors considering the IEEE rounding error. This bounds may not be the tightest one, but a bound that can be determined with a reasonable analysis effort.  
- During step 2, an analysis of the code of an actual implementation (in our case, the reference implementation) is carried out using a tool developed for that purpose by one of the SONNX WG contributor (Franck Vedrine, [CEA List](www.cea.fr/)).

Please refer to the [specific set of guidelines](../../docs/guidelines/accuracy.md) are given for the analysis of accuracy.

# Specification guidelines
This section is composed of two sub-sections:
- *General guidelines* defining presentation rules such as fonts, notations, use of tags for tracability, etc. 
- *Structure and Contents of the specification* defining the organization and the contents of the non-formal specification of an operator. This section applies the general guidelines.

## General guidelines  
The non-formal specification is intended for both users *and* implementers of operators who both need to understand what an operator does and how to use it. For instance, the first kind of readers might be satisfied with one or two sentences about the semantics of an operator whereas the second category of readers would like to get all the details of the semantics.

More precisely, the non-formal specification:
- Is aimed at showing clearly what a given operator is supposed to do,
- Without calling on a strict formal, mathematical language,
- Knowing that the exact and complete specification is given in the "formal" specification.
- May provide diagrams and examples to make things clear.
- Follows ONNX nomenclature, which includes naming convention, for operator names, types, identifiers of operator inputs, outputs and attribute, etc.
  - Examples: 
    - The element-wise addition of tensors is $Add$, not $add$
    - The 16-bit floating-point type is $float16$, not $FP16$

The writer of the non-formal specification must take care to keep it readable and understandable by a ML developer. The recommendations given in the following guidelines target this objective.

### Styling
- Mathematical objects are represented using *italic*. LaTeX formulae are used.
- In the text, operator attributes are represented using `this font`.  
- As far as possible, names of arguments and attributes shall be used in mathematical formulae. In the case the name is "too long", another, shorter designation, may be used with a clear statement of the redefinition. If the symbol refers to a greek symbol (e.g., $\text{alpha}$), the symbol itself can be used (e.g., $\alpha$).  

### Basic operators

The specification may use some mathematical operators or functions without defining them. Those operators / functions are considered to be "well-known" so that there is no need to define them.

The following operators and functions belong to this set:
- basic mathematical operations: $+$, $-$, $*$, $/$
- trignonometric operations: $-x$, $\sin(x)$, $\cos(x)$, $\tan(x)$, $\exp(x)$, $\sqrt x$, $\ln(x)$, $x^y$, $|x|$
- $\min(x,y)$ and $\max(x,y)$
- logical operators: $\wedge$, $\vee$, $\lnot$ 
  

### Naming conventions
- As far as possible, ONNX names for inputs, outputs, and attributes must be used.

### Notations
#### Tensors
- A tensor is always represented in uppercase letters (e.g., $A, B,...,X, Y, Z$).
- In the case of a variadic operator (e.g., **Concat**), the tensor parameters are designated by an index: $A0$, $A1$, etc. Indexes start at 0 to be consistent with the other use of indexes. 
- The rank of a tensor $T$, i.e., the number of its dimensions, is denoted $rT$. 
- The shape of a tensor $A$ is denoted by a vector $(dA_0, ..., dA_i, ..., dA_n)$ where $dA_i$ refers to the dimension along axis $i$ and $n=rA-1$.
- For a tensor used as a variadic parameter (denoted $Ai$), the shape is denoted by $(dAi_{0}, dAi_{1}, ...)$.
- A specific element of a tensor is denoted:
  - either as: $A[i]$, where $i$ is a [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index)
  - or as: $A[i_0, i_1, ..., i_{rA-1}]$. 
 
#### Tags
The non-formal specification makes use of three different types of tags:
- A **restrictions tag** expresses a restriction with respect to the ONNX standard (see the section about restriction below). They are indicated by tag `[R<i>]` where `<i>` is a number.\
A synthesis of all restrictions is given in section "Restrictions" (see below).
- A **constraints tag** expresses a constraint on one or several inputs, outputs, or attributes. They are indicated using `[C<i>]` where `<i>` is a number.
- A **traceability tag** identifies a specific location in the non-formal specification. These tags are used to establish traceability between the informal and formal specifications. They are indicated by `[T<i>]` where `<i>` is a number.
 
For instance, here is a tag introducing a constraint relating some input and output tensors:
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
- The type names shall be the ones used in the ONNX description of the operators, without surrounding them with "tensor()".
  - Example: "tensor(double)" in ONNX becomes "double" in the non-formal specification.
- The data types allowed in SONNX operators are: 
  - IEEE 754 floating-point types: double, float, float16
  - Signed integer types: int64, int32, int16, int8
  - Unsigned integer types: uint64, uint32, uint16, uint8
  - bool
  - string
- IEEE 754 floating-point types, i.e., double, float and float16 have the following special numbers:
  - +0 and -0
  - +inf and -inf
  - NaN (Not a Number)
- All operators applicable to numeric values shall first be specified for values in the domain of real numbers, then specific descriptions shall be given for the other types (float, double, etc.).
- A description can be applicable to multiple types as long as its **semantics description** remains the same for all types.  

## Structure and contents of the specification

This section describes the required structure and contents of the non-formal specification of an operator.

The [specification template](informal_spec_template.md) gives an example of the required structure.

### Contents

This section gives the list of all non-formal specifications of the operator, for each of the applicable types, with hyperlinks to the sections (see [template](informal_spec_template.md)). 

- **Op** operator for type real
- **Op** operator for types &lt;T1&gt;, &lt;T2&gt;,...
- **Op** operator for types &lt;T1&gt;, &lt;T2&gt;,...
- etc.

The reference, with link, to the ONNX definition of **Op** shall be inserted in this section. See **Div** example below. 

Here is an example for operator **Div**:
> Contents
>- **Div** operator for type real
>- **Div** operator for types float16, float32, float64
>- **Div** operator for types int8, int16, int32, int64, uint8, uint16, uint32, uint64
>
> Based on ONNX [Div version 14](https://onnx.ai/onnx/operators/onnx__Div.html).

The following section must be repeated for each set of types for which the semantics is the same. One section corresponds to one entry in the "Contents" list. 

## **Op**  (<type 1>, <type 2>,...)

### Signature

Definition of operator **Op** signature:

 $O = \textbf{Op}(X,Y,...,Z)$

 where
 - $X$: Brief description of argument $X$
 - $Y$: Brief description of argument $Y$
 - ...
 - $O$: Brief description of output 
 
Arguments shall have different names. For instance 

$O = \textbf{Op}(X, Y)$

When the same name is used for different arguments such as in 

 $O = \textbf{Op}(X0,X1,...,XL)$

 this means that the operator is **variadic**, i.e., it accepts a variable number of arguments. In this example, there are n arguments that are discriminated by their index.  

### Restrictions
This section lists all restrictions applicable to the operator. A restriction is **a limit with respect to the normal usage domain** of the ONNX operator. A restriction may concern the dimension of tensors, the values of attributes, etc. 

Some SONNX restrictions apply to all the operators. Therefore, this section shall contain the following markdown link:

`\[General restrictions](../common/general_restrictions.md)`

Restrictions marked as "Transient" are introduced by the working group in order to reduce the specification, proof, etc. effort. Those restrictions, which are not traceable to a need, are aimed at being eventually relaxed. However, in the meantime, both transient and non-transient restrictions are applicable by the operator user or implementer. 

Restrictions not marked as "transient" are traced to some [end-user requirement](../../../../deliverables/reqs/reqs.md) using an hyperlink.
 
An example is given hereafter

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` | Attribute `auto_pad` is restricted to NOTSET  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

 ### Specification
 
 This section contains the specification of the operator. The specification is "informal", ie., it does not use a formal language, even though it usually uses some mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include illustrations if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.
 
The specification shall be composed of the following parts:
- A short description of the operator. For instance, for the $Conv$ operator: 

> Operator **Conv}** computes the convolution of the input tensor $A$ with the kernel $W$ and adds bias $B$ to the result. Two types of convolutions are supported: standard convolution and depthwise convolution.

- A detailed description that:
  - Uses the notations proposed in section "Notations" of these guidelines
  - Implements the traceability tags proposed in Section "Tags" of these guidelines
  - Presents the mathematical formulae, if necessary, according to the following pattern: the complete formula is first given and its atomic elements and sub-expressions are defined afterward, by introducing them with "Where" or "In which".
  - Insert a blank line before and after each formula so that it renders correctly in the browser.
        
For instance, for the **Conv** operator:

> $$
    Y[b, c, m, n] = \sum_{i=0}^{dW_1-1} \sum_{j=0}^{dW_2-1} \sum_{z=0}^{dW_3-1} \\ (X_p[b,i,m \cdot \text{strides}[0]+ j , n \cdot \text{strides}[1]+ z ] \cdot W_d[c, i, j, z]) \\ + B_b[c]
$$
> Where
>- $b \in [0,dY_0-1]$ is the batch index. $dY_0$ is the batch size of output $Y$
>- $c \in [0,dY_1-1]$ is the data channel. $dY_1$ is the number of data channels of output $Y$
>- $m \in [0,dY_2-1]$ is the index of the first spatial axis of output $Y$
>- $n \in [0,dY_3-1]$ is the index of the second spatial axis of output $Y$
>- etc.

## Examples

The specification must provide examples to illustrate the behaviour of the operator. As far as possible, examples must cover special values, domain bounds, etc., in order to clarify the behaviour of the operator, especially for non trivial cases. If possible, a jupyter notebook allowing the generation of the examples shall be provided (and placed aside the specification document). 

When the displayed result is not exact (for instance when using some real or float numbers that cannot be represented exactly), please use the $\approx$ symbol instead of the $=$ symbol.

## Error conditions

This section identifies the conditions that may occur during the execution of the operator leading to unexpected results (e.g., a IEEE special value while there was no special value in the inputs, a runtime error, etc.)

When writing a specification, the writer must identify the following failure conditions:
- for floating point computations 
  - invalid operation as defined in IEEE 754 section 7.2, i.e.
    - $0 \times\infty$ or $\infty \times 0$
    - addition or subtraction or fusedMultiplyAdd: magnitude subtraction of infinities, such as addition $(+\infty, -\infty)$ 
    - division $(0, 0)$ or division ($\infty, \infty)$
    - remainder(x, y), when y is zero or x is infinite and neither is a NaN
    - square root if the operand is less than zero
    - etc. Refer to the standard for a complete list of error conditions.
  - overflows (computations leading to +Inf or -Inf)
- for integer computations 
  - division by zero,
  - overflows, i.e., operations leading to a value out of the range (e.g., addition of two large int32 values non representable in int32)

The following rules must be applied.
  - Restrict the input domain to prevent the occurrence failures if it is not too conservative. for instance, $x \ge 0$ for $sqrt(x)$ is deemed acceptable whereas, using `uint32`, $A\leq2^{31}$ and $B\leq2^{31}$ for $A+B$ is deemed too conservative.
  - Give the most detailed description of the conditions in which a failure can occur, and the possible expected result. For instance for a matrix multiplication in int32, explain that the accumulator may overflow and may wrap around, leading to an incorrect and inconsistent result. If possible, point out the location in the specification where the error may occur. 
- If no indication is given about occurrence of a "failure", this means that the operator returns a correct value (as per specification) for **any** input value in the domain defined by the type.  
- If applicable and possible, provide "recommendations" about the implementation to prevent failure. For instance, propose to substract $max(Xi)$ to the argument to make the **Softmax** operator more robust.

Note that these rules concern the *specification* of the operation. Therefore,  they must be independent from implementation choices. For instance, *generally speaking*, it is always possible for the operation to overflow if the domain is output domain limited (e.g., `int32`), so there must be a warning about this failure condition. Nevertheless, a specific implementation may be failure-free if, for example, the size for the matrices is limited and the accumulator is sufficiently large. In that case, the implementation must give these conditions. Otherwise, the implementation is deemed compliant with the specification. 

## Attributes
This section describes the operator's attributes. This section must be introduced in the section about real numbers. Sections concerning the other types (floats, integers) shall shall not repeat this contents and provide a link to it whenever applicable. See the [template](./informal_spec_template.md) for an example. 

### `name`: \<type\>
where `name` is the attribute's name and \<type\> is the attribute's type.

 #### Constraints
This section gives all constraints applicable to the attribute.

- When a constraint involves several inputs/outputs/attributes, it is only described once when the first input or attribute concerned by the constraint is described. Then, for the other inputs, attributes, or outputs concerned by the same constraint, a cross-reference is given. 
The description is structured as follows:*

 - `[C<i>]` &lt;Title of constraint&gt;
   - Statement: &lt;Expression of the constraint&gt; or cross-reference to the previous location where this constraint was first introduced.
   - Rationale: &lt;Justification for the constraint&gt;. When the title and/or the statement of the constraint are sufficiently explicit, the rationale may be omitted. 

## Inputs

This section describes the operator's inputs.
 
### $\text{name}$: \<type\>

where $\text{name}$ is the name of the input and \<type\> is the type of the input.

#### Constraints
Same as for the attributes.

### Outputs
 This section describes the operator output.

### $\text{name}$: \<type\>
where $\text{name}$ is the output's name and \<type\> is the output's type.

 #### Constraints
Same as for the inputs.

                          End of the document.
