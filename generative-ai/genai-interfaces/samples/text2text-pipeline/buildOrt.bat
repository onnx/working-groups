@REM echo "------------ Script initiatialization ------------"
set BUILD_FOLDER_PATH=<path_to_central_build_folder>
set OPENVINO_PATH=<path_to_downloaded_openvino_folder>
set ONE_TIME_SETUPS=""
set BUILD_ORT=""
set ORT_PATH=%BUILD_FOLDER_PATH%\onnxruntime
set ORT_BUILD_PATH=%BUILD_FOLDER_PATH%\onnxruntime-install
set BUILD_ORT_GENAI=""
set ORT_GENAI_PATH=%BUILD_FOLDER_PATH%\onnxruntime-genai
set WG_REPO_PATH=<path_to_workging_group_repo>

IF %ONE_TIME_SETUPS%=="True" (
    echo "------------ One-time setups ------------"
    cd %BUILD_FOLDER_PATH%
    python -m venv build_env
    call "build_env\Scripts\activate"
    git clone --branch stateful_fixes https://github.com/RyanMetcalfeInt8/onnxruntime.git
    cd %ORT_PATH%
    git checkout 91ffc0377e5b2333beb0af7ac74f4292014f3154
    pip install -r requirements.txt || exit /b 1
    pip install requests cmake==3.26.3 || exit /b 1
    cd %BUILD_FOLDER_PATH%
    git clone --branch v1.0 https://github.com/kkhode/onnxruntime-genai.git
)

echo "------------ Creating/Loading virtualenv ------------"
cd %BUILD_FOLDER_PATH%
call "build_env\Scripts\activate"

echo "------------ Setting up OpenVINO environment ------------"
call %OPENVINO_PATH%\setupvars.bat || exit /b 1


IF %BUILD_ORT%=="True" (
    echo "------------ Building ORTGenAI Prerequisites i.e. ORT ------------"
    cd %ORT_PATH%
    call build.bat --build --update --config RelWithDebInfo --build_dir .\build --use_openvino --build_shared_lib --cmake_extra_defines CMAKE_TLS_VERIFY=OFF --parallel --skip_tests --build_wheel || exit /b 1
    cd build\RelWithDebInfo
    cmake -DCMAKE_INSTALL_PREFIX=%ORT_BUILD_PATH% -DCMAKE_INSTALL_CONFIG_NAME=RelWithDebInfo -P cmake_install.cmake
    cd %ORT_BUILD_PATH%\bin
    move * ..\lib\.
    cd  %ORT_BUILD_PATH%\include\onnxruntime
    move * ..\.
)

IF %BUILD_ORT_GENAI%=="True" (
    echo "------------ Syncing example headers to ORT GenAI headers ------------"
    cd %ORT_GENAI_PATH%
    @REM xcopy /y examples\c\include\ort_genai.h src\ort_genai.h
    @REM xcopy /y examples\c\include\ort_genai_c.h src\ort_genai_c.h

    echo "------------ Syncing GenAI interface, ORT GenAI & example headers ------------"
    cd %ORT_GENAI_PATH%
    del /s /q .\src\pipelines\
    mkdir .\src\pipelines\
    xcopy %WG_REPO_PATH%\generative-ai\genai-interfaces\include\pipelines\* .\src\pipelines\

    echo "------------ Building onnxruntime-genai ------------"
    cd %ORT_GENAI_PATH%
    python build.py --config RelWithDebInfo --parallel --skip_tests --ort_home %ORT_BUILD_PATH% || exit /b 1
)

echo "------------ Building common sample  ------------"
del /s /q %BUILD_FOLDER_PATH%\samples-build\text2text-pipeline
mkdir %BUILD_FOLDER_PATH%\samples-build\text2text-pipeline
cd %BUILD_FOLDER_PATH%\samples-build\text2text-pipeline
mkdir ort_genai\include ort_genai\include\pipelines ort_genai\lib
copy /y %ORT_BUILD_PATH%\include\* .\ort_genai\include\
copy /y %ORT_GENAI_PATH%\src\ort_genai.h .\ort_genai\include\ort_genai.h
copy /y %ORT_GENAI_PATH%\src\ort_genai_c.h .\ort_genai\include\ort_genai_c.h
copy /y %ORT_GENAI_PATH%\examples\c\include\ortgenai_text2text_pipeline.hpp .\ort_genai\include\
copy /y %WG_REPO_PATH%\generative-ai\genai-interfaces\include\pipelines\* .\ort_genai\include\pipelines\
copy /y %ORT_BUILD_PATH%\lib\* .\ort_genai\lib\
copy /y %ORT_GENAI_PATH%\build\Windows\RelWithDebInfo\RelWithDebInfo\onnxruntime-genai.lib .\ort_genai\lib\.
copy /y %ORT_GENAI_PATH%\build\Windows\RelWithDebInfo\RelWithDebInfo\onnxruntime-genai.dll .\ort_genai\lib\.
cmake %WG_REPO_PATH%\generative-ai\genai-interfaces\samples\text2text-pipeline
cmake --build . --config Release
