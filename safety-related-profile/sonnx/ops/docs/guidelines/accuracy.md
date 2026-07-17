# Objectives and limits

## Introduction

This document provides guidelines to conduct the accuracy analysis of the SONNX
numerical operators. 

SONNX does not provide a definitive specification of accuracy. Instead, it
provides a way to estimate the error of a specific implementation with respect
to an ideal algorithm that would implement integer arithmetic or floating point
arithmetic according to IEEE754.

Towards that goal, SONNX provides:
- an analytical expression of the upper bound of the error considering some
  ideal algorithm applying integer or IEEE 754 arithmetic and
  under a narrow set of acceptable assumptions  
- a tool to estimate numerically an upper bound of the error of a given implementation.
  
Notes:  
1. There may exist multiple ideal algorithms for any operator. In SONNX, we use
   the algorithm that is given in the informal specification.
2. There exists an infinite number of upper bounds of the error, some of them
   being more conservative (less accurate) than others. The accuracy of the
   estimation first depends on the simplifications done to facilitate calculus.
   It may also depend on the hypotheses done concerning the domain of the
   operator arguments. For instance, the estimation of the error bound for a
   matrix multiplication may be different under the hypothesis that one matrix
   is diagonal or under the hypothesis that both matrices are dense with a same
   order of magnitude for every coefficients.</br>
   In SONNX, we estimate accuracies according to the following principles:
   - we favour manageable formulas (simple and short) even if this leads to
     very conservative accuracy estimation
   - we make no hypothesis about the domain of the arguments of operators.  
3. The acceptable assumptions provide concrete or symbolic ranges for the imput values
   in first-order logical expressions. It is likely to provide a floating-point
   or an integer format for the operator interface.

# Principles of Numerical Accuracy Estimation
 
The numerical error is the difference between the implemented algorithm
$op_{\textit{impl}}$ applied on data with error resulting from previous
approximated computations and an ideal algorithm $op_{\textit{ideal}}$
operating on data also coming from previous ideal computations:

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x})$$

Note: we consider the problem of error accumulation throughout the SONNX graph,
rather than studying each operator in isolation

We decompose the error into

* a <span style="color:blue">propagated error</span> depending on the numerical
  error and the numerical values of the inputs $-$ in particular, it is
  independent of the implementation and the storage format  
* a <span style="color:red">introduced error</span> depending on the
  concrete value of the inputs and the implementation with its storage format. 

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x}) = \textcolor{blue}{(op_{\textit{ideal}}(\overrightarrow{x+e}) - op_{\textit{ideal}}(\overrightarrow{x}))} + \textcolor{red}{(op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x+e}))}$$

The error associated with the result of the operator corresponds to the sum of
the propagated errors and the introduced error. This new error is then
propagated to the next operator.

## Specification and Verification Strategy

In order to simplify the calculus and preserve the readability of the formulas,
the provided estimations may result from the application of conservative
simplifications   of the native computer operations (e.g., IEEE 754). In some
cases, additional hypotheses about the operator arguments (e.g., the fact that
the matrices are diagonal) are done alongside the general formulation to
provide more accurate estimations.

The error specification comes with unit verification scenarios to verify the
implementation's conformity. In the absence of value ranges for the inputs, the
unit verification scenarios operate on symbolic values and errors to propagate
correct formulas throughout the scenario and thus provide a proof for the
assertions. In particular, the C implementation generated from the Why3 formal
specification must be verified using these scenarios, for example by using
symbolic instrumentation libraries.

An implementation that claims to check the accuracy specification should
precise the set of the specification assumptions it has been verified.
It should also define the verification method with the guarantees it brings.
Here is a list of possible verification methods that can be combined:

* manual (or aided with tools) symbolic reasoning about the accuracy of
  the implementation,  
* static analysis verification with additional ranges assumptions for the
  input values - CPU offline verification for small components,  
* dynamic analysis synchronous stochastic verification - CPU or GPU,
  off-line for big compononents, on-line for small components,  
* dynamic analysis asynchronous stochastic verification - CPU or GPU,
  off-line for big compononents, on-line for small components,
