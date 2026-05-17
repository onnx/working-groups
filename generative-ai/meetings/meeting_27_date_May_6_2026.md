# Recording and Transcript:

https://zoom.us/rec/share/fQh4o0_bHJgSjWBvnUB10n2ggKua4CHkHFmV1u9HCC-iB4fdwH8WNKT0rvS3y2IW.Q-_7P93DRJSQ88mz

# Meeting Minutes:

## Linear Attention & Causal Convolution Operators

- Tommaso is working on a proposal to add two new operators to ONNX: Linear Attention and Causal Convolution.
- This implementation follows a previous [proposal](https://github.com/onnx/onnx/issues/7689) made by Justin. It is currently a work in progress but will be ready for review soon. The operators are required for models like Qwen 3.5 and Mamba.
- ONNX Runtime (ORT) has a contrib op loosely based on this proposal that is currently being used in several models, including Nemotron-3 (https://github.com/microsoft/onnxruntime/pull/27842) 
- The initial plan is to support these operators as a block in Model Builder to construct models, rather than immediately integrating them into PyTorch-to-ONNX export scripts (like ONNX Script). 

## Mixture of Experts (MoE) & Grouped MatMul Proposal

- Rama shared a link to a recent proposal regarding [Grouped MatMul](https://github.com/onnx/onnx/issues/7902) targeted at Mixture of Experts (MoE) models.
- Unlike ORT’s native MoE op (which fuses activations), the Grouped MatMul proposal focuses strictly on the core expert selection part. While it won't offer maximum fusion benefits and may result in a chain of 4 to 5 ops (requiring separate activations), it offers a more flexible alternative to handle the constantly changing activation functions and variants in newer MoE models.
- Action Item: Community to share feedback on the Grouped MatMul proposal.


## FlexAttention Backend Implementation Strategy
Yamini shared a [draft document](https://docs.google.com/document/d/1fKnhu7LQe1EKDLYNjrTEMFcNf7pt3Nf4O8Z1R5oNF5E/edit?usp=sharing) outlining the next steps for backend consumption of the recently merged FlexAttention op.

- Proposed Workflow:
  - Export a reference model from PyTorch using torch.onnx with the attention implementation set to FlexAttention in Transformers, creating a higher-order flex_attention op.
  - Validate against the MLAS CPU implementation using two performance tiers:
    - Level A: Inline the function and execute using individual primitives (GEMM, Softmax, etc.).
    - Level B: Use a pattern-matched fused kernel (leveraging existing MLAS support for SoftGap, Alibi, etc.).
  - Validate across hardware Execution Providers (EPs) like OpenVINO, TensorRT, or CUDA.
- Compilation Strategies & Trade-offs: Rama and Yamini discussed three primary compilation paths for backends:
  - Decomposition: Execution via individual primitive ops. (Rama noted that unfused function expansion works reasonably well on CPU, but carries a high kernel launch overhead penalty on GPU/CUDA).
  - Handwritten Fused Kernels: Pattern matching to specific fused implementations (e.g., OpenVINO's direct mapping to Scaled Dot Product Attention via oneDNN for CPU/GPU).
  - JIT Compilation / CodeGen: (e.g., MLIR-based compiler lowering for optimized inference).
- Action Item: Yamini to update the draft to explicitly include a CodeGen / JIT Compilation path as a stretch goal for backends that support it, then circulate the document for further review. (Done)

## Hugging Face Exporters (TorchDynamo) Validation
Yamini presented initial AI-assisted testing [results](https://drive.google.com/file/d/1zdHxw3rSc_9G6OsPR7rgLd4u_X5Za5MY/) assessing whether ONNX models can be successfully generated using the Hugging Face (HF) exporters path via the TorchDynamo exporter architecture.

- Findings:
  - Standard Text Generation models, Mixture of Experts (MoE) models, and Encoder-only NLP models pass ONNX checker test
  - Some of the Vision-Language (VL) / Multi-modal models fail (likely missing corresponding auto classes or ORT classes), and certain Encoder-Decoder architectures (e.g., Marian).

- The testing currently only checks if a valid ONNX graph is successfully produced and passes the ONNX structural checker; end-to-end execution accuracy has not yet been verified.
