# ONNX GenAI Interfaces

A repository containing standard interfaces for ONNX GenAI pipelines

## Instructions to build the GenAI Interfaces

Follow the below instructions to build GenAI interfaces

```
git clone https://github.com/ynimmaga/genai-interfaces.git
cd genai-interfaces
cmake -B build -S .
cmake --build build
cmake --install build --prefix <your_preferred_path>/genai_interfaces_install

```
This will create the following cmake files in your genai_interfaces_install/lib/cmake/genai_interfaces directory

```
genai_interfacesConfig.cmake
genai_interfacesConfigVersion.cmake
genai_interfacesTargets.cmake
```
