# Introduction

This document is a followup to our July 2nd discussion about the way to specify the behaviour of operators in the presence of errors conditions.

# The issue 
Some operator are not defined for some input values. Typical examples are division by zero, overflows, etc.

For simple operators, those conditions can be specified in the definition of the input domain. For instance `y = Div (a , b)` is not defined for $b=0$, and the domain of the inputs in $\mathbb R$ or $\mathbb Z$ is $\mathbb R\times \mathbb R^*$  or $\mathbb Z\times \mathbb Z^*$, respectively.

For complex operators, the correct domain (where the function is defined) can't be defined easily due to the complexity of the relation between the error condition (e.g., some denominator equal to 0 or some overflow) and the inputs. 

**How can we address this in our informal specification?**

For instance, let's take the `Add` operator whose signature is:

`y : int32 = Add(a: int32, b: int32)`

It can be specified as 

$y = a+b$ where operator $+$ is the usual mathematical addition defined in $\mathbb R$, $\mathbb Z$, etc.

Several options for the specification can be proposed...

# The options

#### Option 0
**Don't say anything...**

The operator `Add` is simply specified as 
$$y = a + b $$

Problem: this specification is incorrect since, as soon as $a+b > 2^{32}$, the value $a+b$ does not belong to the set of integers `INT32`
.

The user may hopefully be in the case where the condition $a+b\leq 2^{32}$  holds, but the specification remains incorrect or inconsistent (i.e., the "user" of the operator cannot expect condition $y=a+b$ to be satisfied for all values in the domain). 

#### Option 1
**Specify the exact conditions (the domain) for which the specification is applicable.**

Here, the condition is $a+b \leq 2^{32}-1$ (for the right bound of the domain) where, again, operator "$+$" is the usual addition.

The specification becomes
$$y = a + b $$
for any $a$ and $b$ in $\mathbb Z \times \mathbb Z$  such that 
$-2^{32} \leq a+b \leq 2^{32}-1$

This solution makes sense but it is not really practical since to check the condition *in practice*, we have to compute the result in $\mathbb Z$)...

In practice, we would be happier with some condition - possibly more conservative - easier to check.

For instance, for a simple addition, this could be : $-2^{31}+1\leq a \leq 2^{31}$  and $-2^{31}+1 \leq b \leq 2^{31}$ .

However, this approach is not easy to implement for more complex operators. It **may** work for instance if we know that the input values are in a certain range (e.g., because they have been normalized) so that not overflow can occur. 

#### Option 2 
**Specify the operator in the set `INT32`, i.e.,  using signed, two's complement arithmetic.**

Expressed using the usual $+$ operator, the specification becomes
$$
y =
\begin{cases}
(a + b) \bmod 2^n & \text{if } (a + b) \bmod 2^n < 2^{n-1} \\
(a + b) \bmod 2^n - 2^n & \text{otherwise}
\end{cases}
$$

Advantage: the operation is fully and precisely defined in `INT32`. It matches exactly what happens in an implementation where our `INT32` isa 32 bit machine value. 

Problem: This approach could be applied to simple operators but for more complex operator such as, for instance, a matrix multiplication, all intermediate operations used to describe the matrix multiplication would actually refer to operation in `INT32`. The usual $+$ will be replaced by $(+)$, etc. This approach is cumbersome and does not really express what we expect. In practice, we would probably prefer all intermediate "computations" to be carried out in $\mathbb Z$ and the final result to be mapped to `INT32` (to be compared with the case where all intermediate operations are carried out in $\mathbb Z$).

Another solution would be to do all computations using standard arithmetic in $\mathbb Z$  (i.e., use $+$ in the usual addition in $Z$) and require that no "intermediate value" ever gets out of the `INT32`domain.

In that case, it'll be the responsibility of the implementer or the user to ensure that all these "intermediate values" remain in the appropriate domain:
- The implementer could perform actual (2's arithmetic) intermediate computations in a larger domain (tahn `INT32`) in order to prevent overflows
- The user could perform some verification (by testing, formal verification, etc.) to ensure that all intermediate values actual remain in the `INT32` domain.

Note that the concept of "intermediate values" is strange in a specification. In a specification, when we write $y=a+b+c+d$, we do not say anything about the order in which the operations shall be actually  performed (thanks to commutativity and associativity). We just express that the result $y$ must be equal to $a+b+c+d$ which, for the usual operator $+$ and values in $\mathbb Z$, can be done in any possible way ($a+(b+c+d))$, $((a+b)+(c+d)$), etc.

### Option 3
**Specify that the semantics is the one defined using the usual $+$ operator considering that no overflow shall occur (some  would write "no runtime error occurs").**

Such specification is a bit of a chicken-egg problem in the sense that saying the "no overflow shall occur" is not a complete specification: what are those "overflows"? what is the actual conditions to be checked?

Stated differently, the specification is something abstract and we don't really know "when" those "overflow" may occur. 

If we were to be more explicit, we could (for instance) require that, in the case of operation $y=a+b+c+d$ :
- $a+b$ is in the domain of `INT32`
- $b+c$ is in the domain of `INT32`
- $c+d$ is in the domain of `INT32`
- $a+c$ is in the domain of `INT32`
- etc. 
  
because we simply don't know in which order the operations will be carried out.

### Option 4
**Simply state that "some error condition may occur" (e.g., an overflow). 
**

This is strange to write such a thing in a specification... because (i) it is unclear and (ii) brings no useful information (besides the one of being "careful").

### Option 5
**Chose the most accurate option among the previous ones that can be implemented in practice for a given operator.**

In the example of an operator that can lead to a division by zero, we would either say that "some division by zero could occur" (option 4) or "division by zero will occur for such or such input value" (option 1).

