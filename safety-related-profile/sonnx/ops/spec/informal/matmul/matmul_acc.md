# Numerical Accuracy

The numerical accuracy of `Matmul` is defined by the propagated error and the
introduced error.

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

Any SONNX-compliant implementation of `Matmul` shall provide sound bounds for the
introduced error. The propagated error defined below comes from the [SONNX informal
specification](matmul.md).

$$
  \forall i \in [0, dA_0 - 1], \forall j \in [0, dB_1 - 1] \quad C[i,j] = \sum_{k=0}^{dA_1-1} A[i,k]\times B[k,j]
$$

with $n = dA_1 = dB_0$, $m = dA_0$, $p = dB_1$.

## Note Algorithm

We retain the mathematical definition of the operator for a 2D tensor

$$     
   Y = A \times B  
$$

$$
     \begin{bmatrix}
         Y[0, 0] & Y[0, 1] & \cdots & Y[0, p-1]\\
         Y[1, 0] & Y[1, 1] & \cdots & Y[1, p-1]\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         Y[m-1, 0] & Y[m-1, 1] & \cdots & Y[m-1, p-1] 
     \end{bmatrix}
      =
     \begin{bmatrix}
         A[0, 0] & A[0, 1] & \cdots & A[0, n-1]\\
         A[1, 0] & A[1, 1] & \cdots & A[1, n-1]\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         A[m-1, 0] & A[m-1, 1] & \cdots & A[m-1, n-1] 
     \end{bmatrix}
     \times
     \begin{bmatrix}
         B[0, 0] & B[0, 1] & \cdots & B[0, p-1]\\
         B[1, 0] & B[1, 1] & \cdots & B[1, p-1]\\ 
         \vdots & \vdots & \ddots & \vdots\\ 
         B[n-1, 0] & B[n-1, 1] & \cdots & B[n-1, p-1] 
     \end{bmatrix}
$$
$$     
   Y[i, j]= A[i, 0]\times B[0, j] + A[i, 1]\times B[1, j] +\cdots+ A[i, n-1]\times B[n-1, j] = \sum_{k=0}^{n-1} A[i, k]\times B[k, j]  
$$

Where

- $m$ is the number of rows of matrix $A$ (= $dA[0]$)
- $n$ the number of columns of matrix $A$ (= $dA[1]$) and the number of rows of matrix B (= $dA[0]$),
- $p$ is the number of columns of matrix $B$ (= $dB[1]$)

Let us define $|A| = \max_{0 \leq i < m, 0 \leq j < n} | A[i, j] |$,
$|B| = \max_{0 \leq i < n, 0 \leq j < p} | B[i, j] |$,
$|A_{\textit{err}}| = \max_{0 \leq i < m, 0 \leq j < n} | A_{\textit{err}}[i, j] |$
and $|B_{\textit{err}}| = \max_{0 \leq i < n, 0 \leq j < p} | B_{\textit{err}}[i, j] |$.

We propose a first specification that only depends from $n$, $|A|$ and $|B|$.
A second specification is also provided to take into account the specificity of
every coefficient. The first specification aims to check the worst case accuracy
of an implementation, whereas the second is useful to infer the accuracy of a
SONNX-graph in a modular approach.

## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error,
where $Y$ is the tensor result of the **Matmul** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$).
For $Y = A \times B$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from
the input errors $A_{\textit{err}}[i, j]$ and $B_{\textit{err}}[i, j]$.

Using the derivative of Matmul, a first-order bound is:

- For every index $i, j$:
  - $Y_{\textit{err}}^{\textit{propag}}[i, j] = \left(\sum_{k=0}^{n-1}
    A_{\textit{err}}[i, k]\times B[k, j]\right) + \left(\sum_{k=0}^{n-1}
    A[i, k]\times B_{\textit{err}}[k, j]\right) + \left(\sum_{k=0}^{n-1}
    A_{\textit{err}}[i, k]\times  B_{\textit{err}}[k, j]\right)$  
  - $|Y_{\textit{err}}^{\textit{propag}}[i, j]| \leq n\times
    (|A_{\textit{err}}|\times|B| + |B_{\textit{err}}|\times |A| +
    |A_{\textit{err}}|\times|B_{\textit{err}}|)$  

In the worst case, this operator amplifies an initial error by the matrix
dimension and by the maximum of the absolute value of the coefficients of the
other matrix.

