## Introduction
This document proposes an approach to develop tests of the SONNX operators. 

Note that it does not (yet) cover the actual implementation of tests (using [Hypothesis](https://hypothesis.works/) or any other test framework such as [pytest](https://docs.pytest.org/en/stable/), [doctest](https://docs.python.org/3/library/doctest.html), etc.). This will be done in a future version of the document.

The current version of this note is organized as follows:
- The first section recalls the objectives of testing in the context of SONNX and give some elements about the test strategy,
- The second section focuses on the practical implementation of the test strategy for SONNX operators 
### Test objectives and scope in SONNX

In SONNX, tests target two main objectives:
- **Validating** the informal specification through comparison with existing implementations (e.g., ONNX runtime) 
- **Verifying** implementations of the SONNX specification, using the SONNX reference implementation as the test oracle. 

Concerning the first objective, it could be interpreted at first sight as some sort of "retro-engineering" activity in which the specification is derived from the implementation. *This is clearly not the case*. Tests against an implementation is a way to increase our confidence in the SONNX specification by comparing it to existing reliable implementations. 
In case of discrepancy, no immediate conclusion can be drawn since the error may be either in the specification or in the implementation. However, this reveals a problem in either or both sides that needs to be addressed. This approach has already  been fruitful by raising issues both in our specification and in the ONNX runtime implementation. 

Concerning the second objective, it is worth noting that passing all tests developed in SONNX does not **guarantee** full  conformance with the SONNX specification. In particular, in the context of the development of a certified system, demonstration of conformance remains the responsibility of the applicant.
### Test strategies
#### Functional *vs. implementation-based* tests

In SONNX, tests are essentially *functional*, i.e., they only refer to *what* the operators are expected to do. They do not consider *how* they will be implemented. 

However, in practice, additional tests may be defined to account for possible implementations solutions and well-known sources of errors. In that case, the reason for the test shall be clearly documented. 

#### Test traceability

Tests must be traceable to a specific part of the informal specification. Traceability shall be done using reference to the specification section or to a specic requirement tag (e.g., `E_DIV_REAL_FUNC_010`). 

#### Equivalence class-based testing

Except for very simple cases such as e.g., **Add** on int8 scalars, it is generally impossible test an operator against all its possible input values. Therefore, tests are generally performed on a selected subset of all possible input values.

One strategy to select those values can be based on the definition of *equivalence classes*. 

Two values $x$ and $y$ are said to belong to the same equivalence class with respect to testing (i.e., $a R b$) if the capability of those values to reveal some design or implementation error are *expected* to be the same, i.e., if an error is revealed by input $a$ then it is also revealed by input $b$. For instance, testing **Add(x1,x2)** with $a=(x_1:10,x_2:20)$ is considered to reveal the same kind of errors as with $b=(x_1:15, x_2:-10)$. 

This definition clearly shows that equivalence classes rely on some *hypotheses* about some "reasonable" underlying fault model. For instance, in the previous example, nothing prevents a specific implementation to behave correctly for $x=10,y=20$ and incorrectly for $x=15,y=-10$: 
```
int add(int x, int y) {
	if ((15 == x) && (-10 ==y) 
		return 42;
	else
		return x+y;
}
```
But in general, such fault model -- which is some kind of "easter-egg" in this case -- is simply deemed  very unlikely and is not considered in the definition of the equivalence classes. 

Reciprocally, some fault models are well-known. This is, for instance, the case of faults concerning the incorrect handling of domain boundaries, whether it is the bounds of an array (i.e., the min and max value of an index in this array), the min and max values of some data type, some "special" functional values (e.g., a null denominator for a division), etc.  

Since we are considering *functional* testing,  classes of equivalence are based on the specified behaviour of the operator, not on any specific implementation.

#### Equivalence classes based on the input domain

##### Principles

 In some cases, equivalence classes are derived from the domains of valid values of variables. A domain by be defined by the type of the variable (for instance, $[0,255]$ for an unsigned integer, $[-128,127]$ for a signed integer, etc.), or by  some constraint  involving one or multiple variables. 

Once the domain is defined, several equivalence classes can be built, for instance: 
- the class of all values on the boundary of the domain
- the class of all values inside the domain defined by the boundary (the boundary themselves being excluded).

Let us consider a domain defined by some predicate $p_i(x_1,x_2,...,x_n)$ over a subset of the operator input variables. A predicate can be an inequality or an equality relation involving some input variables. For instance:  $x_1< 10$,  $x_1+x_2\leq x_3$ or $x_1^2+x_2^2=c$, etc. A domain is defined by the set of predicates $P={p_1,p_2,...,p_m}$. 

We want to distinguish the points located on the boundary of the domain defined by the set of constraints from the points located in the domain but not on the boundary. 

First, we replace all strict inequality by non-strict inequality. 
For instance, in the integer domain, predicate $x_1<10$ become $x_1\le 9$. 
In the floating point domain, $x_1+x_2<x_3$ becomes $x_1+x_2 \le \text{nextdown}(x_3)$ with $\text{nextdown}(x_3)$ being the largest floating point number strictly smaller than $x_3$, considering the round-to-nearest, ties-to-even IEEE754 rounding mode. 

Then,  we decompose each (possibly rewritten) inequality predicate $p_i$ into two predicates $p'_i$ and $p''_i$ such that
- $p'i$ is obtained by replacing operator $\le$ and $\ge$  in $p_i$ by operator  $=$  
- $p''_i$ is obtained by  replacing operators $\le$ (resp.  $\ge$)  in $p_i$ by operator $\lt$ (resp. $\gt$). 
and equality predicates $p_j$ are kept as is and denoted $p'_j$.  

The initial system is $p_1 \wedge p_2 \wedge ... \wedge p_n = (p'_1 \vee p''_1) \wedge (p'_2 \vee p''2) \wedge ... \wedge (p'_n \vee p''_n)$ , which can be written  $(p'_1 \wedge p'_2 \wedge ... \wedge p'_n) \vee (p'_1 \wedge p'_2 \wedge ... \wedge p'_{n-1} \wedge p''_n) \vee ... \vee (p''_1 \wedge p''_2 \wedge... \wedge p''_n)$ $

Note that, by construction, $p'_i$ and $p''_i$ are disjoint so all combinations involving the product $p'i \wedge p''_i$$ could be simply ignored since they can't be satisfied, but to simply the description, we keep them. 

Each member of the last expression related by the $\vee$ operator represents a domain. The first domain $p'_1 \wedge p'_2 \wedge ... \wedge p'_n$  is the most constrained since all $p'_i$ are equality relations. Conversely, the last one is the least constrained. 

Each member represent an equivalence relation, hence a testing domain. 

Let us take for example the following set of constraints, with $x_i \in \mathbb{N}$: 
- $p_1(x_1) \Leftrightarrow x_1 < 100$
- $p_2(x_1,x_2) \Leftrightarrow x_1+x_2 < 150$

The predicate $p_i(x_1)\Leftrightarrow (x_1 < 100) \Leftrightarrow (x_1 \le 99)$ gives
- $p'_i(x_1) \Leftrightarrow x_1 = 99$ and 
- $p''_i(x_1) \Leftrightarrow x_1 \lt 99$. 

The predicate $p_2(x_1,x_2) \Leftrightarrow (x_1+x_2 < 150)  \Leftrightarrow (x_1+x_2 \le 149)$  gives
- $p'_2(x_1,x_2) \Leftrightarrow x_1+x_2 = 149$ and 
- $p''_2(x_1,x_2) \Leftrightarrow x_1+x_2 \lt 149$. 

This system of constraints will lead to the following domains:
1. $p'1 \wedge p'_2 \Leftrightarrow (x_1=99) \wedge (x_1+x_2=149)$ 
2. $p'1_1 \wedge p''_2 \Leftrightarrow (x_1 = 99) \wedge (x_1+x_2 \lt 149)$
3. $p''_1 \wedge p'_2 \Leftrightarrow (x_1\le 98) \wedge (x_1+x_2=149)$ 
4. $p''_1 \wedge p''_2 \Leftrightarrow (x_1<99) \wedge (x_1+x_2<149)$  

Now, let's consider the simple case of the **Add(x1,x2)** for `unsigned int8` values.
Variable $x_1$ is in the domain $[0,255]$, variable $x_2$ is in the domain $[0,255]$.

The system of equations is:
- $p_1 \Leftrightarrow x_1\ge 0$
- $p_2 \Leftrightarrow x_1\le 255$
- $p_3 \Leftrightarrow x_2 \ge 0$
- $p_4 \Leftrightarrow x_2 \le 255$

(Note that we may also consider the constraint about the type of the output, e.g., $x_1+x_2 \leq 255$ for unsigned ints.)

This lead to the follow systems of equations: 
- 4 out of 4 combination of $p'_i$:
	- $P_{4/4} \Leftrightarrow p'1 \wedge p'_2 \wedge p'_3 \wedge p'_4$ 
- 3 out of 4 combinations of $p'_i$: 
	- $P_{3/4.1} \Leftrightarrow p'1 \wedge p'_2 \wedge p'_3 \wedge p''_4$ 
	- $P_{3/4.2} \Leftrightarrow p'1 \wedge p'_2 \wedge p''_3 \wedge p'_4$ 
	- $P_{3/4.3} \Leftrightarrow p'1 \wedge p''_2 \wedge p'_3 \wedge p'_4$ 
	- $P_{3/4.4} \Leftrightarrow  p''1 \wedge p'_2 \wedge p'_3 \wedge p_4$
- 2 out of 4 combinations of $p'_i$:
	- $P_{2/4.1} \Leftrightarrow  p'1 \wedge p'_2 \wedge p''_3 \wedge p''_4$ 
	- ...
	- $P_{2/4.6} \Leftrightarrow  p''1 \wedge p''_2 \wedge p'_3 \wedge p'_4$
- 1 out of 4 combinations of $p'_i$:
	- $P_{1/4.1} \Leftrightarrow  p'1 \wedge p''_2 \wedge p''_3 \wedge p''_4$ 
	- $P_{1/4.2} \Leftrightarrow p''1 \wedge p'_2 \wedge p''_3 \wedge p''_4$ 
	- $P_{1/4.3} \Leftrightarrow p''1 \wedge p''_2 \wedge p'_3 \wedge p''_4$ 
	- $P_{1/4.4} \Leftrightarrow p''1 \wedge p''_2 \wedge p''_3 \wedge p'_4$ 
- no $p'_i$:
	- $P_{0/4} \Leftrightarrow  p''1 \wedge p''_2 \wedge p''_3 \wedge p''_4$ 

Applied to our example, the problem simplifies since some of the predicates are incompatible (for instance $p'1$ and $p'_2$ cannot be true simultaneously and $p'_1 \implies p''_1$ because they respectively define the left and right bounds of the domain). This leads to the following predicates:
- $P_{4/4}:$ *no solution*
- $P_{3/4.i, i=1..4}:$ *no solution*
- $P_{2/4.1}: p'1 \wedge p'_2 \wedge p''_3 \wedge p''_4$ : *no solution*
- $P_{2/4.2}: p'1 \wedge p''_2 \wedge p'_3 \wedge p''_4$ : $(x_1=0) \wedge (x_2=0)$
- $P_{2/4.3}: p'1 \wedge p''_2 \wedge p''_3 \wedge p'_4$ : $(x_1=0) \wedge (x_2=255)$
- $P_{2/4.4}: p''1 \wedge p'_2 \wedge p'_3 \wedge p''_4$ : $(x_1=255) \wedge (x_2=0)$
- $P_{2/4.5}: p''1 \wedge p'_2 \wedge p''_3 \wedge p'_4$ : $(x_1=255) \wedge (x_2=255)$
- $P_{2/4.6}: p''1 \wedge p''_2 \wedge p'_3 \wedge p'_4$ : *no solution*
- $P_{1/4.1}:p'_1  \wedge p''_2 \wedge p''_3 \wedge p''_4$ : $(x_1=0) \wedge (x_2\in ]0,255[)$
- $P_{1/4.2}:p''_1  \wedge p'_2 \wedge p''_3 \wedge p''_4$ : $(x_1=255)\wedge (x_2\in ]0,255[)$
- $P_{1/4.3}:p''_1 \wedge p''_2 \wedge p'_3 \wedge p''_4$ : $(x_1\in ]0,255[) \wedge (x_2=0)$
- $P_{1/4.4}:p''_1 \wedge p''_2 \wedge p''_3 \wedge p'_4$ : $(x_1\in ]0,255[) \wedge (x_2=255)$
- $P0/4: p''_1 \wedge p''_2 \wedge p''_3 \wedge p''_4$ : $(x_1\in ]0,255[) \wedge (x_2\in]0, 255[)$

The application of this strategy leads to consider 9 classes defined as follows:
- 4 classes corresponding to the 4 edges of the domain
- 4 classes corresponding to the 4 vertices of the domain (edges excluded) 
- 1 class corresponding to the rest of the domain

This is illustrated on the following figure. The points represented by a red crosses correspond to 1 out of 4 combinations ; the points represented by blue crosses correspond to 2 out of 4 combinations. 

![[file-20260518180058243.png|408]]

In the case of the $Div(x,y)$ for signed integers, the domain of $y$ is $]-128,0[ \cup ]0, 127]$. By applying the same strategy, we end up with the following classes:
- Edges: (-128,-128),(-128,0),(-128,127),(127,-128),(127,0),(127,127)
- Boundaries: 
	- $(x=-128) \wedge (y \in ]-128,0[)$
	- $(x=-128) \wedge (y \in ]0,127[)$ 
	- $(x=127) \wedge (y \in ]-128,0[)$
	- $(x=127) \wedge (y \in ]0,127[)$
	- $(x\in]-127,128[) \wedge (y=-128)$
	- $(x\in]-127,128[) \wedge (y=127)$
- and the rest of the domain:
	- $(x\in]-127,128[) \wedge (y \in ]0,127[)$

In the case of SONNX, the definition of the input domain can be much more complex. and involve not only  type constraints for each variable, but also constraints relating multiple variables.
In the case of the **Maxpool** operator for instance, the input domain is defined by the following set of constraints (we consider the restricted version of the operator specified in SONNX and we only consider the structural parameters of the tensors, not their values):
- Type constraints
	- $\text{dilations}[0..1] \in \mathbb{N}$ 
	- $\text{strides}[0..1] \in \mathbb{N}$ 
	- $\text{pads}[0..3] \in \mathbb{N}$ 
	- $dX_{0..3} \in \mathbb{N}$ 
	- $dY_{0..3} \in \mathbb{N}$ 
	- $dW_{0..1} \in \mathbb{N}$ 
	- $X[i,j,k,l] \in \mathbb{N}$
	- $Y[i,j,k,l] \in \mathbb{N}$
- Functional constraints 
	- $\text{dilations}[0] > 0$
	- $\text{dilations}[1] > 0$
	- $\text{strides}[0]>0$
	- $\text{strides}[1] > 0$
	- The kernel shall not completely fit in the padding area (\*)
		- $\text{dilations}[0]\times(dW_0-1)+1 > \text{pads}[0]$
		- $\text{dilations}[0]\times(dW_0-1)+1 > \text{pads}[2]$
		- $\text{dilations}[1]\times(dW_1-1)+1 > \text{pads}[1]$
		- $\text{dilations}[1]\times(dW_1-1)+1 > \text{pads}[3]$
	- Size of the output tensor (\*\*)
		- $(dY_2-1)\times\text{strides}[0]+(\text{dilations}[0] (dW_0-1)+1) \le dX2+\text{pads}[0]+\text{pads}[2]$
		- $dY_2\times\text{strides}[0]+(\text{dilations}[0] (dW_0-1)+1) \gt dX2+\text{pads}[0]+\text{pads}[2]$

(\*) This constraint is due to the fact that the operator also returns the index of the maximum value **in the input tensor**. This index does not makes sense if the kernel completely "fits" in the padding area since, in that case, the maximum value is found in the padded area. 
In ONNX runtime, the constraint is stronger: the padding shall be smaller than the kernel size (before dilation).
(\*\*) If the size of output tensor is $dY_2$ , it means that the kernel has been applied $dY_2$ times on the input. The application of the kernel shall not overflow the padded tensor, so 

$$(dY_2-1)\times\text{strides}[0]+(\text{dilations}[0] (dW_0-1)+1) \le dX2+\text{pads}[0]+\text{pads}[2]$$ 

But the kernel shall be applied as many times as possible, so we have also 
$$dY_2\times\text{strides}[0]+(\text{dilations}[0] (dW_0-1)+1) \gt dX2+\text{pads}[0]+\text{pads}[2]$$

##### Solving the system of equations

When considering all constraints, finding all solutions can become extremely tedious. One possible solution is to use a constraint solver such as z3. An example is given in this [Jupyter notebook](https://colab.research.google.com/drive/14wIuDS6uYxWioI7IzVirBsSdbtp0xbct?usp=sharing).  

##### Eliminating useless combinations of constraints

Up to now, we have considered all possible combinations of constraints without considering the actual dependencies between those predicates and, more generally, between variables. 

The first case is the one where some predicates are incompatible.  For instance, when the predicates  define the boundaries of an interval (its left and right bounds),  they cannot be simultaneous true:  a value cannot be simultaneously the minimum and the maximum of the domain, except for intervals reduced to a unique value. Those combinations can be eliminated when building the set of constraints. However, if some solver is used (e.g., Z3), they can be left since they will easily be detected as "non satisfiable" (NONSAT) by the solver.

The second case concern combinations that are considered not pertinent with respect to the test objectives. By "not pertinent", we mean that *we do not expect a particular erroneous behaviour for that specific combination of values*.  

For instance, let's consider a pointwise operation such as **$Y$=Add($X_1$,$X_2$)**. It is not necessary (and usually impossible) to generate  test cases for every possible value of tensors $X_1$ and $X_2$. 
It is not necessary either to generate test cases so that for any couple of multi-index $(i, i')$, $X_1[i]$ and $X_1[i']$ takes every possible value in min, max, and some value in-between. Indeed, from a functional perspective, computation of $Y[i]$ does only depend on the input $X_1[i]$. 
Similarly, we consider that the behaviour of the operator does not depend on the exact value of the multi-index, so if the operator behaves correctly for some multi-index $i$, then we consider that it will behave correctly for any other multi-indexes $i'$.  In practice, this mean that we can test the operator on the domain of the elements of the input tensors for some multi-index $i$ to ensure that the computation on one element is correct. So we will test (e.g.) $X_1[0]+X_2[0]$ for all combinations in $\{\text{minint}, \text{maxint}, x \in ]\text{minint}, \text{maxint}[\}$. 

However, additional tests must be done with respect to the domain of the multi-indexes themselves, but we will not fully test the $X_1[i]+X_2[i]$  for each multi-index $i$ on the boundary of the multi-index domain. Instead, we will
- "fully" test the addition for some multi-index $i$ (e.g., $i=0$ for a unidimensional tensor, or an empty multi-index for a scalar tensor)
- test the addition on one value for each boundary of the multi-index domain. 

Stated differently, test cases are generated separately for each independent subset of variables so that we do not need to consider all combinations of constraints on the values of each element of each tensor of each possible multi-index.

However, the absence of dependency must be assessed. For instance, if we consider an operator that computes a matrix multiplication, we know that the accumulator creates a dependency between the size of the tensor and the values. Indeed, the greater the tensor and the greater the values contained in the tensor, the greater the value of the accumulator.  Since the accumulator may overflow (which is a classical fault model), we have to consider the specific combination of the largest sizes and the largest values! 
For instance, the **MatMulInteger** operator will overflow when multiplying two unsigned integer vectors of size $N> {2^{32}-1 \over 255^2}$  if all the values in the tensor are equal to 255.  

In the example of the **Maxpool** operator, we can consider the set of constraints concerning the first spatial dimension and the second spatial dimension separately, wihci

#####  Unbounded variables

All variables are bounded by their types but for some of them such as variables describing a structural property such as a rank or a dimension, the bounds defined by the type can not be tested. 

For instance the right bound of the tensor ranks and sizes domains can be -- theoretically -- as large as $2^{32}-1$ , but, in reality, those bounds are impossible to reach due to physical limits on the memory and/or execution time. In that case, tests shall be carried out against some arbitrary "limit" (for instance, a rank of 4 and a size  of 1000 per dimension...). Those arbitrary limits can be handled in exactly the same way as those reflecting the actual domain of the operator even though they do not reflect any functional limit. They can be considered as "usage domain" conditions, i.e., conditions reflecting the domain in which the operator are guaranteed to behave correctly.  

##### Symmetry and asymmetry

Consider the the `pads` parameter for the convolution. Besides testing the boundaries of the domain  (in 2D), we may also exercice certain relations between the parameters. For instance, we may want to exercize symmetric and asymmetric padding. It may be the case that by generating tests with respect to the bounds of the domain will also cover symmetric and asymmetric configurations (simply because we will generate a test for all combinations of min and max values for all paddings), but this is fortuitous. A good test strategy shall make this test against symmetry explicit. 

##### Test completeness

In our context, a test set is deemed complete relative to an operator specification if :
1. It covers every equivalence classes built upon data-types, for all data types supported by the operator
2. It covers every equivalence classes built upon the tensor shapes (rank and sizes)
3. It covers every equivalence classes built upon broadcasting
4. It covers every equivalence classes built upon the operator pre-conditions (so-called "constraints" in the specification)
5. It covers every equivalence classes built upon the operator functional specification 
6. (it covers every important implementation-risk pattern.)

### Domains
#### Type-specific domains
Type-specific domains are defined with respect to the data type.  They are independent of the semantics of operators.
##### Floating point numbers
For instance, for floating point number, the domains are the following (some domains are singletons): 
- NaN
- +inf, -inf
- +0, -0
- subnormal values (also called "denormalized" values)
	- for float: 
		- min positive: $2^{-149} \approx 1.45\times 10^{-45}$ 
		- max positive: $(1−2^{−23})\times 2^{−126} \approx 1.18×10^{-38}$
	- for double: 
		- min positive: $2^{-1074} \approx 4.9×10^{-324}$ 
		- max positive: $(1−2^{−52})\times2^{−1022} \approx 2.23\times 10^{-308}$
- normal value
	- for float:
		- min positive: $2^{-126} \approx 1.18×10^{-38}$ 
		- max positive: $(1-2^{-24})\times 2^{128} \approx 3.40 \times 10^{38}$
	- for double 
		- min positive: $2^{-1022} \approx 2.23\times 10^{-308}$ 
		- max positive:  $(1-2^{-53})\times 2^{1024} \approx 1.80 \times 10^{308}$

Note: Several reasons make subnormal values worth considering: 
- This is "where" underflows may occur (values rounded to 0)
- The relative precision of subnormal values is lower than for normal number. Indeed, normal numbers have *fixed relative* precision whereas subnormal numbers have *fixed absolute* spacing near zero. Therefore, their relative precision becomes worse as they get closer to zero. (However, note that accuracy is not addressed in the specification)
- The treatment of subnormal values may depend on the compiler / hardware platform
- The subnormal hey may expose corner cases in comparisons and branching (e.g., comparison to 0)

The domain is pretty complex, so a strict application of the test generation strategy will end-up with a very large number of test cases, even for an operator with two arguments. A strategy must be defined to restrict the number of combinations to be considered.  

##### Integer numbers
For integer numbers (uint, int):
- min int  (``minInt`` for the considered integer type)
- max int (``maxInt`` for the considered integer type)
#### Structure-specific domains

In the context of SONNX, a structure is a tensor characterized by its shape (number of dimensions -- or rank -- and a size per dimension).  The domains are defined with respect to these two parameters. 

In the context of SONNX, tests shall consider the 
- rank
	- scalar tensors (rank = 0)
	- vector (rank=1)
	- matrix (rank=2)
	- all other ranks
- dimension
	- null-tensors (at least one dimension with size zero)
	* multi-dimensional tensors reduced to a lower dimension tensor, such as a 2-dimensional tensor of shapes 1x1 (a scalar), 1xn (a line vector), nx1 (a column vector)
	* all other dimensions
#### Operator-specific constraints

Operator-specific constraints are derived from the operator semantics, that is to say from the informal (or formal) specification. They do not concern pre-conditions (which have been covered in the previous sections). 

We consider two general cases:
- the case of "special values", which consist in identifying of values playing a "special" role in the specification of the operator
- the case of "properties", which consists in identifying of special properties of the operator. 
##### Special values

The test designer has to consider the existence of:
- neutral values
- absorbing values
- dominating values 

For instance:
- for **Add** 
	- 0 :  neutral element
- for **Mul** 
	- 1 :  neutral element
	- 0 :  absorbing element
- for **Div** 
	- 1 at denominator : neutral element

- for **Max** 
	- +inf : absorbing value
	- -inf : neutral element
- etc.

Tests must be generated for all these values.

###### Example

For the **Maxpool** operator:
- `-inf` is a neutral element
- `+inf` is an absorbing element

##### Discontinuities 

Values representing a "discontinuity" in the function behavior (in the general and mathematical sense), including exceptional cases and error cases.

- for **Div** 
	- 0 at denominator :  discontinuity (division-by-zero)
- for **Relu** 
	- 0 :  Relu threshold
##### High-level functional properties
The test designer has to consider some generic properties of the operator such as :
- commutativity (**Add**, **Mul**, **Max**, etc.), 
- linearity (e.g., **Conv**(X+Y,W) = **Conv**(X,W)+**Conv**(Y,W)).
- invariance against a transformation (e.g., **Sin**(x)=**Sin**(x+2k\Pi), the indices returned by **MaxPool(** are invariant by the addition of a constant $c$ to all elements of the tensor). 

Tests must be generated to verify that these relations hold. 

###### Example
*To be completed.*


#### Testing against functional properties

Testing against the input domain was a matter of covering equivalence classes derived from the domain of definition of the operator. The domain of definition is defined considering type constraints and preconditions. 
Basically, we have considered two equivalence classes: 
- $Cb$: class of all inputs on the boundary of the domain of definition
- $Ci$: class of all inputs in the domain of definition, without the boundaries.   

Testing against the functional properties consists in partitioning $Cb \cup C_i$ the same domain considering the definition of the behaviour of the operator. 

For instance, the **Abs** operator is defined as follows for the floating point numbers, where $i$ is any multi-index compatible with the structure of $X$:
$$
Y[i] =
\begin{cases}
\text{NaN} & \text{if } X[i] = \text{NaN} \\
\text{+Inf} & \text{if } X[i] = \pm \text{Inf} \\
\text{+0} & \text{if } X[i] = \pm \text{0} \\
-X[i] & \text{if } X[i] \lt 0  \\
X[i] & \text{otherwise}
\end{cases}
$$
So, there must be a test for each of the classes defined by the conditions: 
- $p'1 : (X[i] = NaN)$
- $p'2 : (X[i] = +\text{Inf})$
- $p'3 : (X[i] = -\text{Inf})$
- $p'4 : (X[i] = -\text{0})$
- $p'5 : (X[i] = +\text{0})$
- $p'6 : (X[i] < 0) \wedge (X[i] \neq \text{-Inf})$
- $p'7 : (X[i] > 0) \wedge (X[i] \neq \text{+Inf})$

This operator applies on a signal argument $X$ characterized by
- a number $n$ of dimensions (or rank)
- a size for each dimension 
- a value of each element $X[i]$, with $i$ a multi-index compatible with the rank and sizes

The complete domain is the cartesian product  $\mathbb{F}^{dX_0+dX_1+ ... +dX_n}$  

As shown on the functional specification, the behaviour of the operator does not depend on the value of the muti-index $i$, so there is no need to exercice all combinations of $i$ (rank and sizes) and values. 
If for any given $i$, the operator behaves correctly for all of the values defined previously, then it is considered to behave correctly for all of the values and all $i$.  

### On values and indexes...

When designing the test, care shall be taken to verify that the result of the computation of some input value $X[i]$ for multi-index $i$  is actually stored at the appropriate output $Y[i']$. more generally, we are checking that $Y[i'_1]=f_1(X[i_1], X[i_2], ..., X[i_n]$, $Y[i'_2]=f_2(X[i_1], X[i_2], ..., X[i_n]$, etc.) which means that we are testing that the values are correct in the correct for the correct multi-indexes.  

As the indexes $i'$ are not explicit outputs of the operator, the test must be designed so that the value of $i'$ can be derived from the observation of the output tensor $Y$. For instance, when testing the **Mul($X1$,$X2$)** operator, the contents of $X1$ and $X2$ must be such that all expected values of $Y$ are different. Using $X2[i]=0$  for all $i$ will, for instance, not satisfy this property since all $Y[i']$ will be equal to zero so there will be no way to check that the 0 at $Y[i']$ have been computed from the appopriate $X1[i]$ and $X2[i]$ (in that case, $i$ = $i'$). 

The same constraint applies when dealing with structural operators such as **Flatten**. Note that the explicit property stating that the **Flatten** operator must preserve the values of the input tensor (invariance) is not sufficient since the output may well preserve the input values but place them at inappropriate indexes.  
