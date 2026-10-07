# Introduction

This document gives the guidelines to be followed when writing an operator's non-formal specification. Guidelines for the development of a formal specification are given in a [dedicated document](./formal.md).

It is organised in three parts:

- The "Definitions" section fixes the meaning of the terms used throughout the document: *specification*, *specifying information*, *restriction*, *constraint* and *precondition*, *family*, *tag*.
- The "Rationales" section explains the principles on which the guidelines rest: the level of formalization aimed at, the data types covered, the relation to the IEEE 754 standard and to implementation standards, what counts as specifying information, the treatment of error conditions, and the place of the accuracy analysis.
- The "Specification guidelines" section states the rules themselves, in two sub-sections: "General guidelines" gives the presentation rules (fonts, basic operations, naming conventions, notations, tags, types, and reuse), and "Structure and contents of the specification" gives the organization and the contents of the specification of an operator, section by section, following the headings of the specification itself.

A reader who only needs the rules may go directly to the "Specification guidelines" section; the "Rationales" section is there to make the rules understandable and to justify them.

# Definitions

The terms below are used with the meaning given here throughout this document.

- **Specification.** The non-formal specification of an operator: the document whose required structure and contents are given in the "Structure and contents of the specification" section. The other specification of the same operator, written in Why3, is always designated as the *formal specification*.
- **Specifying information.** Text that states a property of the operator, and is therefore part of the meaning of the specification; the rest of the text is informational (see the "Specifying and non-specifying information" section).
- **Restriction.** A limit imposed by the SONNX profile with respect to the normal usage domain of the ONNX operator, marked with a restriction tag `[R<i>]` (see the "Tags" section).
- **Constraint.** A property of a call to the operator: what its arguments, its attributes and the tensors it returns are. A constraint that restricts the arguments or the attributes of a call is called a **precondition**, and it is what makes the operator applicable. Constraints are marked with traceability tags.
- **Family.** A collective name for a set of types that share one specification: `real`, `float`, `int`, `uint` (see the "Types" section).
- **Tag.** A marker either of a restriction or of a specifying statement: see the "Tags" section.

# Rationales

The non-formal specification is first an entry-point for any *user* of the SONNX profile. Towards that goal, it shall explain clearly the purpose of the operator, i.e., the relation between its inputs (arguments and attributes) and its outputs. To that end, it may use whatever means deemed useful, including text descriptions, mathematical formulae, graphics, examples.

It shall also provide a clear statement about:
- the usage restrictions for the operator imposed by SONNX,
- the constraints on the arguments and attributes of the operator (or preconditions) for the operator to be applicable,
- the possible errors that may arise during the execution of the operator.

In the following paragraphs, we express some of the "principles" that we applied to elaborate the guidelines.

## About the level of formalization

The non-formal specification aims at providing a clear and complete description of the behavior of the subset of operators considered in the SONNX profile. Understandability is favored over formalization, accordingly, the non-formal specification essentially relies on natural language, with mathematical formulae when deemed necessary. In addition, for each operator, a formal specification expressed using a formal language (Why3) is provided separately. Throughout the rest of this document, "specification" designates the non-formal specification, as defined in the "Definitions" section.

The two specifications of an operator are a pair: they shall not contradict each other, and any change to one shall be reviewed against the other. The formal specification shall cover at least the same domain, the same range and the same error conditions.

## About data types

The specification is given for all the data types considered in SONNX, i.e., `float16`, `float`, `double`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `bool`, and `string`. In addition, SONNX also provides a specification of each (mathematical) operator for real numbers. This is aimed at facilitating the understanding of the core function of the operator without dealing with implementation-specific issues such as the effect of overflows (for the int and uint families) or the handling of special floating-point values (see next paragraph).

## About floating point numbers

Floating point operations are specified in compliance with the IEEE 754 standard (IEEE Standard for Floating-Point Arithmetic, IEEE Std 754-2019, IEEE). In particular, care is taken to describe the expected behavior of a mathematical operator when dealing with IEEE special values (+Inf, -Inf, +0, -0, and NaN).

