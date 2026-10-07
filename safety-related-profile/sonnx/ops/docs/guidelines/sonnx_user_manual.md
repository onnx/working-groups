# Introduction

## Overview of the SONNX profile operator specification

## Preamble

### Definitions
The [following definitions](../../spec/informal/common/definitions.md) are applicable for all operations.

### Restrictions
The [following restrictions](../../spec/informal/common/general_restrictions.md) are applicable for all operators.

### Notations 
The [following notations](../../spec/informal/common/notations.md) are applicable for all operators.

# The structure of a specification

A specification is organized as follows:
- Table of contents with hyperlinks organized according to the datatypes supported by the operator. A specification for real numbers is systematically given (see later in this document).
- Specification for type \<T\>
  - Signature of the operator giving the type of the arguments and outputs
  - Applicable restrictions applicable to the SONNX profile
  - Functional specification including illustrations and examples when needed
  - Error conditions
  - Attributes (if applicable)
  - Inputs
  - Outputs

Section "Specification for type \<T\>" is repeated for all datatypes suppted by the operator. If the specification for type \<T\> is strictly identical to specification for type \<T'\>, then section \<T'\> may simply refer to section \<T\>.

# Specific points

## Restrictions

*To be completed.*

## The "real" type

In order to provide the simplest specification of each operator, SONNX specifies each operators for real numbers ($\mathbb{R}$). This allows giving a simple mathematical specification of operators without having to care about the peculiarities of computer arithmetic (IEEE754's floating point special values such as NaN, +Inf, etc., integer overflows, etc.).

When the specification of a computer data type strictly follows the semantics of the operator in $\mathbb{R}$, it may directly refer to the real number section. Structural operators that do not perform any arithmetic operation are a specific case where all operators refer to the specification for Real numbers.

## Requirement tags 

Specification items are enclosed between the following tags:

<span style="background: red; color: white; font-size:0.7em;">[E\_\<op\>\_\<type\>\_\<cat\>\_<id\>]</br></span>

*Some specification text...*

<span style="background: red; color: white; font-size:0.7em;">[END]</br></span>

where 
- <span style="background: red; color: white; font-size:0.7em;">[<id\>]</span> designates the operator
- <span style="background: red; color: white; font-size:0.7em;">[<type\>]</span>  designates the data type (real, float, int, etc.) 
- <span style="background: red; color: white; font-size:0.7em;">[<cat\>]</span>  designates the requirement category among
  - CONSTRAINT for a constraint specificition item 
  - FUNC for a functional specification item 
- <span style="background: red; color: white; font-size:0.7em;">[<id\>]</span>  is a 5-digit numerical id.

Several exception apply
- Constraints are not closed by a <span style="background: red; color: white; font-size:0.7em;">[end]</span> tag. Constraints are listed using a "bullet list" in which one item is one (tagged) requirement. 
- The signature paragraphs are requirements *by right*. They are not tagged because they can be referred to using the section number.
- If section \<T'\> refers to section \<T\> in order to avoid redundancy, tags <span style="background: red; color: white; font-size:0.7em;">[E\_\<op\>\_T'\_\<cat\>\_<id\>]</br></span> 
  is considered to be implicitly defined, and with the same specification text as for <span style="background: red; color: white; font-size:0.7em;">[E\_\<op\>\_T\_\<cat\>\_<id\>]</br></span>.

## Basic operators

When considering real numbers, some operators are considered "well-known" and not specified any further. This is the case for instance of the four basic operators ($+,-,\times,/$), trigonometric operators ($sin(x)$, $cos(x)$, etc.), square root ($\sqrt x$), etc.

For computer datatypes such as `float`, `double`, `int8`, `uint8`, etc., primitive operators (**Add**, **Sub**, **Mul**, **Div**) are fully specified and the coresponding operator ($+,-,\times, /$) refer to those operators. For instance, expression $x+y$ for `int8` actually refers to **Add(x,y)**. By extension, this also applies to iretaive sums ($\sum$) and products ($\prod$). 


