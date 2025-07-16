#ifndef PIPELINE_FACTORY_HPP
#define PIPELINE_FACTORY_HPP

#include "pipelines/text2text_pipeline.hpp"
#include <functional>
#include <map>
#include <stdexcept>

// A function pointer type for creating a pipeline instance.
using PipelineCreator = std::function<std::shared_ptr<onnx::genai::Text2TextPipeline>(
    const std::filesystem::path& models_path,
    const std::string& device
)>;

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
    std::shared_ptr<onnx::genai::Text2TextPipeline> Create(
        const std::string& name,
        const std::filesystem::path& models_path,
        const std::string& device) {
        
        auto it = m_creators.find(name);
        if (it == m_creators.end()) {
            throw std::runtime_error("Unknown pipeline backend: " + name);
        }
        return it->second(models_path, device); // Call the registered creator function.
    }

private:
    PipelineFactory() = default;
    std::map<std::string, PipelineCreator> m_creators;
};

#endif // PIPELINE_FACTORY_HPP
