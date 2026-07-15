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
   in first-order logical expressions.

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
$\textbf{f}: \mathbb{R}^n \longrightarrow \mathbb{R}^m$ and an existing vector
error $E = (e^i)_{0 \leq i < n}$ for the vector argument $X = (x^i)_{0 \leq i
< n}$.

The **propagated error** of the $\textbf{f} = (f^0, \ldots, f^{m-1})$ function as ideal
operator is

$$\forall 0 \leq j < m. \, f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0, \ldots, x^{n-1}$$

Hence if $\textbf{f}$ is derivable two times, the formula

$$\forall 0 \leq j < m. \, \sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}
  (x^0, \ldots, x^{n-1})\times e^i + \mathcal{O}(E^2)
  \textit{ where } E = \max(e^0, \ldots, e^{n-1}}) \ll 1$$

is a correct propagated error with the natural following definition for
$\mathcal{O}^j(E^2)$:

$$\mathcal{O}^j(E^2) = \left(f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0,
\ldots, x^{n-1})\right) - \sum_{0 \leq i < n} \frac{\delta f^j}{\delta x^i}(x^0,
\ldots, x^{n-1})\times e^i$$

In term of matrix computations, this means

$$\mathcal{O}^j(E^2) = \left(\textbf{f}(X + E) - \textbf{f}(X)\right)
- (\textbf{J}_{\textbf{f}}) (E)$$

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
* $(\textbf{J}_{\textbf{f}}) (E) + \left(\textbf{f}(X + E) - \textbf{f}(X) - (\textbf{J}_{\textbf{f}}) (E)\right)$  
* $\forall 0 \leq j < m$, the absolute value of the propagated error is bound
  by $|f^j(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f^j(x^0, \ldots, x^{n-1})|$  
* $\forall 0 \leq j < m$, the absolute value of the propagated error is bound
  by $\sum_{0 \leq i < n} \max_{-|e^i| \leq e'_i \leq |e^i| \left( \left|
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

with

$$\begin{array}{rcl}
  \mathcal{O}(E^2) & = & \left(f(x^0 + e^0, \ldots, x^{n-1} + e^{n-1}) - f(x^0, \ldots, x^{n-1})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0, \ldots, x^{n-1})\times e^i\\
  & = & \frac{x^1\times e^0 - x^0\times e^1}{x^1(x^1 + e^1)} - \frac{1}{x^1}\times e^0 - \frac{x^0}{y^2_{\textit{val}}}\times e^1\\
  & = & \frac{x^0\times y^2_{\textit{err}} - x^1\times e^0\times e^1}{x^1^2(x^1 + e^1)}
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
& \leq & |PE(f)| & \leq &
\frac{1}{\max(|x^1|-|e^1|, 0)}\times |e^0| + \frac{|x^0|+|e^0|}{\max((|x^1|-|e^1|, 0))^2}
\times |e^1|
\end{array}$$


**Example:** 2D Matrix multiplication

Tensor operators require a methodology to propose an **over-approximation of the propagated error**,
since the algorithm combine many atomic operations on $\mathbb{R}$.

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

    By symplifying the formula, we progressively build a pattern that is candidate for a loop invariant

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

    If the pattern verify a loop induction, it becomes a loop invariant

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

    Then the loop invariant enables to establish the post-condition when exiting the loop

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

3. Final specification

    At the end, we can specify that

    * If A is a matrix of dimension $n \times p$, B a matrix of dimension $p \times q$,
    * if the absolute value of every coefficient of A is bound by $a$ with an error whose absolute value is bound by $ae$,  
    * if the absolute value of every coefficient of B is bound by $b$ with an error whose absolute value is bound by $be$,  
    * then the propagated error of every coefficient of C is bound by $p\times a\times be + p\times b \times ae$

###### Error Introduction

This section contains tight properties of $Y_{\textit{err}}^{\textit{intro}}$,
the introduced error, where $Y$ is the tensor result of an operator.
The objective is to provide a specification that any implementation should respect. Hence

$$Y_{\textit{err}}^{\textit{intro}} = op_{\textit{impl}}(\overrightarrow{x}) - op_{\textit{ideal}}(\overrightarrow{x})$$

From the theoretical point of view, the introduced error depends on the storage format of the result of any intermediate computation.
It is always defined as the difference between the implementation result and the ideal result, for which we additionaly
substract the propagated error of the previous section.

The introduced error is an over-approximation of difference between the implementation result and the ideal result
when there is no error on the input.

For IEEE-754 format, let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\bf u} = \frac{\varepsilon}{2}$. For every floating-point operator
whose result $r$ is a normal floating-point number, the introduced error is less or equal than
$|r| \times \frac{\varepsilon}{2} = |r| \times \textit{\bf u}$ in the standard mode
round to nearest even. Moreover if $r \in [a, b]$ with $a$ and $b$ normal numbers (the interval
may contain denormal numbers), the introduced error is less or equal than
$\max(|a|, |b|) \times \textit{\bf u}$ in the standard mode round to nearest even.
There exists more accurate formulas, but such formulas usually take too much
details into account.

**Example:** multiplication $f(x, y) = x * y$ and division $g(x, y) = x / y$

For the multiplication, the **introduced error** $IE(f)$ should be less or equal than

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


$$\begin{array}{rcl}
|IE(f)| & < & 1
\end{array}$$

for any fixpoint implementation.

For the division, the **introduced error** $IE(g)$ should be less or equal than

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

for any fixpoint implementation.

**Example:** 2D Matrix multiplication

Tensor operators require a methodology to find an **over-approximation of the introduced error**,
since their algorithms combine many atomic operations.

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

Hence, for the matrix multiplication of A, matrix of dimension $n \times p$ with B, matrix of dimension $p \times q$, the **introduced error** should be less or equal than

$$\begin{array}{rcl}
  |IE(C[i][j])| & \leq & \left(\frac{(1+u)^{p+1}-1}{u}\times(1+u)^2 - p-1\right)\times a \times b\\
                & \leq & \left(\frac{(1+u)^{p+1}-1-(p+1)\times u }{u^2}\times(1+u)^2 - (p+1)\times(2+u)\right)\times a \times b \times u\\
\end{array}$$

where the absolute value of every coefficient of A is bound by $a$ and the absolute value of every coefficient of B is bound by $b$.

###### Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

* The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
* The `float` field is a symbolic abstract domain for the computed value.  
* The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
* The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

# Formal specification guidelines

*To be completed.*
