# Introduction

This document is a followup to our July 2nd discussion about the way to specify the behaviour of operators in the presence of errors conditions.

# The issue 
Some operator are not defined for some input values. Typical examples are division by zero, overflows, etc.

For simple operators, those conditions can be specified in the definition of the input domain. For instance `y = Div (a , b)` is not defined for $b=0$, and the domain of the inputs in $\mathbb R$ or $\mathbb Z$ is $\mathbb R\times \mathbb R^*$  or $\mathbb Z\times \mathbb Z^*$, respectively.

For complex operators, the correct domain (where the function is defined) can't be defined easily due to the complexity of the relation between the error condition (e.g., some denominator equal to 0 or some overflow) and the inputs. 

**How can we address this in our informal specification?**

For instance, let's take the `Add` operator: 

`y : int32 = Add(a: int32, b: int32)`

It can be specified as 

$y = a+b$ with $+$ being the usual mathematical addition...

Several levels of specification could be proposed 

#### Option 0
**We don't say anything.**

The operator add is simply specified as 
$$y = a + b $$

Problem: this specification is incorrect since, as soon as $a+b > 2^{32}$,  $a+b$ does not belong to the set of integers `INT32`
.
The user may hopefully be in the case where the condition $a+b\leq 2^{32}$  holds, but the specification remains incorrect (or inconsistent). 

#### Option 1
**We specify the exact conditions for which the specification is applicable.**

Here, the condition is $a+b <= 2^{32}-1$  where operator "$+$" is the usual  addition in $Z$.

Basically, it boils down to specifying the contract using number in $Z$ as "the values computed in $Z$ should be in $[-2^{32}, 2^{32}-1]$ ".
This makes sense (the constraint is correct), but it is not really practical since to check the condition, we have to compute the result (in $Z$)...

In practice, we would be happier with more conservative restrictions, but easier to compute.

For instance, for a simple addition, this could be : $a \leq 2^{31}$  and $b \leq 2^{31}$ .

However, this approach does not work that easily for more complex operators. It **may** work for instance if we know that the input values are in a certain range (e.g., because they have been normalized) so that not overflow can occur. 

#### Option 2 
We specify the operator in the set `INT32`, i.e.,  considering the wrap-around and the signed, two's complement arithmetic.

In that case, operator "+" is replaced by operator "(+)" in the specification. This captures the representation of signed values in two's complement and applies the appropriate addition in this modulus.

Expressed using the usual $+$ operator, the specification becomes
$$
y =
\begin{cases}
(a + b) \bmod 2^n & \text{if } (a + b) \bmod 2^n < 2^{n-1} \\
(a + b) \bmod 2^n - 2^n & \text{otherwise}
\end{cases}
$$

Advantage: the operation is fully and precisely defined in `INT32`. 

It matches exactly what happens in an implementation where our `INT32` in a 32 bit machine value. 

Problem: This approach could be applied to simple operators but for more complex operator such as, for instance, a matrix multiplication, all intermediate operations used to describe the matrix multiplication would actually refer to operation in `INT32`.: the $+$ will be replaced by $(+)$, etc. This approach is cumbersome and does not really express what we expect. In practice, we would prefer all intermediate "computations" to be carried out in $Z$ and the final result to be mapped to `INT32`.  

We may also simply keep all computation in $Z$  (i.e., $+$ in the usual addition in $Z$) and require that no "intermediate value" ever gets out of the `INT32`domain.

In that case, it'll be the responsibility of the implementer or the user to ensure that all intermediate values remains in the appropriate domain:
- The implementer could perform intermediate computations in "larger" domains in order to prevent overflows/
- The user could perform some verification (by testing, formal verification, etc.) to ensure that all intermediate values remain in the `INT32`domain.

Note that the concept of "intermediate values" is strange in a specification. 

In a specification, when iI write $y=a+b+c+d$, I do not say anything about the order in which the operations are performed. I just express that the result $y$ must be equal to $a+b+c+d$ which, for the usual operator $+$ and values in $Z$, can be done in any possible way ($a+(b+c+d))$, $((a+b)+(c+d)$), etc.

### Option 3
- We simply specify that the semantics is the one defined using the usual $+$ operator considering that no overflow shall occur (some  would write "no runtime error occurs").

### Option 4
We simply state that "some error condition may occur" (e.g., an overflow), but it is strange to write this in a specification.

### Option 5
We chose the most accurate option among the previous one that can be implemeted in practice for a given operator.
In the example of an operator that can lead to a division by zero, we would either say that "some division by zero could occur" (option 4) or "division by zero will occur for such or such input value" (option 1).

