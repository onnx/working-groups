#ifndef DEVICE_FACTORY_HPP
#define DEVICE_FACTORY_HPP

#include <functional>
#include <stdexcept>
#include <string>
#include <map>
#include <any>

namespace onnx::genai {

struct Device {
    std::string identifier;
    std::map<std::string, std::any> config;
};

// A function pointer type for providing device options.
using DeviceEnumerator = std::function<const std::vector<Device>()>;

class DeviceFactory {
public:
    static DeviceFactory& GetInstance() {
        static DeviceFactory instance;
        return instance;
    }

    // Called by GenAI frameworks  to register their device enumeration logic.
    void Register(const std::string& name, DeviceEnumerator enumerator) {
        m_device_enumerator[name] = enumerator;
    }

    // Called by the application to get devices enumerated by GenAI frameworks.
    const std::vector<Device> Enumerate(const std::string& name) {
        auto it = m_device_enumerator.find(name);
        if (it == m_device_enumerator.end()) {
            throw std::runtime_error("Unregistered GenAI framework: " + name);
        }
        return it->second();
    }

private:
    DeviceFactory() = default;
    std::map<std::string, DeviceEnumerator> m_device_enumerator;
};

} // namespace onnx::genai

#endif // DEVICE_FACTORY_HPP
