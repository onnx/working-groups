See also the previous note [here](./error_conditions_2.md).

- An operator in the SONNX set shall be fully specified. 
	- In particular, the domain and range of the operator must be fully defined.
	- The expected value to be returned by the operator must be specified for all possible input value in the domain. 

- The domain must be specified by constraints on the inputs (e.g, "x > 0" for operator log(x)). 
	- For complex functions, providing an explicit definition of the domain may be difficult... For instance, what is the domain of definition of f(x,y)=tan(sqrt(x+y))? [well, thi sis not the most complicated case, but you probably get the point...]

- Let's call "abstract" the mathematical operator.
	- An abstract operator may be a *** partial function ***, i.e., a function that is not be defined for some values of the input. 

- Let's call "concrete" the actual, computer-based, implementation of an operator. 
	- Ideally, a concrete operator should be a *** total function ***, i.e., a function that *** always *** returns a value, even if the input value is not in the domain defined by the abstract function. 
	- For instance, the concrete Div(x,y) for the float32 data type shall return an Inf is y=0.0 whereas operator Div(x,y) is simply not defined in R.
	- The SONNX specification shall specify the total function. 

- The principle of defining total functions is applicable for concrete operators in the domain of IEEE floating point numbers because this behaviour is completely supported by the current hardware targets. 

- This principle is *** not applicable *** to integers because there is no direct hardware support for that.
	- This means that, for integer data types, there should be something such as an "undefined	 behaviour" and an "undefined output".
	- Concerning "undefined behaviour" 
		- This occurs for instance in the case of a division by zero. The behaviour depends on the target (including HW, runtime, OS). For instance, a trap may be raised by the processor and handled by the OS, the runtime, etc. From a SONNX user perspective, this means that the operator never returns.
		- We *** could *** specify an operator with a controlled behaviour, but 
			- (i) this would certainly require modifying the operator interface to carry the information that the operator failed (since this data cannot be carried in the integer value itself, as it is the case for floats).  
			- (ii) no implementation would be able to comply with it (and, in particular, no existing implementation would) because testing the condition of occurence of the error would be prohitively costly. 
	- Concerning "undefined value" 
		- In the case of wrap-arounds, the error may simply be undetected and propagate. Back in the days, there used to be traps for wrap-around conditions, but it is no more the case today: to detect a wrap-around, there shall be some code to test the condition (there might be some exceptions, but I think that this is the most general case). 
			- SONNX could require wrap-around conditions to be detected and processed. If detected, this error would be handled in the same way as division by zero (the operator simply does not return). But this is practically unfeasible since it would require testing the condition bits after every operator that may lead to a wraparound. 
		- So, the specification must indicate that an operator may return an "undefined value" when a wrap-around condition may occur. 
		- Another solution woul dbe to specifiy the exact behaviour of the interger operators, *** including the wrap-around ***. In that case, there would be no "undefined value", but the specification would be slightly more complicated ("+" on signed ints would be specified in 2's complement arithmetic. See "Option 2" in my note.

- So, 
	- For IEEE data types
		- operators *** must *** be total functions, which means that we have to cover all cases, including those where inputs are Infs and NaNs and where operator may return Infs and NaNs. The specification shall indicate what is the value returned by the operator when the inputs contains Infs or NaNs. 
	- For integer data types, 
		- for wrap-around : we fully specify operators with wrap around, i.e., see "Option 2" in this note or we specify that operations may wrap around and return "undefined value"
		- for div / 0 : we specify that some "undefined behaviour" may occur.
 
- The specification shall not refer to or impose a specific implementation. If the specification uses an operational way (a series of computations) to compute the function, it does not imply that the function will actually be implemented that way. 

- We have to discriminate errors that are inherent to the function (i.e., that are part of the mathematical definition of the function, so they shall appear in the definition of the abstract operator) from errors that depend on the way the function is implemented. 
	- For instance, let's consider the SoftMax function. The abstract function is fully defined over ]-\intfy, +\infty[. There is no constraint inherent to the function. 
	- The concrete SoftMax for float32 should return the correct approximate value of the abstract SoftMax for any value between FLOAT_MIN and FLOAT_MAX. The specification shall also specify what is the expected output when inputs contains Inf or NaNs. 
	- In this very case, this specification is "feasible" (i.e., there is a simple way to comply with it): one has simply to implement SoftMax using the "-max(zi)" trick. This means that it is reasonable to specify it that way.
	- In other cases, preventing error cases at the implementation level is much more difficult. 
		- For instance, preventing an overflow or even a NaN in a matrix multiplication is not (easily) feasible, which means that we cannot write that the MatMul should return the correct approximate value of the abstract MatMul for any value between FLOAT_MIN and FLOAT_MAX. 
		- This can only be required for a specific domain where we know that this property can be achieved "simply" (whatever that means...).  
 
- The SONXX specification may specify a "minimum" level of service". For instance, operator Op return f(x) for x in D and f(x) or NaN for x out of D. 
	- A specific implementation may provide a better "service" such as "operator Op returns f(x) for any x". See the example of Softmax given by Franck.
	- In that case, SONNX would require the implementer to provide an updated version of the specification of Op corresponding to its own implemenaton. 
	- However, the operator will at least comply with the SONNX specification. 

- The semantics of a SONNX model will be the one derived from the SONNX specification of operators, not the one considering the "improvements" done in some specific implementation. So, even if this approach makes sense, it cannot really be part of SONNX...  

*[Edoardo]* Regarding the integer overflow issue, just bear in mind that not all hardware platforms deal with overflow by wrap-around. Instead, some Digital Signal Processors (DSP) may favour saturation, i.e. INT_MAX + 1 == INT_MAX and INT_MIN - 1 == INT_MIN. Specifying overflow as undefined behaviour in SONNX will cover both cases.

*[Edoardo]* Regarding the floating-point behaviour, there are two opposite philosophies. The IEEE754 standard recommends implementing correctly-rounded operators. That is, the operator behaves as if it was computing the result in infinite precision and then rounding to the nearest flaoting-point value. In contrast, the C standard leaves room to implementation-dependent behaviour which, in the extreme case, could mean that log(x) == 42 for any x is a valid C operator. Interestingly, the upcoming C standard plans to introduce "correctly rounded" version of mathematical operators with a prefix "cr_". That is, log(x) is implementation dependent, but cr_log(x) must be correctly rounded.

*[Edoardo]* Implementing a correctly-rounded operator is quite hard. Even more so if the operator is a function of many variables. Restricting the domain would not mitigate this issue. Hence, the biggest problem I see does not lie in specifying a restricted domain (e.g. Sigmoid(x) should be correctly-rounded for -4 <= x <= +4), but specifying a "softer" requirement than correct roundedness (e.g. the relative error produced by Sigmoid(x) should not exceed 2%). In this respect, I suggest considering bounds on the maximum relative and absolute error allowed. A thorough empirical analysis of existing float32 and float64 libraries might give an indication on how to fix reasonable bounds on the numerical error.
