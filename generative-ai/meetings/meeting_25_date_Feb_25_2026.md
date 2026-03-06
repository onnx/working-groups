# Recording and Transcript:

https://zoom.us/rec/share/gGd3eNPl3h50qnYwktPSf6hoxPbDvm3nhuqDWaruk-Hw4pZ_JnX4BqmJKYI1SU03.ccAEP0X-NUdMfBKd

# Meeting Minutes:

## FlexAttention Operator Progress
- Review Status: Rama has reviewed Masahiro’s updates on the [Flex Attention PR](https://github.com/onnx/onnx/pull/7534). The subgraphs have been updated to use whole-tensor updates as previously requested.
- Next Steps:
  - Group to review the latest commits and provide any further comments to accelerate merging the PR
  - Once merged, the group plans to test the operator using ONNX Runtime with MLAS and other backends. This can be a follow up Github issue to encourage opensource contributions from the community
  - For initial performance and functionality testing,  the models can be custom built with Flex Attention operator in lieu of automatically exporting it as part of the PyTorch to ONNX export.

## ONNX Export and Quantization:
- Hugging Face is currently reviewing Xavier’s proposal regarding optimum-onnx integration and will share their feedback soon
- The group discussed how GGML interleaves weights and scales for better CPU dequantization performance (fetching blocks with scales at the end).
- Current ONNX standards store weights and scales separately, which is better for GPUs/NPUs. The group debated whether ONNX should support "Package of Model Variants" to allow different layouts for different hardware targets.

## Ternary Storage & Compression
- Soumendu presented trade-offs for packing ternary values (5 values into 1 byte) at different granularities as part of Ternary storage proposal ([paper](https://drive.google.com/file/d/1oeHVpCygJ9XlWKChB5e1tCWVFil9j9gY/view?usp=drive_link), [presentation](https://drive.google.com/file/d/1ofjAkMWh0XEXm2WauN1CLSwNF49kpMwb/view?usp=drive_link)).
  - Per Block (128): Approximately 1.5% wastage. This approach works well for localized reading but introduces a small overhead.
  - Per Channel: Lower wastage overall, with unused space appearing only at the end of the output channel.
  - Per Tensor: Minimal wastage and the highest compression efficiency, but it is the most difficult approach when partial decompression is required.
- Rama suggested leaving the choice to the user via parameters in the Proto rather than hardcoding a single strategy.
- Action Item: Soumendu will create the RFC and complete data analysis on layer dimensions to see actual compression gains.

## Backend Context Proposal
Javier reintroduced the proposal for Equivalent Subgraphs/Backend Context.
- Goal: Define an ahead-of-time (AOT) caching representation that is target-dependent but retains the original ONNX graph. This allows backends to perform inference without being locked into the specific compiler used during the AOT flow.
-	The group discussed and agreed on using the GenAI WG to continue the discussion to leverage the existing GenAI WG channels and attendee inputs for refining the proposal. To facilitate driving the meetings, Javier will co-chair the GenAI WG going forward. Meeting times and logistics will be worked out to accommodate cross-Geo participants. 
  