The floating-point results are those of the roundTiesToEven attribute of the standard, in the exponent range of the type of the result; this is also the mode on which the accuracy analysis rests (see the "About accuracy" section). In particular, overflow is the case of section 7.4 of the standard: a result is an overflow only when the value rounded to the type of the result with an unbounded exponent range exceeds the largest finite value of that type. For `float16`, for instance, the largest finite value is 65504 and the next power of two is 65536; an exact difference of 65512 lies below their midpoint 65520 and therefore rounds to 65504, and not to an infinity.

## About the compliance with implementation standards

SONNX shall remain independent from any specific implementation and, instead, shall simply express the intended behavior of each operator according to some usual and/or consensual understanding of its semantics.

However, tests carried out by the SONNX working group (SONNX WG) on the implementations of some operators (e.g., **MaxPool**) show that the behavior observed in actual implementations of operators sometimes differs significantly from the one that would be expected "naturally". When this happens, SONNX preferably sticks to the semantics adopted in the ONNX Runtime CPU implementation, and indicates this "discrepancy" in the specification.

## Specifying and non-specifying information

By default,
- all the text in the "Signature" section is specifying
- all the text enclosed between traceability tags (see the "Tags" section below) is specifying.

The rest of the text is provided for information.

## Specifying error conditions

The three-step procedure that shall be applied to handle error conditions, together with the list of conditions that shall at least be considered, is given in the "Error conditions" section of the operator specification (see the "Structure and contents of the specification" section).

The procedure is ordered so that an error condition is avoided whenever it can be: a condition whose result is fully determined is part of the nominal behavior of the operator and is not an error, and a condition that can be ruled out by a precondition cannot occur. Describing what can happen at runtime is the last resort.

## About accuracy

The SONNX profile does not specify the accuracy of operators, instead, it provides guidance on how to analyze the propagation and introduction of errors on a given implementation and illustrates the approach on SONNX's reference implementation.

