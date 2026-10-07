# Objectives and limits

**EM: my notes and correction are in bold**
**FV: my comments, corrections are in the file [accuracy.md](../../accuracy.md)**

## Introduction

This document provides theory and techniques to write a formal specification for the
accuracy of numerical components used in neural networks. The result is
a specification that should be verified by any implementation, **EM: under a narrow
set of acceptable assumption. Here is a list of accepted assumptions:**

* floating-point computation **conforming** to the IEEE-754 standard  
* fixed-point computation **[EM: for a given bit width? AFAIK, the ONNX
  standard only offers integer types, ergo any treatment of integer vs
  fractional part is left implicit]** **FV: The AIDGE platform may help
  to specify this point - integer division and integer right shift operation
  should have special meaning (but also combined with integer increment
  for rounding instead of truncating). **
* concrete or symbolic range for the input values **[EM: do we restrict the
  language in which symbolic ranges/constraints can be expressed? Any
  first-order logical expression over the reals?]** **FV: good question.
  Yes for the moment, but higher order logic may be interesting for
  algorithms providing the index of a tensor having a minimum value.
  To be seen later with examples**
* symbolic constraints over some computations  

There **may** exists **different** specifications for the accuracy **of the
same operator**. For instance, the specification for the matrix multiplication
will be different if one matrix is diagonal or if both matrices are dense with
a same order of magnitude for every coefficients.

We will favour short formulas, even if they may seem approximate. **[EM: are
they approximate or not?]** **FV: removed paragraph. To answer EM, if the
accuracy formula are equalities, they are exact, except if they are
existentially quantified; inequalities generate approximate formula**

# Principles of Numerical Accuracy Estimation
 
This section provides a tight and verifiable specification of the numerical error
on the operator's results. **In general, we define the numerical error as** the
difference between the current implementation on data with error resulting from
previous approximated computations and an ideal algorithm operating on data
also coming from previous ideal computations. **I.e. we consider the problem of
error accumulation throughout the SONNX graph, rather than studying each
operator in isolation** **FV: Yes, but we specify the numerical accuracy of
components, before specifying the numerical accuracy of the SONNX graph - the
approach oscillates between deductive verification and supervised abstract
interpretation (for the synthesis of formula)**

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x})$$

This framework decomposes the error into two parts:

* the first, the <span style="color:blue">propagated error</span>, depends on the numerical
  error and the numerical values of the inputs - in particular, it is independent of the
  implementation and the storage format  
* the second part, the <span style="color:red">introduced error</span>, depends on the
  concrete value of the inputs and the implementation with its storage format. 

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x}) = \textcolor{blue}{(op_{\textit{ideal}}(\overrightarrow{x+e}) - op_{\textit{ideal}}(\overrightarrow{x}))} + \textcolor{red}{(op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x+e}))}$$

The error associated with the result of the operator corresponds to the sum of
the propagated errors and the introduced error. **This new error is then
propagated to** the next operator.

## Specification and Verification Strategy

The provided specification **is based on** an over-approximated semantics of the
numerical error of native computer operations approximating real number
operations **(e.g. IEEE-754).** In order to preserve the readability of the
formulas, the general specification introduces additional (conservative)
simplifications compared to the original specifications.
However, this general specification may be too over-approximated for some
specific inputs (**e.g.** tensor representing diagonal matrices). In this case,
more precise specific specifications are provided alongside the general
specification.

The error specification comes with unit verification scenarios to verify the
implementation's conformity. In the absence of value ranges for the inputs, the
unit verification scenarios operate on symbolic values and errors to propagate
correct formulas throughout the scenario and thus provide a proof for the
assertions. In particular, the C implementation generated from the Why3 formal
specification must be verified using these scenarios, for example by using
symbolic instrumentation libraries.

