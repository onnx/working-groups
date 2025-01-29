# Introduction

This document gives guidelines to be followed when writing an operator's specification. 

# Structure
The specification on an operator is structured as described below. The text is *italics* is not part of the specification. 

## `<op>` operator 

*where `<op>`is the name of the operator.*
 
### Restrictions
*This section lists all restrictions applicable to the operator. A restriction is a limit with respect to the normal usage domain of the ONNX operator. restriction may concern the dimension of tensors, values of attributes, etc. They are introduced to simplify the implementation of operators, ensure resource usage predictability, enforce explicitness, etc.*  

### Signature
*Definition of the operator's signature:*

 `<O> = <op>(<I1>,<I2>,...<In>)`

 where
 - `<In>`: &lt;Brief description of the nth input &gt;
 - `<O>`: &lt;Brief description of output &gt;
   
 #### Informal specification
 
 *This section contains the informal specification of the operator. By "informal", we mean that the description does not rely on a formal language, even though it will usually include mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include figures if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.*
 
#### Inputs

*This section describes all operator's inputs.*
 
##### `<name>`: `<type>`

*where `<name>` is the attribute's name and `<type>` is the type of the attribute.*

#### Attributes

*This section describes all operator's attributes.*

*This section describes all constraints applicable to the input/output/attribute (if any). When a constraint involves several inputs/outputs/attributes, it will only be described for the first one and will be cross-referenced in the "constraint" section of the other ones..\
The description is structured as follows:*

 - (C&lt;i&gt;) &lt;Title of constraint&gt;
   - Statement: &lt;Expression of the constraint&gt;
   - Rationale: &lt;Justification for the constraint&gt;

##### `<name>`: `<type>`

*where `<name>` is the attribute's name and `<type>` is the attribute's type.*

 ###### Constraints

*(same as above)*

 #### Output
 
 *This section describes the operator output*

 ##### `<name>`: `<type>`

 *where `<name>` is the output's name and `<type>` is the output's type.*

 
 ###### Constraints

 *(same as above)*
 
 #### Formal specification
 
*This section contains the operators' formal specification.*
 

## Notations
- Notations $h(X)$ and $w(X)$ respectively denote the _height_ and the _width_ of tensor $X$. If the tensor represents an image, $h(X)$ and $w(X)$ represent the _height_ and the _width_ of the image.

## Fonts
- Inputs, outputs, and attributes are represented using a non-serif font. For instance, the "pads" attribute is represented by `pads`.

## Tags
- Restrictions with respect to the ONNX standard are indicated in the text with the tag `[R<i>]` where `<i>` is a number.\
A synthesis of all restrictions is given in section "Restrictions".

## Types
- Operators shall first be described for values in the domain of real numbers. A specific description is given for the other types (float, doubles).

 