
 (Availability : use the [When2Meet](https://www.when2meet.com/?34146939-oceVQ))
 
 #### 2025/02/13 

*To be completed.*

#### 2025/02/04 

*To be completed.*

#### 2025/01/15
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
##### Actions
  - [ ] (1501-1, Jean-Baptiste) Faire une proposition de contenu pour une soumission à  CETiC
  - [ ] (1501-2, Jean-Loup) Remove the relation NaN>Inf... and replace it by an explicit test for NaNs... 
  - [ ] (1501-3, ???) Introduce the term "Scalar" in the glossary. 
  - [ ] (1501-4, ???) Clarify the meaning of "heterogeneous" in ONNX
  - [ ] (1501-5, ???) Clarify how we handle  value constraints for attributes
  - [ ] (1501-6,Eric) Check the actual behavior of Relu and LeakyRelu in ONNX. Check if alpha can be negative.
  - [ ] (1501-7,???) Update the informal spec guidelines (enforce usage of ONNX names and provision of denotation, use of generic types: "with int in (int8,int16,...)" )