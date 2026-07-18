"""
This file checks edge cases in the generated data for the Clip operation in ONNX.
"""
import json
import numpy as np

index_types = {
    "INT32": np.int32,
    "INT64": np.int64,
}

def check_edges(data):
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)


        check_rank_input_tensor = check_individual_variables(
            "rank_input_tensor", data["rank_input_tensor"], data["min_rank_input"], data["max_rank_input"]
        )
        shape_size_input_tensor = data["shape_input_tensor"]
        shape_size_input_tensor_flatten = [item for sublist in shape_size_input_tensor for item in sublist]
        check_shape_size_input_tensor = check_individual_variables(
            "shape_size_input_tensor", shape_size_input_tensor_flatten,
            data["min_dim_size_input"], data["max_dim_size_input"])
        
        start_tensor = data["s_tensor"]
        start_tensor_flatten = [item for sublist in start_tensor for item in sublist]
        check_start_tensor = check_individual_variables(
            "start_tensor", start_tensor_flatten,
            -data["max_dim_size_input"], data["max_dim_size_input"] - 1
        )

        end_tensor = data["e_tensor"]
        end_tensor_flatten = [item for sublist in end_tensor for item in sublist]
        check_end_tensor = check_individual_variables(
            "end_tensor", end_tensor_flatten,
            -data["max_dim_size_input"] - 1, data["max_dim_size_input"]
        )

        check_start_tensor_input = check_start_input_tensor(
            "start_tensor", start_tensor_flatten, shape_size_input_tensor_flatten
        )

        steps = data["k_tensor"]
        steps_flatten = [item for sublist in steps for item in sublist[0]]
        check_end_tensor_input = check_end_input_tensor(
            "end_tensor", end_tensor_flatten, shape_size_input_tensor_flatten, steps_flatten
        )

        check_steps_tensor = check_bondaries_tensors("steps_tensor", data["k_tensor"])

        return all([check_rank_input_tensor, check_shape_size_input_tensor, check_start_tensor, check_end_tensor, check_start_tensor_input, check_end_tensor_input, check_steps_tensor])


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

def check_start_input_tensor(variable_name, variable_analysis, input_tensor):
    """
    Check start tensor edge cases on input tensor
    """
    min_edge_case = set()
    max_edge_case = set()
    for i in range(len(input_tensor)):
        min_val = -input_tensor[i] 
        max_val = input_tensor[i] - 1
        if min_val == variable_analysis[i]:
            min_edge_case.add(variable_analysis[i])
        if max_val == variable_analysis[i]:
            max_edge_case.add(variable_analysis[i])
    if len(min_edge_case) < 1 and len(max_edge_case) < 1:
        print(f"Edge case analysis: {variable_name}")
        print(f"  - Found only {len(min_edge_case)} min edge cases and {len(max_edge_case)} max edge cases for input tensor entries")
        return False
    else:
        print(f"Edge case analysis: {variable_name}")
    return True

def check_end_input_tensor(variable_name, variable_analysis, input_tensor, steps):
    """
    Check end tensor edge cases on input tensor
    """
    min_edge_case = set()
    max_edge_case = set()
    for i in range(len(input_tensor)):
        if steps[i] > 0:
            min_val = -input_tensor[i]
            max_val = input_tensor[i]
        else:
            min_val = -input_tensor[i] - 1
            max_val = input_tensor[i] - 1
        if min_val == variable_analysis[i]:
            min_edge_case.add(variable_analysis[i])
        if max_val == variable_analysis[i]:
            max_edge_case.add(variable_analysis[i])
    if len(min_edge_case) < 1 and len(max_edge_case) < 1:
        print(f"Edge case analysis: {variable_name}")
        print(f"  - Found only {len(min_edge_case)} min edge cases and {len(max_edge_case)} max edge cases for input tensor entries")
        return False
    else:
        print(f"Edge case analysis: {variable_name}")
    return True


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
    separated_analysis = {np.dtype(dtype).name: [] for dtype in index_types.values()}
    for item in variable_analysis:
        dtype = str(item[1])
        if dtype.startswith("<class '"):
            dtype = dtype.split("'")[1].split('.')[-1]
        # item[0] pode ser uma lista de ints, então faça flatten
        if isinstance(item[0], list):
            separated_analysis.setdefault(dtype, []).extend(item[0])
        else:
            separated_analysis.setdefault(dtype, []).append(item[0])
    return separated_analysis

def get_minimum_dtype():
    """
    Get the minimum dtype that can hold the value
    """
    minimum_dtypes = {}
    min_value = None
    for dtype_name, dtype in index_types.items():
        min_value = np.iinfo(dtype).min
        minimum_dtypes[np.dtype(dtype).name] = min_value

    return minimum_dtypes

def get_maximum_dtype():
    """
    Get the maximum dtype that can hold the value
    """
    maximum_dtypes = {}
    max_value = None
    for dtype_name, dtype in index_types.items():
        max_value = np.iinfo(dtype).max
        maximum_dtypes[np.dtype(dtype).name] = max_value

    return maximum_dtypes

print(check_edges("generated_data.json"))

