
<img src="https://github.com/user-attachments/assets/c3204542-6453-44ae-86fb-76d5db61be8e" alt="drawing" width="200"/>

## Glossary:
- MLMD: Machine Learning Model Description
- MLMID: Machine Learning model Implementation Description

## Definitions: 
- ML MODEL: Model characterized by parameters determined by a data-driven training process to perform one or more
specific functions.
- ML constituent: An AI/ML Constituent is a collection of hardware and/or software items (including the necessary pre- and post-processing elements), and at least one specialized hardware or software item containing one (or several) ML Model(s). (see ARP, p.7).

## Elements:
- The MLDL is the input of the ML items implementation process.
	- The (MLMD, ML constituent requirements, test dataset) are the inputs of the implementation phase (see ARP, Figure 20).
	- The MLMD only covers processings expressed using the ML graph. (pre- and post-processing are done by non-ML contituents)

_There is no clear definition of the MLMD besides the implicit one for which the MLMD is "the decription of the ML model that is necessary to implement the inference process". Note that in the glossary, the entry for MLMD is "TBD"_

- Verification activities of the MLMD are listed in §6.8.1.5:
	- ML Model Description is complete, correct, and consistent.
	- ML Model Description is traceable to ML Model. <<Nothing prevents the ML model and the MLMD to be expressed using the same language. If someone writes his model using (e.g.) PyTorch, is the Pytorch code "the ML model"? If yes, shall traceability be done with respect to the Pytorch code? Shall we provide a tool to trace the SONNX model elements to the Pytorch lines of code?>> 
	- ML Model additional information is complete, correct, and consistent. <<What is this "additional information?>>	
	- ML Model Description, ML Data processing description, and ML Model additional information are consistent.

_There is no constraints about the performance "achieved by" the MLMD (i.e., the performance that would be achieved by some perfect implementation of the MLMD. The only verification objective relating the ML model and the MLMD concerns "traceability" and "consistency"._

_Nothing is said about the evaluation of the performance of the ML model. This evaluation may depend on the execution target (a desktop PC, a desktop PC with a GPU, a computer in the cloud) and framework. If the actual (measured) performance of the ML model (during the design phase) is a requirement, the measurement process should be defined precisely._

- The SONNX standard defines the language in which the MLMD is expressed. 
	- SONNX is an "extension" of the ONNX standard. 
		- ONNX has ** not ** been targeted towards safety critical applications. 
		- SONNX is aimed at completing the ONNX standard to address concerns of safety-related systems. 
	- SONNX shall define the constructs (operators, graph) and the semantics of those constructs. 
		- A SONNX MLMD shall give a non ambiguous functional specification of the constructs.
			- This definition is necessary both to ensure that developper will be able to implement the model correctly, and to 
			- It may also capture derrived requirements such as the explicit ordering of operators when the ordering imposed by the dataflow semantics is not unique.
			- The specification of operators is purely functional. 
				- For a given operator, it describes what the operator shall do. 
					- In some cases, the specification may be operational and describe how to calculate the result. But this shall normaly not preclude other implementations as long as the computed results are identical.
						- "Identity" of results may be achievable when considering mathematical abstractions such as "exact" operations performed on Real numbers. But in most cases, this cannot be achieved, even if the operational description of the algorithm is followed scruptuously. 
							- This means that an actual implementation may produce results that are "slightly" different from those that would be produced by a mathematically strictly exact implementation. 
							- The correctness criterion must be expressed by a maximal acceptable error. 
								- This could be part of the MLMD specification (i.e., the implementer is allowed to produce an implementation that is epsilon-off to the mathematically exact value.
									- In some cases, it may be impossible to formally estimate the actual value of epsilon. in that case, epsilon may be estimated by testing and comparing the result of the implementation with the one of the reference implementation.
										- But the error of the reference implementation with respect to the exact implementation must itself be estimated... 
					- In some cases, the implementation may be requested to striclty follow the operational specification (not in terms of results, but in terms of oeprations). 
						- This is a derived requirement that shall be captured explicitly
					
	- SONNX shall facilitate development and verification activities (possibly by introducing specific annotations)
		
- "The performance of the MLMD is verified against the test dataset on the target environment" (ARP)
	- To do this verification, we need to interpret (or "execute") the model for a given set of inputs. 
	- We have to provide everything that is necessary to do this interpretation.
		- This includes: 
			- an ** executable specification ** of the operators, of the graph,
			- a specification or a clear designation of the interpretation infrastructure (including the compiler, the libraries, if any, and target machine).
		- This executable specification is what we call a "reference implementation"
			- There is an existing ONNX reference implementation, but (as indicated by ONNX), it is incomplete.
		- The reference implementation shall be 
			- simple enough to facilitate its implementation / verification. 
			- demonstrated to comply with the SONNX semantics

- Several properties (stability, robustness,...) shall be verified during the MLDL part of the process (see §6 of the ARP).
	- If we want to take credit of these verifications (do we?), we have to demonstrate that those properties are preserved throughout the implementation process. 
		- Are the element determining those properties captured by the MLMD? (if not, this means that the MLMD cannot carry the constraints about those properties). If not, what should be added? 

- A MLMD is transformed into one or several MLMIDs.

- The MLMID shall be demonstrated to comply with the MLMD. 
	- This can be achieved 
		- by testing the MLMID on the test dataset and showing that the performances are the same as for the MLMD
		- by demonstrating that the MLMID correctly implements the MLMD (by testing)
		
- We have to demonstrate that the MLMID is traceable to the MLMD. This may be achieved by providing an MLMD to MLMID mapping. 
	- If optimizations (e.g., fusion,...) are performed during the transformation process, those transformations shall be described so as to restore traceability (i.e., prove that the preservation of the semantics). 
	- In the simplest case, each operator in the implementation can be traced directly to an operator in the MLMD. In the ARP, parts of the model to be mapped to a specific target is called a "ML model (logical) elements". Several "logical elements" may be deployed on the same HW target. Therefore, one MLMID may concern several logical elements.


- We have to demonstrate that the "combination of MLMIDs semantics reproduces the semantic of MLMD without introducing new of unexpected behaviours".
	- Verification will (usually) be done using testing, which means that the MLMD must be interpretale (or "executable"). 

- Ensuring this property can be done by construction, for instance by introducing derived requirements about, e.g., the execution sequencing and verfying that these requirements are actually applied, and/or by verification.

- The derived requirements for one MLMID are captured in the MLPADR. 

- One MLMID specifies one SW item.
  
- Derived requirements may be added during the refinement process. We may want those requirements to be captured by the SONNX profile. For instance, the mapping of parts of the MLMD to targets may be captured thanks to dedicated annotations. 







