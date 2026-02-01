# Recording and Transcript:

https://zoom.us/rec/share/Tej9nFPPA46beheUTHUftH5J_bGKSOAYA7Vp6cGmdmDRzVazUiOx7ZB8aOICvc-d.YQDpi8IhNHsIukAA

# Meeting Minutes:

**Ternary Storage Format Proposal**
- Soumendu Ghosh presented a proposal ([paper](https://drive.google.com/file/d/1oeHVpCygJ9XlWKChB5e1tCWVFil9j9gY/view?usp=drive_link), [presentation](https://drive.google.com/file/d/1ofjAkMWh0XEXm2WauN1CLSwNF49kpMwb/view?usp=drive_link)) for a standardized storage format for ternary weights in LLMs, specifically targeting models like BitNet b1.58.
- Key Technical Points:
  - The Concept: Ternary weights consist of three values (-1, 0, 1). While theoretically requiring 1.58 bits, they are typically stored in 2 bits.
  - Proposed Encoding: Packing 5 ternary values into 1 byte (8 bits).
    - 3^5 = 243 states, which fits within the 256 states available in 8 bits.
    - This provides a 20% memory reduction compared to standard 2-bit packing (8 bits vs 10 bits).
  - Benefits: This is a deterministic, lossless compression scheme that reduces memory footprint and energy consumption by minimizing off-chip memory transactions.
  - Hardware Support:
    - Native: Hardware with decompression engines can unpack data in the data path.
    - Fallback: Systems without native support can use a TernaryDecode operator at compile-time or runtime.
- Discussion & Opens:
  - Block Size: Discussion around the optimal block size for alignment. A block size of 320 or 640 provides the best alignment for 64-byte cache lines without padding wastage.
  - Lookup Table: The proposal includes a standardized 256-entry lookup table for encoding/decoding across all models and layers.

**Flex Attention PR**
- The group discussed Rama’s feedback on the [Flex Attention Pull Request](https://github.com/onnx/onnx/pull/7534).
- Current State: The PR follows PyTorch's element-wise transformation approach.
- Feedback: Ganesan suggested moving to a tensor-to-tensor computation representation.
  - Reasoning: Element-by-element loops are inefficient in interpreter-based systems. Tensor-oriented ops (Softmax, MatMul) leverage existing optimized backend kernels.
  - Outcome: This change is expected to significantly simplify the PR by removing complex loop-building logic.

**Optimum-ONNX & Exporter Path**
- Yamini and Xavier discussed the path forward for exporting LLM models.
- Current Issues:
  - Optimum-ONNX currently defaults to dynamo=False.
  - Enabling Dynamo requires significant patching for different models.
  - The "Transformers" repo is slow to merge necessary patches (some pending for 6 months).
- Proposed Solution:
  - Xavier has a set of patches for various Transformer versions that handle cache classes and control flow.
  - Yamini expressed a preference for support of the optimum workflow as it is used by many developers.
- Next Steps:
  - Xavier will prepare a presentation for the next meeting on Transformer patches and options.
  - Xavier shared the following links:
    - [Link](https://github.com/sdpython/onnx-diagnostic/tree/main/onnx_diagnostic/torch_export_patches) to the code of the patches made so far for the ONNX export
    - [PR to transformers](https://github.com/huggingface/transformers/pull/41992) to check if models are exportable
    - [PR to optimum-onnx](https://github.com/huggingface/optimum-onnx/pull/113) adds a ‘--dynamo’ parameter to trigger the dynamo exporter, but may not work for all models and fails with transformers 5.0 

**Action Items**
- All: Review ternary storage proposal ([paper](https://drive.google.com/file/d/1oeHVpCygJ9XlWKChB5e1tCWVFil9j9gY/view?usp=drive_link), [presentation](https://drive.google.com/file/d/1ofjAkMWh0XEXm2WauN1CLSwNF49kpMwb/view?usp=drive_link)) from Soumendu and give feedback/inputs
- Xavier: Prepare presentation on Transformer/optimum patches and options to review in the next meeting
- PR contributor (mshr-h): Update [Flex Attention Pull Request](https://github.com/onnx/onnx/pull/7534) to tensor-to-tensor logic
