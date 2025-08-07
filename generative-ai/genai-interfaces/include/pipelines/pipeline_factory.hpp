#ifndef PIPELINE_FACTORY_HPP
#define PIPELINE_FACTORY_HPP

#include <functional>
#include <map>
#include <stdexcept>
#include <filesystem>

#include "pipelines/text2text_pipeline.hpp"

namespace onnx::genai {

// A function pointer type for creating a pipeline instance.
using PipelineCreator = std::function<std::shared_ptr<onnx::genai::Text2Text::Pipeline>(const std::filesystem::path& models_path, const std::vector<Device> devices)>;

// The Factory is a singleton that acts as a central registry.
class PipelineFactory {
public:
    static PipelineFactory& GetInstance() {
        static PipelineFactory instance;
        return instance;
    }

    // Called by implementations to register their creation logic.
    void Register(const std::string& name, PipelineCreator creator) {
        m_creators[name] = creator;
    }

    // Called by the application to create a pipeline instance by name.
    std::shared_ptr<onnx::genai::Text2Text::Pipeline> Create(
        const std::string& name,
        const std::filesystem::path& models_path,
        const std::vector<Device> devices) {

        auto it = m_creators.find(name);
        if (it == m_creators.end()) {
            throw std::runtime_error("Unregistered GenAI framework: " + name);
        }
        return it->second(models_path, devices); // Call the registered creator function.
    }

private:
    PipelineFactory() = default;
    std::map<std::string, PipelineCreator> m_creators;
};

} // namespace onnx::genai

#endif // PIPELINE_FACTORY_HPP
