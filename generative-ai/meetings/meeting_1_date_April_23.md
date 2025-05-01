# Recording and Transcript:

https://zoom.us/rec/share/UmJO9yfv2ZzMt2lnG0VKP59SsHnLwR_yA-0ybOw3N4Tv5XYxvG-TSPsENJC8-LX0.ZzyJp4IihZYLZ4FF

# Meeting Minutes:

- Continued from last week's overview of the working group's scope; this session focused on diving deeper, identifying actionable items, and considering breakout groups. The material shared in the meeting can be found [here](https://docs.google.com/presentation/d/1PYAHauEVhhdTuKMYiOsOjOVz6u8OzWka/edit?slide=id.g34f6d699a61_0_0#slide=id.g34f6d699a61_0_0): 

## ONNX operators/functions:
- Preference is to define operations as functions rather than operators when they can be composed from existing primitives
- Nested functions are supported in ONNX (as long as there's no recursion), allowing functions to use other function-based ops
- There's limited usage of ONNX functions in practice today; need to improve adoption via exporters and tools like Optimum or ModelBuilder
- Need to discuss how function usage can be preserved in exported graphs so that backends can recognize and optimize them instead of seeing expanded subgraphs – this doesn’t seem to be the case today
- There was a discussion about FlexAttention and whether we can use it in ONNX to represent different attention variants. Rama mentioned that it is more complex than traditional attention and behaves like a higher-order operator and needs some sort of control flow
- Yamini proposed to develop PoCs that express different attention variants using FlexAttention to evaluate feasibility

## Contrib ops:
- There is interest in standardizing commonly used contrib ops as ONNX functions. There's a need for better documentation and tooling around contrib ops. The best way to understand the implementation is to check the code
- Shubham raised a PR to implement the SkipLayerNormalization, but there were concerns expressed by Yuan about whether this was intended for fusion pattern and where to draw the line between adding genuinely useful patterns vs. overloading the spec with too many function ops
- Proposal to review common contrib ops and select candidates to elevate to standardized ONNX functions or operators

## Backend-specific representations:
- Can we include optimized subgraphs or precompiled blobs in an ONNX model while keeping it hardware-agnostic?
- One idea: use model-local functions to define backend-specific function variants, allowing each backend to select its optimized version
- This enables ahead-of-time (AOT) compilation without turning the model into a hardware-specific blob
- Shared weights should be referenced, not duplicated, across backend-specific functions to avoid bloating
- Suggestion to introduce a generalized version of ONNX Runtime’s EP context nodes, which can bundle custom logic and refer to shared weights
- For quantized models, QDQ pattern matching must be performed before function inlining to preserve valid quantization patterns
- Cleaner approach: allow function definitions to include QDQ variants as attributes, enabling the inliner to insert them properly

## Proposed Breakout groups:
- Group #1: Identify, define, and implement new ONNX functions from popular models, contrib ops, GenAI pipelines
- Group #2: Analyze the current state of model exporters. Identify gaps and implement better function usage in exporters
- Group #3: Define backend specific representations to support aot compilation, weight sharing, structured function inlining etc.

Please let Yamini know if you are interested in participating in the above breakout groups and how you would like to contribute
