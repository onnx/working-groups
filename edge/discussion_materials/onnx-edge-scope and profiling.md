# ONNX Edge scope and profiling
Author: Yedong Liu

## Scope of Edge

Edge computing is computing that’s done at or near the source of the data, instead of relying on the cloud at one of a dozen data centers to do all the work. Edge computation is largely or completely performed on distributed edge devices. The target of edge computing is any application or general functionality needing to be closer to the source of the action where system can process and interact with the real world instantly.


## Edge scenario

Computation offloading for real-time applications, such as facial recognition, smart city, intelligent traffic control, industrial IoT, video analysis and monitoring, border control, unattended shops, auto pilot and smart drones are all considered within edge computing scope. 

Edge provides lower latency and reduces transmission costs, and edge computing still varies is highly scenario dependent. 

In one of the scenarios, specifically for IoT devices, data comes in from the physical world via various sensors, and actions are taken to change physical state via various forms of output; by performing analytics and generating output directly at the site, communications bandwidth between edge and cloud is reduced. Edge computing takes advantage of proximity to the physical items of interest and also exploits the relationships those items may have to each other.

In another scenario which requires low latency like auto pilot cars. A notable applications include online gaming. Game servers are running in the cloud and the rendered video is transferred to lightweight clients such as AR devices (mobile phone), VR glasses, etc. Conventional cloud games may suffer from high latency and insufficient bandwidth. As real-time games have strict constraints on latency, processing game simulation at the edge node is necessary for the immersive game plays.


## Edge device

An edge device is a device which provides an entry point into enterprise or service provider core networks. Examples include routers, routing switches, terminals and other devices. Edge devices also provide connections into carrier and internet service provider networks.

In general, edge devices are normally routers and terminals that provide authenticated access to faster, more efficient backbone and core networks. Edge device is usually smart and has access to the core devices, often include Quality of Service (QoS) and multi-service functions to manage different types of traffic.

## ONNX Edge profile

The work of the ONNX Edge profile includes:

1. Attributes / characteristics: Power, Size, accuracy, speed, Security, etc.

2. ONNX operations subset

3. Other ONNX related limitations 

Work to define strict subsets of the operator sets which apply to edge devices which avoid complex operations imposed by limitations on edge devices with high computational complexity. Exclude use-cases not applicable to the edge (e.g. large scale training scenarios)


###Metrics for ONNX Edge

#### Accuracy

The ONNX model zoo collected many wide-used models for image classification, face recognition and image segmentation. While the accuracy number varies, the top-5 accuracy seems acceptable with VGG, resent and mobile net are all above or close to 90%. Accuracy is critical for scenarios like smart city, face recognition and smart monitoring. If put these models in edge device in actual use, primary work is to keep the accuracy still in a decent level while compressing the model and changing ops to low-bit version. Detailed work can be achieved cooperating with the quantization WG.

#### Size

In ONNX 1.4 release, support for large models (larger than 2GB) and store the data externally is added as a new feature. But in edge device, we do not want such huge models running and consuming the precious memory. There will always be compromises between performance, speed, cost and consumption. There are many ways to compress our models while keeping the accuracy like changing to quantized ops, model compression etc. ONNX Edge WG works to define the compression method for ONNX model and to develope quantized ops.

#### Speed

In many scenarios, fast processing speed and low latency are required. Vendor-specific runtime optimization are encouraged while we should also keep our optimization work going. works on the speed over laps with some of the work on the bandwidth, since a broader bandwidth always provide less latency thus improving overall speed.

#### Power consumption

Power consumption is critical for an edge device. 

//MLPerf community is a broad ML benchmark suite for measuring performance of ML software frameworks, ML hardware accelerators, and ML cloud platforms. In MLPerf Edge Inference WG, power consumption is outlined as a metrics to be measured thus I suggest that our community can cooperate with MLPerf community to improve our power consumption performance. MLPerf Edge Inference Power/Energy [4] is the official document of MLPerf on how to handle the measurement and benchmarking for the power/ energy consumption. I suggest we look into the doc and cooperate with the MLPerf community to improve our power/ energy consumption performance based on the Spec mentioned.//

#### Security

#### Bandwidth














