This sample can be conditionally compiled to use either ORT GenAI or OpenVINO GenAI.

# Prepare GenAI Interfaces:

First step, is to prepare the GenAI Interfaces directory.
```
cd generative-ai/genai-interfaces
cmake -B build -S .
cmake --build build
cmake --install build --prefix <your_preferred_path>/genai_interfaces_install
set genai_interfaces_DIR=<your_preferred_path>\genai_interfaces_install\lib\cmake
```

# Conditionaly building the sample with ORT GenAI
*(Assuming Windows cmd.exe shell)*

To build the sample conditionaly for ORT GenAI, the buildOrt.bat script from generative-ai/genai-interfaces/samples needs to be used. Before using the script the following variables would need modification.
- Modify BUILD_FOLDER_PATH in the buildOrt.bat script to a folder location used for download repos and storing builds.
- Modify OPENVINO_PATH to the folder location of a download openvino build. You can use the following link to download an openvino build: https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/windows/openvino_toolkit_windows_2025.2.0.19140.c01cd93e24d_x86_64.zip.
- Modify ONE_TIME_SETUPS, BUILD_ORT, BUILD_ORT_GENAI to appropriate values based on requirement.
- Modify WG_REPO_PATH to the folder location of the working_group repo.

Next execute the script.
```
.\buildOrt.bat
```

If you encounter any failures, please refer to buildOrt.bat for commands to run manually. If all goes well, you should have `ort_sample_build\Release\chat_sample.exe`.

# OpenVINO GenAI build
*(Assuming Windows cmd.exe shell)*
To build the sample conditionaly for ORT GenAI, the buildOrt.bat script from generative-ai/genai-interfaces/samples needs to be used. Before using the script the following variables would need modification.
- Modify BUILD_FOLDER_PATH in the buildOrt.bat script to a folder location used for download repos and storing builds.
- Modify WG_REPO_PATH to the folder location of the working_group repo.
- Modify OPENVINO_PATH to the folder location of a download openvino build. You can use the following link to download an openvino build: https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/windows/openvino_toolkit_windows_2025.2.0.19140.c01cd93e24d_x86_64.zip.
- Modify ONE_TIME_SETUPS, BUILD_GENAI_INTERFACES, BUILD_OV_GENAI to appropriate values based on requirement.

Next execute the script.
```
.\buildOV.bat
```

If you encounter any failures, please refer to buildOrt.bat for commands to run manually. If all goes well, you should have `ov_sample_build\Release\chat_sample.exe`.
