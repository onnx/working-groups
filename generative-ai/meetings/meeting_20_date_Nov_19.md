# Recording and Transcript:

https://zoom.us/rec/share/3wclYWDDTgflxIRAXXDdO7VAkARn77djNA8ASmFKZxGSZI8jEY0jSypRbexpL02j.-jTQkSRBL1HgqTWN

# Meeting Minutes:

- Flex Attention Proposal:
  - Yamini shared the [draft proposal](https://docs.google.com/document/d/1DOYD4xxqyhg9wSdtwKGp9RBS62V9pnwp/) for the FlexAttention operator.
  - The group is requested to review the proposal
  - Next Step: Yamini plans to create the formal GitHub issue and Call for Proposals next week

- Streamlining LLM Export Options
The group discussed the current fragmentation in exporting Transformer/LLM models to ONNX. Yamini presented an overview of existing methods and the need to streamline the developer experience.
  - Current Export Pathways Identified:
    - torch.onnx.export: Generally used for simple Vision/NLP models. Less robust for complex LLMs.
    - Optimum ONNX (CLI): Relies on ONNX Runtime integration. Analysis by Nikita indicates missing ORT classes for some models.
    - Transformers Export with Static Cache: Currently used in ExecuTorch.
    - Transformers Export with Dynamic Cache:
      - Yuan/Xavier’s work mapping dynamic cache to a Concat op.
      - Implementation Detail: Requires wrapping the model to accept cache objects as input arguments.
      - Ti-Tai shared Justin’s [example code](https://github.com/justinchuby/pytorch-conference-2025/blob/c7073b660ffcbe40ce054ec6230b1c8de33c5e4a/demo/export_hf_model.py) regarding exporting quantized models and wrapping dynamic cache for torch.onnx.export
  - Native Transformers Export (POC): Yamini shared a [POC](https://github.com/huggingface/transformers/pull/41992) by Ilyas (Hugging Face) regarding native export capabilities directly within Transformers, bypassing Optimum

- Discussion: Infrastructure for Ahead-of-Time (AOT) Optimized Models
  - The discussion shifted to the architectural proposal of storing backend-specific, AOT-optimized graphs within a single ONNX model file.
  - The "Packager" vs. "Tool Update" Dilemma:
    - Rama raised a concern: How do existing ecosystem tools (optimizers, quantizers) handle this new multi-graph representation? Updating every tool to be aware of the new format is likely impractical.
    - Proposed Solution (The "Packager" Approach):
      - Tools should continue to operate on standard ONNX models.
      - A separate "Packager" tool (or infrastructure step) should be responsible for taking a standard model and "zipping" or injecting the optimized backend variants into the final artifact.
      - This treats the final model as a collection/package of variants rather than requiring a fundamental rewrite of upstream optimization tools.

- Discussion: Model Storage & Distribution
  - ONNX Model Zoo Migration:
    - Javier Confirmed that the ONNX Model Zoo is migrating to Hugging Face (Namespace: onnx-model-zoo) to solve bandwidth/LFS issues associated with GitHub.
  - Pre-Exported Models:
    - Yuan emphasized the value of storing successfully exported ONNX models in the Hub.
    - This allows users to simply download a working model (like a pip install experience) rather than fighting dependency conflicts to run the export script themselves.


