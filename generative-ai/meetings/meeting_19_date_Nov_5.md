# Recording and Transcript:

https://zoom.us/rec/share/OqvDe89Z-0wuIai1ScdInYlbg8yntukq9qb0ZbalgMEWNT0nZFYUsf8BXmFMcw.2MJttRI2rQmjFD0Y

# Meeting Minutes:

## Flex Attention ONNX Proposal
- Yamini introduced a [draft proposal](https://docs.google.com/document/d/1DOYD4xxqyhg9wSdtwKGp9RBS62V9pnwp/) for adding a FlexAttention operator to the ONNX specification as an open-source contribution.
- Goal: To mirror the capabilities of PyTorch's Flex Attention and allow for exporting models from Hugging Face that use it.
- Experimental Domain: The new operator would be placed in the ["preview"](https://github.com/onnx/onnx/blob/76981e3cac0afc70f56c1565092bfcb8e2f83e16/onnx/defs/__init__.py#L28) domain. Rama clarified that this domain exists for experimentation and is assigned on a per-node basis, complete with its own versioning.
- Technical Details:
  - The proposal will use subgraph attributes to define custom logic within the attention block.
  - Based on feedback from Yuan, the proposal will be updated to include a graph attribute after the Softmax operator (to support quantization use cases) in addition to the one before it (for score modification).
  - Contribution Scope: Rama stressed that the most critical and challenging part of the contribution is creating a backend implementation (e.g., for ONNX Runtime). He suggested that this backend implementation is more important at this experimental stage than adding support to the torch.onnx.export pipeline.
  - Motivating Use Cases: Rama requested that the proposal be strengthened with motivating examples—specifically, models or use cases that require Flex Attention and cannot be expressed using the existing standard ONNX Attention operator.

## Ahead-of-Time (AOT) Compiled Model Support
- The [RFC](https://github.com/onnx/onnx/issues/7301) regarding support for AOT compiled objects in ONNX was discussed.
- Goal: To allow a single ONNX model file to store multiple pre-compiled, optimized versions of a model or subgraph for different target backends (e.g., CPU, various GPUs, NPUs).
- Practical Challenges: Javier raised several significant implementation concerns:
- Combinatorial Explosion: The number of potential compiled targets is vast (vendor, hardware generation, OS, memory, etc.).
- Partitioning Issues: AOT compilation and on-the-fly partitioning (splitting a model across different devices) seem incompatible, as the optimal partition may change for each target.
- Model Size: If each target requires differently transformed weights (totaling gigabytes), storing all permutations in one package would lead to enormous file sizes.
- Proposed Long-Term Vision: Rama suggested a "package" or central repository model. A full package could contain all possible variants, but a user would only download the specific compiled blobs relevant to their machine's hardware.
- [ORT "Compatibility String"](https://github.com/microsoft/onnxruntime/pull/25454): Javier mentioned a useful concept from ONNX Runtime (ORT)—a "compatibility string." This is a hash that serializes a compiled blob's runtime dependencies. It allows a system to inexpensively check if a blob is compatible before downloading the large file.

## Other topics:
- 2-bit Support: Rama mentioned a new [PR](https://github.com/onnx/onnx/pull/7446) in the ONNX repo adding support for 2-bit quantization.
- LLM export paths from PyTorch to ONNX to be discussed in the next meeting
