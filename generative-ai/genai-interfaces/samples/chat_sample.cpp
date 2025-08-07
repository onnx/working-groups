// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#include <iostream>

#if defined(USE_ONNXRUNTIME_GENAI)
#include <ortgenai_text2text_pipeline.hpp>
#elif defined(USE_OPENVINO_GENAI)
#include "openvino/onnx_genai/ovgenai_text2text_pipeline.hpp"
#endif

int main(int argc, char* argv[]) try {
  if (argc < 3 || argc > 4) {
    throw std::runtime_error(std::string{"Usage: "} + argv[0] + " <BACKEND> <MODEL_DIR> [DEVICE]");
  }

  std::string backend_name = argv[1];
  std::string models_path = argv[2];
  std::string device = (argc == 4) ? argv[3] : "CPU";  // GPU, NPU can be used as well
  std::string prompt;

  // Create the pipeline using the backend name provided as an argument
  auto devices = DeviceFactory::GetInstance().Enumerate(backend_name);
  auto text2text_pipeline = PipelineFactory::GetInstance().Create(backend_name, models_path, devices);

  std::cout << "Successfully created '" << backend_name << "' backend." << std::endl;

  // --- The rest of your logic remains the same ---

  auto generation_config = text2text_pipeline->get_generation_config();
  generation_config.sampling_config.do_sample = true;
  generation_config.sampling_config.temperature = 0.7;
  generation_config.sampling_config.top_k = 40;
  generation_config.sampling_config.rng_seed = 42;
  text2text_pipeline->set_generation_config(generation_config);

  std::cout << "Question:\n";
  while (std::getline(std::cin, prompt)) {
    if (prompt == "quit()") break;
    GenerationInput input(prompt);
    GenerationResult result = (*text2text_pipeline)(input);
    std::cout << result.text << std::endl;
    std::cout << "\n----------\n"
              << "Question:\n";
  }

} catch (const std::exception& error) {
  try {
    std::cerr << "Error: " << error.what() << '\n';
  } catch (const std::ios_base::failure&) {
  }
  return EXIT_FAILURE;
} catch (...) {
  try {
    std::cerr << "Non-exception object thrown\n";
  } catch (const std::ios_base::failure&) {
  }
  return EXIT_FAILURE;
}
