"""
This file checks edge cases in the generated data for the Clip operation in ONNX.
"""
import json
import numpy as np
import ml_dtypes

clip_types = {
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
    "BFLOAT16": ml_dtypes.bfloat16
}


def check_edges(data):
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)


        check_shape_size_input_x = check_individual_variables(
            "shape_size_input_tensors_x", data["shape_size_input_x"], 
            data["min_shape_size_input_x"], data["max_shape_size_input_x"])

        size_input_axis = data["size_input_axis"]
        size_input_axis_flatten = [item for sublist in size_input_axis for item in sublist]
        check_size_input_axis = check_individual_variables(
            "size_input_axis", size_input_axis_flatten, 
            data["min_size_input_axis"], data["max_size_input_axis"])

        check_l_tensor = check_bondaries_tensors("l_tensor", data["l_tensor"])
        check_m_tensor = check_bondaries_tensors("m_tensor", data["m_tensor"])

        check_inverted_boundaries_ = check_inverted_boundaries("l_tensor", data["l_tensor"], "m_tensor", data["m_tensor"])

        return all([check_shape_size_input_x, check_size_input_axis,
                     check_l_tensor, check_m_tensor, check_inverted_boundaries_])


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

def check_bondaries_tensors(variable_name, variable_analysis):
    """
    Check interval tensors
    """
    minimum_dtypes = get_minimum_dtype()
    maximum_dtypes = get_maximum_dtype()
    separated_analysis = separate_by_dtype(variable_analysis)
    checks = []
    for key, value in separated_analysis.items():
        checks.append(check_individual_variables(
            f"{variable_name} - {key}", value, minimum_dtypes[key], maximum_dtypes[key]))
    return all(checks)


def separate_by_dtype(variable_analysis):
    """
    Separate the analysis by dtype
    """
    separated_analysis = {np.dtype(dtype).name: [] for dtype in clip_types.values()}
    for item in variable_analysis:
        dtype = str(item[1])
        if dtype.startswith("<class '"):
            dtype = dtype.split("'")[1].split('.')[-1]
        separated_analysis.setdefault(dtype, []).append(item[0])
    return separated_analysis

def get_minimum_dtype():
    """
    Get the minimum dtype that can hold the value
    """
    minimum_dtypes = {}
    min_value = None
    for dtype_name, dtype in clip_types.items():
        if np.issubdtype(dtype, np.integer):
            min_value = np.iinfo(dtype).min
        if np.issubdtype(dtype, np.floating):
            min_value = np.finfo(dtype).min
        if dtype_name == "BFLOAT16":
            min_value = float(ml_dtypes.finfo(clip_types["BFLOAT16"]).min)
        minimum_dtypes[np.dtype(dtype).name] = min_value

    return minimum_dtypes

def get_maximum_dtype():
    """
    Get the maximum dtype that can hold the value
    """
    maximum_dtypes = {}
    max_value = None
    for dtype_name, dtype in clip_types.items():
        if np.issubdtype(dtype, np.integer):
            max_value = np.iinfo(dtype).max
        if np.issubdtype(dtype, np.floating):
            max_value = np.finfo(dtype).max
        if dtype_name == "BFLOAT16":
            max_value = float(ml_dtypes.finfo(clip_types["BFLOAT16"]).max)
        maximum_dtypes[np.dtype(dtype).name] = max_value

    return maximum_dtypes

def check_inverted_boundaries(l_variable_name, l_variable_analysis, m_variable_name, m_variable_analysis):
    """
    Check if m < l in the test cases
    """
    print(f"Inverted Boundaries analysis: {l_variable_name} and {m_variable_name}")
    for i in range(len(l_variable_analysis)):
        l_value = l_variable_analysis[i][0]
        m_value = m_variable_analysis[i][0]
        if m_value < l_value:
            return True
    print("  - No case found where m < l")
    return False

print(check_edges("generated_data.json"))
