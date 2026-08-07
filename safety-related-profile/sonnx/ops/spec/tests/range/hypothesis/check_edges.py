"""
This file checks edge cases in the generated data for the Range operation in ONNX.
"""
import json
import numpy as np

"""
Range supported types, organized by ONNXRuntime_Provider
"""
range_types = {
    "CPUExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32, 
        "FP64": np.float64, 
    },
    "CUDAExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32, 
        "FP64": np.float64, 
    },
    "DmlExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32
    }
}

def check_edges():
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        check_s_tensor_int = check_individual_variables(
            "s_tensor (int)", data["s_tensor_int"], data["min_input_int"], data["max_input_int"]
        )

        check_s_tensor_float = check_individual_variables(
            "s_tensor (float)", data["s_tensor_float"], 
            data["min_input_float"], data["max_input_float"]
        )

        check_l_tensor_int = check_individual_variables(
            "l_tensor (int)", data["l_tensor_int"], 
            data["min_input_int"], data["max_input_int"]
        )

        check_l_tensor_float = check_individual_variables(
            "l_tensor (float)", data["l_tensor_float"], 
            data["min_input_float"], data["max_input_float"]
        )

        check_d_tensor_int = check_individual_variables(
            "d_tensor (int)", data["d_tensor_int"], 
            data["min_input_int"], data["max_input_int"]
        )

        check_d_tensor_float = check_individual_variables(
            "d_tensor (float)", data["d_tensor_float"], 
            data["min_input_float"], data["max_input_float"]
        )

        check_input_type = check_type(
            "input_type", data["input_type"], data["ONNXRuntime_Provider"]
        )

        return all([check_s_tensor_int, check_s_tensor_float, check_l_tensor_int,
                    check_l_tensor_float, check_d_tensor_int,
                    check_d_tensor_float, check_input_type])


def check_individual_variables(variable_name, variable_analysis, min_value, max_value):
    """
    Check individual variable analysis
    """
    corner_cases = [min_value, max_value]
    corner_cases_test = all(corner_case in variable_analysis for corner_case in corner_cases)
    has_mean_case_mean = any(d for d in variable_analysis if d > min_value and d < max_value)
    has_out_of_bounds = not any(d for d in variable_analysis if d < min_value or d > max_value)

    print(f"Individual variable analysis: {variable_name}")
    if not corner_cases_test:
        for corner_case in corner_cases:
            if corner_case not in variable_analysis:
                print(f"    - Missing corner case: {corner_case}")
    if not has_mean_case_mean:
        print("  - Missing mean case")
    if not has_out_of_bounds:
        print("  - Found out of bounds values")

    return all([corner_cases_test, has_mean_case_mean, has_out_of_bounds])



def check_type(variable_name, variable_analysis, provider):
    """
    Check input types
    """
    supported_types = set(range_types.get(provider).keys())
    variable_analysis_types = set(variable_analysis)
    missing_types = supported_types - variable_analysis_types
    print(f"Type analysis: {variable_name}")
    if missing_types:
        for missing_type in missing_types:
            print(f"    - Missing type: {missing_type}")
        return False
    return True


print(check_edges())