**FV: Following the 15/07/2026 meeting, I started to introduce how to verify
the implementation. More in the section [Unit Verification](#unit-verification).
But I hesitate for this section - need more return of experiments from the
tooling.**

## Error Propagation

We split our analysis of numerical error in two parts. First, we analyse the
propagation of input error through ideal operators. Then, we analyse the
additional error introduced by non-ideal implementations.

**[EM: this section requires considerable polishing. I leave my suggestions as notes]**

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$,
the propagated error, where $Y$ is the tensor result of an operator.

It is only for information, since the properties does not depend on the
implementation. The formula aims to explain how an input error is amplified by
the operator just from its functional description. **[EM: why is it "only for
information"? It seems quite important to me: it's one of the two error terms
we must compute!]** **FV: I agree: the specification has at least two interests;
the first one is for the implementation that should conform to the
implementation and the second one is to produce models that can replace
the implementation in a modular verification approach. The propagated error
is not useful for the first interest but is essential for the second interest.**

**[EM: to make the point more general, why not $f: \mathbb{R}^n \longrightarrow \mathbb{R}^m$?]**
**FV: corrected in the document**

From the theoretical point of view, let us consider a function $f: \mathbb{R}^n
\longrightarrow \mathbb{R}^n$ and an existing error for each argument $x^i =
(x^i_{\textit{val}}, x^i_{\textit{err}})$.
**[EM: I am not sure this notation is useful. Why not keeping the $x^i+e^i$ notation used above?]**
**FV: replace by $x^i+e^i$ in the document**

### Estimation of the propagated error

The **propagated error** of the $f$ function as ideal operator is

$$f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} +
x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})$$

**[EM: with the simpler notation, this becomes:]**
$$f(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f(x^0, \ldots, x^{n-1})$$
**[EM: which would still require the reader to understand that $op_{ideal}$
above has become $f$ here. I would try to minimise the cognitive effort the
reader needs to put.]** **FV: just reminded before the title "Estimation of
the propagated error" (newly added). Possible to remplace f by
$op_{\textit{ideal}}$, but there is no more ambiguity between
$op_{\textit{ideal}}$ and  $op_{\textit{impl}}$ in this section because
$op_{\textit{impl}}$ is not concerned here**

Hence if $f$ is derivable two times, the formula**[EM: something is missing
here; we cannot differentiate w.r.t. $\delta x^i$ since it is defined as a
vector $x^i = (x^i_{\textit{val}}, x^i_{\textit{err}})$. Furthermore, the
definition of $X_{err}\leq 1$ is completely lost on me.]** **FV: it is a
typo $\ll$ instead of $\leq$. And the derivative is always relative to
$x^i_{\textit{val}}$. Moreover, it could be any norm and if the remainder
is negligeable, we cannot remove them for soundness reasons.**

$$\sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}} + \mathcal{O}(X^2_{\textit{err}})
  \textit{ where } X_{\textit{err}} = \max(x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{err}}) \leq 1$$

**[EM: I assume we are building a first-order Taylor expansion here w.r.t. the
error term. In my simplified notation, it becomes:]** **FV: partial derivative
with respect to the value, not the error - no need to add e^i in the derivative**
$$e_{prop}=\sum_{0 \leq i < n}\frac{\delta }{\delta e^i}f(x^0 + e^0, \ldots,
x^{n-1} + e^{n-1})e^i+\mathcal{O}(e_i^2)$$
**[EM: but it still contains some mysterious terms, e.g. why are we summing
over $i$? Shouldn't we compute the full Jacobian matrix, since $f: \mathbb{R}^n
\longrightarrow \mathbb{R}^m$? Even for a scalar function $f: \mathbb{R}^n
\longrightarrow \mathbb{R}^1$, the Taylor expansion would produce a gradient
vector; why not taking its norm, rather than adding the terms (which might
cancel out)?]** **FV: Yes, the Jacobian matrix is the correct notion here**

is a correct propagated error with the natural following definition for $\mathcal{O}(X^2_{\textit{err}})$:

$$\mathcal{O}(X^2_{\textit{err}}) = \left(f(x^0_{\textit{val}} +
x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) -
f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i <
n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots,
x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}$$

