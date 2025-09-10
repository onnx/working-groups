# Recording and Transcript:

https://zoom.us/rec/share/Hja3nYupbj42sfdvCh_vgnj60dTHg0EF0UpOKsk-yIfKXWXcnXw3mnCG19ALbM_y.fHNg9eHiq_5xOCzy

# Meeting Minutes:

This meeting covered updates on the attention operator, the design of a Mixture of Experts (MOE) operator, and paged attention. The group also agreed to change the meeting frequency to bi-weekly.

## Attention & MOE Operators
- The discussion began with the status of the attention operator updates, specifically the proposal to use subgraph attributes. Yuan noted this was not included in the last release due to concerns about backend compiler complexity and a lack of consensus on its necessity for quantization.
- Kunal suggested that the upcoming Mixture of Experts (MOE) operator should also use a subgraph approach, similar to the "flex attention" proposal. This would provide the flexibility to handle the many variations of MOE and future-proof the operator. 
- The consensus was that the design approach for the MOE op should be consistent with the final decision made for the attention op.
- Next Step: The discussion on subgraphs for both attention and MOE operators to be continued in the next meeting when Rama returns from vacation.

## Paged Attention
Yamini presented her initial research on creating a paged attention operator ([Link to the document](https://docs.google.com/document/d/1v8vdeAldERsuQTziYhM9pzJBxoyq58fa)). Key points included:
- Different KV Cache Layout: Unlike regular attention which uses contiguous tensors, paged attention uses a non-contiguous paged memory layout for the KV cache.
- New Inputs: It requires additional inputs, most importantly a KV page table to map logical to physical memory blocks. This is typically managed by a higher-level framework like vLLM.
- Implementation Strategy: A central question was whether to create a new operator or to modify the existing attention op. Alexandre suggested using annotations to signal to the compiler that the inputs are paged, and Yuan proposed creating an experimental namespace to test new operators like this before standardization.
- Next Step: Yamini will share her research document on paged attention ([Link to the document](https://docs.google.com/document/d/1v8vdeAldERsuQTziYhM9pzJBxoyq58fa)). The team will continue to study different variants to develop a generalized representation.

## Meeting Schedule
The team agreed to change the meeting cadence from weekly to bi-weekly to allow more time for progress between discussions. 