In a modular approach for the accuracy inference, the first formula enables
to replace a full implementation for the propagation of the accuracy by
a small [Wolfram](https://www.wolfram.com/mathematica) code to be evaluated
in real numbers within a symbolic and/or approximate environment:

```
ec[i][j] = 0;
For (k = 0, k < n, k = k+1, ec[i][j] += a[i][k]*eb[k][j] + ea[i][k]*b[k][j] + ea[i][k]*eb[k][j])
```

### Note about the construction of such a specification

1. Naïve Algorithm Description

   Since it is simpler to provide intermediate annotations inside code lines than a formula,
   we suggest to translate the formula in a naive way to compute it.

    ```c++
    // A matrix of dimension m x n, B matrix of dimension n x p.
    // C result matrix of dimension m x p
    for (int i = 0; i < m; ++i)
      for (int j = 0; j < p; ++j) {
        C[i][j] = 0;
        for (int k = 0; k < n; ++k)
          C[i][j] += A[i][k]*B[k][j];
      }
    ```

2. Progressive decoration of the algorithm starting from inner loop

   To simplify the specification and to benefit from simplifications in the
   annotations, we add some hypotheses:

   * the absolute value of every coefficient of A is bound by 'a' with an error
     whose absolute value is bound by 'ae'  
   * the absolute value of every coefficient of B is bound by 'b' with an error
     whose absolute value is bound by 'be'

   These hypotheses are likely to introduce big over-approximations, especially
   for non-dense matrices. The specifier can introduce different hypotheses
   or not introduce any hypothese but provide a code (for instance in the Wolfram
   language) in real numbers to "compute" the specification of the error (see
   point 4. instead of a formula).

    ```c++
    // A matrix of dimension m x n, B matrix of dimension n x p.
    // C result matrix of dimension m x p
    for (int i = 0; i < m; ++i)
      for (int j = 0; j < p; ++j) {
        C[i][j] = 0;
        // OAPE(C[i][j]) = 0
          C[i][j] += A[i][0]*B[0][j];
        // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
        // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
        // |PE(C[i][j])| <= a*be + b*ae + ae*be
          C[i][j] += A[i][1]*B[1][j];
        // |PE(C[i][j])| <= 2*a*be + 2*b*ae + 2*ae*be
        for (int k = 2; k < n; ++k)
          C[i][j] += A[i][k]*B[k][j];
      }
    ```

    By symplifying the formula, we progressively build a pattern that is candidate
    for a proof by induction

    ```c++
    // A matrix of dimension m x n, B matrix of dimension n x p.
    // C result matrix of dimension m x p
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < m; ++i)
      for (int j = 0; j < p; ++j) {
        C[i][j] = 0;
        // |PE(C[i][j]| = 0
        for (int k = 0; k < 2; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |PE(C[i][j]| <= k*a*be + k*b*ae + k*ae*be
        for (int k = 2; k < n; ++k)
          C[i][j] += A[i][k]*B[k][j];
      }
    ```

    If the pattern verifies the loop induction - the annotations at the end of the
    loop body matches with (or are included in) the annotations at the beginning of
    the loop body, it becomes a property that holds (infinitely) for every loop cycle.

    ```c++
    // A matrix of dimension m x n, B matrix of dimension n x p.
    // C result matrix of dimension m x p
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < m; ++i)
      for (int j = 0; j < p; ++j) {
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
        for (int k = 3; k < n; ++k)
          C[i][j] += A[i][k]*B[k][j];
      }
    ```

    Then the property inside the loop enables to establish a property that
    holds after the loop by adding the constraints exiting the loop.

    ```c++
    // A matrix of dimension m x n, B matrix of dimension n x p.
    // C result matrix of dimension m x p
    // the absolute value of every coefficient of A is bound by 'a' with an error whose absolute value is bound by 'ae'
    // the absolute value of every coefficient of B is bound by 'b' with an error whose absolute value is bound by 'be'
    for (int i = 0; i < m; ++i)
      for (int j = 0; j < p; ++j) {
        C[i][j] = 0;
        // PE(C[i][j]) = 0
        for (int k = 0; k < n; ++k)
          C[i][j] += A[i][k]*B[l][j];
          // |OAPE(C[i][j]| <= k*a*be + k*b*ae + k*ae*be
        // |PE(C[i][j])| <= n*a*be + n*b*ae + n*ae*be
      }
    ```

3. Final specification

    At the end, we can specify that

    * If A is a matrix of dimension $m \times n$, B a matrix of dimension $n \times p$,
    * if the absolute value of every coefficient of A is bound by $a$ with an error whose absolute value is bound by $ae$,  
    * if the absolute value of every coefficient of B is bound by $b$ with an error whose absolute value is bound by $be$,  
    * then the propagated error of every coefficient of C is bound by $n\times a\times be + n\times b \times ae + n\times ae\times be$

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $Y_{\textit{err}}^{\textit{intro}} = [0]$.

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\textbf{u}} = \frac{\varepsilon}{2}$.

We suppose a naïve implementation for the computation of $\sum_{k=0}^{n-1} A[i, k]\times B[k, j]$
to establish the formula above. Every implementation could improve the accuracy by reordering
the terms of the sum and/or with more accurate local additions and multiplications.
Any such implementation must be accompanied by valid error bounds to be
SONNX-compliant. The job of producing such error bounds is left to the implementor.
As example, we provide a way to produce such error from the following naïve algorithm
in C/C++ syntax.

```c++
// A matrix of dimension m x n, B matrix of dimension n x p.
// C result matrix of dimension m x p
for (int i = 0; i < m; ++i)
  for (int j = 0; j < p; ++j) {
    C[i][j] = 0;
    for (int k = 0; k < n; ++k)
      C[i][j] += A[i][k]*B[k][j];
  }
```

