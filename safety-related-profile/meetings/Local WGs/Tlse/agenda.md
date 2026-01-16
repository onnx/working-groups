
 (Availability : use the [When2Meet](https://www.when2meet.com/?34146939-oceVQ))
 
 #### 2025/02/13 

*To be completed.*

#### 2025/02/04 

*To be completed.*

#### 2025/01/15
##### Agenda
- Case of max:min/maxpool with NaN: for all operators, try to rely on the spec of Max and Min. (Nota: I don't like the spec NaN > Inf > ... I think that we should treat NaN as a special case because NaN is no normally  comparable and here we are defining a comparison...)
- Processing of existing issues: see [issues tagged "TLSE WG"](https://github.com/users/ericjenn/projects/4/views/14))
  - Clip
  - Relu
- Sujet pour CEtIC
- Interesting links identified by Jean-Loup in ONNX:
  - https://onnx.ai/onnx/repo-docs/DimensionDenotation.html
  - https://onnx.ai/onnx/repo-docs/TypeDenotation.html
  - https://onnx.ai/onnx/repo-docs/MetadataProps.html
- Status of formal specification of CONV (Mariem)
- Discussion about SONNX event in late Feb / March
##### Minutes
- review of Clip
- review of Relu
- creation of Relu
- discussion about CETiC
  
##### Actions
##### New actions
  - [ ] (1501-1, Jean-Baptiste) Faire une proposition de contenu pour une soumission à  CETiC
  - [ ] (1501-2, Jean-Loup) Remove the relation NaN>Inf... and replace it by an explicit test for NaNs... 
  - [ ] (1501-3, ???) Introduce the term "Scalar" and (our) concept of "type" (numerical / value type) in the glossary. 
  - [X] (1501-4, eric Clarify the meaning of "heterogeneous" in ONNX
    - ONNX, heterogeneous seems to mean that the inputs can be of different types. But this is not the case. For instance, operator `Where` has "heterogeneous" arguments but, in ORT, `Where` requires the same types for `X` and `Y`. For example, one cannot mix an int32 tensor with a float tensor, or an int32 tensor with an int64 tensor. There is no type promotion.
    - Heterogeneous simply means that the operator is able to handle types that are both numeric and non numeric (for instance, integers and strings), but it does not mean that one specific instance of the operator in a graph can accept arguments of different types.  It seems to be an artifacts of the automatic documentation generation (according to ChatGPT), it is redundant with the notation "T", with T in {....}; it doesn't bring any additoinal information. 
    - BTW, note that, for  `Where` nothing is said about the fact that all tensor have to have the same type. This is implicit.
    - In addition, operator  `Add` is defined using the "T" notation that would imply that all argument must have the same type ((float,int) is rejected and so is (int32,int64)). 

  - [ ] (1501-5, ???) Clarify how we handle  value constraints for attributes
  - [X] (1501-6,Eric) Check the actual behavior of Relu and LeakyRelu in ONNX. Check if alpha can be negative.
    - Relu: input [-1.0, 0.0, 1.0, float("nan")] =>  [ 0.  0.  1. nan]
    - Leaky relu: [-1.0, 0.0, 1.0, float("nan")] =>  [nan  0.  1. nan] with alpha = NaN, as expected. Alpha can be negative and the value for X<0 becomes positive.
  - [ ] (1501-7,???) Update the informal spec guidelines (enforce usage of ONNX names and provision of denotation, use of generic types: "with int in (int8,int16,...)" )

##### Past actions
None.