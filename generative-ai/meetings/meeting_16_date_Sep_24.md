# Recording and Transcript:

https://zoom.us/rec/share/sKanBtKN5fqsFTdjJDcPxTBhsX-q9w67bL7YISOr2VYmH1CJDsbAIFZ10WYLXRY_.0gAy2ha54YQNxvEi

# Meeting Minutes

##	Recap of Previous Discussion
- Prior meeting covered paged attention proposal and Mixture of Experts (MoE).
- Yamini drafted a proposal for paged attention building on Yuan’s Attention updates.
- Discussion centered on attention op updates, flex attention, and the need for graph attributes.
- Quantization settled on static attributes, but flex attention and MoE may require graph attributes.

## Experimental Domain Proposal
- Previous discussion suggested an experimental domain to iterate quickly without disrupting standard ops.
- Rama confirmed that experimental domain already exists and can be used for this purpose.

##	Graph Attributes Discussion
-	Pros: Allow flexible expression of new attention variants and MoE.
-	Cons: Make handwritten kernel optimizations harder; backends may struggle with efficient implementation.
-	Possible solution:
  -	Use graph attributes only for special cases (not common ones like SDPA).
  -	Backend could either map to subgraphs (standard ops like matmul, softmax) or generate indirect functions (C++-style float-to-float transformations).

## Implementation Considerations
-	Backends could unpack graphs into primitive ops when fused kernels are unavailable.
-	Concern about defining specs before proving backend feasibility—suggested prototyping implementations first.
-	Need experimentation to validate backend support before standardization.
-	Backend/Runtime Support
  -	Krishna asked about minimum criteria for new ops in experimental domain—should CPU/MLAS backend support be mandatory? 
  - Open question: Is ONNX Runtime implementation required for adoption, or is spec + experimental domain sufficient?

## Action Items / Next Steps
-	Group to consider prototyping flex attention/MoE with experimental domain before standardization. Yamini to put together a proposal for open source/hackathon contributions for these ops
