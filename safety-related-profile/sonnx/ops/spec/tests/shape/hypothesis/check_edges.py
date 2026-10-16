"""
This file checks edge cases in the generated data for the Shape operation in ONNX.
"""
import json
import numpy as np
import ml_dtypes

"""
Shape supported types, organized by ONNXRuntime_Provider
"""
shape_types = {
    "CPUExecutionProvider": {
        "INT8": np.int8, 
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "UINT8": np.uint8, 
        "UINT16": np.uint16, 
        "UINT32": np.uint32, 
        "UINT64": np.uint64, 
        "FP16": np.float16, 
        "FP32": np.float32, 
        "FP64": np.float64, 
        "STRING": np.str_, 
        "BOOL": np.bool_
    },
    "CUDAExecutionProvider": {
        "INT8": np.int8,
        "INT16": np.int16,
        "INT32": np.int32,
        "INT64": np.int64,
        "UINT8": np.uint8,
        "UINT16": np.uint16,
        "UINT32": np.uint32,
        "UINT64": np.uint64,
        "FP16": np.float16,
        "FP32": np.float32,
        "FP64": np.float64,
        "BOOL": np.bool_,
        "BFLOAT16": ml_dtypes.bfloat16
    },
    "DmlExecutionProvider": {
        "INT8": np.int8, 
        "INT16": np.int16,
        "INT32": np.int32,
        "INT64": np.int64,
        "UINT8": np.uint8,
        "UINT16": np.uint16,
        "UINT32": np.uint32,
        "UINT64": np.uint64,
        "FP16": np.float16,
        "FP32": np.float32,
        "FP64": np.float64,
        "BOOL": np.bool_
    }
}


def check_edges():
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        check_rank_input = check_individual_variables(
            "rank_input_tensor", data["rank_input_tensor"], 
            data["min_rank_input"], data["max_rank_input"])
        
        check_shape_size_input = check_individual_variables(
            "shape_input_tensor", 
            [size for shape in data["shape_input_tensor"] for size in shape], 
            data["min_dim_size_input"], data["max_dim_size_input"])
        
        provider = data["ONNXRuntime_Provider"]

        check_x_type = check_type("x_type", data["x_type"], provider)

        check_start = check_individual_variables(
            "start", data["start"], 
            data["start_min"], data["start_max"])

        check_end = check_individual_variables(
            "end", data["end"], 
            data["end_min"], data["end_max"])

        return all([check_rank_input, check_shape_size_input, check_x_type, check_start, check_end])


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
    supported_types = set(shape_types.get(provider).keys())
    variable_analysis_types = set(variable_analysis)
    missing_types = supported_types - variable_analysis_types
    print(f"Type analysis: {variable_name}")
    if missing_types:
        for missing_type in missing_types:
            print(f"    - Missing type: {missing_type}")
        return False
    return True


print(check_edges())