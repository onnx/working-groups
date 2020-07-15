# ONNX Release Verification

## SCENARIO 1 (Ideal case)

Assumption:
1. ONNX specification is independent and all the verification process is inside ONNX core repo. It doesn't depend on any backend/frontend converter or runtime.
2. Each operator has a very clear description on how it works. If there are any optional attributes, then a default value will be defined for each optional attribute. If there are optional inputs, then user can provide an empty string as name to skip that input.
3. The test cases of each operator cover all combination of required/optional inputs and required/optional attributes. The test cases cover corner cases too. The expected values of the test cases are all computed in the testcases.

Release Verification Process:
1. Run ONNX CI. If the CI pass, then the release verification process completed.

## SCENARIO 2

Assumption:
1. ONNX specification is independent.
2. Each operator has good description on how it works. But some operators didn't define the default values for optional attribute/inputs
3. Test cases only cover the main or simple usages, didn't cover corner cases. Some operators don't have any test cases at all.
4. The verification process depends on a backend runtime to verify the ONNX specification is implementable. And ONNX relies on this backend runtime to test the operators that don't have any test cases in ONNX core. This runtime supported all of the latest ONNX operators.
5. ONNX doesn't depend on any frontend/backend converter. However, in release 1.7 ONNX depend on a few frontend converters like TensorFlow-ONNX converter.

Release Verification Process:
1. Run ONNX CI.
2. Run all the ONNX backend tests on the selected backend runtime in assumption 4.
3. Create and run test that is not covered in ONNX backend tests on the selected backend runtime.
4. Run test on converter?

Problems need to address in Scenario 2:
1. What is the selected backend runtime? ONNX Runtime? Or some other runtime?
```ONNX Runtime is the selected backend runtime.```
2. Who in charge of making sure the selected backend runtime supports all the latest ONNX operators before the next ONNX release?
```ONNX Runtime community is responsible to implement all ONNX operators in a reasonable timeframe.```
3. Should the author of the PR that introduce the new/updated operator implement the support for that operator on the selected backend runtime? Or the author just needs to open an issue on the selected runtime and let the runtime to prioritize when to implement it?
```No. ONNX Runtime community is responsible to implement all ONNX operators in a reasonable timeframe.```
4. Who is responsible to create the test cases that is not covered in ONNX backend tests and the selected backend runtime?
5. How to verify those ONNX operators that are not supported in the selected runtime? Wait until the selected runtime support them and if there are any problem open issue in ONNX at that time?
```ONNX Runtime community is responsible to implement all ONNX operators in a reasonable timeframe. Any operators that are not supported by ONNX Runtime are not fully verify yet. ONNX Runtime community will open issue for ONNX operator specification problem identify during their implementation time. ONNX Runtime community will try to align with the ONNX release schedule.```
6. What converters are ONNX depend on? Frontend or backend converter or both? TensorFlow-ONNX converter? Or some other frontend converter? How about backend converter? How does the converter verify ONNX? What test need to run?


What is the release verification process in Release 1.7?
1. What are the actual verification tests in release 1.7?
2. After running ONNX CI, did it run any other test?
3. Did it run test on any backend/frontend converter or runtime? If yes, what kind of test did it run? How to run those tests?
