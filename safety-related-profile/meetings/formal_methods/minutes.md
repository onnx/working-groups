# 2025/01/28

## Agenda
The objectives of the meeting are the following :
- Determine the approach for operators and graphs specification. On the basis of Loïc’s proposal:
    * Option 1: use C code
        * The reference implementation (in C) is the specification. Compliance of an implementation to this specification will be demonstrated by     testing with epsilon precision. No formal specification language (e.g., ACSL, Why3, etc.) is required.
    * Option 2: use Why3
        * O2.1:  Write a reference algorithm in Why3 (without loops). Compliance of an implementation to this specification will be demonstrated by testing with epsilon precision.
        * O2.2: O2.1 + Prove the correctness of the C reference implementation against the Why3 reference algorithm under the assumption F = ℝ
        * Algebraic Properties: Show some good algebraic properties of the reference algorithm in Why3 (in ℝ) (e.g., linearity, commutativity,     associativity, distributivity with respect to addition, existence of a neutral element, symmetry, etc.).
    * Option 3: use ACSL
      * Similar to the Why3 versions above, but using ACSL/Frama-C.
- Determine the formalism for operators specification     
- Determine the process/worksharing for developing the operator (starting with CONV)

## Participants
Edoardo, Loïc, Nicolas, Jean, Christophe Gar., Eric, Augustin, Mariem
## Minutes
This document summarizes the discussions and conclusions from our meeting on the specification approaches for ONNX operators and graphs.
### What is the purpose of the specification (ACSL or Why3)? What is the added value? Is the C reference algorithm not enough? (Eric)
(Loïc) It depends on our needs. If we only require tests, then the C implementation is sufficient. However, if we need proofs, we require a specification in a formal language.
The specification cannot be written in C. It should either be a reference implementation (in Coq, Why3, etc.) or a mathematical specification.
(Jean) ACSL specification is suitable for industrial purposes.
### What can we do with Why3 specification ?
- Generate C program
- Execute the Why3 specification
- Generate coq program
- Use it as input to ACSL
### What do we need to succeed with the Why3 specification?
  - Libraries such as matrices, algebraic signatures, logical signatures, etc.
### Is graph specification the same as operator specifications?
(Loïc) No, it is not the same. It is a separate subject and likely more complex than operator specifications.
The specification technique used for graph specification differs from that used for operator specifications, as we need to find a way to describe the graph.
### Conclusion on objectives 1 and 2
- We will use the Why3 specification approach. This involves implementing the reference algorithm of ONNX operators in Why3.
- From the Why3 implementation, it is possible to generate C programs and other implementations.
- This template can be integrated into Edge.
### How will we proceed with developing the reference operator (e.g., convolution or others)?
- We will organize a workshop in Toulouse in March. During this workshop, Loïc will provide all the necessary foundations and knowledge about Why3, and we will develop the reference operator together.
### Conclusion on objective 3
- We will implement the specification of the reference operator together during a workshop to be held in Toulouse in March.
- The date of the workshop is to be determined.

# 2024/11/29

## Agenda

The objective of the meeting is to answer the following quesiotns:
- Do we need a formal specification?
- For what purpose?
  - Documentation only?
  - Support to certification?
  - Implementation generation / implementation verification?
- Using which formal language?
- With what short-term objectives (PoC)?

## Participants

Dumitru, Nicolas, Christophe Gar., Mariem, Augustin, Jean, Eric [ed.]

## Minutes
- Supporting slides are available [here](./slides-29-11.pdf).

