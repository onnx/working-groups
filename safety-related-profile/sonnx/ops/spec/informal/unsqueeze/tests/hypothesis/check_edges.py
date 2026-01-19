import json
import numpy as np
import ml_dtypes


unsqueeze_types = {
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
        "BOOL": np.bool_,
        "STRING": np.str_
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
        "BOOL": np.bool_
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
    with open("generated_data.json", "r") as f:
        data = json.load(f)
        check_shape_size_input_x = check_individual_variables(
            "shape_size_input_x",
            data["shape_size_input_x"],
            data["min_shape_size_input_x"],
            data["max_shape_size_input_x"]
        )
        size_input_x_axis = [ item for sublist in data["size_input_x"] for item in sublist ]
        check_size_input_x = check_individual_variables(
            "size_input_x",
            size_input_x_axis,
            data["min_size_input_x"],
            data["max_size_input_x"]
        )
        check_size_input_axes = check_individual_variables(
            "size_input_axes",
            data["size_input_axes"],
            data["min_number_of_axes"],
            data["max_number_of_axes"]
        )
        provider = data["ONNXRuntime_Provider"]
        check_x_type = check_type("x_type", data["x_type"], provider)

        return all([check_shape_size_input_x, check_size_input_x, check_size_input_axes, check_x_type])


"""
Check individual variable analysis
"""
def check_individual_variables(variable_name, variable_analysis, min, max):    
    corner_cases = [min, max]
    corner_cases_test = all(corner_case in variable_analysis for corner_case in corner_cases)

    has_mean_case_mean = any(d for d in variable_analysis if d > min and d < max)
    has_out_of_bounds = not(any(d for d in variable_analysis if d < min or d > max))

    print(f"Individual variable analysis: {variable_name}")
    if not corner_cases_test:
        for corner_case in corner_cases:
            if corner_case not in variable_analysis:
                print(f"    - Missing corner case: {corner_case}")
    if not has_mean_case_mean:
        print(f"  - Missing mean case")
    if not has_out_of_bounds:
        print(f"  - Found out of bounds values")

    return all([corner_cases_test, has_mean_case_mean, has_out_of_bounds])

def check_type(variable_name, variable_analysis, provider):
    """
    Check input types
    """
    supported_types = set(unsqueeze_types.get(provider).keys())
    variable_analysis_types = set(variable_analysis)
    missing_types = supported_types - variable_analysis_types
    print(f"Type analysis: {variable_name}")
    if missing_types:
        for missing_type in missing_types:
            print(f"    - Missing type: {missing_type}")
        return False
    return True

check_edges()