# Communications

### On the working group activities 
- ERTS 2026 (Toulouse) [with paper]
	- Feedback: 
		- Positive feedback from EASA who's willing to help...
- CETIC 2026 (Toulouse) [presentation]
	- Feedback: Positive feedback from EASA who's willing to help...
- ONNX Meetup [presentation]
	- Feedback: Need tighter collaboration with ONNX core teams (e.g., operators)
- DATE 2026 (Verona) [presentation]

Absolutely **no** effect on the size of the working group...

### On formal specification and verification
- SAIV 2026
- OVERLAY 2026 

Absolutely **no** effect on the size of the working group...

# The results of the working group
### Documents

#### Input documents

- [Issues](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/deliverables/issues/issues.md)
	- *Obsolete*
	- No systematic analysis.
	- Some problems identified during the specification / test work, not reported.
- [Needs](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/deliverables/needs/needs.md)
	- *To be updated. (if useful...)*
- [Requirements](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/deliverables/reqs/reqs.md)
	- *To be updated. (if useful...)*
- [Scope](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/deliverables/scope/scope.md) 
	- *To be updated (if useful...)*

- Compliance with standards 
	- No real document... 
	- Probably to be done against the latest versions of the concept paper and ARP.

### Guidelines
- [Informal spec guidelines ]()
	- OK: reviewed and corrected.
- [Formal spec guidelines]()
	- OK: reviewed and corrected (to be completed)
- [Implementation guidelines (user manual)]()
	- *Draft*
- [Numerical analysis guidelines]()
	- Reviewed and corrected
- [Testing guidelines]()
	- *Draft, to be completed, consolidated, reviewed*

### Informal spec

| Backlog  | Dev in prog | Rdy for rew.       | Rev in progress | Rew Complete | Corr. in prog. | Corr. completed | Completed |
| -------- | ----------- | ------------------ | --------------- | ------------ | -------------- | --------------- | --------- |
| Sub      | Conv        | ConvInteger        |                 | Pow          | Relu           | Unsqueeze       | Tanh      |
| Neg      | Concat      | BatchNormalization |                 | SoftMax      | Slide          |                 | Clip      |
| Constant |             | ArgMax             |                 |              | Mul            |                 | Flatten   |
| Gemm     |             | MatMul             |                 |              | Add            |                 | Div       |
| Lstm     |             |                    |                 |              | Broadcast      |                 | Max       |
| Pad      |             |                    |                 |              | Where          |                 | Sigmoid   |
|          |             |                    |                 |              | MaxPool        |                 | Sqrt      |

### Formal spec

| Backlog   | Dev in prog     | Rdy for rev.       | Rev. in progress | Rev. Complete | Corr. in prog. | Corr. completed | Completed |
| --------- | --------------- | ------------------ | ---------------- | ------------- | -------------- | --------------- | --------- |
| Broadcast | Add             | Flatten            |                  |               |                |                 |           |
| MaxPool   | Concat          | Mul                |                  |               |                |                 |           |
|           | [ Graph]        | BatchNormalization |                  |               |                |                 |           |
|           | Leakyrelu       | Conv               |                  |               |                |                 |           |
|           | Shape           |                    |                  |               |                |                 |           |
|           | Range           |                    |                  |               |                |                 |           |
|           | Squeeze         |                    |                  |               |                |                 |           |
|           | Where           |                    |                  |               |                |                 |           |
|           | [Ctensor (int)] |                    |                  |               |                |                 |           |
|           | ConInteger      |                    |                  |               |                |                 |           |

### Tests

|         |             |              |                 |              |                |                 |           |
| ------- | ----------- | ------------ | --------------- | ------------ | -------------- | --------------- | --------- |
| Backlog | Dev in prog | Rdy for rew. | Rev in progress | Rew Complete | Corr. in prog. | Corr. completed | Completed |
|         | Slice       | Flatten      |                 |              |                |                 |           |
|         | Conv        | Unsqueeze    |                 |              |                |                 |           |
|         | Conct       | Clip         |                 |              |                |                 |           |
|         |             | Shape        |                 |              |                |                 |           |
|         |             | Range        |                 |              |                |                 |           |

### C implementation

Kanban seems empty...
Mandatory for AI!

### Num accuracy

Kanban seems empty...

### Integration

- Status of integration in AIDGE

### Full examples
- MNIST
- Tiny YOLO V2

# Roadmap

#### What is going on?...
- On-going work on a subset of operator useful for Airbus (funded by Airbus...) 

#### What remains to be done?
- On informal spec
	- *Complete coverage of the target set (see previous table)*
	- Most informal specs needs to be aligned with the latest version of the guidelines.
	- Complete informal spec of graph execution for "control flow" operators \[non critical\]
- On formal spec 
	- *Complete coverage of the target set (see previous table)*
- On implementation?
	- *Complete coverage of the target set (see previous table)*
- On numerical analysis?
	- To be discussed with Franck.

#### What are the priorities?
- What are the most important / most urgent expectations?
- Favour a "breadth-first" approach against a "depth-first" approach?
	- For instance 
		1. Informal spec.
		2. Testing.
		3. Formal spec.
		4. Implementation.

#### The usual question: actions to stimulate participations?
- Show our current results? 
	- Opportunity : proposal for a workshop in Paris or Toulouse, see next point
- Ask companies to contribute via internships ?
	- Revealed to be EXTREMELY efficient (João and Ricardo funded by Critical Software (thanks to them!) 
		- João and Ricardo hired by Critical SW (possibility to contribute to SONNX?) 
### Other questions / topics 
- Should we involve our new silicon friends?
	- We have sufficient "good" example to ask some agentic system to work (at least) on the informal (possibly formal...) simple operators... 
	- We could also use them to generate tests...