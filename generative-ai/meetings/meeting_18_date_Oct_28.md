# Recording and Transcript:

https://zoom.us/rec/share/ggOyXsfGFvo0bPSfzFObjNcyBdNT_XdnOblhMxIcF-IZEVHmzRIvac1sPrTuEbO0.yrtfj7ntnF8pFGY0

# Meeting Minutes:

- **Follow up from previous meeting:** The team continued their discussion from the previous meeting (https://github.com/onnx/onnx/issues/7301) about the proposal to allow backend-specific, pre-compiled objects to be stored within an ONNX model.
  - Weight Sharing: Yuan asked how weights (initializers) would be handled.
    - Rama and Justin explained that the proposal assumes initializers will remain in the main graph and be passed as inputs to the precompiled object.
    - This is to ensure the subgraph has its own separate naming scope, which prevents name collisions with the main graph. The runtime would handle the graph replacement and connect the initializers.
  - Single Node vs. List of Nodes: Justin stated he is leaning toward allowing the replacement to be a list of nodes rather than a single function call. He feels this is more self-contained and avoids forcing the model to include "extra model-local functions" that are only there for the replacement logic.
  - Interaction with ONNX Runtime (ORT) EPs: Rama raised a complex issue:
    - This proposal is for ahead-of-time (AOT) compilation, but ORT dynamically partitions the graph across a sequence of Execution Providers (EPs) (e.g., [CPU_EP, NPU_EP]).
    - An optimization cached for the NPU might assume it sees the full graph. However, if it's the second EP in the list, it will only receive a partial graph (whatever the CPU_EP didn't take).
    - Yamini noted that creating cached optimizations for every possible combination of EPs would be impossible.
    - The group concluded that the most practical solution is to bound the problem: these AOT optimizations would likely only apply to the primary (first) EP in the list.
 
- **PyTorch 2.9 and torch.export for LLMs:** Yamini raised the topic of PyTorch 2.9 deprecating TorchScript, forcing a move to torch.export. She asked if the new exporter is mature enough for LLMs.
  - Current Status (from Justin):
    - Text-generation models (Llama, Gemma) are "pretty confident" and exportable.
    - Multi-modal models (like Phi) are more difficult due to control-flow loops for image processing.
    - The main blockers are the exporter's strictness (it fails if it can't prove graph soundness) and control flow, as old iit.script workarounds are no longer supported.
    - Some patches are still needed for Hugging Face Transformers models. Justin shared a notebook from his PyTorch conference talk that has the patches: https://github.com/justinchuby/pytorch-conference-2025/blob/main/demo.ipynb

  - Static Cache vs. Dynamic Cache: Related to the export topic, Yuan asked about the status of exporting static cache, which is preferred by NPUs (as Yamini noted) and needed for the TensorScatter op.
    - Dynamic cache exports fine (using Concat ops), but static cache export fails.
    - Root Cause (from Justin): The issue is a "representation" problem. PyTorch (and Executorch) treats the static cache as a mutable buffer. ONNX does not support mutable buffers as inputs. The current workaround (e.g., in Executorch) is to treat the cache as an initializer (a weight), which is not correct.
    - Path Forward: The team agreed more investigation is needed. The goal is to generate a TensorScatter op. This might be achieved via graph surgery after export or by pushing new "wrapper" models into Optimum-ONNX (which Justin plans to investigate).

- **New Op Standardization:** The team discussed standardizing new, complex operators to reduce the number of contrib ops.
    - MOE (Mixture of Experts) & Flex Attention: Justin asked about the status of standardizing MOE. Yamini noted both MOE and Flex Attention were discussed as candidates.
    - Rama explained the main problem:
      - Old Style: Backends are efficient at handling ops with simple attributes
      - New Style: MOE and Flex Attention require graph attributes (passing an entire subgraph/function as an attribute). Backends do not yet have an efficient, proven way to handle this
    - Action Item: Yamini offered to create a draft for open-source contribution request for Flex Attention to start building a proof-of-concept (POC) and explore backend implementation challenges.

- **Gaps in QDQ (Quantization) Representation:** Justin asked what is missing from the current QDQ (Quantize/Dequantize) specification.
  - Yuan noted that for SAGE Attention, block quantization is needed on multiple axes, whereas the current ONNX op only supports one.
  - Rama highlighted a strong need for a 2-bit quantized type, which ONNX currently lacks. 3-bit was also mentioned.
  - Action Item: Justin created an issue on the ONNX GitHub repo to collect these requirements (https://github.com/onnx/onnx/issues/7435)
