"""
This file checks edge cases in the generated data for the Matmul operation in ONNX.
"""
import json
import numpy as np

matmul_types = {
    "INT32": np.int32,
    "INT64": np.int64,
    "UINT32": np.uint32,
    "UINT64": np.uint64,
    "FP32": np.float32,
    "FP64": np.float64
}


def check_edges(data):
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        size_input_axis_a = data["size_input_a"]
        size_input_axis_flatten_a = [item for sublist in size_input_axis_a for item in sublist]
        check_size_input_axis_a = check_individual_variables(
            "size_input_a", size_input_axis_flatten_a, 
            data["min_size_input_a"], data["max_size_input_a"])
        
        size_input_axis_b = data["size_input_b"]
        size_input_axis_flatten_b = [item for sublist in size_input_axis_b for item in sublist]
        check_size_input_axis_b = check_individual_variables(
            "size_input_b", size_input_axis_flatten_b, 
            data["min_size_input_b"], data["max_size_input_b"])

        return all([check_size_input_axis_a, check_size_input_axis_b])


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


print(check_edges("generated_data.json"))
