# Recording and Transcript:

https://zoom.us/rec/share/ZgK5OQxRDc8YD5obHRMMMVwRy7daTL5t90zK0742cCXEaH4s_fIOOrg4tOCxRi-G.Z2W99T-5kgy1t_ya

# Meeting Minutes

This week’s discussion is focused on the 3 breakout groups for operators, exporters, and backend specific representations. The slides from today’s discussion are [here](https://docs.google.com/presentation/d/1PYAHauEVhhdTuKMYiOsOjOVz6u8OzWka/edit?slide=id.g353238bb0c4_0_0#slide=id.g353238bb0c4_0_0). Below are the notes:

## Group #1 – Operators:
-	Contrib op Analysis:
    -	There are 112 ops in contrib op list today
    - We should identify some criteria to identify ops that can be standardized from contrib ops. Below are some suggestions:
      - Github issues or feature requests raised by community to support certain patterns or contrib ops
      - Customer usage
      - How models are represented in other frameworks and exported
-	The group reviewed ops in the [sheet](https://docs.google.com/spreadsheets/d/1JIykwXJEPT8FTLzvb0_5p_odvTYS9zzZjPNN33ziEbQ/edit?gid=0#gid=0)
-	Inputs from Kunal and Rama:
    -	Operator additions (e.g., rotary embedding, attention, RMSNorm) were based on model usage feedback within Microsoft.
    -	Flex attention is of interest and want to explore it for representing different attention variants
    -	Beam search and greedy search were initially added as contrib ops due to limitations in ONNX representation.
    -	Today, ONNX Runtime GenAI is preferred for generation loops rather than encoding them as static ONNX graphs. 
    -	Sid to analyze the search ops if they can benefit from ONNX representation and potentially backend acceleration.
    -	Paged Attention is also of interest, particularly to handle continuous batching requests. There is a PR for CUDA EP: https://github.com/microsoft/onnxruntime/pull/24595
-	Recommenders to add description in the column D of the sheet to the proposed operators
-	Max suggested introducing a special I/O concept in ONNX to mark tensors as reusable cache (e.g., for KV caching), avoiding separate input/output definitions and enabling more efficient memory handling that can help with stateful execution. This might not be an operator, could be an IR extension. It is documented in the sheet to track the idea

## Group #2 – Exporters:
-	Kshitij has been doing experiments to understand the status of pytorch exporter and observed that functions are not preserved with latest opsets. Many ONNX functions exist but aren’t seen in pytorch exported models
-	Rama mentioned that his team is working on pytorch exporter. Current exporter uses low-level ops, but work is ongoing to building fusion passes to detect and replace subgraphs with high-level ops like Attention.
-	Torchdynamo based onnx exporter will be prioritized going forward
-	Alex asked if the fusions are part of PyTorch exporter or ORT. Rama mentioned that the fusion logic lives in onnxscript and is not tied to ORT
-	Yamini asked if this group should be looking into this analysis as Rama’s team is already aware of the issues and looking into it. Rama welcomed more contributors to join and help accelerate the effort

## Group #3 – Backend representations:

-	The group briefly discussed about backend-specific representation and if we can use the EPContext design in a standard way
-	Max also suggested that we look into quantization representation as it is different for different backends
-	Yamini suggested the breakout group to come up with a proposal, do necessary experiments/POCs and present in 2 weeks

## Logistics:
-	Meeting will be extended to 45 mins going forward to allow more time for discussions
-	Below are the 3 channels for the breakout groups. Please feel free to join one or all of them and use those channels for discussion and exchange of ideas:
    - Breakout group for operators: https://lfaifoundation.slack.com/archives/C08QJA20HV1
    - Breakout group for exporters: https://lfaifoundation.slack.com/archives/C08QD56HLUD
    - Breakout group for backend representations: https://lfaifoundation.slack.com/archives/C08R47MGK16