If there are no error on the arguments, the propagated error is $0$.
Otherwise, we **recommend** a first order expression like: **[EM: I vaguely
understand the intuition behind taking the L1 norm (absolute value); however, a
clearer explanation should be given to the reader (e.g. in terms of soundness
of the overapproximation). Also, are we still computing a separate error term
for each function output?]** **FV: It is just to offer a possibility of
simplification (among the 6 ones described below in the update accuracy.md).
Not sure it will be useful for the SONNX components**

The absolute value of the propagated error is less or equal than

$$\sum_{0 \leq i < n} \left| \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}}) \right| \times |x^i_{\textit{err}}|$$

### Example 1: Multiplication

For the multiplication $f(x, y) = x\times y$ in $\mathbb{R}\times\mathbb{R}\longrightarrow\mathbb{R}$, the **propagated error** $PE(f)$ is

$$\begin{array}{rcl}
PE(f) & = & (x_{\textit{val}} + x_{\textit{err}})\times (y_{\textit{val}} + y_{\textit{err}}) - x_{\textit{val}}\times y_{\textit{val}} \\
    & = & y_{\textit{val}}\times x_{\textit{err}} + x_{\textit{val}}\times y_{\textit{err}} + x_{\textit{err}}\times y_{\textit{err}}
\end{array}$$

that is simplified into

$$\begin{array}{rcl}
PE(f) & = & y_{\textit{val}}\times x_{\textit{err}} + x_{\textit{val}}\times y_{\textit{err}} + \mathcal{O}(X^2_{\textit{err}})
\end{array}$$

with $\mathcal{O}(X^2_{\textit{err}}) = x_{\textit{err}}\times y_{\textit{err}}$.

Hence, the accuracy definition of the operator will just indicate that

$$\begin{array}{rcl}
|PE(f)| & \leq & |y_{\textit{val}}| \times |x_{\textit{err}}| + |x_{\textit{val}}|\times |y_{\textit{err}}| + |\mathcal{O}(X^2_{\textit{err}})|
\end{array}$$

The definition of $\mathcal{O}(X^2_{\textit{err}})$ is optional, since it is
always **[EM: not sure what "optional" means here. That we do not need to
estimate the higher-order term because it is small? We might still need to do
so if we want a sound over-approximation...]** **FV: yes, you are right, I
removed optional in the file accuracy.md**

$$\begin{array}{rcl}
  \mathcal{O}(X^2_{\textit{err}}) & = & \left(f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}\\
  & = & (x_{\textit{val}} + x_{\textit{err}})\times(y_{\textit{val}} + y_{\textit{err}}) - x_{\textit{val}}\times y_{\textit{val}} - (y_{\textit{val}}\times x_{\textit{err}} + x_{\textit{val}}\times y_{\textit{err}})\\
  & = & x_{\textit{err}}\times y_{\textit{err}}
\end{array}$$

### Example 2: Division

For the division $g(x, y) = x / y$ in $\mathbb{R}\times\mathbb{R}\longrightarrow\mathbb{R}$, the **propagated error** $PE(g)$ is

$$\begin{array}{rcl}
PE(g) & = & \frac{x_{\textit{val}} + x_{\textit{err}}}{y_{\textit{val}} + y_{\textit{err}}} - \frac{x_{\textit{val}}}{y_{\textit{val}}} \\
    & = & \frac{y_{\textit{val}}\times x_{\textit{err}} - x_{\textit{val}}\times y_{\textit{err}}}{y_{\textit{val}}(y_{\textit{val}} + y_{\textit{err}})}
\end{array}$$

that is simplified into **[EM: by using the first-order Taylor expansion?]**

$$\begin{array}{rcl}
PE(g) & = & \frac{1}{y_{\textit{val}}}\times x_{\textit{err}} - \frac{x_{\textit{val}}}{y^2_{\textit{val}}}\times y_{\textit{err}} + \mathcal{O}(X^2_{\textit{err}})
\end{array}$$

