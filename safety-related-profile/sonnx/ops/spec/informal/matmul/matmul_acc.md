# Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

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
- $n$ the number of columns of matrix $A$ (= $dA[1]$) and the number of rows of matrix B (=$dA[0]$),
- $p$ is the number of columns of matrix $B$ (=$dB[1]$)

Let us define $|A| = \max_{0 \leq i < m, 0 \leq j < n} | A[i, j] |$,
$|B| = \max_{0 \leq i < n, 0 \leq j < p} | B[i, j] |$,
$|A_{\textit{err}}| = \max_{0 \leq i < m, 0 \leq j < n} | A_{\textit{err}}[i, j] |$
and $|B_{\textit{err}}| = \max_{0 \leq i < n, 0 \leq j < p} | B_{\textit{err}}[i, j] |$.

## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error,
where $Y$ is the tensor result of the **Matmul** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$).
For $Y = A \times B$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from
the input errors $A_{\textit{err}}[i, j]$ and $B_{\textit{err}}[i, j]$.

Using the derivative of Matmul, a first-order bound is:

- For every index $i, j$:
  - $|Y_{\textit{err}}^{\textit{propag}}[i, j]| = \left(\sum_{k=0}^{n-1} A_{\textit{err}}[i, k]\times B[k, j]\right) + \left(\sum_{k=0}^{n-1} A[i, k]\times B_{\textit{err}}[k, j]\right) +\mathcal{O}(|A_{\textit{err}}|\times |B_{\textit{err}}|)$

- The complete definition of $\mathcal{O}(|A_{\textit{err}}|\times |B_{\textit{err}}|)$
  is available in the [guidelines](../../../docs/guidelines/accuracy.md#error-propagation).  
- A global bound for the propagated error is:
  - $|Y_{\textit{err}}^{\textit{propag}}[i, j]| \le n\times (|A_{\textit{err}}||B| + |A||B_{\textit{err}}|) + n\times (|A_{\textit{err}}||B_{\textit{err}}|)$

This operator amplifies an initial error by absolute value of the coefficients of the other matrix.

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $Y_{\textit{err}}^{\textit{intro}} = [0]$.

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\textbf{u}} = \frac{\varepsilon}{2}$.

We suppose a naïve implementation for the computation of $\sum_{k=0}^{n-1} A[i, k]\times B[k, j]$.

Hence, for the standard rounding mode round to nearest even, provided $Y_{\textit{val}}[i, j]$ are
normal numbers

$$|Y_{\textit{err}}^{\textit{intro}}[i, j]| \leq \left((1+\textit{\textbf{u}}^2) \times \frac{(1 + \textit{\textbf{u}})^n - 1}{\textit{\textbf{u}}} - n\right) \times (|A| + |A_{\textit{err}}|) \times (|B| + |B_{\textit{err}}|) $$

This formula is obtained with a proof by induction over $n$.

## Unit Verification

To be defined