The analysis is carried out in two steps:
- During step 1, an analysis is carried out to specify bounds on propagated and introduced errors considering the IEEE rounding error. These bounds may not be the tightest ones, but bounds that can be determined with a reasonable analysis effort.
- During step 2, an analysis of the code of an actual implementation (in our case, the reference implementation) is carried out using a tool developed for that purpose by one of the SONNX WG contributors (Franck Vedrine, [CEA List](https://www.cea.fr/)).

Please refer to the [specific set of guidelines](./other/accuracy.md) given for the analysis of accuracy.

# Specification guidelines

This section is composed of two sub-sections:
- "General guidelines" defining presentation rules such as fonts, notations, use of tags for traceability, etc.
- "Structure and contents of the specification" defining the organization and the contents of the specification of an operator. This section applies these general guidelines.

## General guidelines

The specification is intended for both users *and* implementers of operators, who need to understand what an operator does and how to use it. For instance, the first kind of readers might be satisfied with one or two sentences about the semantics of an operator whereas the second category of readers would like to get all the details of the semantics.

More precisely, the specification:
- Shows clearly what a given operator is supposed to do, without calling on a strict formal, mathematical language; the exact and complete specification is given in the formal specification written in Why3.
- May provide diagrams and examples to make things clear.
- Follows ONNX nomenclature, which includes naming conventions for operator names, types, identifiers of operator inputs, outputs and attributes, etc.
  - Examples:
    - The element-wise addition of tensors is `Add`, not `add`.
    - The 16-bit floating-point type is `float16`, not `FP16`.

The writer of the specification shall take care to keep it readable and understandable by an ML developer. The recommendations given in the following guidelines target this objective.

### Styling

- Mathematical objects are represented using *italic*. LaTeX formulae are used.
- In the text, operator attributes are represented using `code font`.
- Operator names are represented in **bold** (e.g., **Add**, **MaxPool**) and type names in `code font` (e.g., `float16`, `int32`).
- As far as possible, names of arguments and attributes shall be used as is in mathematical formulae. If the name is "too long", another, shorter designation may be used with a clear statement of the redefinition. If the name refers to a Greek symbol (e.g., $\text{alpha}$), the symbol itself can be used (e.g., $\alpha$) in formulae.
- **Modality.** *Shall* marks a requirement on the writer of a specification, or on the specification document itself; it is not used to state what an operator does. The semantics of an operator, including the constraints that its arguments, its attributes and its results satisfy, is stated in the present indicative, e.g. "Tensors $A$, $B$ and $C$ have the same shape." and "each element $C[i]$ is the result of dividing $A[i]$ by $B[i]$". The same convention applies to the specification documents.

### Basic operations

The specification can use the following basic operations without first defining them:
- $+$, $-$, $*$, $/$, $-x$ (negation),
- $\sin(x)$, $\cos(x)$, $\tan(x)$,
- $\exp(x)$, $\sqrt x$, $\ln(x)$, $|x|$,
- $\min(x,y)$, $\max(x,y)$,
- logical operators: $\wedge$, $\vee$, $\lnot$
- comparison operators: $\lt$, $\gt$, $\le$, $\ge$.

When necessary, the domain of the operator is specified using an index indicating the type, as illustrated hereafter for the $+$ operator:
- $+_{(\text{f16})}$, $+_{(\text{f32})}$ and $+_{(\text{f64})}$ are the additions for `float16`, `float` and `double` floating-point numbers
- $+_{(\text{i<x>})}$ is the addition for XX-bit signed integers (\<x> in {8,16,32,64})
- $+_{(\text{u<x>})}$ is the addition for XX-bit unsigned integers (\<x>=8,16,32,64)

When the operator is used without an index, it refers to the operator applied to real numbers ($\mathbb{R}$).

The same convention applies to iterative operators such as the sum or product ($\Sigma$, $\Pi$). For instance:

$$\sum_{(\text{u32})~i=0}^{10}~i$$

Note that in order to improve readability of iterative operators, preferably use the display form using "\$\$".

### Naming conventions

Use ONNX names for inputs, outputs, and attributes.

### Notations
#### Tensors

- An input (argument) or output tensor is always represented in italics, with an uppercase letter when the name is composed of a unique letter, or in lowercase when the name is composed of multiple letters (e.g., $X, Y$ for operator **Abs**, but *inputs* for operator **Concat**).
- In the case of a variadic operator, the tensor parameters are designated by an index: $T0, ..., TL$. Indices start at 0 to be consistent with the other use of indices.
- The rank of a tensor $T$, i.e., the number of its dimensions, is denoted $rT$.
- The shape of a tensor $T$ is denoted by a vector $(dT_0, ..., dT_i, ..., dT_n)$ where $dT_i$ refers to the dimension along axis $i$ and $n=rT-1$.
- For a tensor $Ti$ used as a variadic parameter, the shape is denoted by $(dTi_{0}, dTi_{1}, ...)$.
- A specific element of a tensor $T$ is denoted:
  - either as: $T[i]$, where $i$ is a [tensor index](./../common/definitions.md#tensor_index)
  - or as $T[i_0, i_1, ..., i_{rT-1}]$.

Indices are 0-based: the elements of a dimension of size $d$ are indexed from $0$ to $d-1$, and the bounds written in a formula are inclusive. A multi-dimensional index lists the axes in the ONNX order, i.e. $i_0$ is the index along the first axis and $i_{rT-1}$ the index along the last.

#### Tags

The specification makes use of two different types of tags:
- A **restriction tag** expresses a restriction with respect to the ONNX standard. It is indicated by the tag `[R<i>]` where `<i>` is a number. A synthesis of all restrictions is given in section "Restrictions" (see below).
- A **traceability tag** expresses a constraint on one or several inputs, outputs, or attributes. It is enclosed between two tags:
- a beginning tag `[E_<op>_<type>_<zone>_<number>]`.
  The components of a tag are
  - \<op\> is the name of the operator
  - \<type\> is the type family, in uppercase letters (e.g., `REAL`, `INT`)
  - \<zone\> designates the section in which the tag appears (e.g., `FUNC` or `CONSTR_<IO>`). In the case of a `CONSTR` (constraint), `<IO>` designates the input or output on which the constraint applies.
  - \<number\> is a 4-digit tag id. (Prefer a 10-by-10 increment in order to avoid renumbering when a new tag is added.)
- an end tag `[END]`, except when the tag is in a list or a table: in that case the scope of the tag is implicit (the row of a table, or the item of a list).

A tag is permanent: it is allocated once and is never re-used, renumbered or deleted, including when the statement it marks is withdrawn; a withdrawn tag is recorded as withdrawn rather than removed from the specification.

For instance, here is a tag introducing a constraint relating some input and output tensors:
> <a id="E_ADD_INT_CONSTR_A_0010"></a>
> - `[E_ADD_INT_CONSTR_A_0010]` Shape consistency
>   - Statement: Tensors $A$, $B$ and $C$ have the same shape.

When part of the documentation refers to a tag, a hyperlink is used. This is achieved using the following elements:
```
<a id="E_<op>_<type>_<zone>_<number>"></a>
- `[E_<op>_<type>_<zone>_<number>]` some text...
  - Statement: some text...
```

   to declare the location of the tagged element and
```
  [<b><span style="font-family: 'Courier New', monospace">E_<op>_<type>_<zone>_<number></span></b>](#E_<op>_<type>_<zone>_<number>) some text...
```

to refer to the tagged element.

On the page, the beginning tag and the end tag that delimit a specifying part are displayed in red:
```
<span style="background: red; color: white; font-size:0.7em;">[E_<op>_<type>_<zone>_<number>]</br></span>
...
<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>
```

The color is a display convention for the reader only: the tags themselves are the plain text described above, and the text they enclose is the specifying part (see the "Specifying and non-specifying information" section).

### Types

- The type names shall be the ones used in the ONNX description of the operators, without surrounding them with "tensor()".
  - Example: "tensor(double)" in ONNX becomes "double" in the specification.
  - In a section that covers a set of types (a family), the input or output is designated by the family name followed by "tensor", e.g. `real tensor`, `floating-point tensor`, `integer tensor`.
- The data types allowed in SONNX operators are:
  - IEEE 754 floating-point types: `float16`, `float`, `double`
  - Signed integer types: `int8`, `int16`, `int32`, `int64`
  - Unsigned integer types: `uint8`, `uint16`, `uint32`, `uint64`
  - `bool`
  - `string`
- The types listed above are referred to collectively by the following family names, which shall be used consistently in the prose, in the operator headings and in the traceability tags:
  - real: the specification established for real numbers (there is no corresponding ONNX type)
  - float: the IEEE 754 floating-point types `float16`, `float` and `double`
  - int: the signed integer types `int8`, `int16`, `int32` and `int64`
  - uint: the unsigned integer types `uint8`, `uint16`, `uint32` and `uint64`
  - In a traceability tag, the family name is written in uppercase letters, the uppercase spelling being the `<type>` component (e.g. `E_DIV_FLOAT_CONSTR_A_0010`).
- IEEE 754 floating-point types, i.e., `float16`, `float`, and `double` have the following special numbers:
  - +0 and -0 (or $\pm 0$ when applicable)
  - +Inf and -Inf (or $\pm$Inf when applicable)
  - NaN (Not a Number)

### Reuse

Part of a specification can reference another part using traceability tags. Note that, in any case, there shall be a local traceability tag.

## Structure and contents of the specification

This section describes the required structure and contents of the specification of an operator.

The [specification template](informal_spec_template.md) gives a template of the required structure. Every section of a specification that is referred to from elsewhere carries a stable anchor (`<a id="..."></a>`), and a reference is written as a link to that anchor rather than as the name of a section.

The headings used from here on are the headings of the operator specification document itself. They are reproduced here at their own level and are not sections of this guideline.

# Contents

This section gives the list of the specifications of the operator, one for each applicable set of types. Each entry is a hyperlink to the corresponding section, and each of those sections carries the matching anchor (see [template](informal_spec_template.md)).

- **Op** operator for type real
- **Op** operator for types \<type 1\>, \<type 2\>,...
- **Op** operator for types \<type 3\>, \<type 4\>,...
- etc.

where the `\<type i\>` are the SONNX-supported types.

An operator applicable to numeric values shall first be specified for values in the domain of real numbers; specific descriptions shall then be given for the other types (`float`, `double`, etc.). This is why the first entry of the list above is the real-number specification.

The reference, with a link to the ONNX definition of **Op**, shall be inserted in this section, with the opset(s) on which the specification is based. See the **Div** example below.

Each specification carries a revision line giving the ONNX opset it is based on, the date of the revision and the change it makes; when ONNX publishes a new opset for the operator, the specification is re-baselined and the revision line updated.

Here is an example for operator **Div**:
> Contents
>- **Div** operator for type [real](#real)
>- **Div** operator for types [`float16`, `float`, `double`](#float)
>- **Div** operator for types [`int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`](#int)
>
> Based on ONNX [Div version 14](https://onnx.ai/onnx/operators/onnx__Div.html#div-14).

The three sections of the specification carry the anchors `<a id="real"></a>`, `<a id="float"></a>` and `<a id="int"></a>`, respectively, as in the **Div** operator specification.

The following section shall be repeated for each set of types for which the semantics is the same. One section corresponds to one entry in the "Contents" list. The grouping shall be justified in one line, stating why the types of a section share one semantics; types whose semantics differ shall be given separate sections.

# **Op** (\<type 1\>, \<type 2\>)

`\<type i\>` may be either a family name designating a set of types (e.g. float or int) or a specific type (e.g. `uint16`, `int64`).

In the former case, the family name shall be designated, e.g.,
> ...where float is in {`float16`, `float`, `double`}.

## Signature

Definition of operator **Op** signature:

 $A,B,...,C = \text{Op}(X,Y,...,Z)$

 where
 - $X$: Brief description of argument $X$
 - ...
 - $Z$: Brief description of argument $Z$
 - $A$: Brief description of output $A$
 - ...
 - $C$: Brief description of output $C$

An input or an output that is optional is written between square brackets, e.g. `$C = \text{Op}(X, Y\,[, Z])$`. The "Function" section states what the operator does when an optional input or output is absent.

## Restrictions

This section lists all restrictions applicable to the operator. A restriction is **a limit with respect to the normal usage domain** of the ONNX operator. A restriction may concern the dimension of tensors, the values of attributes, etc.

An example is given hereafter

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` | Attribute `auto_pad` is restricted to `NOTSET`  | [No default values](../../../../deliverables/reqs/reqs.md#no_default_value) |

Some SONNX restrictions apply to all the operators. Therefore, this section shall always contain the following markdown link:

> [General restrictions](./../common/general_restrictions.md) are applicable.

When there are no other restrictions, the following sentence shall be added:

> No specific restrictions apply to the **Op** operator.

Restrictions marked as "Transient" are introduced by the SONNX WG in order to reduce the specification, proof, etc. effort. Those restrictions, which are not traceable to a need, are aimed at being eventually relaxed. However, in the meantime, both transient and non-transient restrictions are applicable to the operator user or implementer.

## Function

 This section contains the functional part of the specification of the operator. The specification is "informal", i.e., it does not use a formal language, even though it usually uses some mathematical formulae. The specification shall be readable and understandable. It can include illustrations if deemed necessary. The objective is that a reader can fully understand the domain, range, and semantics of the operator with no additional information. Stated differently, they should be able to implement the operator from the specification alone.

The specification shall be composed of two main parts:
- **Part 1.** A short description of the operator. For instance, for the **Conv** operator:

> Operator **Conv** computes the convolution of the input tensor $A$ with the kernel $W$ and adds bias $B$ to the result. Two types of convolutions are supported: standard convolution and depthwise convolution.

- **Part 2.** A detailed description that:
  - Presents the mathematical formulae, if necessary, according to the following pattern: the complete formula is first given and its atomic elements and sub-expressions are defined afterward, by introducing them with "where..." or "in which...".
  - Uses the notations proposed in section "Notations" of these guidelines
  - Implements the traceability tags proposed in section "Tags" of these guidelines
  - States, for every case that applies to the operator, what the operator does. These cases are where two implementations of the same operator most often disagree, so they are either decided by the specification or left to each implementer; they are at least:
    - an input with a zero-sized dimension, and an input with no dimension at all (a rank-0 tensor);
    - inputs whose shapes differ and are combined, where ONNX allows it (broadcasting);
    - the types whose behaviour differs inside a section, in particular the signed and the unsigned integer types;
    - the special values of the floating-point types, i.e., $+0$, $-0$, $+\infty$, $-\infty$ and NaN, as operands and as results.
  - Declares the cases it leaves to each implementer. A case that the specification does not decide shall be stated as such, together with the set of results that conform, so that a reader can tell a case left open from a case that is decided. For instance, when the result is a NaN whose payload the standard does not fix, stating that every quiet NaN of the type of the result is a conforming result is such a declaration.

For instance, for the **Conv** operator:

> $$
> Y[b, c, m, n] = \sum_{i=0}^{dW_1-1} \sum_{j=0}^{dW_2-1} \sum_{z=0}^{dW_3-1} X_p[b, i, m \cdot s_0 + j, n \cdot s_1 + z] \cdot W[c, i, j, z] + B[c]
> $$
> where
>- $Y = \text{Conv}(X, W, B)$ is the output tensor and $Y[b, c, m, n]$ one of its elements
>- $b \in [0,dY_0-1]$ is the batch index. $dY_0$ is the batch size of output $Y$
>- $c \in [0,dY_1-1]$ is the data channel. $dY_1$ is the number of data channels of output $Y$
>- $m \in [0,dY_2-1]$ is the index of the first spatial axis of output $Y$
>- $n \in [0,dY_3-1]$ is the index of the second spatial axis of output $Y$
>- $X$ is the input tensor and $X_p$ the tensor obtained by padding $X$ according to the `pads` attribute; $X_p[b, i, h, w]$ is one of its elements
>- $W$ is the kernel (the weights) and $W[c, i, j, z]$ one of its elements; $dW_1$ is the number of input channels, $dW_2$ and $dW_3$ the two kernel dimensions
>- $B$ is the bias and $B[c]$ the bias of data channel $c$
>- $s_0$ and $s_1$ are the two values of the `strides` attribute
>- etc.

Note: A displayed formula in the description is written between `$$` and `$$`, with a blank line before and after it so that it renders correctly. The worked results given in the "Examples" section are written in the same way, between `$$` and `$$`: a fenced block tagged `math` is not rendered by every Markdown editor used to read the specifications, in particular not by Obsidian, whereas a `$$` block is.

Part 2 presents the mathematical formulae of the operator; an operator can also be specified **axiomatically**, i.e., by the properties that determine its result rather than by a formula that computes it. The specification then states the conditions that the result satisfies — conditions that only one value satisfies — and the domain on which they are stated. This is the natural form for an operator whose value is defined by a property rather than by an expression, and for the operators that are defined as the inverses of other operators.

For instance, the inverse sine is specified by the equation that its result satisfies and by the branch on which that equation has a single solution:

> For every $x$ in $[-1, 1]$, the result of **Asin** is the unique value $y$ such that $\sin(y) = x$ and $y \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right]$.

The equation $\sin(y) = x$ alone determines nothing, since it has infinitely many solutions; it is the interval that selects the result, and that interval is therefore as specifying as the equation. The inverse cosine is specified in the same way, with $\cos(y) = x$ and $y \in [0, \pi]$, and so is the inverse tangent, whose branch is the open interval: $\tan(y) = x$ and $y \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)$.

As for an operator specified by a formula, the axioms are what decide the cases of the operator — the bounds of its domain, the special values of the type — or what declares the cases left to each implementer (see above). An axiomatic specification states the value of the result, not a way of computing it, so that the accuracy of a computation remains outside the specification, as it does for a formula (see the "About accuracy" section).

### Example 1

The specification shall provide examples to illustrate the behavior of the operator. As far as possible, examples shall cover special values, domain bounds, etc., in order to clarify the behavior of the operator, especially for non-trivial cases. If possible, a Jupyter notebook allowing the generation of the examples shall be provided (and placed inside the `Examples` subfolder of the operator folder).

Each example is given its own subsection, numbered from 1 (`### Example 1`, `### Example 2`, ...); an operator with a single example uses `### Example`.

When the displayed result is not exact (for instance when using some float numbers that cannot be represented exactly), please use the $\approx$ symbol instead of the $=$ symbol. For real numbers, use the exact result (e.g., "1/3" instead of "0.3333"...)

## Error conditions

This section identifies the conditions that may occur during the execution of the operator and lead to a result that does not comply with the specification.

The following conditions shall at least be considered:
- for floating point computations
  - invalid operation as defined in IEEE 754 section 7.2, i.e.,
    - $0 \times\infty$ or $\infty \times 0$
    - addition or subtraction or fusedMultiplyAdd: magnitude subtraction of infinities, such as addition $(+\infty, -\infty)$
    - division $(0, 0)$ or division $(\infty, \infty)$
    - remainder(x, y), when y is zero or x is infinite and neither is a NaN
    - square root if the operand is less than zero
    - etc. Refer to the standard for a complete list of error conditions.
  - overflows (computations leading to +Inf or -Inf)
- for integer computations
  - overflows, i.e., operations leading to a value out of the range (e.g., addition of two large `int32` values not representable in `int32`)
  - division by zero

Every condition of the list above shall be given a disposition in the specification, and so shall every further condition introduced by the operator: for each of them the specification states whether it is part of the nominal behavior of the operator (naming the statement of the "Function" section in which it is specified), or ruled out by a precondition (naming the constraint tag that rules it out), or an error condition described in this section. The list is a minimum, not a menu: a condition that is silently left out cannot be seen, neither by the reviewer nor by the reader, whereas a disposition shows it has been considered. A table giving each condition and its disposition is the recommended form. A disposition refers to the statement that specifies the condition; it does not restate it, since a restatement is a second formulation of the same rule and the two may drift apart.

Each applicable condition shall be handled using the first applicable approach of the following list:

1. **Specify the condition as part of the nominal behavior of the operator.** When the result produced by the condition is fully determined, the condition is not an error: its behavior shall be specified in the "Function" section like any other part of the operator semantics, and the condition shall not be reported in this section.

   > Example: for an integer **Add** operator, the overflow of the result is specified as a wrap-around modulo $2^n$, where $n$ is the number of bits of the type. For instance, the addition of the `int8` values $127$ and $1$ is specified to produce $-128$. This is the nominal behavior of the operator, hence not an error condition.

2. **Otherwise, specify a precondition on the arguments and/or attributes that prevents the condition from occurring.** The precondition is expressed as a constraint in the "Attributes" section for an attribute, or in the "Inputs" section for an argument (see the "Constraints" sections), and cross-referenced here. Since the condition cannot occur when the precondition holds, it needs not be described further.

   > Example: for a **Sqrt** operator, the invalid operation produced by the square root of a negative number is prevented by the precondition $\forall i, X[i] \geq 0$ on the operand, given as the "Definition domain" constraint of input $X$.

3. **Otherwise, describe the error condition**, i.e., what can happen at runtime when the condition occurs. The writer shall give the most detailed description of the conditions in which a non-complying result can be produced, shall point out, if possible, the location in the specification where the error may occur, and shall, if applicable and possible, provide recommendations about the implementation to prevent the non-complying result.

   > Example: for an integer **Div** operator that cannot restrict the domain of its denominator, a null $B[i]$ cannot be ruled out and the result is not defined. The specification shall state what can happen at runtime, for instance a division-by-zero exception raised by the hardware or an implementation-dependent result.

## Attributes

This section describes the operator's attributes. Usually, its content does not depend on the type of the arguments. So, it shall be given for real numbers and referred to in the sections for other types. See the [template](./informal_spec_template.md) for an example.

### `name`: \<type\>

where `name` is the attribute's name and \<type\> is the attribute's type.

#### Constraints

This section gives all constraints applicable to the attribute.

- When a constraint involves several inputs/outputs/attributes, it is only described once when the first input or attribute concerned by the constraint is described. Then, for the other inputs, attributes, or outputs concerned by the same constraint, a cross-reference is given.

The description is structured as follows:

 - `[E_<op>_<type>_<zone>_<number>]` Title of constraint
   - Statement: Expression of the constraint or cross-reference to the previous location where this constraint was first introduced.
   - Rationale: Justification for the constraint. When the title and/or the statement of the constraint are sufficiently explicit, the rationale may be omitted.

## Inputs

This section describes the operator's inputs.

### $\text{name}$: \<type\>

where $\text{name}$ is the name of the input and \<type\> is the type of the input.

#### Constraints

Same as for the attributes.

## Outputs

This section describes the operator's outputs.

### $\text{name}$: \<type\>

where $\text{name}$ is the output's name and \<type\> is the output's type.

#### Constraints

Same as for the inputs.
