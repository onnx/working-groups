# Review of the Conv informal spec

## Conv

### Groups
### 1. Wrong property statement
On SONNX only two types of convolution are allowed:
- **Standard** - $groups = 1$
- **Depthwise** - $groups = dX1$

After testing our Hypothesis script for the Conv operator an error was being raised due to the following properties:
**X[C2]** and **W[C1]** that state: $$dX1 = dW1$$
This errors occred whenever the value of groups was the same as $dX1$ (i.e using depthwise convolution)

This property does not match the structure proposed by the [ONNX documentation](https://onnx.ai/onnx/operators/onnx__Conv.html#l-onnx-doc-conv).

Actually, according to the documentation the property should state: $$dW1 = \frac{dX1}{groups}$$

Here is an image proving our point:

![groups_dW1](imgs/groups_dW1.png)


### 2. Missing an important property
It might be important to **include** the following property in the **SONNX informal spec**: $$dW0 \text{ mod } \text{ groups } == 0$$

Here is an image from the documentation that states this property:

![groups_dW0](imgs/groups_dW0.png)