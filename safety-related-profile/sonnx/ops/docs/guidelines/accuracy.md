#### Objectives and limits

This document provides theory and techniques to write a formal specification for the
accuracy of numerical components used in neural networks. The result is
a specification that should be verified by any implementation for the
considered hypotheses. Here is a list of acceptable hypotheses :

* floating-point computation conformed to the IEEE-754 standard  
* fixed-point computation  
* concrete or symbolic range for the input values  
* symbolic constraints over some computations  

There exists many possible specifications for the accuracy. For instance, the specification
for the matrix multiplication will be different if one matrix is diagonal or if both matrices
are dense with a same order of magnitude for every coefficients.

We will favour short formulas, even if they may seem approximate.

#### Numerical Accuracy
 
This section provides a tight and verifiable specification of the numerical error
on the operator's results. The numerical error is the difference between the
current implementation on data with error resulting from previous approximated
computations and an ideal algorithm operating on data also coming from previous ideal
computations.

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x})$$

This framework decomposes the error into two parts:

* the first, the <span style="color:blue">propagated error</span>, depends on the numerical
  error and the numerical values of the inputs - in particular, it is independent of the
  implementation and the storage format  
* the second part, the <span style="color:red">introduced error</span>, depends on the
  concrete value of the inputs and the implementation with its storage format. 

$$op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x}) = \textcolor{blue}{(op_{\textit{ideal}}(\overrightarrow{x+e}) - op_{\textit{ideal}}(\overrightarrow{x}))} + \textcolor{red}{(op_{\textit{impl}}(\overrightarrow{x + e}) - op_{\textit{ideal}}(\overrightarrow{x+e})}$$

The error associated with the result of the operator corresponds to the sum of the propagated
errors and the introduced error and this new error is then propagated by the next operator.

The provided specification results from an over-approximated semantics (ex: IEEE-754) of the
numerical error of native computer operations approximating real number
operations. In order to preserve the readability of the formulas, the general specification introduces additional (conservative) simplifications compared to the original specifications.
However, this general specification may be too over-approximated for some specific inputs (ex tensor representing diagonal matrices). In this case, more precise specific specifications are provided alongside the general specification.

The error specification comes with unit verification scenarios to verify the implementation's conformity. In the absence of value ranges for the inputs, the unit verification scenarios operate on symbolic values and errors to propagate correct formulas throughout the scenario and thus provide a proof for the assertions. In particular, the C implementation generated from the Why3 formal specification must be verified using these scenarios, for example by using symbolic instrumentation libraries.

###### Error Propagation

This section contains tight properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of an operator.

**It is only for information**, since the properties does not depend on the implementation.
The formula aims to explain how an input error is amplified by the operator just from its
functional description.

From the theoretical point of view, let us consider a function $f: \mathbb{R}^n \longrightarrow \mathbb{R}^n$ and
an existing error for each argument $x^i = (x^i_{\textit{val}}, x^i_{\textit{err}})$.

The **propagated error** of the $f$ function as ideal operator is

$$f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})$$

Hence if $f$ is derivable two times, the formula

$$\sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}} + \mathcal{O}(X^2_{\textit{err}})
  \textit{ where } X_{\textit{err}} = \max(x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{err}}) \leq 1$$

is a correct propagated error with the natural following definition for $\mathcal{O}(X^2_{\textit{err}})$:

$$\mathcal{O}(X^2_{\textit{err}}) = \left(f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}$$

If there are no error on the arguments, the propagated error is $0$.
Otherwise, we preconise a first order expression like:

The absolute value of the propagated error is less or equal than

$$\sum_{0 \leq i < n} \left| \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}}) \right| \times |x^i_{\textit{err}}|$$

**Example:** multiplication $f(x, y) = x\times y$ and division $g(x, y) = x / y$ in $\mathbb{R}\times\mathbb{R}\longrightarrow\mathbb{R}$

For the multiplication, the **propagated error** $PE(f)$ is

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

The definition of $\mathcal{O}(X^2_{\textit{err}})$ is optional, since it is always

$$\begin{array}{rcl}
  \mathcal{O}(X^2_{\textit{err}}) & = & \left(f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}\\
  & = & (x_{\textit{val}} + x_{\textit{err}})\times(y_{\textit{val}} + y_{\textit{err}}) - x_{\textit{val}}\times y_{\textit{val}} - (y_{\textit{val}}\times x_{\textit{err}} + x_{\textit{val}}\times y_{\textit{err}})\\
  & = & x_{\textit{err}}\times y_{\textit{err}}
\end{array}$$

For the division, the **propagated error** $PE(g)$ is

$$\begin{array}{rcl}
PE(g) & = & \frac{x_{\textit{val}} + x_{\textit{err}}}{y_{\textit{val}} + y_{\textit{err}}} - \frac{x_{\textit{val}}}{y_{\textit{val}}} \\
    & = & \frac{y_{\textit{val}}\times x_{\textit{err}} - x_{\textit{val}}\times y_{\textit{err}}}{y_{\textit{val}}(y_{\textit{val}} + y_{\textit{err}})}
\end{array}$$

that is simplified into

$$\begin{array}{rcl}
PE(g) & = & \frac{1}{y_{\textit{val}}}\times x_{\textit{err}} - \frac{x_{\textit{val}}}{y^2_{\textit{val}}}\times y_{\textit{err}} + \mathcal{O}(X^2_{\textit{err}})
\end{array}$$

The definition of $\mathcal{O}(X^2_{\textit{err}})$ is optional

$$\begin{array}{rcl}
  \mathcal{O}(X^2_{\textit{err}}) & = & \left(f(x^0_{\textit{val}} + x^0_{\textit{err}}, \ldots, x^{n-1}_{\textit{val}} + x^{n-1}_{\textit{err}}) - f(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\right) - \sum_{0 \leq i < n} \frac{\delta f}{\delta x^i}(x^0_{\textit{val}}, \ldots, x^{n-1}_{\textit{val}})\times x^i_{\textit{err}}\\
  & = & \frac{y_{\textit{val}}\times x_{\textit{err}} - x_{\textit{val}}\times y_{\textit{err}}}{y_{\textit{val}}(y_{\textit{val}} + y_{\textit{err}})} - \frac{1}{y_{\textit{val}}}\times x_{\textit{err}} - \frac{x_{\textit{val}}}{y^2_{\textit{val}}}\times y_{\textit{err}}\\
  & = & \frac{x_{\textit{val}}\times y^2_{\textit{err}} - y_{\textit{val}}\times x_{\textit{err}}\times y_{\textit{err}}}{y_{\textit{val}}^2(y_{\textit{val}} + y_{\textit{err}})}
\end{array}$$

Hence, the accuracy definition of the operator will just indicate that

$$\begin{array}{rcl}
|PE(g)| & \leq & \frac{1}{|y_{\textit{val}}|}\times |x_{\textit{err}}| + \frac{|x_{\textit{val}}|}{y^2_{\textit{val}}}\times |y_{\textit{err}}| + |\mathcal{O}(X^2_{\textit{err}})|
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
