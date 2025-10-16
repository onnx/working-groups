"""
This file checks edge cases in the generated data for the Concat operation in ONNX.
"""

import json

def check_edges(data):
    """
    Check edge cases in the generated data
    """
    with open("generated_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

        check_number_of_input_tensors = check_individual_variables(
            "number_of_input_tensors", data["number_of_input_tensors"], 
            data["min_input_tensors"], data["max_input_tensors"])

        check_shape_size_input_tensors = check_individual_variables(
            "shape_size_input_tensors", data["shape_size_input"], 
            data["min_shape_size_input"], data["max_shape_size_input"])

        # TODO check concatenation_axis and input_tensors_shapes is not done (Doubts)
        return all([check_number_of_input_tensors, check_shape_size_input_tensors])



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