### Can the code be a specification?
- For some simple operators, the code may be a sufficient specification. For others, the code may be more complicated (e.g., broadcasting). The combination of the informal specificaiton and the code can be sufficient.
### How to trust the formal specification?
- If there is a strong proximity between the code and the formal specification (as in the case of `CONV`, for instance), proving that the code complies with the formal spec may be a plus but, still, the formal specification remains to be verified.
  - In our exercize on `CONV` we have actually "tested" the formal specification by verifying that some simple code for which we knew *a priori* the expected result complied with the specification...
  - The formal spec may be reviewed, but it woiuld be nice to leverage on the fact that it is formal to verify that the spec satisfies some basic properties (for instance, the convolution of M and somewhell chosen F returns M).  
  - This kind of verification of the formal spec is a usual practice of people using formal verification. 
  - See e.g., work of [Basile Clément](https://basile.clement.pm/thesis.html)
  - Trying to prove "false" is one typical smoke test (there are others). Care shall be taken that the proof actually ends: it is times-out, what is the conclusion?
  - [ ] (Loïc) how do you proceed to verify the spec ('smoke test')?
  - [ ] (all) What coud be those properties for the type of operators we are dealing with?
  - This effort could be done once and delivered as a library...
### The multiple uses of formal specification
- The formal specification may be useful in different ways:
  - The formal specification may be directly used to prove the end-user's implementation. 
    - In that case, the choice of the formalism is very important since it must support th verification tool (otherwise, the specification will have to be translated)?
    - This scenario will probably be very rare (end-users doing formal verification are pretty rare, and they use these techniques for th most critical apps...)
  - The formal specification may be used to verify (prove) the reference implementation that will be used by the developper to test his/her own implementation. *This is what we plan to do...*
  - The formal specification  may be used by the developer as the implementation specification. In that case, the formal specification must be readable, understandable. 
### On the complexity of the proofs
- Proving operators with many loops is not that trivial (loop invariants must be written) but seems feasible, at least in $R$ and for some operators. When floating point number are used, the effort may be much greater, possibly requiring the use of other, specific tools (e.g., fluctuat). 
- Experiences on other types of operations (on quaternions) show that formal verification it may become quite complex...
- Note that we have not done proved complianc ot the `CONV` code to its ACSL specification
- [ ] (IRT) Complete the proof with the help of CEA...
- In any case, formal proof of a complete graph is out of reach (but htis is not our objective).
### On the specification of the graph execution
- What about reccurrent networks? 
  - Those network can be handled by managing the state out of the graph or by using dedicated operators (e.g; LSTM).
  - In any case, handling recurrent networks remaijns a matter of executing operators in the correct order. It does not make the specification of the graph execution more complex. The semantic of the graph execution remains the same and is simple. 
- [ ] (Eric) Ask Loïc if doing proofs on graphs (acyclic graph) is feasible with ACSL? With what effort?
- [ ] (Augustin) See with Virgile is FramaC has some specific capability ("greffon" suchas AORAI...) to handle this. 
### On the question of floating point numbers and accuracy
- This problem was briefly addressed. The accuracy of basic operators (e.g., $log$) shows to be extremely variable. 
- Verification of floating point operations is complex and may not scale up. 
- [ ] (Augustin) Ask Franck what he thinks about our problem... 
- This raises the remaining question of the specification of accuracy.
- We could specify the operator in $R$. But in that case, the proof will be incomplete: the code will be proved to be correct when using real numbers, but nothing can be said about the same operation manipulating floating points...
- The strategy of AI is to combine formal proof with verification with the use of Fluctuat to handle floating point computations. 
-  [ ] (All) Problem of floating point number remains to be addressed...
-  [ ] (Eric) See work of Pierre Roux at ONERA
### On the ONNX format
- An ONNX file is written according to a syntax defined in the standard. The syntax could be "formally" defined by a grammar. But the semantic of a given text written in this language must be defined to.  For instance, if we define formally what is a graph, we have to express formally how a given part of the ONNX file translates to a graph.
- [ ] (all) Formal specification of the file format to be investigated (secondry subject)
### On the choice of the formalism
- We have to chose a formalism for we we have the skill at hand, that is not too complicated and, if possible, that is already familiar to end-users.
- ACSL seems to be the right choice.
  - If someone uses another formal language, s/he will haev to do the translation.
- The `CONV` example uses a flattened representation of arrays, which makes it difficult to read and match with the informal spec. TThis has been done because we started with a flattened representation in Why3. It should be rewritten so as to use multidimentional arrays.
### On the "reasonable effort"
- Formal methods are not used by all industrialists. So, we have to be reasonnable (in SONNX) about the effort that we will spend on that spect of the problem. It is likely that covering informally a large set of operators will be a more better results (for most end users) than formally specifying a very small set of operators... 
