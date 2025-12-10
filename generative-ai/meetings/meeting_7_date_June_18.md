# Recording and Transcript:

https://zoom.us/rec/share/qckhrTvo1WtKmVUmM2MGXHi25zSZVVYYhEoO3k_EEniK-y6nmXb0B5RtJgI6if7u.WLrXGKhXDpIVhCi1

# Meeting Minutes:

_Attendees_: Ti-Tai Wang (Microsoft), Rama (Microsoft), Yuan Yao, Rajnish Aggarwal,
Bhavik Sharda (Nvidia), Kevin (Nvidia).

## Exporter support for opset 23:

* The PR to map Torch's SDPA to ONNX Attention has been merged in.
* Yuan and Justin pointed out a couple of issues with the PR. One is that it was producing
the wrong head-size attribute, and the second is that Torch's op supports more dimensions
than the ONNX op. The solutions seem straightforward, but it would be good to merge them
in for the upcoming Torch release.
* As for RotaryEmbedding and RMSNormalization, these are not aten ops. Typically, these
are composed using lower level torch ops. Hence, it will be necessary to use fusion
optimizations to introduce these ops. The necessary infrastucture exists in the onnxscript
rewriter, and preliminary versions of these fusion ops exists, though they target ORT's
contrib ops for the same. It was decided that these fusions should be added and should be
called as part of the export process when the target opset is 23 (or greater). Yuan offered
to help, and Yuan and Rama to follow up.

## Attention Op and KV Cache Op Design:
* Yuan and Rama summarized their discussions offline from the meetup. One of the usage
scenarios is to perform Matmul with 16bit floats, but using 32bit float for reduction.
Rajnish said that this was commonly required, but not universal. Thus, there are kernel
implementations that perform 16bit float matmul with 16bit accumulation as well. Given
that both of these are in use, a question to be considered is whether the ONNX Matmul
(and Gemm) ops should be updated to indicate the accumulation precision explicitly via
an attribute. Meanwhile, the pattern used to achieve higher-precision accumulation is
to cast to higher-precision, do the matmul, and cast back to lower-precision.
* With regards the Tensor scatter/gather ops for KV cache udpate, there was a discussion
whether the existing GatherND/ScatterND suffices or whether new ops are required. Two
limitations of the existing op are that it can be used to update the tensor at only one
position (though the updated value can span multiple dimensions), and that the updated
values dimensions must be some sequence of trailing dimensions. Hence, a new op would help
avoid these limitations.
* The Attention op's proposed graph attributes was also discussed. Rama expressed a
concern that the graph attribute allows for more general computations to be described,
which might not be easy for backends to support. Yuan mentioned that, in addition to
varying the accumulation precision of MatMuls and Softmax, another issue was the need
for introducing Q & DQ after a MatMul. The conclusion was that it would be helpful to
describe the common code patterns expected in these graph attributes, as these are the
ones to be supported initially.


