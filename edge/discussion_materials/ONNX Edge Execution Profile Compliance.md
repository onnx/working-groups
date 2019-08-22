# ONNX Edge Execution Mode Proposal
Author: Saurabh Tangri, Milan Oljaca, Yedong Liu, Ofer Rosenberg

Version: 0.1

## Background
Edge profiles are intended to provide guidelines and compliance procedures for solution vendors. Please refer [here](https://github.com/onnx/working-groups/blob/master/edge/discussion_materials/ONNX%20Edge%20scope%20and%20profile%20definition.md) for details on edge profiles. The edge profiles can be static or dynamic depending on the nature of edge device. A fixed function device such as a smart speaker supports a single static edge profile. For other multi-function edge devices(example PC) a profile can be viewed as a mode of operation. Such a device can support multiple ONNX edge profiles. At times when such a device is operating multiple profiles simultaneously ONNX Edge execution mode attributes provide hints to the platform. This establishes an execution contract between the application and the underlying platform which guarantees Quality of Service.

## Definition
For multi-function devices such as a PC, ONNX Edge profile execution mode is an optional mechanism to express configuration needed to run a particular Machine Learning model. The collection of attributes contained in edge profile help ML frameworks and underlying runtimes allocate and manage resources prior to running the model. It is described in the model file and used by the runtime.

## Purpose/Objective
To ensure unambiguous usage of ONNX edge execution modes and profile attributes during training and inference we need to describe runtime behavior.

## Scope
ONNX execution modes describe the minimum deployment configuration needed to successfully run a particular model. It should describe the assumptions that were made when authoring the model and are needed to comply to the requirements of edge profiles. These can be viewed as a contract between author of a ML model and the executor of the model. 

|              | Details                                                             | How to populate                                  | Data Type                                          | Example |
|--------------|---------------------------------------------------------------------|--------------------------------------------------|----------------------------------------------------|---------|
| Accuracy     | What accuracy to expect when deploying the model with this profile. | Accuracy noted. (Post training)                  | DatasetName: Metric:                               |         |
| Memory       | What memory footprint to expect when running in this profile.       | Average steady state working set memory          | Size                                               |         |
| Latency      | What minimum performance is expected by this profile                | latency noted during model validation.           | Batch Size First time latency Steady state latency |         |
| Power        | What power performance is expected by this profile                  | What is minimum steady state throughput per watt | IPS/W                                              |         |
| Data Locality | Is model intended to run on a network connected device?             | What is Network QoS required to run the model    | Yes/No or QoS                                      |         |

Following are the implications of adding Edge Execution Modes 
1. A producer of a ONNX model(Training frameworks or conversion tools) should be able to store profiles and attributes.
2. Visualization tools like(ex: Netron) should be able to show profile attributes.


## Compliance Policy
In order to be compliant the executing entity:example a runtime or framework needs to run the model in a configuration that meets the requirements described by the attributes. 

## Compliance Procedure

## Related Procedures

## References