* dynamic analysis asynchronous concrete verification - CPU or GPU,
  could be on-line for big compononents.

## Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$,
the propagated error, where $Y$ is the tensor result of an operator.

**This section is only for information**: the propagated error is not part of
the SONNX specification since it is completly independent from the
implementation. The formula aims to explain how an input error is amplified by
the operator just from its functional description. However, it is useful for
the error specification of a sequence of operators since the numerical error
created by the first operator is then amplified by the next operators.

From the theoretical point of view, let us consider $op_{ideal}$ as a function
$\textbf{f}: \mathbb{R}^n \longrightarrow \mathbb{R}^m$ and an input vector
error $E = (e^i)$ for the vector argument $X = (x^i)$ with $i \in [0, n-1]$.

### Estimation of the propagated error

The **propagated error** of the $\textbf{f} = (f^0, \ldots, f^{m-1})$ function as ideal
operator is $\forall 0 \leq j < m$

$$f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0, \ldots, x^{n-1})$$

Hence if $\textbf{f}$ is derivable two times, the formula $\forall 0 \leq j < m$

$$\sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}
  (x^0, \ldots, x^{n-1})\times e^i + \mathcal{O}(E^2)
  \textit{ where } E = \max(e^0, \ldots, e^{n-1}) \ll 1$$

is a correct propagated error with the natural following definition for
$\mathcal{O}^j(E^2)$:

$$\mathcal{O}^j(E^2) = \left(f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0,
\ldots, x^{n-1})\right) - \sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}(x^0,
\ldots, x^{n-1})\times e^i$$

In term of matrix computations, this means

$$\mathcal{O}^j(E^2) = \left(\textbf{f}(X + E) - \textbf{f}(X)\right) -
  (\textbf{J}_{\textbf{f}}) (E)$$

where $\textbf{J}_{\textbf{f}}$ is the Jacobian matrix of the function $\textbf{f}$.

If there are no error on the arguments, the propagated error is $0$.
Otherwise, we propose to choose the more concise formula between the
formulations below:

* $\forall 1 \leq j < m. \, f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0, \ldots, x^{n-1})$  
* $\textbf{f}(X+E) - \textbf{f}(X)$  
* $\forall 0 \leq j < m. \, \sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}
  (x^0, \ldots, x^{n-1})\times e^i + \left(f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0,
  \ldots, x^{n-1}) - \sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}(x^0,
  \ldots, x^{n-1})\times e^i\right)$ 
* $\textbf{J}_{\textbf{f}}(E)$ + $\left(\textbf{f}(X + E) - \textbf{f}(X) - (\textbf{J}_{\textbf{f}})(E)\right)$  
* $\forall 0 \leq j < m$, the absolute value of the propagated error is bound
  by $|f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0, \ldots, x^{n-1})|$  
* $\forall 0 \leq j < m$, the absolute value of the propagated error is bound
  by $\sum_{0 \leq i < n} \max_{-|e^i| \leq e'_i \leq |e^i|}\left(\left|
  \frac{\delta f}{\delta x^i}(x^0+e'_0, \ldots, x^{n-1}+e'_{n-1}) \right|
  \right) \times |e^i|$ (mean value inequality theorem)

### Example 1: Multiplication

Let us consider the multiplication operation $f(x^0, x^1) = x^0\times x^1$ in
$\mathbb{R}\times\mathbb{R}\longrightarrow\mathbb{R}$
 
For the multiplication, the **propagated error** $PE(f)$ is

$$\begin{array}{rcl}
PE(f) & = & (x^0 + e^0)\times (x^1 + e^1) - x^0\times x^1 \\
      & = & x^1\times e^0 + x^0\times e^1 + e^0\times e^1
\end{array}$$

that is simplified by using the first-order Taylor expansion into

$$\begin{array}{rcl}
PE(f) & = & x^1\times e^0 + x^0\times e^1 + \mathcal{O}(E^2)
\end{array}$$

with $\mathcal{O}(E^2) = e^0\times e^1$.

Hence, the accuracy definition of the operator will either indicate

