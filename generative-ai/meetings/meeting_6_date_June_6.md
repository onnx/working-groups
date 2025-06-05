# Recording and Transcript:

https://zoom.us/rec/share/ufcA6SlCvg50p8SnFKhoQWINvwjxCRfxOBCLlCtCfBmSqfWWqsQEDG0ADHVCSpQh.9a36U85GbcDGELuH

# Meeting Minutes:

## Logistics:
- Yamini will be on vacation for the next two weeks.
- The regular meeting next week will be canceled due to the ONNX meetup.
- Rama will lead the meeting on the 18th.

## Gen AI Interfaces for ONNX 
- Yamini presented a proposal to standardize GenAI interfaces (Link)
- Problem: Fragmentation exists across various Gen AI deployment stacks (ONNX Runtime GenAI, OpenVINO GenAI, TensorRT etc.), leading to different APIs and user experiences despite some supporting ONNX.
- Proposal: Define high-level interfaces (not a new runtime) to standardize how applications interact with these deployment stacks using ONNX models. The goal is to reduce fragmentation and make it easier for developers to deploy ONNX models across different optimized backends.
- Phased Approach: Start with high-level pipeline APIs (e.g., text generation, diffusion) and later potentially introduce mid-level/modular interfaces for more granular control (akin to Transformers library's flexibility).
- Discussion Highlights: 
    - General positive feedback on the idea.
    - Clarification that TensorRT-LLM doesn't directly use ONNX models (Updated now in the proposal).
    - The workflow involves exporting ONNX models (e.g., from Transformers using Optimum) before these interfaces come into play.
    - Advanced features like vLLM's continuous batching, paged attention, and speculative decoding are considered relevant and could be incorporated, though a "client-first" approach was favored over immediately tackling complex data center-specific optimizations.
    - Debate on whether to capture entire pipelines (preprocessing, model, postprocessing) within a single ONNX model versus the proposed interface approach. More thought needs to be given to understand the benefits and challenges.
- Next Steps: Yamini to explore and suggest PoCs to assess feasibility.

## Sage Attention (Open from Georgy):
- Discussion on whether Sage Attention needs to be an ONNX standard.
- Yuan noted Sage Attention builds on Flash Attention, which is often a backend-specific kernel optimization rather than an ONNX op. If Flash Attention isn't in ONNX, Sage Attention might not be either.
- Max mentioned seeing good results with Sage Attention for long sequences and video generation models, especially quantized models, but also viewed it as an optimized kernel.
- Next Steps: Yamini will follow up with Georgy for more details.

## SSM Operations (e.g., Mamba, Zamba):
- Yamini inquired about discussions or needs for these ops.
- Rama stated no current discussions in the operators SIG. The key is to determine if they are new op definitions or just optimized kernels.

## Attention Op & KV Cache Op Design Update:
- Yuan presented updates to the design for handling KV cache in attention ops.
- Proposal: Introduce more generic ops: TensorScatter (to update past KV cache with new KV at a specific index) and TensorGather (to read a segment from a tensor).
- This aims to provide more flexibility for managing KV cache, especially for sliding window attention and cases where prefill length exceeds cache size.
-	A discussion with Gaurav explored using these ops to potentially create a single graph that can handle both prefill and decode phases by having TensorGather truncate the KV cache for output while the full KV goes to the attention mechanism.
-	The intention is to retain the existing simpler KV cache behavior in the Attention op (from opset 23 carried to 24) and add these new ops for more advanced/explicit cache management.
-	Next Steps: Yuan will update the design document with the new figures and incorporate feedback.


