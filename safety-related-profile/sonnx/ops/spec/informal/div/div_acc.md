# Numerical Accuracy

The numerical accuracy of `Div` is defined by the propagated error and the
introduced error.

$C_{\textit{err}} = C_{\textit{err}}^{\textit{propag}} + C_{\textit{err}}^{\textit{intro}}$.

Any SONNX-compliant implementation of `Div` shall provide sound bounds for the
introduced error. The propagated error defined below comes from the [SONNX informal
specification](div.md).

$$ C[i] = A[i]/B[i] $$ 

If $B[i] \neq 0$ otherwise $C[i]$ is not defined. 


## Error Propagation - for information - see [guidelines](../../../docs/guidelines/accuracy.md#error-propagation)

This section contains tight properties of $C_{\textit{err}}^{\textit{propag}}$, the propagated error, where $C$ is the tensor result of an operator.
Let tensors of numerical errors be denoted by subscripts “err” (e.g., $A_{\textit{err}}$). For $C = A/B$, the propagated error $C_{\textit{err}}^{\textit{propag}}$ combines contributions from both $A$ and $B$:

- For every $I$ such that $B[I] \neq 0$ and $B[I]$ does not cross zero under perturbation:
  - $C_{\textit{err}}^{\textit{propag}}[I] = \frac{A_{\textit{err}}[I]\cdot B[I] - B_{\textit{err}}[I]\cdot A[I]}{B[I]^2\cdot(B[I] + B_{\textit{err}}[I])}$  
  - $C_{\textit{err}}^{\textit{propag}}[I] = \frac{A_{\textit{err}}[I]}{B[I]} - \frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]^2} - \frac{A_{\textit{err}}[I]\cdot B_{\textit{err}}[I]\cdot B[i] -  B_{\textit{err}}[I]^2\cdot A[i]}{B[I]^2\cdot (B[I] + B_{\textit{err}}[I])}$  
  - $|C_{\textit{err}}^{\textit{propag}}[I]| \leq \frac{1}{|B[I]|\cdot |B[I] + B_{\textit{err}}[I]|} \times\left(\left|A_{\textit{err}}[I]\right| + \left|\frac{A[I]\cdot B_{\textit{err}}[I]}{B[I]}\right|\right)$  

## Error Introduction (real)

Error introduction for real (ideal) arithmetic is null:

- $C_{\textit{err}}^{\textit{intro}} = [0]$.*

## Error Introduction (IEEE-754 floating-point)

Let us define $\varepsilon$ the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon)
for the considered format and $\textit{\bf u} = \frac{\varepsilon}{2}$. Let us also define
$\textit{min-normalized}$ the minimal normalized number for the considered format.

According to the IEEE-754 standard, division $c=a/b$ is implemented as rounding
the infinite-precision result to the nearest floating-point number in the 
mode round to nearest even, i.e.

$$\hat{c}=round(a/b)$$

As a result, the
rounding (introduced) error is bounded by $|C[i]|\times\textit{\bf u}$
for the standard rounding mode round to nearest even, provided $\frac{|A[I]|}{|B[I]|}$ is
a normal number (or for any normal number greater or equal than $\frac{|A[I]|}{|B[I]|}$).

- $|C_{\textit{err}}^{\textit{intro}}[I]| \leq \textit{\bf u}\times\max\left(\frac{|A[I]|}{|B[I]|}, \textit{min-normalized}\right)$.

## Error Introduction (int)

where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}.

Error introduction for int arithmetic is less than 0.5:

- $|C_{\textit{err}}^{\textit{intro}}| < [0.5]$.

Division by zero remains undefined and shall be prevented by input constraints.

## Unit Verification

This section contains a verification scenario to verify the above specification for any C/C++ implementation. It uses an abstract type `SymbolicDomainError` replacing each real number in the Why3 specification. `SymbolicDomainError` is a data structure with 4 fields:

- The `real` field is a symbolic abstract domain for ideal (infinitely precise) C/C++ floating-point (or fixed-point) computations.  
- The `float` field is a symbolic abstract domain for the computed value.  
- The `err` field is a symbolic abstract domain for the absolute error, that is the difference between the possible values of `float` and `real`.  
- The `rel_err` field is a symbolic abstract domain for the relative error, that is the difference between the possible values of `float` and `real` divided by `real`.

```c++
Tensor<TSymbolicDomainError<...>> A, B;

/* A, B symbolic initialization */

auto result = [&A,&B](auto I) {
  return (B[I].real != 0) ? A[I] / B[I] :
      /* undefined */ SymbolicDomainError::undef();
};

void init() { // initialization with a default scenario
  for (auto I : A.indexes()) {
    A[I] = BETWEEN(-MAX, +MAX); // no error for A
    B[I] = BETWEEN(-MAX, +MAX); // no error for B
  }
}

template <typename T>
Real getSpecError(T val) { return Real(); }

template <std::floating_type T>
Real getSpecError(const TSymbolicDomainError<T>& val)
   { return std::abs(val.real)*std::numeric_limits<T>::epsilon/2.0; }

template <std::integral T>
Real getSpecError(const TSymbolicDomainError<T>& val) { return 0.5; }

int main() {
   init();
   for (auto I : A.indexes()) {
      auto a = A[I];
      auto b = B[I];
      if (b != 0) {
         auto c = result(I);
         assert(std::abs(c.err) <= getSpecError(c));
      }
   }
}
```