$$\begin{array}{rcl}
|PE(f)| & \leq & |x^1| \times |e^0| + |x^0|\times |e^1| + |\mathcal{O}(E^2)|
\end{array}$$

with the generic definition for $\mathcal{O}(E^2)$

$$\begin{array}{rcl}
  \mathcal{O}(E^2) & = & \left(f(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f(x^0, \ldots, x^{n-1})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0, \ldots, x^{n-1})\times e^i\\
  & = & (x^0 + e^0)\times(x^1 + e^1) - x^0\times x^1 - (x^1\times e^0 + x^0\times e^1)\\
  & = & e^0\times e^1
\end{array}$$

or indicate

$$\begin{array}{rcl}
|PE(f)| & \leq & \max_{-|e^0| \leq e'_0 \leq |e^0|, -|e^1| \leq e'_1 \leq |e^1} |x^1+e'_1| \times |e^0| + |x^0+e'_0|\times |e^1| \\
|PE(f)| & \leq & (|x^1|+|e^1|) \times |e^0| + (|x^0|+|e^0|)\times |e^1|
\end{array}$$

### Example 2: Division

Let us consider the division operation $g(x, y) = x / y$ in
$\mathbb{R}\times\mathbb{R}\longrightarrow\mathbb{R}$

For the division, the **propagated error** $PE(g)$ is

$$\begin{array}{rcl}
PE(g) & = & \frac{x^0 + e^0}{x^1 + e^1} - \frac{x^0}{x^1} \\
    & = & \frac{x^1\times e^0 - x^0\times e^1}{x^1(x^1 + e^1)}
\end{array}$$

that is simplified by using the first-order Taylor expansion into

$$\begin{array}{rcl}
PE(g) & = & \frac{1}{x^1}\times e^0 - \frac{x^0}{y^2_{\textit{val}}}\times e^1 + \mathcal{O}(E^2)
\end{array}$$

with the generic definition for $\mathcal{O}(E^2)$

$$\begin{array}{rcl}
  \mathcal{O}(E^2) & = & \left(f(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) -
    f(x^0, \ldots, x^{n-1})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0, \ldots, x^{n-1})\times e^i\\
  & = & \frac{x^1\times e^0 - x^0\times e^1}{x^1(x^1 + e^1)} - \frac{1}{x^1}\times e^0 - \frac{x^0}{(x^1)^2}\times e^1\\
  & = & \frac{x^0\times (e^1)^2 - x^1\times e^0\times e^1}{(x^1)^2(x^1 + e^1)}
\end{array}$$

Hence, the accuracy definition of the operator will either indicate

$$\begin{array}{rcl}
|PE(g)| & \leq & \frac{1}{|x^1|}\times |e^0| + \frac{|x^0|}{(x^1)^2}\times |e^1| + |\mathcal{O}(E^2)|
\end{array}$$

or indicate

$$\begin{array}{rcl}
|PE(f)| & \leq & \max_{-|e^0| \leq e'_0 \leq |e^0|, -|e^1| \leq e'_1 \leq |e^1}\left(
\frac{1}{|x^1-e'_1|}\times |e^0| + \frac{|x^0+e'_0|}{(x^1-e'_1)^2}
\times |e^1|\right)\\
& \leq & \frac{1}{\max(|x^1|-|e^1|, 0)}\times |e^0| + \frac{|x^0|+|e^0|}{\max((|x^1|-|e^1|, 0))^2}
\times |e^1|
\end{array}$$

### Example 3: 2D Matrix multiplication

Tensor operators require a more complex methodology, since the algorithm
combine many atomic operations on $\mathbb{R}$. Again, the objective is
deriving a sound over-approximation of the propagated error.

The mathematical definition specified in the
[SONNX informal specification](../../spec/informal/matmul/matmul.md) of
the operator is given hereafter .

$$
  \forall i \in [0, dA_0 - 1], \forall j \in [0, dB_1 - 1] \quad Y[i,j] = \sum_{k=0}^{dA_1-1} A[i,k]\times B[k,j]
$$

with $p = dA_1 = dB_0$, $n = dA_0$, $q = dB_1$.

This suggests the combination of the operators $+$ and $\times$, each one
being likely to introduce numerical errors.

Here are possible specifications of the propagated error

1. If all the coefficients of the matrix $A$ are bound by $a$ and the error by $ea$
   and if all the coefficients of the matrix $B$ are bound by $b$ and the error by $eb$,
   then all the coefficients of the result matrix carry a propagated error
   bound by $p\times((a + ea)\times(b + eb)- a\times b)$.  

2. The coefficients $c[i][j]$ of the result matrix carry a propagated error
   $ec[i][j]$ bound by following computation (Wolfram language of Mathematica) in real
   number.

   ```
   ec[i][j] = 0;
   For (k = 0, k < p, k = k+1, ec[i][j] += ((a[i][k]+ea[i][k])*(b[k][j]+eb[k][j]) - a[i][k]*b[k][j]))
   ```

It is possible to incrementaly build these specifications with the 
following methodology. Here is how we build the first specification

1. Naïve Algorithm Description

Since it is simpler to provide intermediate annotations inside code lines than a formula,
we suggest to translate the formula in a naive way to compute it.

    ```c++
    // A matrix of dimension n x p, B matrix of dimension p x q.
    // C result matrix of dimension n x q
    for (int i = 0; i < n; ++i)
      for (int j = 0; j < q; ++j) {
        C[i][j] = 0;
        for (int k = 0; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

2. Progressive decoration of the algorithm starting from inner loop

To simplify the specification and to benefit from simplifications in the
annotations, we add some assumptions:

* the absolute value of every coefficient of A is bound by 'a' with an error
  whose absolute value is bound by 'ae'  
* the absolute value of every coefficient of B is bound by 'b' with an error
  whose absolute value is bound by 'be'

These assumptions are likely to introduce big over-approximations, especially
for non-dense matrices. The specifier can introduce different assumptions
or not introduce any assumption but provide a code in real numbers to
"compute" the specification of the error (see point 4. instead of a formula).

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
        // |PE(C[i][j])| <= a*be + b*ae + ae*be
          C[i][j] += A[i][1]*B[1][j];
        // |PE(C[i][j])| <= 2*a*be + 2*b*ae + 2*ae*be
        for (int k = 2; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    By symplifying the formula, we progressively build a pattern that is candidate
    for a proof by induction

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
          // |PE(C[i][j]| <= k*a*be + k*b*ae + k*ae*be
        for (int k = 2; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    If the pattern verifies the loop induction - the annotations at the end of the
    loop body matches with (or are included in) the annotations at the beginning of
    the loop body, it becomes a property that holds (infinitely) for every loop cycle.

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
          // |PE(C[i][j])| <= k*a*be + k*b*ae + k*ae*be

        int k = 2;
        // if |PE(C[i][j])| <= k*a*be + k*b*ae + k*ae*be
          C[i][j] += A[i][k]*B[k][j];
        ++k;
        // then |PE(C[i][j])| <= k*a*be + k*b*ae + k*ae*be // same formula than the induction hypotheses
        for (int k = 3; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    Then the porpoerty inside the loop enables to establish a property that
    holds after the loop by adding the constraints exiting the loop.

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
          // |OAPE(C[i][j]| <= k*a*be + k*b*ae + k*ae*be
        // |PE(C[i][j])| <= p*a*be + p*b*ae + p*ae*be
    ```

3. Final specification

    At the end, we can specify that

    * If A is a matrix of dimension $n \times p$, B a matrix of dimension $p \times q$,
    * if the absolute value of every coefficient of A is bound by $a$ with an error whose absolute value is bound by $ae$,  
    * if the absolute value of every coefficient of B is bound by $b$ with an error whose absolute value is bound by $be$,  
    * then the propagated error of every coefficient of C is bound by $p\times a\times be + p\times b \times ae + p\times ae\times be$

4. Generic specification as a Mathematica code

[TODO]

## Error Introduction with non-Ideal Operators

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$,
the introduced error, where $Y$ is the tensor result of an operator.
The objective is to provide a specification over the actual implementation of
an operator. Hence

$$Y_{\textit{err}}^{\textit{intro}} = op_{\textit{impl}}(\overrightarrow{x}) - op_{\textit{ideal}}(\overrightarrow{x})$$

The introduced error is an over-approximation of difference between the
implementation result and the ideal result when there is no error on the input.

In this section, we switch back to the notation $op$ instead of
$f = op_{\textit{ideal}}$ to make a clear distinction between
$op_{\textit{impl}}$ and $op_{\textit{ideal}}$.

From the theoretical point of view, the introduced error depends on the storage
format of the result of any intermediate computation. It is always defined as
the difference between the implementation result and the ideal result, for
which we additionaly substract the propagated error of the previous section.

### IEEE-754 implementations

The introduced error is an over-approximation of difference between the
implementation result and the ideal result when there is no error on the input.

For IEEE-754 format, let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\bf u} = \frac{\varepsilon}{2}$. For every floating-point operator
whose result $r$ is a normal floating-point number, the introduced error is less or equal than
$|r| \times \frac{\varepsilon}{2} = |r| \times \textit{\bf u}$ in the standard mode
round to nearest even. Moreover if $r \in [a, b]$ with $a$ and $b$ normal numbers (the interval
may contain denormal numbers), the introduced error is less or equal than
$\max(|a|, |b|) \times \textit{\bf u}$ in the standard mode round to nearest even.

Note that there exists more accurate formulas, but by application of the
principles stated introduction, we use a formulation that is remains simple and
acceptably conservative. 

#### Example 4 (IEEE-754 multiplication)

Let us consider the multiplication operation: $op_{\textit{impl}}(x, y) = f(x, y) = x * y$. 

The **introduced error** of any SONNX-compliant implementation $IE(f)$ should be less or equal
than

$$\begin{array}{rcl}
|IE(f)| & \leq & |x|\times |y|\times\textit{\bf u}
\end{array}$$

for any floating-point implementation with the standard rounding mode round to nearest even, provided
$|x|\times |y|$ is a normal number

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


### Example 5 (IEEE-754 division)

Let us consider the division operation: $op_{\textit{impl}}(x, y) = g(x, y) = x / y$

The **introduced error** of any SONNX-compliant implementation $IE(g)$ should be less or equal than

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

### Example 6 (IEEE-754 2D matrix multiplication)

The mathematical definition specified in the
[SONNX informal specification](../../spec/informal/matmul/matmul.md) of
the operator is given hereafter .

$$
  \forall i \in [0, dA_0 - 1], \forall j \in [0, dB_1 - 1] \quad Y[i,j] = \sum_{k=0}^{dA_1-1} A[i,k]\times B[k,j]
$$

with $p = dA_1 = dB_0$, $n = dA_0$, $q = dB_1$.

Tensor operators require the [methodology of the propagated error](#example-3:-2d-matrix-multiplication)
to find an **over-approximation of the introduced error**, due to the
combination of many atomic operations.

Here are possible specifications for the introduced error of any IEEE-754 SONNX-compliant
implementation

1. If all the coefficients of the matrix $A$ are bound by $a$
   and if all the coefficients of the matrix $B$ are bound by $b$,
   then all the coefficients of the result matrix should carry an introduced
   error bound by $\left((1+u)^2\times \frac{(1+u)^p-1}{u} - n\right)\times a\times b$.  

2.  Let us define `min_normalized` is the smallest positive normalized number, then
   Then, the coefficients $c[i][j]$ of the result matrix carry a propagated error
   $eic[i][j]$ bound by following computation (Wolfram language of Mathematica) in real
   number.

   ```
   eic[i][j] = 0; epc[i][j] = 0; c[i](j] = 0; eic[i](j] = 0;
   For (k = 0, k < p, k = k+1,
     m[i][j] = a[i][k] * b[k][j];
     eim[i][j] = u*max(abs(m[i][j]), min_normalized);
     c[i][j] = c[i][j] + m[i][j];
     eic[i][j] = (1+u)*(eic[i][j] + eim[i][j]) + u*max(abs(c[i][j] ), min_normalized))
   ```

It is possible to incrementaly build these specifications with the 
following methodology. Here is how we build the first specification


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

2. Progressive decoration of the algorithm starting from inner loop

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
        // The introduced error is the one due to the multiplication  
        // at A[i][0]*B[0][j] and at  A[i][1]*B[1][j]:  a*b*u + a*b*u
        // plus the one due to the addition: (a*b*(1+u)+a*b(1+u))*u  
        // |IE(C[i][j])| <= a*b*u + a*b*u + 2*a*b*(1+u)*u = a*b*u*(4+2u)
        // |C[i][j])| <= (a*b*(1+u) + a*b*(1+u))*(1+u) = 2*a*b*(1+u)²
          C[i][j] += A[i][2]*B[2][j];
        // |IE(C[i][j])| <= a*b*u*(4+2u) + a*b*u + (2*a*b*(1+u)² + a*b*(1+u))*u = a*b*u*(8+7u+2u²)
        // |C[i][j]| <= (2*a*b*(1+u)² + a*b*(1+u))*(1+u) = (3+2*u)*a*b*(1+u)²
        for (int k = 3; k < p; ++k)
          C[i][j] += A[i][k]*B[k][j];
    ```

    By symplifying the formula, we progressively build a pattern that is candidate
    for a proof by induction

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

    If the pattern verifies the loop induction - the annotations at the end of the
    loop body matches with (or are included in) the annotations at the beginning of
    the loop body, it becomes a property that holds (infinitely) for every loop cycle.

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

    Then the porpoerty inside the loop enables to establish a property that
    holds after the loop by adding the constraints exiting the loop.


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
        // |IE(C[i][j])| <= (((1+u)^p-1)/u*(1+u)² - p)*a*b // same formula than the induction hypotheses
        // |C[i][j])| <= ((1+u)^p)-1)/u*a*b*(1+u)²
    ```

Hence, for the matrix multiplication of A, matrix of dimension $n \times p$
with B, matrix of dimension $p \times q$, the **introduced error** should be
less or equal than

$$\begin{array}{rcl}
  |IE(C[i][j])| & \leq & \left(\frac{(1+u)^{p}-1}{u}\times(1+u)^2 - p\right)\times a \times b\\
                & \leq & \left(\frac{(1+u)^{p}-1-p\times u}{u^2}\times(1+u)^2 - p\times(2+u)\right)\times a \times b \times u\\
\end{array}$$

where the absolute value of every coefficient of A is bound by $a$ and the
absolute value of every coefficient of B is bound by $b$.

[TODO] > Are we sure to be able to do the same analysis for higher dimension tensors? 

### integer implementation

[TODO]

#### Example 4 (Integer multiplication)

$$\begin{array}{rcl}
|IE(f)| & < & 1
\end{array}$$

for any integer implementation.

#### Example 4 (Integer division)

$$\begin{array}{rcl}
|IE(g)| & < & 1
\end{array}$$

for any integer implementation.

## Unit Verification

In the previous sections, we have described how to derive a possible error
upper bound considering (i) the semantics of computer arithmetic in integers
and floating point numbers and (ii) the algorithm used to define the operator
in the informal and formal specifications. In this section, we propose a
solution to evaluate the error upper bound on an actual C/C++ implementation.
Examples are given for the reference implementation developed in SONNX. The
same approach can be applied on a end-user implementation.   

The solution uses an abstract type `SymbolicDomainError` replacing each real
number in the Why3 specification. `SymbolicDomainError` is a data structure with
4 fields:

> Why do you refer to the specification? Should n't we write "replacing each floating point number in the implementation"? 

* The `real` field is a symbolic abstract domain for ideal (infinitely precise)
  C/C++ floating-point (or integer) computations.
* The `float` field is a symbolic abstract domain for the computed value.
* The `err` field is a symbolic abstract domain for the absolute error, that is
  the difference between the possible values of float and real.
* The `rel_err` field is a symbolic abstract domain for the relative error,
  that is the difference between the possible values of float and real divided by real.

[TODO] > It would be nice to give links to the library (e.g., github with user manual).

[TODO] > ### Example : division

[TODO] > It would be nice to give the actual result of the analysis.

[TODO] Verification of the Implementation, By static analysis, At Run-time.



