# Recording and Transcript:

https://zoom.us/rec/share/c3NTkC39OTyDITEH-SDWWOvmCs_eaTO3U6UV74s_mgp95nn-EJQUS2AW-irsGOH1.YqIMtJR2UAVTB_rc

# Meeting Minutes:

- FlexAttention PR 
  - Review: Rama and Yamini have both performed initial reviews on the [FlexAttention PR](https://github.com/onnx/onnx/pull/7534) and believe it is close to merging, though final checks are needed.
  - Next Steps: Kunal will also review the PR. Yamini suggested Mixture of Experts (MoE) as the next operator to target after this merge. 
  - Implementation Strategy: Discussion held on Just-In-Time (JIT) vs. Ahead-Of-Time (AOT) compilation for backends. The goal is to reduce the number of contributed ops (contribs) for new attention types.

- Hugging Face / Edge Exporters
  - Proposal: Discussion on Ilya’s (Hugging Face) ["HF Exporters"](https://github.com/huggingface/transformers/pull/41992) regarding direct model export from Transformers.
  - Architecture Clarification: Sahar questioned if this approach replaces the Input Observer method proposed by Xavier.
  - Outlook: Yamini clarified that Optimum would likely sit on top of HF exporters to provide higher-level tooling (e.g., NNCF integration). A follow-up meeting with the Hugging Face team is planned to discuss the pros/cons of both approaches once Xavier returns from vacation.

- Linear Attention & Fused Operators 
  - Proposal: A new [proposal](https://github.com/onnx/onnx/issues/7689) for high-level fused operators in ONNX to support models like Qwen 2.5 and linear attention variants.
  - Performance: The group discussed whether fused ops (Recurrent, Chunk, Parallel) would yield better performance than decomposing them into primitives.
  - Action: The team will review the issue and provide feedback on the necessity of these specific kernels.

- Ternary and Low-Bit Quantization
  - GGUF Support: The team discussed the rising popularity of GGUF models (Q4_0, Q4_K_M, etc.) and the potential for a GGUF-to-ONNX converter.
  - Technical Bottlenecks: Kunal noted that while conversion is feasible, the primary bottleneck is kernel support in ONNX Runtime (ORT) and Execution Providers (EP).
  - Hierarchical Quantization: Discussion on the trade-offs between accuracy and performance with hierarchical block quantization. Most backends currently flatten these super-blocks during computation.
  - Next steps: Provide feedback on the [GitHub issue](https://github.com/onnx/onnx/issues/7691) discussing the support of non-uniform block quantization in ONNX
