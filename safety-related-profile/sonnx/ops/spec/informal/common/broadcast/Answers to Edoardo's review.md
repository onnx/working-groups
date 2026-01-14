**Note 1: all questions and comments are explicitly numbered. Whenever I have suggestions in terms of writing/phrasing, I just changed the text (highlighted in bold capital font).**

*Got it.*

**Note 2: it is unclear why L cannot be 2^31-1. Why "minus one"?**

*The broadcast was defined initialy in the scope of the Max operator. In the definition of the Max operator (https://onnx.ai/onnx/operators/onnx__Max.html) it is indicated "Between 1 and 2147483647 inputs". 2147483648 = 2^31. Thus the number of inputs for the Max operator is 2^31-1. Moreover, note that L is the last index. I.e. the input tensors are numbered from 0 to L. In consequence the L is the number of inputs minus one. Note that this constraint is only relevant for the operators Max, Mean, Min and Sum. Other operators where broadcasting is applicable have only two or three inputs.*

**Note 3: this remark (the access to the tensor data remains possible) is unclear. Is it a statement about copying the data vs accessing by reference? Or is it a subtle reference to the Description fo Step 1 below? Is the meaning something like "during the broadcasting, the data of the input tensor remains in place", where "in place" is to be intended as the technical memory access terminology? In general, it seems the intention here is to say something about the implementation of the broadcasting operator, which I am not sure is the desired goal.**

*The intention is not to say something about the implementation. The intention of the three bullet points is to indicate that there are consequences on (1) the number of dimensions, (2) the size of each dimension and (3) the indexes used to access the data. May be we could change this last bullet point by "access to the data through tensor index is modified accordingly"*

**Note 4: the notation was difficult to parse, I have tried to improve it.**

**Note 5: the link below ("Origin") does not cover the error conditions explicitly. Examples of errors are in the numpy documentation linked therein. Are we happy with the reader having to follow two links to get to the actual information? https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules**

**Note 6: for m ∈ [ 0 , L ] means that there are L + 1 input tensors. This issue is present throughout the document.**

**Note 7: the shape might change, so is it really the same "type"? Maybe we can say "the entries of Xm and Zm must have the same numerical type"**

**Note 8: see note 6**
