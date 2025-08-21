// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#include <iostream>
#include "imwrite.hpp"

#if defined(USE_OPENVINO_GENAI)
#include "openvino/onnx_genai/ovgenai_text2image_pipeline.hpp"
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

  std::vector<Device> chosen_devices;
  for (auto d: devices) {
    if (device == d.identifier) {
      chosen_devices.push_back(d);
    }
  }
  auto text2image_pipeline = Text2ImagePipelineFactory::GetInstance().Create(backend_name, models_path, chosen_devices);

  std::cout << "Successfully created '" << backend_name << "' backend." << std::endl;

  // --- The rest of your logic remains the same ---

  auto generation_config = text2image_pipeline->get_generation_config();
  generation_config.image_width = 512;
  generation_config.image_height = 512;
  generation_config.num_inference_steps = 20;
  generation_config.num_images_per_prompt = 1;
  text2image_pipeline->set_generation_config(generation_config);

  std::cout << "Prompt:\n";
  while (std::getline(std::cin, prompt)) {
    if (prompt == "quit()") break;
    GenerationInput input(prompt);
    GenerationResult result = (*text2image_pipeline)(input);
    ov::Tensor img_tensor(ov::element::u8, ov::Shape{1, 512, 512, 3}, result.tensor.data);
    imwrite("image_%d.bmp", img_tensor, true);
    std::cout << "Created image and saved in current folder." << std::endl;
    std::cout << "\n----------\n"
              << "Prompt:\n";
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
