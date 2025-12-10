# Recording and Transcript:

https://zoom.us/rec/share/KYsNy6m4LD7iPuIxpbz2pXPnfLelIhAPBRRh9cHiT6sNU9TYq6yHxLWhY310vzMd.gefPlL0bBBcjzxdx

# Meeting Minutes:

## Mixture of Experts (MOE)
- The team is looking to define a standard representation for MOE models. Kunal shared a [paper](https://arxiv.org/pdf/2503.07137) suggesting a general flow that could serve as a base, with specific variations handled as attributes.
- Action Item: The group will review the paper to discuss it further in the next meeting.

## Paged Attention
- The central question was whether paged attention could be a backend-only implementation or if it required model-level changes. The group concluded that because paged attention requires additional inputs like block_tables, the ONNX model's signature must be modified. This means the application layer needs to be aware of the change, and it cannot be hidden as a simple backend graph transformation.
  - The team noted that this technique is valuable not just for data centers but also for client devices to optimize memory.
  - The team discussed that while frameworks like VLLM handle this in PyTorch, having a clear path for ONNX is important.
  - Yamini suggested that investigating the existing Flex Attention operator might be a viable path to supporting paged attention.
- Action Items: Yamini will investigate how Flex Attention maps to paged attention and research how PyTorch models handle the modified inputs. 

## GenAI Text-to-Image Interface
-	A new [text-to-image interface](https://github.com/onnx/working-groups/blob/main/generative-ai/genai-interfaces/include/pipelines/text2image_pipeline.hpp) has been added to the ongoing GenAI interfaces POC.
-	Action Item: The team to review the new interface and provide feedback.

## Backend Context for AOT Optimizations
- The team continued the discussion on [ONNX Backend Context](https://docs.google.com/presentation/d/1oPgfK2qvuYsOa4_eT0bsiwV96eI66rsH) and explored how to save ahead-of-time (AOT) compiled optimizations for different backends within an ONNX model. The key requirement is to preserve the original, standard graph as a fallback. Two main proposals were compared:
  - Graph Modification (EP Context style): This involves replacing a subgraph with a new, single operator node that holds the pre-compiled "blob" for a specific backend. The main drawback is that this creates multiple versions of the graph, which can become combinatorially complex and loses the original graph information for fallback.
  - Metadata Annotation: This approach keeps the original graph structure intact and adds metadata that "scopes" or groups nodes, associating them with a pre-compiled blob for a specific backend. The team thought of it as a cleaner approach, avoiding graph duplication, and supporting a fallback mechanism if the compiled blob fails.
- Action Items: Javier will work with Yamini to define a proof-of-concept (POC) demonstrating the metadata-based approach. This POC will help the team understand the practical challenges, such as handling data formats between optimized blocks and defining the metadata structure, before finalizing a proposal.