The definition of $\mathcal{O}(X^2_{\textit{err}})$ is optional **[EM: ditto]**

$$\begin{array}{rcl}
  \mathcal{O}(X^2_{\textit{err}}) & = & \left(f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}\\
  & = & \frac{y_{\textit{val}}\times x_{\textit{err}} - x_{\textit{val}}\times y_{\textit{err}}}{y_{\textit{val}}(y_{\textit{val}} + y_{\textit{err}})} - \frac{1}{y_{\textit{val}}}\times x_{\textit{err}} - \frac{x_{\textit{val}}}{y^2_{\textit{val}}}\times y_{\textit{err}}\\
  & = & \frac{x_{\textit{val}}\times y^2_{\textit{err}} - y_{\textit{val}}\times x_{\textit{err}}\times y_{\textit{err}}}{y_{\textit{val}}^2(y_{\textit{val}} + y_{\textit{err}})}
\end{array}$$

Hence, the accuracy definition of the operator will just indicate that

$$\begin{array}{rcl}
|PE(g)| & \leq & \frac{1}{|y_{\textit{val}}|}\times |x_{\textit{err}}| + \frac{|x_{\textit{val}}|}{y^2_{\textit{val}}}\times |y_{\textit{err}}| + |\mathcal{O}(X^2_{\textit{err}})|
\end{array}$$

### Example 3: 2D Matrix multiplication

Tensor operators require a **more complex** methodology, since the algorithm combine many atomic operations on $\mathbb{R}$. **Again, the objective is deriving a sound** over-approximation of the propagated error.

**[EM: we suddenly switch to code, rather than standard mathematical notation
as above. This is not good, since we haven't yet introduced how the code
analysis work. In my opinion, examples should always be introduce after the
theory.]** **I just remind the SONNX specification here, but I need a support
that has lines to explain the intermediate annotations leading the final
specification**

