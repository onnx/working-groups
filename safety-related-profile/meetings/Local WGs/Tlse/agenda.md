
 (Availability : use the [When2Meet](https://www.when2meet.com/?34146939-oceVQ))
 
#### 2025/02/27 

##### Agenda
- Review of actions 
- Operators: [MaxPool](../../../sonnx/ops/spec/informal/maxpool/maxpool.md) and [Pow](../../../sonnx/ops/spec/informal/pow/pow.md).
- Accuracy: check the accuracy analysis of [div](../../../sonnx/ops/spec/informal/div/div_acc.md) and [tanh](../../../sonnx/ops/spec/informal/tanh/tanh_acc.md). See Franck's mail dated 2026/02/13.
- (Re-)discussion about using composition when defining complex operator. The case of **Conv**.
- Testing
  - Shouldn't our reference implementation be using multiple precision (e.g., mpfr)? 
  
##### Minutes
- Reviewed: **Maxpool**, **Where**, **Pow**
- About **Pow**
  - The specification currently imposes no restriction and goes beyond what is required by IEEE. 
- [ ] Review **Pow** against IEEE 754
- [ ] Restrict **Pwo** to match IEEE's spec of Pow.
- About formal specification and verification
  - Might be wise to limit format specification and proof to "complex" operators (and the graph semantics), especially the structural ones that make complex (hence error prone) manipulations of indexes.
- [ ] Propose a restriction for the format specification and verification effort (at least in a first phase)


#### 2025/02/13
##### Agenda
No agenda defined...

##### Minutes 
- Travail sur **LeakyRelu**, **Max**, **Sigmoid**,  **Sqrt**, **Exp**, **Log**

- [X] Complete the disclaimer about tests and place emphasis on the last sentence (the rest being more methodological)
  - (Eric) Done. 
- [X In the set of "basic mathematical operators" that , remove the inverse trigonometric functions
  - (Eric) Done.
- [ ] Check if, in the real domain, we use "$=\pm \infty$" without saying that it is a limit.
- [ ] Check that the sections of the spec are always ordered as follows: Real, Float, Int  
- [ ] Introduce broadcasting for all operators that support it. 
    - (Eric) The other solution is to specify what is broadcasting and simply indicate, for a given operator, if it supports broadcasting or not. The effect of broadcasting on the operator can be explained once for all (see e.g., what has been done for **Max**).
- [ ] Checks that all hyperlinks are relative (i.e., they shall not point to the current repo / branch)
- [X] Introduce the IEEE special values in the definition section. In particular, define "+0", "-0"
    - (Eric) Done.
    - I think that a brief section about FP number would be worthwhile (with appropriate references to the standard and to the well-known "What Every Computer Scientist...") ) 
- [X] When 0 is actually "+0", use "+0". "0" must be used either as the usual 0, or as "+0" or "-0".
  - (eric) Added in [notations](../../../sonnx/ops/spec/informal/common/notations.md).
- [ ] Check the behaviour of **Max** for NaNs
- [ ] Check **Max** for "-0".
- [ ] Check all integer operators against overflow conditions
- [X] In the definition section, introduce the constants `minfloat16`, `maxfloat16`, etc. that are used (e.g.,) in the specification of **Exp**.
  - (Eric) Added in [definitions](../../../sonnx/ops/spec/informal/common/definitions.md).


#### 2025/02/04 
- Feedback on strange observations on $MaxPool$ and code analysis. (30 min max)
- Proposal of guidelines modifications to factorize restrictions and constraints. 
- Discussion (1h max) about the specification of ops in FP. 
  - What do we need exactly?
  - Specification *vs.* implementation... Up to what point shall we be prescriptive wrt the implementation?
  - Paper pointed out by Jean-Loup "Make it Real: Effective Floating Point Reasoning via Exact Arithmetic"
  - The question of accuracy...
- Review of [Max](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/max/max.md), [Range](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/range/range.md), [Div](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/div/div.md)?

#### Minutes

##### Updates to the guidelines
- The section about attributes must be described only once, in the subsection about reals. The other sections (for the other types) must simply refer to it and express other specific constraint is necessary.
- The same applies to constraints: as far as they are not specific to a certain data type, they will not be restated, but simply refered to by an hyperlink. See the example of $Maxpool$.  
- About constraints : 
	- We add a line about the "general constraints" for all operators. We do not specify precisely which of those constraints are actually applicable. This is up to the user to check...
- [X] Include factorizations of attributes and constraints and the sentence about general constraints in the guidelines and template
    - Added in the guidelines (Eric)

##### Update to preamble / lexicon etc.
- Introduce a "preamble" / "introduction" that will express some important general information and disclaimers
	- Tests are provided to support the validation of the specification and the verification of a given implementation against the reference implementation. However:
		- They only cover functional tests (they do not cover implementation) 
		- They are not aimed at being exhaustive and do not substitute to applicable practices in the domain of use (e.g., aeronautics...)

##### Mathematical operators
- The specification is defined using the operators in R (in particular).
- A specific implementation (the one that we will actually generate) may be described in the "Accuracy" section in order to support the accuracy analysis. In that case, the operators will not be those in R but thos ein F. So we will use (e.g., "+." to express the addition in F).
- The specification will be written using a certain set of "basic" operator that will nt be defined any further. This includes at least `+`, `-`, `*`, `/`, `exp`, `sin`, etc.  They have to be defined in the "preamble" or "introduction" to SONNX.
- [X] Define the set of basic operators in the SONNX introduction
  - Added in the guidelines (Eric)
- The operator shall be specified for all special values (infs, +/-0, and NaN). 
	- This may be expressed using "if" clauses that will specify the behavior for those specific values, or using some general, informal sentence covering thoses cases. The point is that the behaviour of the operator must be covered for all these special values.
- [X] Check if infs ($\pm \infty$) belong to set the of real numbers
  - Infinities are **not** real numbers (simply R is a field, an infs do not satisfy the law of fields, think about the addition of infinities). $R$  only contains finite numbers (excluding infinities).  Infinities are introduced in the "extended real number system".  See [here]([Rudin W. Principles of Mathematical Analysis 3ed](https://david92jackson.neocities.org/images/Principles_of_Mathematical_Analysis-Rudin.pdf)).   
- (off meeting : if it is the case, then we will have to define what +inf (- | / ) -inf means exactly in R...)...
- [ ] In the section about accuracy, clarify the purpose of the analysis (methodological)  
- [X] In the examples, use $\approx$ instead of $=$ when applicable 
  - Added in the guidelines (eric)
- [X] The jupyter notebook used to compute the examples must be provided
  - Added in the guidelines (Eric)

##### Tests 
- We need a clear functional testing strategy. We cannot only rely to the tests automatically generated by Hypotheses. We may provide guidance on a "per operator class" basis. For instance, we may give specific guidance for operators using padding, etc.
- [ ] Elaborate a clear testing strategy
- The main test oracle is ORT. However, in some cases (e.g., MaxPool) the behaviour of ORT may be different from what we would expect (example: effect of inf in inputs). In that case, if the behaviour is not a manifest error (such as the case of "-4)...), we will add a notice explaining the discrepancy between our spec and the observable behaviour of ORT. 
  - Notice added (Eric)
- [X] Move the existing tests in the test folder
- [ ] (Henri) Check the behaviour of MaxPool with ORT on a GPU executor. 

##### Error conditions
- An "error condition" is a condition for which an operator can not compute a value that maps to some real counterpart (i.e., excluding Infs and NaN). It shall not cover the case where the output is not a value due to a simple propagation (of NaN, of Inf...).
- basically, we must put in the "error conditions" all results that are,  , "not expected". 
- The name of this section could possibly be changed: "Special cases" ? 

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
  - [X] (1501-1, Jean-Baptiste) Faire une proposition de contenu pour une soumission à  CETiC
    - Proposition faite par JB le 16/01. 
    - Modifications proposées par Eric le <19/01>
  - [X] (1501-2, Jean-Loup) Remove the relation NaN>Inf... and replace it by an explicit test for NaNs... 
  - [X] (1501-3, Eric) Introduce the term "Scalar" and (our) concept of "type" (numerical / value type) in the glossary. 
    - Done, see [here](../../../sonnx/ops/spec/informal/common/definitions.md).
  - [X] (1501-4, eric Clarify the meaning of "heterogeneous" in ONNX
    - ONNX, heterogeneous seems to mean that the inputs can be of different types. But this is not the case. For instance, operator `Where` has "heterogeneous" arguments but, in ORT, `Where` requires the same types for `X` and `Y`. For example, one cannot mix an int32 tensor with a float tensor, or an int32 tensor with an int64 tensor. There is no type promotion. 
    - Heterogeneous **seems** to mean that the operator have arguments of different type: boolean for B and other for `X` and `Y`. 
    - But this is not the case for operator `Add` that is also tagged `heterogeneous` even though all arguments must be of the same generic type `T`
(`Add(float,int)` is rejected and so is `(int32,int64)`). 
    - Tag "Heterogeneous" is automatically generated by ONNX' documentation generator that is located in [onnx/docs/gen_doc.py](https://github.com/onnx/onnx/blob/main/onnx/defs/gen_doc.py). 
    - Normally, "heterogeneous" should only refers to variadic arguments that are not "homogeneous". The generation of "heterogeneous" appear in version ONNX 1.4.0. And it is always related to variadic arguments.  The schema is generated by function `display_schema` which calls `generate_formal_parameter_tags`:
    
    ```python
      def generate_formal_parameter_tags(formal_parameter: OpSchema.FormalParameter) -> str:
      tags: list[str] = []
    if OpSchema.FormalParameterOption.Optional == formal_parameter.option:
        tags = ["optional"]
    elif OpSchema.FormalParameterOption.Variadic == formal_parameter.option:
        if formal_parameter.is_homogeneous:
            tags = ["variadic"]
        else:
            tags = ["variadic", "heterogeneous"]
    differentiable: OpSchema.DifferentiationCategory = (
        OpSchema.DifferentiationCategory.Differentiable
    )
    non_differentiable: OpSchema.DifferentiationCategory = (
        OpSchema.DifferentiationCategory.NonDifferentiable
    )
    if differentiable == formal_parameter.differentiation_category:
        tags.append("differentiable")
    elif non_differentiable == formal_parameter.differentiation_category:
        tags.append("non-differentiable")

    return "" if len(tags) == 0 else " (" + ", ".join(tags) + ")"
    ```

  - By the way, even if the test was not only done for variadic argumebnts, it depends on the `is_homogeneous` boolean that comes from the schema defined in the `defs.cc` files (for instance, for `Where`: see [here](https://github.com/onnx/onnx/blob/main/onnx/defs/tensor/defs.cc#L2865). For the `Where` operator, the schema is the following:
    ```
    ONNX_OPERATOR_SET_SCHEMA(
    Where,
    16,
    OpSchema()
        .SetDoc(GET_OP_DOC_STR(std::string(Where_ver16_doc) + GenerateBroadcastingDocMul()))
        .Input(
            0,
            "condition",
            "When True (nonzero), yield X, otherwise yield Y",
            "B",
            OpSchema::Single,
            true, // <= This is the "homogeneous" boolean 
            1,
            OpSchema::NonDifferentiable)
        .Input(
            1,
            "X",
            "values selected at indices where condition is True",
            "T",
            OpSchema::Single,
            true,
            1,
            OpSchema::Differentiable)
        .Input(
            2,
            "Y",
            "values selected at indices where condition is False",
            "T",
            OpSchema::Single,
            true,
            1,
            OpSchema::Differentiable)
        .Output(
            0,
            "output",
            "Tensor of shape equal to the broadcasted shape of condition, X, and Y.",
            "T",
            OpSchema::Single,
            true,
            1,
            OpSchema::Differentiable)
        .TypeConstraint("B", {"tensor(bool)"}, "Constrain to boolean tensors.")
        .TypeConstraint(
            "T",
            OpSchema::all_tensor_types_ir4(),
            "Constrain input and output types to all tensor types (including bfloat).")
        .TypeAndShapeInferenceFunction([](InferenceContext& ctx) {
          propagateElemTypeFromInputToOutput(ctx, 1, 0);
          if (hasNInputShapes(ctx, 3)) {
            std::vector<const TensorShapeProto*> shapes;
            shapes.push_back(&ctx.getInputType(0)->tensor_type().shape());
            shapes.push_back(&ctx.getInputType(1)->tensor_type().shape());
            shapes.push_back(&ctx.getInputType(2)->tensor_type().shape());
            multidirectionalBroadcastShapeInference(
                shapes, *ctx.getOutputType(0)->mutable_tensor_type()->mutable_shape());
          }
        }));
    ``` 
    
      - As all boolean values are "true", "heterogeneous" should never be displayed!! 

  - [ ] (1501-5, ???) Clarify how we handle value constraints for attributes
  - [X] (1501-6,Eric) Check the actual behavior of Relu and LeakyRelu in ONNX. Check if alpha can be negative.
    - Relu: input [-1.0, 0.0, 1.0, float("nan")] =>  [ 0.  0.  1. nan]
    - Leaky relu: [-1.0, 0.0, 1.0, float("nan")] =>  [nan  0.  1. nan] with alpha = NaN, as expected. Alpha can be negative and the value for X<0 becomes positive.
  - [ ] (1501-7,???) Update the informal spec guidelines (enforce usage of ONNX names and provision of denotation, use of generic types: "with int in (int8,int16,...)" )

##### Past actions
None.