Hence, for the standard rounding mode round to nearest even, provided $Y_{\textit{val}}[i, j]$ are
normal numbers

$$|Y_{\textit{err}}^{\textit{intro}}[i, j]| \leq
\left((1+\textit{\textbf{u}}^2) \times \frac{(1 + \textit{\textbf{u}})^n -
1}{\textit{\textbf{u}}} - n\right) \times |A| \times
|B| $$

This formula is obtained with a proof (see the note below) by induction over $n$.

As for the propagated error, a precise formula is available in the 
[Wolfram](https://www.wolfram.com/mathematica) language to be evaluated
in real numbers within a symbolic and/or approximate environment.
For that, let us define `min_normalized` is the smallest positive normalized number.
Then, the coefficients $c[i][j]$ of the result matrix carry an introduced error
$eic[i][j]$ bound by the following computations:

```
eic[i][j] = 0; epc[i][j] = 0; c[i](j] = 0; eic[i](j] = 0;
For (k = 0, k < n, k = k+1,
  m[i][j] = a[i][k] * b[k][j];
  eim[i][j] = u*max(abs(m[i][j]), min_normalized);
  c[i][j] = c[i][j] + m[i][j];
  eic[i][j] = (1+u)*(eic[i][j] + eim[i][j]) + u*max(abs(c[i][j]), min_normalized))
```

### Note about the construction of such a specification

The construction uses a progressive decoration mechanism with annotations
starting from inner loop

```c++
// A matrix of dimension m x n, B matrix of dimension n x p.
// C result matrix of dimension m x p
for (int i = 0; i < m; ++i)
  for (int j = 0; j < p; ++j) {
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
    for (int k = 3; k < n; ++k)
      C[i][j] += A[i][k]*B[k][j];
  }
```

By symplifying the formula, we progressively build a pattern that is candidate
for a proof by induction

```c++
// A matrix of dimension m x n, B matrix of dimension n x p.
// C result matrix of dimension m x p
// the absolute value of every coefficient of A is bound by 'a'
// the absolute value of every coefficient of B is bound by 'b'
for (int i = 0; i < m; ++i)
  for (int j = 0; j < p; ++j) {
    C[i][j] = 0;
    // IE(C[i][j]) = 0
    for (int k = 0; k < 2; ++k)
      C[i][j] += A[i][k]*B[l][j];
      // |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b
      // |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
    for (int k = 2; k < n; ++k)
      C[i][j] += A[i][k]*B[k][j];
  }
```

If the pattern verifies the loop induction - the annotations at the end of the
loop body matches with (or are included in) the annotations at the beginning of
the loop body, it becomes a property that holds (infinitely) for every loop cycle.

```c++
// A matrix of dimension m x n, B matrix of dimension n x p.
// C result matrix of dimension m x p
// the absolute value of every coefficient of A is bound by 'a'
// the absolute value of every coefficient of B is bound by 'b'
for (int i = 0; i < m; ++i)
  for (int j = 0; j < p; ++j) {
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
    for (int k = 3; k < n; ++k)
      C[i][j] += A[i][k]*B[k][j];
  }
```

Then the porpoerty inside the loop enables to establish a property that
holds after the loop by adding the constraints exiting the loop.

```c++
// A matrix of dimension m x n, B matrix of dimension n x p.
// C result matrix of dimension m x p
// the absolute value of every coefficient of A is bound by 'a'
// the absolute value of every coefficient of B is bound by 'b'
for (int i = 0; i < m; ++i)
  for (int j = 0; j < p; ++j) {
    C[i][j] = 0;
    // IE(C[i][j]) = 0
    for (int k = 0; k < n; ++k)
      C[i][j] += A[i][k]*B[l][j];
      // |IE(C[i][j])| <= (((1+u)^(k+1)-1)/u*(1+u)² - k-1)*a*b // same formula than the induction hypotheses
      // |C[i][j])| <= ((1+u)^(k+1)-1)/u*a*b*(1+u)²
    // |IE(C[i][j])| <= (((1+u)^n-1)/u*(1+u)² - n)*a*b // same formula than the induction hypotheses
    // |C[i][j])| <= ((1+u)^n)-1)/u*a*b*(1+u)²
  }
```

Hence, for the matrix multiplication of A, matrix of dimension $m \times n$
with B, matrix of dimension $n \times p$, the **introduced error** should be
less or equal than

$$\begin{array}{rcl}
  |IE(C[i][j])| & \leq & \left(\frac{(1+u)^{n}-1}{u}\times(1+u)^2 - n\right)\times a \times b\\
                & \leq & \left(\frac{(1+u)^{n}-1-n\times u}{u^2}\times(1+u)^2 - n\times(2+u)\right)\times a \times b \times u\\
\end{array}$$

where the absolute value of every coefficient of A is bound by $a$ and the
absolute value of every coefficient of B is bound by $b$.


# Error Introduction (int)

To be completed

## Unit Verification

To be completed