1. Naïve Algorithm Description

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        for (int k = 0; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

2. Progressive decoration of the algorithm starting from inner loop **[EM:
there is an assumption that the error terms are in the form $|a[i][k]|\leq ae$,
rather than element-wise $|a[i][k]|\leq ae[i][j]$. This follows the spirit of
simplification stated at the beginning of the document. However, it is a big
design choice which (in my experience) will introduce a great deal of
over-approximation; thus, it should be given the space it deserves. E.g. create
a list of requirements/recommendation and clearly state: "For each
variable/tensor $x$ in the SONNX graph, we will compute a single error value
$x_e$, such that all variable/tensor entries satisfy $|x[i,j,\ldots,k]|\leq
x_e$".]** **FV: Yes, good remark. If the specification only aims to
differentiate "good" implementations from "bad" implementations, we can
remove the indices for $ae$. But if the specification is used to replace
the component in a modular verification, we need to differentiate
every coefficient. In the las case, and insprired from the meeting of the
15/07 (remark from Eric) we can produce a Mathematica code instead of an
analytic formula**

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // OAPE(C[i][j]) = 0
          C[i][j] += A[i][0]*B[0][j];
        // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
        // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
        // |PE(C[i][j])| <= a*be + b*ae
          C[i][j] += A[i][1]*B[1][j];
        // |PE(C[i][j])| <= 2*a*be + 2*b*ae
        for (int k = 2; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    By symplifying the formula, we progressively build a pattern that is
    candidate for a loop invariant **[EM: the reader must be well-versed in
    software verification and static analysis to know what a loop invariant is]**
    **FV: ok, replaced by the notion of proof by induction**

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // |PE(C[i][j]| = 0
        for (int k = 0; k < 2; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |PE(C[i][j]| <= k*a*be + k*b*ae
        for (int k = 2; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    If the pattern verify a loop induction, it becomes a loop invariant **[EM:
    how do we prove it satisfies a loop induction? We do not show it here]**
    **FV: Corrected**

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // PE(C[i][j]) = 0
        for (int k = 0; k < 2; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |PE(C[i][j])| <= k*a*be + k*b*ae

        int k = 2;
        // if |PE(C[i][j])| <= k*a*be + k*b*ae
          C[i][j] += A[i][k]*B[k][j];
        ++k;
        // then |PE(C[i][j])| <= k*a*be + k*b*ae // same formula than the induction hypotheses
        for (int k = 3; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    Then the loop invariant enables to establish the post-condition when
    exiting the loop **[EM: what is the post condition? We have not specified it]**
    **FV: removed the notion of post-condition**

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // PE(C[i][j]) = 0
        for (int k = 0; k < p; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |OAPE(C[i][j]| <= k*a*be + k*b*ae
        // |PE(C[i][j])| <= p*a*be + p*b*ae
    ```

3. Final specification **[EM: shouldn't this be presented at the beginning of
Example 3? That way the reader would have an idea of what the objective is.]**
**Yes: done**

    At the end, we can specify that

    * If A is a matrix of dimension $n \times p$, B a matrix of dimension $p \times q$,
    * if the absolute value of every coefficient of A is bound by $a$ with an error whose absolute value is bound by $ae$,  
    * if the absolute value of every coefficient of B is bound by $b$ with an error whose absolute value is bound by $be$,  
    * then the propagated error of every coefficient of C is bound by $p\times a\times be + p\times b \times ae$

#### Non-Ideal Operators

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$,
the introduced error, where $Y$ is the tensor result of an operator.
The objective is to provide a specification **over the actual implementation of an operator.** Hence

$$Y_{\textit{err}}^{\textit{intro}} = op_{\textit{impl}}(\overrightarrow{x}) - op_{\textit{ideal}}(\overrightarrow{x})$$

The introduced error is an over-approximation of difference between the implementation result and the ideal result when there is no error on the input.

**[EM: note that we switched back to the notation $op$ instead of $f$. Also, in
the document introduction, the implementation error is computed over
$\overrightarrow{x+e}$ rather than $\overrightarrow{x}$. The next paragraph
reads like an attempt at explaining whether this change of variables makes a
difference, but it is not clear enough.]** **FV: comment added in the text.
The change of variables is needed but any explanatation that I tryed rather
loses the reader. So I do not mention it, but yes, this is right**

From the theoretical point of view, the introduced error depends on the storage format of the result of any intermediate computation. It is always defined as the difference between the implementation result and the ideal result, for which we additionaly substract the propagated error of the previous section.

##### IEEE-754 implementations

**[EM: what about fixed-point/integer/quantised ones? Will we add them to the guidelines later?]**
**FV: Yes, but I am not familiar with this point. A return from experiments
from the AIDGE platform could help.**

For IEEE-754 format, let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\bf u} = \frac{\varepsilon}{2}$. For every floating-point operator
whose result $r$ is a normal floating-point number, the introduced error is less or equal than
$|r| \times \frac{\varepsilon}{2} = |r| \times \textit{\bf u}$ in the standard mode
round to nearest even. **[EM: this is an oversimplification, as it does not
take into account subnormal numbers and catastrophic cancellation. If the
result of the operation is $r\approx0$, the actual error might be much larger
than $|r|\times\frac{\varepsilon}{2}$]** **FV: This is sound if $a$ and $b$
normal, even if there exists denormal numbers in $[a, b]$, since the error
introduced is monotonic. And if *a* or *b* is denormal, it is sufficient
to choose a greater $a$ or $b$.**

Moreover if $r \in [a, b]$ with $a$ and $b$ normal numbers (the interval
may contain denormal numbers), the introduced error is less or equal than
$\max(|a|, |b|) \times \textit{\bf u}$ in the standard mode round to nearest even.
There exists more accurate formulas, but such formulas usually take too much
details into account.**[EM:I approve of our simplification objective, but is
our error estimate sound? If not, I feel we should give the readers more
details on our design decisions, to convince them that what we are doing is
sensible.]** **FV: yes, we need to be sound, even for denormal numbers.
Try to give more details in the examples**

#### Example 4 (IEEE-754 multiplication)

For the multiplication $f(x, y) = x * y$, the **introduced error** $IE(f)$
should be less or equal than **[EM: are we using "should" as a prescriptive
word here (e.g. any SONNX-compliant implementation must satisfy this)? It is
the first truly prescriptive statement in this document.]** **yes: This is
the first example for which we give a specification that the implementation
should follow.**

$$\begin{array}{rcl}
|IE(f)| & \leq & |x|\times |y|\times\textit{\bf u}
\end{array}$$

for any floating-point implementation with the standard rounding mode round to
nearest even, provided $|x|\times |y|$ is a normal number **[EM: should we give
some extra context in these examples. E.g. "the IEEE-754 standard mandates that
any implementation of the multiplication operator $x_{float}\times_{float}
y_{float}$ must yield the same result as executing the operations in
infinite-precision (ideal) arithmetic and then rounding the result, i.e.
$float(x_{float}\times y_{float})$. Hence, the error only depends from the
magnitude of the result $|x|\times|y|$ and the representable precision $|u|$."]**
**FV: there are many rules to compute a precise accuracy, but here we only
keep the information about the bounds of the relative accuracy (less or equal
than $u$ for normal bounds). Don't know how to provide better explanations**

$$\begin{array}{rcl}
|IE(f)| & \leq & \max(|a|, |b|)\times \max(|c|, |d|)\times\textit{\bf u}
\end{array}$$

for any floating-point implementation with the standard rounding mode round to nearest even, provided
$x \in [a, b], y \in [c, d]$ and $\max(|a|, |b|)\times \max(|c|, |d|)$ is a normal number.

$$\begin{array}{rcl}
|IE(f)| & < & \max(|a|, |b|)\times \max(|c|, |d|)\times\varepsilon
\end{array}$$

for any floating-point implementation with other rounding mode, provided
$x \in [a, b], y \in [c, d]$ and $\max(|a|, |b|)\times \max(|c|, |d|)$ is a normal number.


$$\begin{array}{rcl}
|IE(f)| & < & 1
\end{array}$$

for any fixpoint implementation. **[EM: we only mentioned fixed-point
implementation en passant so far. This error definition makes me think we are
referring to integer implementations, otherwise the error would be fractional.
Also, how does ONNX/SONNX deals with integer overflows?]**
**FV: move in the integer section - to be completed**

### Example 5 (IEEE-754 division)

For the division $g(x, y) = x / y$, the **introduced error** $IE(g)$ should be less or equal than

$$\begin{array}{rcl}
|IE(g)| & \leq & \frac{|x|}{|y|}\times\textit{\bf u}
\end{array}$$

for any floating-point implementation with the standard rounding mode round to nearest even, provided
$\frac{|x|}{|y|}$ is a normal number

$$\begin{array}{rcl}
|IE(g)| & \leq & \frac{\max(|a|, |b|)}{\min(|c|, |d|)}\times\textit{\bf u}
\end{array}$$

for any floating-point implementation with the standard rounding mode round to nearest even, provided
$x \in [a, b], y \in [c, d], 0 \not\in [c, d]$ and $\frac{\max(|a|, |b|)}{\min(|c|, |d|)}$ is a normal number

$$\begin{array}{rcl}
|IE(g)| & < & \frac{\max(|a|, |b|)}{\min(|c|, |d|)}\times\varepsilon
\end{array}$$

for any floating-point implementation with other rounding mode, provided
$x \in [a, b], y \in [c, d], 0 \not\in [c, d]$ and $\frac{\max(|a|, |b|)}{\min(|c|, |d|)}$ is a normal number

$$\begin{array}{rcl}
|IE(g)| & < & 1
\end{array}$$

for any fixpoint implementation. **[EM: see the above comments about
fixed-point for multiplication (no overflow here).]**
**FV: it is the right shift after the multiplication that loses bits
of accuracy, not the multiplication itself.**

### Example 6 (IEEE-754 2D matrix multiplication)

Tensor operators require a methodology to find an **over-approximation of the
introduced error**, since their algorithms combine many atomic operations.
**[EM: many of my comments on Example 3 are also valid here]** **FV: More explanations
for this section too**

1. Naïve Algorithm Description

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        for (int k = 0; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

2. Progressive decoration of the algorithm starting from inner loop **[EM: I do
not understand where the term $2*a*b*(1+u)*u$ comes from. Is it a result of the
accumulation/addition? More explanation is needed.]** **FV: more comments in 
the file accuracy.md.**

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // IE(C[i][j]) = 0
          C[i][j] += A[i][0]*B[0][j];
        // the absolute value of every coefficient of A is bound by 'a'
        // the absolute value of every coefficient of B is bound by 'b'
        // |IE(C[i][j])| <= a*b*u
        // |C[i][j]| <= a*b*(1+u)
          C[i][j] += A[i][1]*B[1][j];
        // |IE(C[i][j])| <= a*b*u + a*b*u + 2*a*b*(1+u)*u = a*b*u*(4+2u)
        // |C[i][j])| <= (a*b*(1+u) + a*b*(1+u))*(1+u) = 2*a*b*(1+u)²
          C[i][j] += A[i][2]*B[2][j];
        // |IE(C[i][j])| <= a*b*u*(4+2u) + a*b*u + (2*a*b*(1+u)² + a*b*(1+u))*u = a*b*u*(8+7u+2u²)
        // |C[i][j]| <= (2*a*b*(1+u)² + a*b*(1+u))*(1+u) = (3+2*u)*a*b*(1+u)²
        for (int k = 3; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    By symplifying the formula, we progressively build a pattern that is candidate for a loop invariant

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a'
    // the absolute value of every coefficient of B is bound by 'b'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // IE(C[i][j]) = 0
        for (int k = 0; k < 2; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b
          // |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
        for (int k = 2; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    If the pattern verify a loop induction, it becomes a loop invariant

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a'
    // the absolute value of every coefficient of B is bound by 'b'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // IE(C[i][j]) = 0
        for (int k = 0; k < 2; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b
          // |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²

        int k = 2;
        // if       |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b
        // and if   |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
        // if OAPE(C[i][j]) <= k*a*be + k*b*ae
          C[i][j] += A[i][k]*B[k][j];
        ++k;
        // then     |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b // same formula than the induction hypotheses
        // and then |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
        for (int k = 3; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    Then the loop invariant enables to establish the post-condition when exiting the loop

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    // the absolute value of every coefficient of A is bound by 'a'
    // the absolute value of every coefficient of B is bound by 'b'
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        // IE(C[i][j]) = 0
        for (int k = 0; k < p; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b // same formula than the induction hypotheses
          // |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
        // |IE(C[i][j])| <= (((1+u)^(p+1)-1)/u*(1+u)² - p-1)*a*b // same formula than the induction hypotheses
        // |C[i][j])| <= ((1+u)^(p+1)-1)/u*a*b*(1+u)²
    ```

Hence, for the matrix multiplication of A, matrix of dimension $n \times p$
with B, matrix of dimension $p \times q$, the **introduced error** should be
less or equal than **[EM: more explanation on this is needed. (1) why is this a
sound over-approximation and (2) how can you automatically compute it for an
arbitrary implementation?]** **FV: all simplifications are sound; automatic
computation is not possible, but LLM can help. No idea on how to develop this
point.**

$$\begin{array}{rcl}
  |IE(C[i][j])| & \leq & \left(\frac{(1+u)^{p+1}-1}{u}\times(1+u)^2 - p-1\right)\times a \times b\\
                & \leq & \left(\frac{(1+u)^{p+1}-1-(p+1)\times u }{u^2}\times(1+u)^2 - (p+1)\times(2+u)\right)\times a \times b \times u\\
\end{array}$$

where the absolute value of every coefficient of A is bound by $a$ and the absolute value of every coefficient of B is bound by $b$.

### Unit Verification

**[EM: incomplete section]**

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

# Formal specification guidelines

*To be completed.*
