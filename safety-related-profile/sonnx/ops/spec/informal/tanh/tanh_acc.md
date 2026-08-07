# Numerical Accuracy

The numerical accuracy of `Tanh` is defined by the propagated error and the
introduced error.

$Y_{\textit{err}} = Y_{\textit{err}}^{\textit{propag}} + Y_{\textit{err}}^{\textit{intro}}$.

Any SONNX-compliant implementation of `Tanh` shall provide sound bounds for the
introduced error. The propagated error defined below comes from the [SONNX informal
specification](tanh.md).

For any [tensor index](./../common/definitions.md#tensor_index) $I$:

$$
Y[I] = \tanh(X[I]) = \frac{e^{X[I]}-e^{-X[I]}}{e^{X[I]}+e^{-X[I]}} = \frac{e^{2X[I]}-1}{e^{2X[I]}+1} = \frac{1 - e^{-2X[I]}}{1 + e^{-2X[I]}}
$$

## Note Algorithm

Tanh is subject to exponent overflow when evaluating large positive exponents
(e.g. exp(2X) for very positive values of X). To remain numerically stable,
the minimal precision algorithm shall split the `X` domain so that only
negative exponents are computed.

```
if X < 0
    Y = (exp(2X) - 1) / (exp(2X) + 1)
else
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

Correctly-rounded floating-point implementations of `tanh` exist, for example:  
- [https://core-math.gitlabpages.inria.fr](https://core-math.gitlabpages.inria.fr)  
- [https://people.cs.rutgers.edu/~sn349/rlibm](https://people.cs.rutgers.edu/~sn349/rlibm)  

In the section [Error Introduction](#error-introduction-ieee-754-floating-point),
we explain how to derive bounds from the algorithm described above with a ulp-accurate
implementation of `exp`.

A SONNX-compliant implementation should prove that it respects these bounds
for the introduced error or exhibit a correct additional reasonable factor
in the formula of the introduced error.

## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains properties of $Y_{\textit{err}}^{\textit{propag}}$, the propagated error, where $Y$ is the tensor result of the **Tanh** operator.  
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $X_{\textit{err}}$).
For $Y = \tanh(X)$, the propagated error $Y_{\textit{err}}^{\textit{propag}}$ comes from the input
error $X_{\textit{err}}$.

- For every $I$:
  - $Y_{\textit{err}}^{\textit{propag}}[I] = \frac{\sinh(X_{\textit{err}}[I])}{\cosh(X[I])\cdot \cosh(X[I]+X_{\textit{err}}[I])}$  
  - $Y_{\textit{err}}^{\textit{propag}}[I] = \tanh(X_{\textit{err}}[I])\times\frac{1 - \tanh(X[I])^2}{1 + \tanh(X[I])\cdot\tanh(X_{\textit{err}}[I])}$  
  - $Y_{\textit{err}}^{\textit{propag}}[I] = \tanh(X_{\textit{err}}[I])\times\frac{(1 - \tanh(X[I]))\cdot(1 + \tanh(X[I]))}{1 + \tanh(X[I])\cdot\tanh(X_{\textit{err}}[I])}$  
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \leq |\tanh(X_{\textit{err}}[I])|\times(1 + \tanh(|X[I]|))$  
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \leq |X_{\textit{err}}[I]|$  
  - $|Y_{\textit{err}}^{\textit{propag}}[I]| \leq |X_{\textit{err}}[I]|\times(1 - \tanh^2(\min(|X[I]|, |X[I]+X_{\textit{err}}[I]|)))$ if $X[I]$ does not cross zero under perturbation  

The penultimate property comes from the derivative of $\tanh$, that is $d\tanh(x)/dx = 1 - \tanh^2(x) \in [0, 1.0]$
and from mean value inequality.

The last property comes from the derivative of $\tanh$, from the mean value theorem and
from the monotonicity and the symetry of the $\tanh^2$ function on the intervals $[-\infty, 0]$ and $[0, +\infty]$.

Hence, this operator does not amplify the initial error and it reduces it with a factor close
to $|1 - \tanh(X[I])^2|$ for most inputs and small errors (see third and last equation).

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $Y_{\textit{err}}^{\textit{intro}} = [0]$.

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\textbf{u}} = \frac{\varepsilon}{2}$. Let us also define
$\textit{min\_norm}$ the minimal normalized number for the considered format.

In this section, wo do not provide a specification for the accuracy, but we explain
on some examples how to derive sound bounds from reference algorithms, $x = X[I]$ and $u$. 
The implementor should choose a reference algorithm for an input and thus indicates
the bound formula (depending from $x$ and $u$) verified by its implementation.

### Correctly rounded specification of `Tanh`

A correctly-rounded libm (see [https://core-math.gitlabpages.inria.fr](https://core-math.gitlabpages.inria.fr)
or [https://people.cs.rutgers.edu/~sn349/rlibm](https://people.cs.rutgers.edu/~sn349/rlibm)
rounds the infinite-precision result to the nearest floating-point number in the 
mode round to nearest even. As a result, the rounding (introduced) error is bounded
by $\max(|Y[i]|, \textit{min\_norm})\times\textit{\bf u}$.

- $|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \textit{\bf u}\times\max\left(\tanh(|X[I]|), \textit{min\_norm}\right)$.

### Specification of `Tanh` from a non-optimised `Exp` implementation

This subsection just provides a procedure to specify bounds with accuracy hypotheses about
an `exp` algorithm. For instance, let us suppose that the `exp` function 
has a $2\varepsilon$ accuracy in the interval $[-1, 0]$.
With the properties $e^{2x} = (e^x)^2$ and $e^{-x} = \frac{1}{e^x}$, the relative
accuracy of `exp` for any number in $[-2^n, -1]$ can be bound by $(2+n/2)\varepsilon$ if the result
is a normal number (see the informal specification of [Exp](../exp/exp_acc.md)). Here is a
possible definition of $\textit{err}_{\textit{rel}}(\exp(x))$

$$\begin{array}{rcl}
  \textit{err}_{\textit{rel}}(\exp(x)) & = & 2\varepsilon \textit{ if } x\in [-1, 0] \\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & (2 + \frac{n}{2})\varepsilon \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}\\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & 2.5\varepsilon \textit{ if } x\in [0, 1]\\
  \textit{err}_{\textit{rel}}(\exp(x)) & = & (2 + \frac{n+1}{2})\varepsilon \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}\\
  \end{array}$$

Nevertheless, any implementor can claim a better precision for the `exp` function. In such a case,
it should recompute the formula below by following the same reasonings to show that the `Tanh`
component verifies it. Even if a custom definition of $err_{rel}(\exp(x))$ could be plugged in
the formula for `Tanh`, we prefer to show how to inline it and simplify the result
in order to obtain a more concise formula.

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

Let us now compare the specification with another reference algorithm.
To avoid overflows in this algorithm, we arbitrarily restrict the inputs between
$[\texttt{numeric\_limits<T>::lowest}(), 10^7]$.

```
    Y = (exp(2X) - 1) / (exp(2X) + 1)
```

Then, the error introduction sound bounds are worse than for the previous algorithm.
For this algorithm, the error introduction is soundly bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + \textcolor{red}{9}(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{4.5}\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (\textcolor{red}{9}+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{4.5}+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

For the following reference algorithm, whose inputs are arbitrarily restricted to
$[-10^7, \texttt{numeric\_limits<T>::highest}()]$

```
    Y = (1 - exp(-2X)) / (1 + exp(-2X))
```

the accuracy is bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + \textcolor{red}{9}(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{4.5}\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (\textcolor{red}{9}+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{4.5}+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + 8(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - 4\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (8+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (4+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

And for the last reference algorithm, whose inputs are arbitrarily restricted to
$[-10^7, 10^7]$

```
    Y = (exp(X) - exp(-X)) / (exp(X) + exp(-X))
```

the accuracy would be bound by

$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + \textcolor{red}{17}(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{8.5}\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{2x}}\times(1+\textit{\textbf{u}}) + 1 - e^{2x}\right)\textit{ if } x\in [-1, 0]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{2x}} \left(\frac{2 + (\textcolor{red}{17}+n)(1+\textit{\textbf{u}})e^{2x}-2e^{4x}}{(1 + e^{2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{8.5}+\frac{n}{2})\textit{\textbf{u}}(1 + \textit{\textbf{u}})e^{2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{2x}\right) \textit{ if } x\in [-2^n, -1] \textit{ with integer } n >= 0 \textit { and } \exp(x) \textit{ is normal}$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + \textcolor{red}{17}(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - \textcolor{red}{8.5}\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [0, 1]$$
$$|Y_{\textit{err}}^{\textit{intro}}[I]| \leq \frac{\textit{\textbf{u}}}{1+2e^{-2x}} \left(\frac{2 + (\textcolor{red}{17}+n)(1+\textit{\textbf{u}})e^{-2x}-2e^{-4x}}{(1 + e^{-2x})\times(1-\textit{\textbf{u}}) - (\textcolor{red}{8.5}+\frac{n}{2})\textit{\textbf{u}}(1+\textit{\textbf{u}})e^{-2x}}\times(1 + \textit{\textbf{u}}) + 1 - e^{-2x}\right) \textit{ if } x\in [1, 2^n] \textit{ with integer } n >= 0 \textit { and } \exp(-x) \textit{ is normal}$$

An implementation can nevertheless use one of these algorithm and verify the adequate accuracy formula, but it should motivate its choice.

# Error Introduction (int)

To be completed

## Unit Verification

This section contains a test scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<SymbolicDomainError> X;

/* X symbolic initialization */

auto result = [&X,&tanh_real](auto I) {
  return tanh(X[I]);
};

void init() { // initialization with a default scenario
  for (auto I : X.indexes()) {
    X[I] = BETWEEN(-MAX, +MAX); // no error for X
  }
}

template <typename T>
Real getSpecError(T val) { return Real(); }

template <std::floating_type T>
Real getSpecError(const TSymbolicDomainError<T>& val)
{
   Real u = std::numeric_limits<T>::epsilon/2.0;
   Real x = val.real;
   if (x >= -1 && x <= 0)
      return u/(1+2*std::exp(2*x))
         *((2+8*(1+u)*std::exp(2*x) -2*std::exp(4*x))
            /((1+2*std::exp(2*x))*(1-u) - 4*u*(1+u)*std::exp(2*x))
         *(1+u) + 1 - std::exp(2*x));
   if (x >= 0 && x <= 1)
      return u/(1+2*std::exp(-2*x))
         *((2+8*(1+u)*std::exp(-2*x) -2*std::exp(-4*x))
            /((1+2*std::exp(-2*x))*(1-u) - 4*u*(1+u)*std::exp(-2*x))
         *(1+u) + 1 - std::exp(-2*x));
   
   Integer n = x.getExponent();
   if (x <= -1)
      return u/(1+2*std::exp(2*x))
         *((2+(8+n)*(1+u)*std::exp(2*x) -2*std::exp(4*x))
            /((1+2*std::exp(2*x))*(1-u) - (4+n/2.0)*u*(1+u)*std::exp(2*x))
         *(1+u) + 1 - std::exp(2*x));
   if (x >= 1)
      return u/(1+2*std::exp(-2*x))
         *((2+(8+n)*(1+u)*std::exp(-2*x) -2*std::exp(-4*x))
            /((1+2*std::exp(-2*x))*(1-u) - (4+n/2.0)*u*(1+u)*std::exp(-2*x))
         *(1+u) + 1 - std::exp(-2*x));
   return Real();
}

template <std::integral T>
Real getSpecError(const TSymbolicDomainError<T>& val) { return 1.0; }

int main() {
   init();
   for (auto I : X.indexes()) {
      auto x = X[I];
      auto y = result(I);
      assert(std::abs(y.err) <= getSpecError(x));
   }
}
```



