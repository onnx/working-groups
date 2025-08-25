echo "------------ Script initiatialization ------------"
set "BUILD_FOLDER_PATH=<path_to_central_build_folder>"
set "WG_REPO_PATH=<path_to_workging_group_repo>"
set "OPENVINO_PATH=<path_to_downloaded_openvino_folder>"
set OVGENAI_PATH=%BUILD_FOLDER_PATH%\openvino.genai
set ONE_TIME_SETUPS=""
set BUILD_GENAI_INTERFACES=""
set BUILD_OV_GENAI=""


IF %ONE_TIME_SETUPS%=="True" (
    echo "------------ One-time setups ------------"
    cd %BUILD_FOLDER_PATH%
    python -m venv build_env
    call "build_env\Scripts\activate"
    git clone --branch v1.0 https://github.com/RyanMetcalfeInt8/openvino.genai.git
    pip install cmake==3.26.3
)

IF %BUILD_GENAI_INTERFACES%=="True" (
    echo "------------ Building GenAI Interfaces ------------"
    cd %WG_REPO_PATH%\generative-ai\genai-interfaces
    cmake -B build -S .
    cmake --build build
    cmake --install build --prefix %BUILD_FOLDER_PATH%/genai_interfaces_install
    set genai_interfaces_DIR=%BUILD_FOLDER_PATH%\genai_interfaces_install\lib\cmake\genai_interfaces
)

IF %BUILD_OV_GENAI%=="True" (
    echo "------------ Building openvino.genai ------------"
    call %OpenVINO_PATH%\setupvars.bat || exit /b 1
    mkdir %BUILD_FOLDER_PATH%\openvino.genai-build
    cd %BUILD_FOLDER_PATH%\openvino.genai-build
    cmake %OVGENAI_PATH%
    cmake --build . --config Release
    cmake --install . --prefix installed
    set OpenVINOGenAI_DIR=%BUILD_FOLDER_PATH%\openvino.genai-build\installed\runtime\cmake
)

echo "------------ Building openvino.genai Sample ------------"
del /s /q %BUILD_FOLDER_PATH%\samples-build\text2image-pipeline
mkdir %BUILD_FOLDER_PATH%\samples-build\text2image-pipeline
cd %BUILD_FOLDER_PATH%\samples-build\text2image-pipeline
cmake %WG_REPO_PATH%\generative-ai\genai-interfaces\samples\text2image-pipeline\
cmake --build . --config Release
copy %BUILD_FOLDER_PATH%\openvino.genai-build\installed\runtime\bin\intel64\Release\* .\Release\
