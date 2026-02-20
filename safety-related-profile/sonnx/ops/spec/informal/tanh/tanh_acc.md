# Numerical Accuracy

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

## Note Algorithm
Tanh is subject to exponent overflow when evaluating large positive exponents (e.g. exp(2X) for very positive values of X).
To remain numerically stable in float, the minimal precision algorithm shall split the `X` domain so that only negative exponents are computed.

```
if X < 0
    Y = (exp(2X) - 1) / (exp(2X) + 1)
else
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Tanh** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$). For $Y = \tanh(X)$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input error $X_{\textit{err}}$.

Using the derivative of $\tanh$ is $d\tanh(x)/dx = 1 - \tanh^2(x)$, a first-order bound is:

- For every index $I$:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |1 - \tanh^2(X[I])|\cdot|X_{\textit{err}}[I]| +\mathcal{O}(|X_{\textit{err}}[I]|^2)$

- The complete definition of $\mathcal{O}(|X_{\textit{err}}[I]|^2)$
  is available in the [guidelines](../../../docs/guidelines/accuracy.md#error-propagation).  
- Since $0 \le 1 - \tanh^2(x) \le 1$ for all real $x$, a global bound is:
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \le |X_{\textit{err}}[I]|$

This operator does not amplify the initial error.

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $Y_{\textit{err}}^{\textit{intro}} = [0]$.

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\textbf{u}} = \frac{\varepsilon}{2}$.

The accuracy of the implementation relies of the accuracy of the `exp` available function.
We can consider that this function has a $2\varepsilon$ accuracy in the interval $[-1, 0]$.
With the properties $e^{2x} = (e^x)^2$ and $e^{-x} = \frac{1}{e^x}$, the relative
accuracy of `exp` for any number in $[-2^n, -1]$ can be bound by $(2+n/2)\varepsilon$ if the result
is a normal number. Here is a possible definition of $\textit{err}_{\textit{rel}}(\exp(x))$

$$\begin{array}{rcl}
  \textit{err}_{\textit{rel}}(\exp(x)) & = & 2\varepsilon \textit{ if } x\in [-1, 0] \\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & (2 + \frac{n}{2})\varepsilon \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}\\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & 2.5\varepsilon \textit{ if } x\in [0, 1]\\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & (2 + \frac{n+1}{2})\varepsilon \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}\\
  \end{array}$$

Nevertheless, any implementor can claim a better precision for this function. In such a case,
it should adapt the formula below to show that the `tanh` opeator verifies it.

$$\begin{array}{rcl}
  |Y_{\textit{err}}^{\textit{intro}}[I]| & \leq & 
  \frac{\textit{err}_{\textit{rel}}(\exp(-2|x|))\times 2e^{-2|x|}(1+\textit{\textbf{u}}) + 2\textit{\textbf{u}}(1-e^{-4|x|})}{(1+e^{-2|x|})\left((1+e^{-2|x|})\times(1 - \textit{\textbf{u}}) - \textit{err}_{\textit{rel}}(\exp(-2|x|))\times e^{-2|x|}\times(1+\textit{\textbf{u}})\right)}\times(1 + \textit{\textbf{u}}) + u\times\frac{1-e^{-2|x|}}{1+e^{-2|x|}}
  \end{array}$$

for the standard rounding mode round to nearest even, provided $e^{-2|x|}$ and $Y_{\textit{val}}[I]$ are
normal numbers.

For the specification of $\textit{err}_{\textit{rel}}(\exp(x))$ given above, that mean

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

This formula is obtained for the computation of

```
if X < 0
    Y = (exp(2X) - 1) / (exp(2X) + 1)
else
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

The bounds are tighter than the following computations

```
    Y = (exp(2X) - 1) / (exp(2X) + 1)
```

for which the accuracy would be bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + \textcolor{red}{9}(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{4.5}\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (\textcolor{red}{9}+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{4.5}+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

and

```
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

for which the accuracy would be bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + \textcolor{red}{9}(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{4.5}\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (\textcolor{red}{9}+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{4.5}+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

and

```
    Y = (exp(X) - exp(-X)) / (exp(X) + exp(-X))
```

for which the accuracy would be bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + \textcolor{red}{17}(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{8.5}\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (\textcolor{red}{17}+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{8.5}+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + \textcolor{red}{17}(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{8.5}\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (\textcolor{red}{17}+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{8.5}+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

An implementation can nevertheless use one of these algorithm and verify the adequate accuracy formula, but it should motivate its choice.
Note that the test `if X < 0` may induce some timing penalties for some architecture and the following implementation avoids it

```
    Y = (1 - exp(-2*abs(X)) / (1 + exp(-2*abs(X)))
```

## Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> X;

/* X symbolic initialization */

auto tanh_real = [](const SymbolicDomainError &v) {
  // Tanh in the real domain
  SymbolicDomainError r;
  r.real = std::tanh(v.real);
  // float/err/rel_err are set by the abstract interpreter / analysis framework
  return r;
};

auto result = [&X,&tanh_real](auto I) {
  return tanh_real(X[I]);
};

for (auto I : X.indexes()) {
   auto x = X[I];
   auto y = result(I);

   // First-order propagated error bound:
   // |err_tanh| <= |1 - tanh(x)^2| * |err_x|
   double tanh_x = std::tanh(x.real);
   double local_lipschitz = std::abs(1.0 - tanh_x * tanh_x);
   double bound = local_lipschitz * std::abs(x.err);

   assert(std::abs(y.err) <= bound + 1e-12);
}
```



