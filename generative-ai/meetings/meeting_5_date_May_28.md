# Recording and Transcript:

https://zoom.us/rec/share/CBYugUyenm4v6AVBZAbeV_0FtTwGq-AVXQZbC-lpBe_o2-hEgVIc4NI3Sx0IozNA.oxt5XVcovb1VMUd1

# Meeting Minutes:

## Exporters & ONNX Script
- Attention Export (Opset 23): 
  - Kshitij Khode reported a PR is ready for converting Scaled Dot Product Attention (SDPA) to the ONNX Attention operator as part of an Opset 23 check-in (PR link to be shared later).
- Fusion for New Ops (RoPE, RMS Norm in Opset 23): 
  - Kshitij is looking into other Opset 23 ops like RoPE and RMS Norm. These are often implemented in PyTorch (e.g., via TorchTune) and require graph fusion on the FX graph.
  - Rama confirmed ONNX Script has existing fusion implementations for ops like RMS Norm and Rotary Embedding (RoPE). Links: https://github.com/microsoft/onnxscript/blob/main/onnxscript/rewriter/ort_fusions/rms_normalization.py, https://github.com/microsoft/onnxscript/blob/main/onnxscript/rewriter/ort_fusions/rotary_embedding.py
  - These fusions currently require explicit calls by the user. The goal is to automate these fusions during the export process if the target opset is 23 or higher.
  - Path Forward: The exporter has a hook to an optimize method in ONNX Script and this method needs to be extended to automatically call these fusion patterns: https://github.com/microsoft/onnxscript/blob/5a8b9e616ead90069914b8693f30bb7e71a561c6/onnxscript/_framework_apis/torch_2_6.py#L32
- Optimum (Hugging Face) Integration: 
  - Kshitij highlighted that Hugging Face Optimum does not currently support opsets higher than 21 and does not use the TorchDynamo export path by default. This prevents leveraging newer ops like Attention at opset 23.
  - Justin mentioned that switching Optimum to use the Dynamo exporter by default is a breaking change for downstream tools that rely on the TorchScript exporter's graph structure or naming conventions.
  - Potential Solution: Gradually migrate Optimum, possibly by adding CLI parameters to enable Dynamo export and specify higher opsets. Contacting Joshua (https://github.com/xenova) from Hugging Face (active in the ONNX space) was suggested
  - Justin noted that Optimum lacks dedicated full-time maintainers at Hugging Face, so community contributions are welcome.

## Operators: Attention & KV Cache
- Continued discussion on Attention operator updates:
  - KV Cache Management: A central point of discussion was whether KV cache management should be within the ONNX graph (e.g., as part of the attention operator or a dedicated KV cache operator) or handled by the user outside the graph (i.e., KV cache as graph input/output).
  - Variations & Complexity: 
    - The group discussed supporting different KV cache variations (e.g., Hugging Face's "static cache" for in-place updates, which the ONNX spec aims for, vs. "dynamic cache").
    - Yuan noted difficulties exporting using Hugging Face's static cache export for GPT-2 using torch.export (FX graph generation errors).
    - The interaction of KV caching with other operations, like positional embeddings (citing the "Efficient Streaming Language Models" paper where embeddings are added after cache retrieval), adds complexity to a unified operator design.
    - Handling scenarios where the prefill sequence length exceeds the cache size (a point raised by Gaurav) would require careful design, potentially different graphs for prefill and decode phases if cache management is in-graph.
  - Performance Implications: 
    - Yamini and Ankit shared that "stateful transformation" (making KV cache an internal graph variable rather than I/O) shows performance benefits due to data locality (e.g., keeping cache on NPU memory without constant transfers).
    - Rama questioned whether similar performance could be achieved with graph I/O using I/O bindings and direct pointer passing if no actual memory copy occurs, highlighting the distinction between logical data flow and physical memory management.
- FlexAttention: Yamini confirmed that PyTorch models using flex attention can be exported via torch.dynamo.export to a torch.higher_order.ops.flexattention op. This could then be mapped to the ONNX attention operator if a mapping is defined.

## Backend Representations & Backend Context
- Yamini proposed exploring the use of ONNX Script's fusion capabilities to capture backend-specific subgraphs and represent them as a "backend context" function within the ONNX model. This could allow for more standardized representation of compiled blobs or hardware-specific optimizations.
- Rama noted that backend context is generally more arbitrary than specific operator fusions and would likely require significant backend compiler involvement to identify and create these subgraphs.
- The discussion touched on whether this process would be part of the main ONNX export (e.g., torch.onnx.export) or a subsequent optimization step.
- The aim is to allow native toolchains (beyond just ONNX Runtime EPs) to recognize and leverage these backend contexts if standardized.

## Pipeline Interfaces
- Yamini mentioned she is working on a proposal regarding pipeline interfaces and will share it with the working group for further review and discussion. Here is the proposal: https://docs.google.com/presentation/d/1cAwOvHTF18Gbr58OVtslQjQtvXX0RIg2

## ONNX Community Meetup Presentation
- The working group will prepare a presentation for the upcoming ONNX Community Meetup.
- It will be a high-level update, likely around 6-8 minutes, summarizing the group's activities and progress.

## Action Items:
- Yamini: Draft a high-level summary presentation for the ONNX Community Meetup and share it with the group for feedback.
- Kshitij/Justin: Create an issue/reach out (e.g., to Joshua from Hugging Face via Optimum GitHub) to discuss enabling newer opsets and the Dynamo exporter path in Optimum, referencing the relevant PRs and needs of the working group.
- Yuan: Continue investigating issues with exporting Hugging Face's static KV cache (e.g., for GPT-2) via torch.export and refining the Attention operator proposal, considering the discussed complexities around KV cache management.
- Rama/All: Investigate extending the optimize method in ONNX Script (called by the exporter) to automatically apply fusions for new ops (like RoPE, RMS Norm) when opset 23+ is targeted.

